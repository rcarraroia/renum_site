"""
Base Agent - Abstract Base Class for All Agents
Sprint 04 - Sistema Multi-Agente

All agents (RENUS, ISA, Discovery, etc) inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the RENUM system.
    
    All agents must inherit from this class and implement:
    - _initialize_llm(): Initialize the LLM (OpenAI, Anthropic, etc)
    - _build_graph(): Build the LangGraph workflow
    - invoke(): Process messages and return response
    
    Attributes:
        model (str): Model name (e.g., "gpt-4-turbo-preview")
        system_prompt (str): System prompt that defines agent behavior
        tools (List[Any]): List of tools the agent can use
        llm (Any): Initialized LLM instance
        graph (Runnable): Compiled LangGraph workflow
    """
    
    def __init__(
        self,
        model: str,
        system_prompt: str,
        tools: Optional[List[Any]] = None,
        **kwargs
    ):
        """
        Initialize base agent.
        
        Args:
            model: Model name (e.g., "gpt-4-turbo-preview", "claude-3-5-sonnet")
            system_prompt: System prompt defining agent behavior
            tools: List of LangChain tools the agent can use
            **kwargs: Additional configuration
        """
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.config = kwargs
        
        # Initialize LLM and graph
        self.llm = self._initialize_llm()
        self.graph = self._build_graph()
    
    @abstractmethod
    def _initialize_llm(self) -> Any:
        """
        Initialize the LLM based on model name.
        
        This method should:
        1. Determine which LLM provider to use (OpenAI, Anthropic, etc)
        2. Initialize the LLM with appropriate settings
        3. Return the initialized LLM instance
        
        Returns:
            Initialized LLM instance (ChatOpenAI, ChatAnthropic, etc)
        
        Example:
            def _initialize_llm(self):
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=self.model,
                    temperature=0.7,
                    streaming=True
                )
        """
        pass
    
    @abstractmethod
    def _build_graph(self) -> Runnable:
        """
        Build the LangGraph workflow for this agent.
        
        This method should:
        1. Create a StateGraph
        2. Define nodes (functions that process state)
        3. Define edges (transitions between nodes)
        4. Compile and return the graph
        
        Returns:
            Compiled LangGraph workflow
        
        Example:
            def _build_graph(self):
                from langgraph.graph import StateGraph, END
                
                workflow = StateGraph(dict)
                workflow.add_node("process", self._process)
                workflow.set_entry_point("process")
                workflow.add_edge("process", END)
                
                return workflow.compile()
        """
        pass
    
    @abstractmethod
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process messages and return response.
        
        This is the main entry point for agent execution.
        
        Args:
            messages: List of messages in the conversation
            context: Additional context (client_id, user_id, etc)
        
        Returns:
            Dict with response and metadata
        
        Example:
            async def invoke(self, messages, context):
                result = await self.graph.ainvoke({
                    "messages": messages,
                    "context": context
                })
                return result
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the agent's model.
        
        Returns:
            Dict with model name and configuration
        """
        return {
            "model": self.model,
            "tools_count": len(self.tools),
            "config": self.config
        }
    
    def __repr__(self) -> str:
        """String representation of the agent"""
        return f"{self.__class__.__name__}(model={self.model}, tools={len(self.tools)})"
