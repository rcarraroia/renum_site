
import sys
import os

# Allow imports from src
sys.path.append('/app')

from src.tools.registry import get_tools_by_names
from langchain_openai import ChatOpenAI
from src.config.settings import settings

def debug():
    print("--- Debugging Tools ---")
    
    # Simulate the call made by DiscoveryAgent
    try:
        # Assuming defaults used in interview_service or discovery_agent
        tool_names = ["database_tools"] 
        print(f"Requesting tools: {tool_names}")
        
        tools = get_tools_by_names(tool_names, client_id="00000000-0000-0000-0000-000000000000")
        
        print(f"Got {len(tools)} tools")
        for i, tool in enumerate(tools):
            print(f"Tool {i}: {type(tool)}")
            print(f"Tool {i} name: {getattr(tool, 'name', 'NO_NAME')}")
            print(f"Tool {i} args_schema: {getattr(tool, 'args_schema', 'NO_SCHEMA')}")
            
        print("\n--- Testing bind_tools ---")
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
        try:
            llm_with_tools = llm.bind_tools(tools)
            print("Successfully bound tools!")
        except Exception as e:
            print(f"Error binding tools: {e}")
            
    except Exception as e:
        print(f"General error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()
