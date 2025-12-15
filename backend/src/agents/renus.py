"""
RENUS Agent - Main Orchestrator Agent
Sprint 04 - Sistema Multi-Agente

RENUS is the main orchestrator that routes conversations to specialized sub-agents.
"""

from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable

from .base import BaseAgent
from ..config.settings import settings
from ..config.langsmith import get_trace_metadata
from ..utils.logger import logger


class RenusAgent(BaseAgent):
    """
    RENUS - Main orchestrator agent for the RENUM system.
    
    Responsibilities:
    1. Analyze incoming messages and determine intent
    2. Route conversations to specialized sub-agents when appropriate
    3. Handle general conversations directly when no sub-agent is needed
    4. Maintain context across multiple turns
    5. Implement fallback logic when sub-agents fail
    6. Log all routing decisions to LangSmith
    
    Available sub-agents:
    - Discovery: Conducts structured interviews
    - (More sub-agents will be added in future)
    """
    
    def __init__(self, model: str = None, system_prompt: str = None, **kwargs):
        """Initialize RENUS with configuration (dynamic from DB or default)"""
        
        # Resolve configuration
        final_model = model or kwargs.get("model") or settings.DEFAULT_RENUS_MODEL
        self._dynamic_system_prompt = system_prompt or kwargs.get("system_prompt")
        
        super().__init__(
            model=final_model,
            system_prompt=self._get_system_prompt(), # Will use dynamic if set
            tools=kwargs.get("tools", []),
            **kwargs
        )
        
        # Dynamic registry (Sprint 09)
        from .agent_loader import get_agent_registry
        from .topic_analyzer import get_topic_analyzer
        from ..utils.logger import logger
        
        self.agent_registry = get_agent_registry()
        self.topic_analyzer = get_topic_analyzer()
        
        # Load agents from database on initialization
        try:
            count = self.agent_registry.load_agents_from_db()
            logger.info(f"RENUS initialized with {count} agents from database")
        except Exception as e:
            logger.error(f"Error loading agents on RENUS init: {e}")
        
        # Start periodic sync (every 60 seconds)
        if kwargs.get("enable_periodic_sync", True):
            self.start_periodic_sync(interval_seconds=60)
        
        # Legacy sub-agents registry (for backward compatibility)
        self.sub_agents: Dict[str, Any] = {}
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for RENUS"""
        if hasattr(self, '_dynamic_system_prompt') and self._dynamic_system_prompt:
            return self._dynamic_system_prompt
            
        return """You are RENUS, the main orchestrator agent for the RENUM system.

Your responsibilities:
1. Analyze incoming messages and determine user intent
2. Route conversations to specialized sub-agents when appropriate
3. Handle general conversations directly when no sub-agent is needed
4. Maintain context across multiple turns and sub-agent delegations
5. Implement fallback logic when sub-agents fail
6. Always explain your routing decisions clearly

Available sub-agents:
- Discovery: Conducts structured interviews for requirement gathering
  Use when: User wants to start an interview, provide information, or answer questions
- (More sub-agents will be added in future)

When routing, consider:
- Message topic and intent
- Conversation history
- Sub-agent capabilities
- User preferences

When no sub-agent is suitable:
- Respond directly with helpful, professional answers
- Provide information about available services
- Guide users on how to get started

