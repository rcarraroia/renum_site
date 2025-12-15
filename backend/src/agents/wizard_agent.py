"""
Wizard Agent - Dynamic Agent Created from Wizard Configuration
Sprint 06 - Task 10

This agent is created dynamically from wizard configuration (not renus_config).
Used in sandbox for testing before publication.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable

from .base import BaseAgent
from ..config.settings import settings


class WizardAgent(BaseAgent):
    """
    Dynamic agent created from wizard configuration.
    
    Used in sandbox to test agent behavior before publication.
    Collects structured data based on custom fields defined in wizard.
    """
    
    def __init__(self, wizard_config: Dict[str, Any], **kwargs):
        """
        Initialize agent from wizard configuration.
        
        Args:
            wizard_config: Complete wizard configuration with all steps
            **kwargs: Additional configuration
        """
        # Extract wizard step data
        self.step_1 = wizard_config.get('step_1_data', {})
        self.step_2 = wizard_config.get('step_2_data', {})
        self.step_3 = wizard_config.get('step_3_data', {})
        self.step_4 = wizard_config.get('step_4_data', {})
        
        # Extract fields to collect
        self.fields_to_collect = self._extract_fields()
        
        # Track collected data
        self.collected_data: Dict[str, Any] = {}
        
        # Generate system prompt from wizard config
        system_prompt = self._generate_system_prompt()
        
        # Initialize base agent
        super().__init__(
            model=kwargs.get("model", settings.DEFAULT_RENUS_MODEL),
            system_prompt=system_prompt,
            tools=kwargs.get("tools", []),
            **kwargs
        )
    
    def _extract_fields(self) -> List[Dict[str, Any]]:
        """
        Extract fields to collect from Step 3 configuration.
        
        Returns:
            List of field configurations in collection order
        """
        fields = []
        
        # Add enabled standard fields
        standard_fields = self.step_3.get('standard_fields', {})
        for field_name, field_config in standard_fields.items():
            if field_config.get('enabled', False):
                fields.append({
                    'name': field_name,
                    'label': field_name.replace('_', ' ').title(),
                    'type': 'text',
                    'required': field_config.get('required', False),
                    'is_standard': True,
                })
        
        # Add custom fields
        custom_fields = self.step_3.get('custom_fields', [])
        for field in custom_fields:
            fields.append({
                'name': field.get('name', field.get('label', '').lower().replace(' ', '_')),
                'label': field.get('label', ''),
                'type': field.get('type', 'text'),
                'required': field.get('required', False),
                'options': field.get('options', []),
                'validation': field.get('validation', {}),
                'is_standard': False,
            })
        
        return fields
    
    def _generate_system_prompt(self) -> str:
        """
        Generate system prompt from wizard configuration.
        
        Returns:
            Complete system prompt with personality and instructions
        """
        # Get template info
        template_type = self.step_1.get('template_type', 'custom')
        agent_name = self.step_1.get('name', 'AI Assistant')
        description = self.step_1.get('description', '')
        niche = self.step_1.get('niche', 'general')
        
        # Get personality
        personality = self.step_2.get('personality', 'professional')
        tone_formal = self.step_2.get('tone_formal', 50)
        tone_direct = self.step_2.get('tone_direct', 50)
        
        # Build system prompt
        prompt = f"""You are {agent_name}, a {personality} AI assistant.

Description: {description}

Niche: {niche}

Personality Traits:
- Formality: {tone_formal}% formal, {100-tone_formal}% casual
- Communication: {tone_direct}% direct, {100-tone_direct}% descriptive

Your task is to collect the following information from the user in a natural conversation:

"""
        
        # Add fields to collect
        for i, field in enumerate(self.fields_to_collect, 1):
            required = "REQUIRED" if field['required'] else "optional"
            prompt += f"{i}. {field['label']} ({field['type']}, {required})\n"
            
            if field.get('options'):
                prompt += f"   Options: {', '.join(field['options'])}\n"
        
        prompt += """
Instructions:
1. Greet the user warmly and explain you'll help them
2. Ask for ONE field at a time in a natural, conversational way
3. If the user provides information, acknowledge it and ask for the next field
4. If information is unclear or invalid, politely ask for clarification
5. Keep track of what information you've already collected
6. Once all required fields are collected, summarize and confirm
7. Maintain your personality throughout the conversation

