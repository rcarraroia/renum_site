"""
ISA Agent - Intelligent System Assistant
Sprint 04 - Sistema Multi-Agente

ISA is an administrative assistant that executes commands through natural language.
"""

from typing import Any, Dict, List
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable

from .base import BaseAgent
from ..config.settings import settings
from ..config.langsmith import get_trace_metadata
from ..tools.supabase_tool import SupabaseTool
from ..services.isa_command_service import IsaCommandService


class IsaAgent(BaseAgent):
    """
    ISA (Intelligent System Assistant) - Administrative assistant agent.
    
    Capabilities:
    1. Generate reports from database queries
    2. Execute bulk operations (send messages, update records)
    3. Query system data (leads, clients, projects, interviews)
    4. Provide system insights and analytics
    5. Execute administrative commands
    
    Available commands:
    - "generate report [type]" - Create various reports
    - "send message to [target]" - Send bulk messages
    - "query [entity] where [conditions]" - Database queries
    - "analyze [data]" - Provide insights
    - "list [entity]" - List records
    """
    
    def __init__(self, model: str = None, system_prompt: str = None, **kwargs):
        """Initialize ISA with configuration (dynamic from DB or default)"""
        # Initialize Supabase tool for database access
        supabase_tool = SupabaseTool()
        
        # Initialize audit service
        self.audit_service = IsaCommandService()
        
        # Resolve configuration
        final_model = model or kwargs.get("model") or settings.DEFAULT_ISA_MODEL
        final_prompt = system_prompt or kwargs.get("system_prompt") or self._get_system_prompt()
        
        super().__init__(
            model=final_model,
            system_prompt=final_prompt,
            tools=[supabase_tool],
            **kwargs
        )
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for ISA"""
        return """You are ISA (Intelligent System Assistant), an administrative assistant for the RENUM system.

Your capabilities:
1. Generate reports from database queries
2. Execute bulk operations (send messages, update records)
3. Query system data (leads, clients, projects, interviews)
4. Provide system insights and analytics
5. Execute administrative commands

Available commands:
- "generate report [type]" - Create various reports
  Examples: "generate report of active interviews", "generate client summary report"
  
- "send message to [target]" - Send bulk messages
  Examples: "send message to all leads", "send reminder to clients"
  
- "query [entity] where [conditions]" - Database queries
  Examples: "query leads where status=active", "query interviews where completed_at is null"
  
- "analyze [data]" - Provide insights
  Examples: "analyze interview completion rates", "analyze lead conversion"
  
- "list [entity]" - List records
  Examples: "list all clients", "list recent interviews"

Guidelines:
- Always confirm destructive operations before executing
- Provide clear summaries of results
- Format responses with tables/lists when appropriate
- Respect admin permissions
- Log all commands for audit purposes
- Be helpful and proactive
- Explain what you're doing and why

When querying data:
- Use the Supabase tool to execute queries
- Filter by client_id when appropriate for multi-tenant isolation
- Return results in a readable format
- Provide context and insights, not just raw data

