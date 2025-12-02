"""
Discovery Agent - Refactored to use BaseAgent + LangGraph
Sprint 04 - Sistema Multi-Agente

Conducts conversational interviews to collect structured lead data.
"""

import re
import json
from typing import Any, Dict, List, Optional, TypedDict
from datetime import datetime

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable

from .base import BaseAgent
from ..config.settings import settings
from ..models.interview import AgentResponse, AIAnalysis


# State definition for LangGraph
class InterviewState(TypedDict):
    """State for interview workflow"""
    messages: List[BaseMessage]
    interview_id: str
    collected_fields: Dict[str, Any]
    required_fields: List[str]
    is_complete: bool
    next_field: Optional[str]
    validation_errors: List[str]
    context: Dict[str, Any]


class DiscoveryAgent(BaseAgent):
    """
    Discovery Agent conducts conversational interviews using LangGraph.
    
    Collects structured data through natural conversation:
    - contact_name (full name)
    - email (validated format)
    - contact_phone (international format with +)
    - country
    - company (business name)
    - experience_level (time and expertise in niche)
    - operation_size (team/network size, revenue)
    
    Uses LangGraph workflow:
    1. extract_fields: Extract data from user message
    2. validate_fields: Validate extracted data
    3. check_completion: Check if all fields collected
    4. generate_response: Generate next question or completion message
    """
    
    # Required fields to collect
    REQUIRED_FIELDS = [
        'contact_name',
        'email',
        'contact_phone',
        'country',
        'company',
        'experience_level',
        'operation_size'
    ]
    
    # Field descriptions
    FIELD_DESCRIPTIONS = {
        'contact_name': 'Full name of the person',
        'email': 'Email address (must contain @ and domain)',
        'contact_phone': 'WhatsApp number with country code (format: +5511999999999)',
        'country': 'Country where they are located',
        'company': 'Company or business name',
        'experience_level': 'Experience in their niche (how long, expertise level)',
        'operation_size': 'Size of operation (team size, network size, revenue range)'
    }
    
    def __init__(self, **kwargs):
        """Initialize Discovery Agent"""
        super().__init__(
            model=kwargs.get("model", "gpt-4o-mini"),
            system_prompt=self._get_system_prompt(),
            tools=kwargs.get("tools", []),
            **kwargs
        )
        self.channel = kwargs.get("channel", "web")
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for Discovery Agent"""
        return """You are a friendly and professional Discovery Agent conducting an interview.

Your goal is to collect the following information naturally through conversation:
1. Full name
2. Email address
3. WhatsApp number (with country code, format: +5511999999999)
4. Country
5. Company/Business name
6. Experience level in their niche (how long, expertise level)
7. Operation size (team size, network size, revenue range)

Guidelines:
- Be conversational and friendly, not robotic
- Ask one question at a time
- Acknowledge answers before moving to next question
- If answer is incomplete or invalid, politely ask for clarification
- Validate email format (must contain @ and domain)
- Validate phone format (must start with + and country code)
- Keep track of what information you've already collected
- When all information is collected, thank them and explain next steps

Important validation rules:
- Email MUST contain @ and a domain (e.g., name@example.com)
- Phone MUST start with + followed by country code and number (e.g., +5511999999999)
- If validation fails, politely ask for correction with an example