Always be:
- Professional and friendly
- Clear and concise
- Helpful and proactive
- Transparent about your capabilities"""
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize OpenAI LLM for RENUS"""
        return ChatOpenAI(
            model=self.model,
            temperature=0.7,
            streaming=True,
            api_key=settings.OPENAI_API_KEY
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for RENUS orchestration"""
        
        workflow = StateGraph(dict)
        
        # Define nodes
        workflow.add_node("analyze", self._analyze_intent)
        workflow.add_node("route", self._route_to_subagent)
        workflow.add_node("respond", self._generate_response)
        
        # Define edges
        workflow.set_entry_point("analyze")
        workflow.add_conditional_edges(
            "analyze",
            self._should_route,
            {
                "route": "route",
                "respond": "respond"
            }
        )
        workflow.add_edge("route", "respond")
        workflow.add_edge("respond", END)
        
        return workflow.compile()
    
    @traceable(name="renus_analyze_intent")
    async def _analyze_intent(self, state: Dict) -> Dict:
        """
        Analyze message intent and context.
        
        Args:
            state: Current state with messages and context
        
        Returns:
            Updated state with intent analysis
        """
        messages = state.get("messages", [])
        context = state.get("context", {})
        
        # Get last user message
        last_message = messages[-1] if messages else None
        
        if not last_message:
            state["intent"] = "unknown"
            state["confidence"] = 0.0
            return state
        
        # Simple intent detection (can be enhanced with LLM)
        content = last_message.content.lower() if hasattr(last_message, 'content') else str(last_message).lower()
        
        # Check for interview/discovery intent
        interview_keywords = ["entrevista", "interview", "pesquisa", "survey", "perguntas", "questions"]
        if any(keyword in content for keyword in interview_keywords):
            state["intent"] = "discovery"
            state["confidence"] = 0.8
            state["target_subagent"] = "discovery"
        else:
            state["intent"] = "general"
            state["confidence"] = 0.6
            state["target_subagent"] = None
        
        return state
    
    def _should_route(self, state: Dict) -> str:
        """
        Decide if routing to sub-agent is needed.
        
        Args:
            state: Current state with intent analysis
        
        Returns:
            "route" if should route to sub-agent, "respond" otherwise
        """
        intent = state.get("intent", "unknown")
        confidence = state.get("confidence", 0.0)
        target = state.get("target_subagent")
        
        # Route if we have a clear intent and target sub-agent
        if target and confidence > 0.7:
            return "route"
        
        return "respond"
    
    @traceable(name="renus_route_to_subagent")
    async def _route_to_subagent(self, state: Dict) -> Dict:
        """
        Route to appropriate sub-agent.
        
        Args:
            state: Current state with target sub-agent
        
        Returns:
            Updated state with sub-agent response
        """
        target = state.get("target_subagent")
        
        if target in self.sub_agents:
            # Get sub-agent
            sub_agent = self.sub_agents[target]
            
            # Invoke sub-agent
            try:
                result = await sub_agent.invoke(
                    messages=state.get("messages", []),
                    context=state.get("context", {})
                )
                
                state["subagent_response"] = result
                state["subagent_success"] = True
                
            except Exception as e:
                state["subagent_error"] = str(e)
                state["subagent_success"] = False
        else:
            state["subagent_error"] = f"Sub-agent '{target}' not found"
            state["subagent_success"] = False
        
        return state
    
    @traceable(name="renus_generate_response")
    async def _generate_response(self, state: Dict) -> Dict:
        """
        Generate final response.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with final response
        """
        messages = state.get("messages", [])
        
        # If sub-agent was successful, use its response
        if state.get("subagent_success"):
            subagent_response = state.get("subagent_response", {})
            state["response"] = subagent_response.get("response", "")
            return state
        
        # Otherwise, generate direct response
        prompt_messages = [
            SystemMessage(content=self.system_prompt),
            *messages
        ]
        
        response = await self.llm.ainvoke(prompt_messages)
        state["response"] = response.content
        
        return state
    
    @traceable(name="renus_invoke")
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process messages and return response.
        
        Args:
            messages: List of messages in conversation
            context: Additional context (client_id, etc)
        
        Returns:
            Dict with response and metadata
        """
        # Add trace metadata
        metadata = get_trace_metadata(
            client_id=context.get("client_id"),
            agent_type="renus",
            intent="orchestration"
        )
        
        # Invoke graph
        result = await self.graph.ainvoke({
            "messages": messages,
            "context": context,
            "metadata": metadata
        })
        
        return {
            "response": result.get("response", ""),
            "intent": result.get("intent"),
            "routed_to": result.get("target_subagent"),
            "metadata": metadata
        }
    
    def register_subagent(self, name: str, agent: Any) -> None:
        """
        Register a sub-agent with RENUS.
        
        Args:
            name: Sub-agent name (e.g., "discovery")
            agent: Sub-agent instance
        """
        self.sub_agents[name] = agent
        print(f"✅ Registered sub-agent: {name}")
    
    def list_subagents(self) -> List[str]:
        """
        List all registered sub-agents.
        
        Returns:
            List of sub-agent names
        """
        return list(self.sub_agents.keys())
    
    def sync_agents(self) -> Dict[str, int]:
        """
        Sync agent registry with database (Sprint 09)
        
        Should be called periodically (e.g., every 60 seconds)
        
        Returns:
            Sync statistics
        """
        from ..utils.logger import logger
        
        stats = self.agent_registry.sync()
        logger.info(f"Agent registry synced: {stats}")
        return stats
    
    def start_periodic_sync(self, interval_seconds: int = 60) -> None:
        """
        Start periodic sync of agent registry (Sprint 09 - E.2)
        
        Detects new agents every N seconds and updates registry
        
        Args:
            interval_seconds: Sync interval (default: 60s)
        """
        import threading
        import time
        
        def sync_loop():
            while True:
                try:
                    time.sleep(interval_seconds)
                    self.sync_agents()
                except Exception as e:
                    logger.error(f"Error in periodic sync: {e}")
        
        # Start sync thread
        sync_thread = threading.Thread(target=sync_loop, daemon=True)
        sync_thread.start()
        logger.info(f"Started periodic agent sync (interval: {interval_seconds}s)")
    
    async def route_message_dynamic(
        self,
        message: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Route message using dynamic agent registry (Sprint 09)
        
        Args:
            message: User message
            agent_id: Target agent ID
            
        Returns:
            Routing decision with agent/sub-agent info
        """
        # Get agent from registry
        agent_data = self.agent_registry.get_agent(agent_id)
        
        if not agent_data:
            raise ValueError(f"Agent {agent_id} not found in registry")
        
        # Get sub-agents for this agent
        sub_agents = self.agent_registry.get_subagents(agent_id)
        
        # Route message
        routing = await self.topic_analyzer.route_message(
            message=message,
            agent_data=agent_data,
            sub_agents=sub_agents
        )
        
        return routing
    
    def get_registry_stats(self) -> dict:
        """
        Get agent registry statistics (Sprint 09)
        
        Returns:
            Registry statistics
        """
        return self.agent_registry.get_stats()