When you cannot execute a command:
- Explain why clearly
- Suggest alternatives
- Provide examples of valid commands"""
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize OpenAI LLM for ISA"""
        return ChatOpenAI(
            model=self.model,
            temperature=0.3,  # Lower temperature for precise commands
            max_tokens=4096,
            api_key=settings.OPENAI_API_KEY
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for ISA"""
        
        workflow = StateGraph(dict)
        
        # Define nodes
        workflow.add_node("parse", self._parse_command)
        workflow.add_node("execute", self._execute_command)
        workflow.add_node("respond", self._generate_response)
        
        # Define edges
        workflow.set_entry_point("parse")
        workflow.add_conditional_edges(
            "parse",
            self._should_execute,
            {
                "execute": "execute",
                "respond": "respond"
            }
        )
        workflow.add_edge("execute", "respond")
        workflow.add_edge("respond", END)
        
        return workflow.compile()
    
    @traceable(name="isa_parse_command")
    async def _parse_command(self, state: Dict) -> Dict:
        """
        Parse command from user message.
        
        Args:
            state: Current state with messages
        
        Returns:
            Updated state with parsed command
        """
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message:
            state["command_type"] = "unknown"
            return state
        
        content = last_message.content.lower() if hasattr(last_message, 'content') else str(last_message).lower()
        
        # Simple command detection
        if "generate report" in content or "report" in content:
            state["command_type"] = "generate_report"
        elif "send message" in content or "send" in content:
            state["command_type"] = "send_message"
        elif "query" in content or "select" in content:
            state["command_type"] = "query"
        elif "analyze" in content or "analysis" in content:
            state["command_type"] = "analyze"
        elif "list" in content or "show" in content:
            state["command_type"] = "list"
        else:
            state["command_type"] = "general"
        
        return state
    
    def _should_execute(self, state: Dict) -> str:
        """
        Decide if command should be executed.
        
        Args:
            state: Current state with command type
        
        Returns:
            "execute" if should execute, "respond" otherwise
        """
        command_type = state.get("command_type", "unknown")
        
        # Execute if it's a recognized command
        if command_type in ["generate_report", "query", "list", "analyze"]:
            return "execute"
        
        return "respond"
    
    @traceable(name="isa_execute_command")
    async def _execute_command(self, state: Dict) -> Dict:
        """
        Execute the parsed command.
        
        Args:
            state: Current state with command
        
        Returns:
            Updated state with execution result
        """
        command_type = state.get("command_type")
        
        try:
            if command_type == "query" or command_type == "list":
                # Use Supabase tool to query data
                # For now, return mock data
                state["execution_result"] = {
                    "success": True,
                    "data": "Query executed successfully (mock data)"
                }
            elif command_type == "generate_report":
                state["execution_result"] = {
                    "success": True,
                    "data": "Report generated successfully (mock)"
                }
            elif command_type == "analyze":
                state["execution_result"] = {
                    "success": True,
                    "data": "Analysis completed (mock)"
                }
            else:
                state["execution_result"] = {
                    "success": False,
                    "error": f"Command type '{command_type}' not implemented yet"
                }
        except Exception as e:
            state["execution_result"] = {
                "success": False,
                "error": str(e)
            }
        
        return state
    
    @traceable(name="isa_generate_response")
    async def _generate_response(self, state: Dict) -> Dict:
        """
        Generate final response.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with response
        """
        messages = state.get("messages", [])
        execution_result = state.get("execution_result")
        
        # Build prompt with execution result if available
        prompt_messages = [SystemMessage(content=self.system_prompt)]
        
        if execution_result:
            context_msg = f"\nCommand execution result: {execution_result}"
            prompt_messages.append(SystemMessage(content=context_msg))
        
        prompt_messages.extend(messages)
        
        # Generate response
        response = await self.llm.ainvoke(prompt_messages)
        state["response"] = response.content
        
        return state
    
    @traceable(name="isa_invoke")
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process admin command and return response.
        
        Args:
            messages: List of messages
            context: Context with admin_id, etc
        
        Returns:
            Dict with response and execution details
        """
        # Verify admin role
        if not context.get("is_admin", False):
            return {
                "response": "❌ Access denied. ISA is only available to administrators.",
                "error": "unauthorized"
            }
        
        # Add trace metadata
        metadata = get_trace_metadata(
            client_id=context.get("client_id"),
            agent_type="isa",
            admin_id=context.get("admin_id")
        )
        
        # Get user message for audit
        user_message = messages[-1].content if messages else ""
        
        # Invoke graph
        result = await self.graph.ainvoke({
            "messages": messages,
            "context": context,
            "metadata": metadata
        })
        
        # Log command to isa_commands table for audit
        admin_id = context.get("admin_id")
        if admin_id:
            try:
                await self.audit_service.log_command(
                    admin_id=admin_id,
                    user_message=user_message,
                    assistant_response=result.get("response", ""),
                    command_executed=result.get("execution_result", {}).get("success", False),
                    command_type=result.get("command_type"),
                    execution_result=result.get("execution_result")
                )
            except Exception as e:
                # Log error but don't fail the request
                from ..utils.logger import logger
                logger.error(f"Failed to log ISA command: {e}")
        
        return {
            "response": result.get("response", ""),
            "command_type": result.get("command_type"),
            "execution_result": result.get("execution_result"),
            "metadata": metadata
        }