You will receive the current interview state showing what's been collected."""
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize OpenAI LLM"""
        return ChatOpenAI(
            model=self.model,
            temperature=0.7,
            streaming=True,
            api_key=settings.OPENAI_API_KEY
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for interview process"""
        
        workflow = StateGraph(InterviewState)
        
        # Define nodes
        workflow.add_node("extract_fields", self._extract_fields_node)
        workflow.add_node("validate_fields", self._validate_fields_node)
        workflow.add_node("check_completion", self._check_completion_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        # Define edges
        workflow.set_entry_point("extract_fields")
        workflow.add_edge("extract_fields", "validate_fields")
        workflow.add_edge("validate_fields", "check_completion")
        
        # Conditional edge: if complete, end; otherwise generate response
        workflow.add_conditional_edges(
            "check_completion",
            lambda state: "complete" if state["is_complete"] else "continue",
            {
                "complete": END,
                "continue": "generate_response"
            }
        )
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    # ========================================================================
    # Node Functions
    # ========================================================================
    
    def _extract_fields_node(self, state: InterviewState) -> InterviewState:
        """
        Node: Extract fields from user message
        
        Uses regex and heuristics to extract structured data from conversation.
        """
        if not state["messages"]:
            return state
        
        # Get last user message
        last_message = state["messages"][-1]
        if not isinstance(last_message, HumanMessage):
            return state
        
        message_content = last_message.content
        extracted = {}
        
        # Email detection
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message_content)
        if email_match and not state["collected_fields"].get('email'):
            extracted['email'] = email_match.group(0)
        
        # Phone detection
        phone_match = re.search(r'\+\d{10,15}', message_content)
        if phone_match and not state["collected_fields"].get('contact_phone'):
            extracted['contact_phone'] = phone_match.group(0)
        
        # Name detection (simple heuristic)
        if not state["collected_fields"].get('contact_name'):
            words = message_content.strip().split()
            if 2 <= len(words) <= 4 and all(word.replace('-', '').isalpha() for word in words):
                extracted['contact_name'] = message_content.strip()
        
        # Update collected fields
        state["collected_fields"].update(extracted)
        
        return state
    
    def _validate_fields_node(self, state: InterviewState) -> InterviewState:
        """
        Node: Validate extracted fields
        
        Checks if extracted data meets validation rules.
        """
        errors = []
        
        # Validate email
        if 'email' in state["collected_fields"]:
            email = state["collected_fields"]['email']
            if not self._validate_email(email):
                errors.append(f"Email '{email}' is invalid. Must contain @ and domain.")
                del state["collected_fields"]['email']
        
        # Validate phone
        if 'contact_phone' in state["collected_fields"]:
            phone = state["collected_fields"]['contact_phone']
            if not self._validate_phone(phone):
                errors.append(f"Phone '{phone}' is invalid. Must start with + and country code.")
                del state["collected_fields"]['contact_phone']
        
        state["validation_errors"] = errors
        return state
    
    def _check_completion_node(self, state: InterviewState) -> InterviewState:
        """
        Node: Check if interview is complete
        
        Determines if all required fields have been collected.
        """
        collected_count = sum(
            1 for field in state["required_fields"]
            if state["collected_fields"].get(field)
        )
        
        state["is_complete"] = collected_count == len(state["required_fields"])
        
        # Determine next field to ask about
        if not state["is_complete"]:
            for field in state["required_fields"]:
                if not state["collected_fields"].get(field):
                    state["next_field"] = field
                    break
        else:
            state["next_field"] = None
        
        return state
    
    @traceable(name="discovery_generate_response")
    async def _generate_response_node(self, state: InterviewState) -> InterviewState:
        """
        Node: Generate conversational response
        
        Uses LLM to generate natural response based on current state.
        """
        # Build context message
        context = self._build_context_message(state)
        
        # Get last user message
        last_user_message = ""
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                last_user_message = msg.content
                break
        
        # Build prompt for LLM
        prompt = f"""{context}

User's latest message: {last_user_message}

Respond naturally and conversationally. 
{f"Ask about: {state['next_field']} - {self.FIELD_DESCRIPTIONS.get(state['next_field'], '')}" if state['next_field'] else "Thank them for completing the interview."}
{f"Validation errors to address: {', '.join(state['validation_errors'])}" if state['validation_errors'] else ""}"""
        
        # Generate response
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        # Add response to messages
        state["messages"].append(AIMessage(content=response.content))
        
        return state
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return bool(re.match(email_pattern, email.strip()))
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone format (international)"""
        if not phone:
            return False
        phone_pattern = r'^\+\d{10,15}$'
        return bool(re.match(phone_pattern, phone.strip()))
    
    def _build_context_message(self, state: InterviewState) -> str:
        """Build context message with current state"""
        collected = []
        missing = []
        
        for field in state["required_fields"]:
            if state["collected_fields"].get(field):
                collected.append(f"✓ {field}: {state['collected_fields'][field]}")
            else:
                missing.append(f"✗ {field}: {self.FIELD_DESCRIPTIONS[field]}")
        
        context = f"""
