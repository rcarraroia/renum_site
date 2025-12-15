from typing import Optional, Type, Any, Dict
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from src.utils.logger import logger

class SubAgentToolInput(BaseModel):
    query: str = Field(description="The full query or instruction to pass to the specialized agent.")

def create_subagent_tool(subagent_id: str, subagent_name: str, subagent_description: str, interview_service: Any, interview_id: str) -> BaseTool:
    """
    Factory to create a tool that delegates to a specific sub-agent.
    """

    class SubAgentTool(BaseTool):
        name = f"delegate_to_{subagent_id.replace('-', '_')}"
        description = f"Delegate task to {subagent_name}. {subagent_description}. Use this tool when the user asks about topics related to this specialist."
        args_schema: Type[BaseModel] = SubAgentToolInput

        def _run(self, query: str) -> str:
            """Synchronous run not implemented for async tool."""
            raise NotImplementedError("This tool is async only")

        async def _arun(self, query: str) -> str:
            try:
                logger.info(f"Delegating query to subagent {subagent_name} ({subagent_id}): {query}")
                
                # We reuse the logic from InterviewService to process with a specific agent ID
                # Effectively, the 'main' agent is pausing and calling the 'sub' agent
                response = await interview_service.process_message_with_agent(
                    interview_id=interview_id,
                    subagent_id=subagent_id, # Target the sub-agent
                    user_message=query
                )
                
                return response.get('message', "No response from sub-agent.")
            except Exception as e:
                logger.error(f"Error executing subagent tool {subagent_name}: {e}")
                return f"Error connecting to specialist {subagent_name}: {str(e)}"

    # Dynamic naming is tricky with Pydantic v2/LangChain, but we try to set it on instance
    tool = SubAgentTool()
    tool.name = f"delegate_to_{subagent_id.split('-')[0]}" # Shorten for tool name safety
    tool.description = f"Delegate to {subagent_name}. {subagent_description}"
    return tool
