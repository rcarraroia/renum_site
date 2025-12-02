"""
Discovery Agent - Conducts conversational interviews to collect lead data
Sprint 04 - Discovery Agent MVP
"""

import os
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langsmith import traceable

from ..models.interview import AgentResponse, AIAnalysis
from ..tools.whatsapp_tool import WhatsAppTool


class DiscoveryAgent:
    """
    Discovery Agent conducts conversational interviews to collect structured data.
    
    Uses LangChain + GPT-4o-mini to maintain natural conversation while extracting:
    - contact_name (full name)
    - email (validated format)
    - contact_phone (international format with +)
    - country
    - company (business name)
    - experience_level (time and expertise in niche)
    - operation_size (team/network size, revenue)
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
    
    # Field descriptions for the agent
    FIELD_DESCRIPTIONS = {
        'contact_name': 'Full name of the person',
        'email': 'Email address (must contain @ and domain)',
        'contact_phone': 'WhatsApp number with country code (format: +5511999999999)',
        'country': 'Country where they are located',
        'company': 'Company or business name',
        'experience_level': 'Experience in their niche (how long, expertise level)',
        'operation_size': 'Size of operation (team size, network size, revenue range)'
    }
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        langsmith_api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.7,
        channel: str = "web"
    ):
        """
        Initialize Discovery Agent
        
        Args:
            openai_api_key: OpenAI API key (defaults to env var)
            langsmith_api_key: LangSmith API key for tracing (defaults to env var)
            model_name: Model to use (default: gpt-4o-mini)
            temperature: Temperature for generation (default: 0.7 for conversational)
            channel: Communication channel ('web' or 'whatsapp')
        """
        self.channel = channel
        # Get API keys from env if not provided
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.langsmith_api_key = langsmith_api_key or os.getenv('LANGSMITH_API_KEY')
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or parameters")
        
        # Configure LangSmith tracing
        if self.langsmith_api_key:
            os.environ['LANGSMITH_API_KEY'] = self.langsmith_api_key
            os.environ['LANGSMITH_TRACING_V2'] = 'true'
            os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT', 'renum-discovery-agent')
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=self.openai_api_key
        )
        
        # Initialize WhatsApp tool for multi-channel support
        self.whatsapp_tool = WhatsAppTool() if channel == "whatsapp" else None
        
        # System prompt template
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for the agent"""
        return """You are a friendly and professional Discovery Agent conducting an interview to learn about a potential client.

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

Current interview state will be provided in each message."""
    
    def _validate_email(self, email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False
        
        # Basic email validation: must have @ and domain
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return bool(re.match(email_pattern, email.strip()))
    
    def _validate_phone(self, phone: str) -> bool:
        """
        Validate phone format (international)
        
        Args:
            phone: Phone string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not phone:
            return False
        
        # Phone must start with + and contain 10-15 digits
        phone_pattern = r'^\+\d{10,15}$'
        return bool(re.match(phone_pattern, phone.strip()))
    
    def _extract_fields(self, message: str, current_state: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract fields from user message based on context
        
        This is a simple extraction - in production, you might want to use
        the LLM to extract fields more intelligently.
        
        Args:
            message: User's message
            current_state: Current interview state
            
        Returns:
            Dictionary of extracted fields
        """
        extracted = {}
        message_lower = message.lower()
        
        # Simple heuristics for extraction
        # In production, you'd use LLM for better extraction
        
        # Email detection
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if email_match and not current_state.get('email'):
            email = email_match.group(0)
            if self._validate_email(email):
                extracted['email'] = email
        
        # Phone detection
        phone_match = re.search(r'\+\d{10,15}', message)
        if phone_match and not current_state.get('contact_phone'):
            phone = phone_match.group(0)
            if self._validate_phone(phone):
                extracted['contact_phone'] = phone
        
        # Name detection (if asking for name and no name yet)
        if not current_state.get('contact_name'):
            # Simple heuristic: if message has 2-4 words and no special chars, might be a name
            words = message.strip().split()
            if 2 <= len(words) <= 4 and all(word.replace('-', '').isalpha() for word in words):
                extracted['contact_name'] = message.strip()
        
        return extracted
    
    def _build_context_message(self, interview_state: Dict[str, Any], conversation_history: List[Dict[str, str]]) -> str:
        """
        Build context message with current state and history
        
        Args:
            interview_state: Current state of collected fields
            conversation_history: List of previous messages
            
        Returns:
            Formatted context string
        """
        # Fields collected
        collected = []
        missing = []
        
        for field in self.REQUIRED_FIELDS:
            if interview_state.get(field):
                collected.append(f"✓ {field}: {interview_state[field]}")
            else:
                missing.append(f"✗ {field}: {self.FIELD_DESCRIPTIONS[field]}")
        
        context = f"""
INTERVIEW STATE:
================

Fields Collected ({len(collected)}/{len(self.REQUIRED_FIELDS)}):
{chr(10).join(collected) if collected else '(none yet)'}

Fields Still Needed:
{chr(10).join(missing) if missing else '(all collected!)'}

Recent Conversation:
"""
        
        # Add last 5 messages for context
        recent_messages = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
        for msg in recent_messages:
            role = "User" if msg['role'] == 'user' else "You"
            context += f"\n{role}: {msg['content']}"
        
        return context
    
    def _format_message_for_channel(self, message: str) -> str:
        """
        Format message according to channel.
        
        Args:
            message: Original message
        
        Returns:
            Formatted message for the channel
        """
        if self.channel == "whatsapp":
            # WhatsApp formatting: use *bold*, _italic_, ~strikethrough~
            # Keep messages concise for mobile
            # Limit to 1000 characters for WhatsApp
            if len(message) > 1000:
                message = message[:997] + "..."
            return message
        else:
            # Web formatting: can be more detailed
            return message
    
    async def send_via_whatsapp(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send message via WhatsApp.
        
        Args:
            phone: Phone number in international format
            message: Message to send
        
        Returns:
            Result of WhatsApp send operation
        """
        if not self.whatsapp_tool:
            return {
                "success": False,
                "error": "WhatsApp tool not initialized for this agent"
            }
        
        try:
            result = await self.whatsapp_tool._arun(phone=phone, message=message)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send WhatsApp message: {str(e)}"
            }
    
    @traceable(name="discovery_agent_process_message")
    async def process_message(
        self,
        interview_id: str,
        user_message: str,
        interview_state: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None,
        channel: Optional[str] = None
    ) -> AgentResponse:
        """
        Process user message and generate agent response
        
        Args:
            interview_id: UUID of the interview
            user_message: Message from user
            interview_state: Current state (fields collected)
            conversation_history: Previous messages in conversation
            
        Returns:
            AgentResponse with message and extracted fields
        """
        if conversation_history is None:
            conversation_history = []
        
        # Extract fields from user message
        extracted_fields = self._extract_fields(user_message, interview_state)
        
        # Update interview state with extracted fields
        updated_state = {**interview_state, **extracted_fields}
        
        # Build context
        context = self._build_context_message(updated_state, conversation_history)
        
        # Build messages for LLM
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"{context}\n\nUser's latest message: {user_message}\n\nRespond naturally and conversationally.")
        ]
        
        # Get response from LLM
        response = await self.llm.ainvoke(messages)
        agent_message = response.content
        
        # Format message for channel
        if channel:
            self.channel = channel
        agent_message = self._format_message_for_channel(agent_message)
        
        # Check if interview is complete
        collected_count = sum(1 for field in self.REQUIRED_FIELDS if updated_state.get(field))
        is_complete = collected_count == len(self.REQUIRED_FIELDS)
        
        # Determine next question if not complete
        next_question = None
        if not is_complete:
            for field in self.REQUIRED_FIELDS:
                if not updated_state.get(field):
                    next_question = f"Next: Ask about {field}"
                    break
        
        return AgentResponse(
            message=agent_message,
            extracted_fields=extracted_fields,
            is_complete=is_complete,
            next_question=next_question
        )
    
    @traceable(name="discovery_agent_generate_analysis")
    async def generate_analysis(
        self,
        interview_id: str,
        collected_data: Dict[str, Any],
        conversation_history: List[Dict[str, str]]
    ) -> AIAnalysis:
        """
        Generate AI analysis of completed interview
        
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
        import json
        try:
            # Extract JSON from response (might have markdown code blocks)
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
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # Fallback if JSON parsing fails
            return AIAnalysis(
                summary=f"Interview completed with {collected_data.get('contact_name', 'lead')}",
                lead_quality='medium',
                pain_points=['Unable to extract pain points from conversation'],
                recommendations=['Review conversation manually for insights'],
                generated_at=datetime.now()
            )