INTERVIEW STATE:
================

Fields Collected ({len(collected)}/{len(state['required_fields'])}):
{chr(10).join(collected) if collected else '(none yet)'}

Fields Still Needed:
{chr(10).join(missing) if missing else '(all collected!)'}
"""
        return context
    
    # ========================================================================
    # Public Interface
    # ========================================================================
    
    @traceable(name="discovery_agent_invoke")
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process messages and return response.
        
        Args:
            messages: List of messages in conversation
            context: Additional context (interview_id, collected_fields, etc)
        
        Returns:
            Dict with response message, extracted fields, and completion status
        """
        # Initialize state
        state: InterviewState = {
            "messages": messages,
            "interview_id": context.get("interview_id", ""),
            "collected_fields": context.get("collected_fields", {}),
            "required_fields": self.REQUIRED_FIELDS,
            "is_complete": False,
            "next_field": None,
            "validation_errors": [],
            "context": context
        }
        
        # Run workflow
        result = await self.graph.ainvoke(state)
        
        # Extract response
        response_message = ""
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                response_message = msg.content
                break
        
        return {
            "message": response_message,
            "collected_fields": result["collected_fields"],
            "is_complete": result["is_complete"],
            "next_field": result["next_field"],
            "validation_errors": result["validation_errors"]
        }
    
    @traceable(name="discovery_agent_generate_analysis")
    async def generate_analysis(
        self,
        interview_id: str,
        collected_data: Dict[str, Any],
        conversation_history: List[Dict[str, str]]
    ) -> AIAnalysis:
        """
        Generate AI analysis of completed interview.
        
        Args:
            interview_id: UUID of the interview
            collected_data: All collected data from interview
            conversation_history: Complete conversation history
        
        Returns:
            AIAnalysis with summary, quality, pain points, and recommendations
        """
        # Build analysis prompt
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history
        ])
        
        data_summary = "\n".join([
            f"- {key}: {value}"
            for key, value in collected_data.items()
            if value and key in self.REQUIRED_FIELDS
        ])
        
        analysis_prompt = f"""Analyze this completed interview and provide insights:

COLLECTED DATA:
{data_summary}

FULL CONVERSATION:
{conversation_text}

Please provide:
1. A brief summary (2-3 sentences) of the lead
2. Lead quality assessment (high/medium/low) based on:
   - Experience level
   - Operation size
   - Engagement in conversation
3. Main pain points or challenges mentioned
4. Recommendations for next steps

Format your response as JSON:
{{
    "summary": "...",
    "lead_quality": "high|medium|low",
    "pain_points": ["...", "..."],
    "recommendations": ["...", "..."]
}}"""
        
        messages = [
            SystemMessage(content="You are an expert at analyzing sales interviews and qualifying leads."),
            HumanMessage(content=analysis_prompt)
        ]
        
        # Get analysis from LLM
        response = await self.llm.ainvoke(messages)
        
        # Parse JSON response
        try:
            content = response.content
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            analysis_data = json.loads(content.strip())
            
            return AIAnalysis(
                summary=analysis_data.get('summary', 'No summary available'),
                lead_quality=analysis_data.get('lead_quality', 'medium'),
                pain_points=analysis_data.get('pain_points', []),
                recommendations=analysis_data.get('recommendations', []),
                generated_at=datetime.now()
            )
        except (json.JSONDecodeError, KeyError, IndexError):
            # Fallback if JSON parsing fails
            return AIAnalysis(
                summary=f"Interview completed with {collected_data.get('contact_name', 'lead')}",
                lead_quality='medium',
                pain_points=['Unable to extract pain points from conversation'],
                recommendations=['Review conversation manually for insights'],
                generated_at=datetime.now()
            )