Remember:
- Be natural and conversational
- Don't sound like a form or questionnaire
- Adapt your tone based on the personality settings
- If user asks questions, answer them before continuing data collection
"""
        
        return prompt
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize OpenAI LLM"""
        return ChatOpenAI(
            model=self.model,
            temperature=0.7,
            streaming=True,
            api_key=settings.OPENAI_API_KEY
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for data collection"""
        
        workflow = StateGraph(dict)
        
        # Define nodes
        workflow.add_node("analyze", self._analyze_message)
        workflow.add_node("extract_data", self._extract_field_data)
        workflow.add_node("validate_data", self._validate_field_data)
        workflow.add_node("respond", self._generate_response)
        
        # Define edges
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "extract_data")
        workflow.add_conditional_edges(
            "extract_data",
            self._has_extractable_data,
            {
                "validate": "validate_data",
                "respond": "respond"
            }
        )
        workflow.add_edge("validate_data", "respond")
        workflow.add_edge("respond", END)
        
        return workflow.compile()
    
    @traceable(name="wizard_agent_analyze")
    async def _analyze_message(self, state: Dict) -> Dict:
        """
        Analyze user message and conversation state.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with analysis
        """
        messages = state.get("messages", [])
        
        # Determine which fields are still needed
        collected_fields = set(state.get("collected_data", {}).keys())
        remaining_fields = [
            f for f in self.fields_to_collect 
            if f['name'] not in collected_fields
        ]
        
        # Determine next field to collect
        next_field = None
        if remaining_fields:
            # Prioritize required fields
            required_remaining = [f for f in remaining_fields if f['required']]
            next_field = required_remaining[0] if required_remaining else remaining_fields[0]
        
        state["remaining_fields"] = remaining_fields
        state["next_field"] = next_field
        state["is_complete"] = len(remaining_fields) == 0
        
        return state
    
    @traceable(name="wizard_agent_extract")
    async def _extract_field_data(self, state: Dict) -> Dict:
        """
        Extract field data from user message using LLM.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with extracted data
        """
        messages = state.get("messages", [])
        next_field = state.get("next_field")
        
        if not next_field or not messages:
            state["extracted_value"] = None
            return state
        
        # Get last user message
        last_message = messages[-1]
        if not isinstance(last_message, HumanMessage):
            state["extracted_value"] = None
            return state
        
        # Use LLM to extract field value
        extraction_prompt = f"""Extract the {next_field['label']} from this message: "{last_message.content}"

Field type: {next_field['type']}
{f"Valid options: {', '.join(next_field.get('options', []))}" if next_field.get('options') else ""}

If the message contains this information, return ONLY the extracted value.
If the message does NOT contain this information, return "NOT_FOUND".
If the message is unclear, return "UNCLEAR".

Extracted value:"""
        
        extraction_result = await self.llm.ainvoke([
            SystemMessage(content="You are a data extraction assistant."),
            HumanMessage(content=extraction_prompt)
        ])
        
        extracted = extraction_result.content.strip()
        
        if extracted in ["NOT_FOUND", "UNCLEAR"]:
            state["extracted_value"] = None
            state["extraction_status"] = extracted
        else:
            state["extracted_value"] = extracted
            state["extraction_status"] = "SUCCESS"
        
        return state
    
    def _has_extractable_data(self, state: Dict) -> str:
        """
        Check if data was extracted from message.
        
        Args:
            state: Current conversation state
            
        Returns:
            "validate" if data was extracted, "respond" otherwise
        """
        if state.get("extracted_value"):
            return "validate"
        return "respond"
    
    @traceable(name="wizard_agent_validate")
    async def _validate_field_data(self, state: Dict) -> Dict:
        """
        Validate extracted field data.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with validation result
        """
        extracted_value = state.get("extracted_value")
        next_field = state.get("next_field")
        
        if not extracted_value or not next_field:
            state["is_valid"] = False
            state["validation_error"] = "No data to validate"
            return state
        
        # Validate based on field type
        field_type = next_field['type']
        
        if field_type in ['select', 'radio']:
            # Check if value is in options
            options = next_field.get('options', [])
            if extracted_value.lower() in [opt.lower() for opt in options]:
                state["is_valid"] = True
            else:
                state["is_valid"] = False
                state["validation_error"] = f"Must be one of: {', '.join(options)}"
        
        elif field_type == 'email':
            # Basic email validation
            if '@' in extracted_value and '.' in extracted_value:
                state["is_valid"] = True
            else:
                state["is_valid"] = False
                state["validation_error"] = "Must be a valid email address"
        
        elif field_type == 'phone':
            # Basic phone validation
            digits = ''.join(c for c in extracted_value if c.isdigit())
            if len(digits) >= 10:
                state["is_valid"] = True
            else:
                state["is_valid"] = False
                state["validation_error"] = "Must be a valid phone number"
        
        else:
            # Text, textarea, etc - accept anything non-empty
            if extracted_value.strip():
                state["is_valid"] = True
            else:
                state["is_valid"] = False
                state["validation_error"] = "Cannot be empty"
        
        # If valid, store in collected_data
        if state.get("is_valid"):
            collected = state.get("collected_data", {})
            collected[next_field['name']] = extracted_value
            state["collected_data"] = collected
        
        return state
    
    @traceable(name="wizard_agent_respond")
    async def _generate_response(self, state: Dict) -> Dict:
        """
        Generate response to user.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with response
        """
        messages = state.get("messages", [])
        is_complete = state.get("is_complete", False)
        is_valid = state.get("is_valid")
        next_field = state.get("next_field")
        extracted_value = state.get("extracted_value")
        validation_error = state.get("validation_error")
        
        # Build context for LLM
        context = f"""Current situation:
- Collected data: {list(state.get('collected_data', {}).keys())}
- Remaining fields: {len(state.get('remaining_fields', []))}
- Is complete: {is_complete}
"""
        
        if is_complete:
            # All data collected - summarize
            context += "\nAll required information has been collected. Summarize what was collected and thank the user."
        
        elif extracted_value and is_valid:
            # Data was collected successfully
            context += f"\nSuccessfully collected: {next_field['label']} = {extracted_value}"
            context += f"\nNext field to collect: {state.get('remaining_fields', [{}])[0].get('label', 'unknown') if state.get('remaining_fields') else 'none'}"
            context += "\nAcknowledge the information and ask for the next field naturally."
        
        elif extracted_value and not is_valid:
            # Data was invalid
            context += f"\nInvalid data for {next_field['label']}: {validation_error}"
            context += "\nPolitely explain the issue and ask again."
        
        else:
            # No data extracted or first message
            if len(messages) == 1:
                context += "\nThis is the first message. Greet the user and ask for the first field."
            else:
                context += f"\nUser message didn't contain {next_field['label']}."
                context += "\nPolitely ask for this information."
        
        # Generate response using LLM
        prompt_messages = [
            SystemMessage(content=self.system_prompt),
            SystemMessage(content=context),
            *messages
        ]
        
        response = await self.llm.ainvoke(prompt_messages)
        state["response"] = response.content
        
        return state
    
    @traceable(name="wizard_agent_invoke")
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process messages and return response.
        
        Args:
            messages: List of messages in conversation
            context: Additional context (conversation_id, etc)
        
        Returns:
            Dict with response and collected data
        """
        # Invoke graph
        result = await self.graph.ainvoke({
            "messages": messages,
            "context": context,
            "collected_data": self.collected_data,
        })
        
        # Update collected data
        self.collected_data = result.get("collected_data", {})
        
        return {
            "response": result.get("response", ""),
            "collected_data": self.collected_data,
            "is_complete": result.get("is_complete", False),
            "remaining_fields": [f['name'] for f in result.get("remaining_fields", [])],
        }


def create_wizard_agent(wizard_config: Dict[str, Any], **kwargs) -> WizardAgent:
    """
    Factory function to create WizardAgent from wizard configuration.
    
    Args:
        wizard_config: Complete wizard configuration
        **kwargs: Additional configuration
        
    Returns:
        Configured WizardAgent instance
    """
    return WizardAgent(wizard_config=wizard_config, **kwargs)
