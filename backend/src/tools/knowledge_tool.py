from typing import List, Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from src.services.knowledge_service import KnowledgeService

class KnowledgeSearchInput(BaseModel):
    query: str = Field(..., description="The question or search query to find information about.")

class KnowledgeBaseTool(BaseTool):
    name: str = "search_knowledge_base"
    description: str = (
        "Useful for searching internal documents, manuals, and reports provided by the user. "
        "Use this tool when you need to answer questions about specific company policies, "
        "branding guidelines, or uploaded content that is not general knowledge."
    )
    args_schema: Type[BaseModel] = KnowledgeSearchInput
    
    # Store client/agent_id context if needed. 
    # Since tools are instantiated per request or bound with context, we need a way to pass agent_id.
    # We can use the bind_tools approach where agent_id is injected, or pass it via constructor.
    # For now, let's assume we get it from the agent's state or injection.
    # However, standard Pydantic tools don't hold state easily unless we subclass carefully.
    
    # Better approach: The tool function takes 'agent_id' as an argument? 
    # But the LLM shouldn't guess the agent_id. 
    # We should partially bind the agent_id when creating the tool instance.
    
    agent_id: str

    def _run(self, query: str) -> str:
        # Synchronous wrapper (not ideal for async service but ok for LangChain sync agents)
        # We really should use _arun
        import asyncio
        return asyncio.run(self._arun(query))

    async def _arun(self, query: str) -> str:
        try:
            service = KnowledgeService()
            results = await service.query_knowledge(self.agent_id, query)
            
            if not results:
                return "No relevant information found in the knowledge base."
            
            # Format results
            formatted = "Found the following information:\n\n"
            for i, res in enumerate(results):
                formatted += f"Source: {res.metadata.get('source', 'Unknown')}\n"
                formatted += f"Content: {res.content}\n\n"
                
            return formatted
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"
