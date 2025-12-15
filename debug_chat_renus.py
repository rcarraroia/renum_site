
import asyncio
import sys
import os
import traceback

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from dotenv import load_dotenv
load_dotenv('backend/.env')

from src.services.agent_service import get_agent_service
from src.services.interview_service import InterviewService
from src.models.interview import AgentResponse

async def debug_renus_flow():
    print("--- START DEBUG ---")
    try:
        service = get_agent_service()
        
        print("1. Searching for 'renus' agent...")
        agent = await service.get_by_slug("renus")
        
        if not agent:
            print("ERROR: Agent 'renus' not found!")
            return
            
        print(f"FOUND: {agent.name} (ID: {agent.id})")
        
        interview_service = InterviewService()
        
        print("2. Creating Interview (mocking public_chat.py flow)...")
        # Trying to create interview via service
        try:
             interview = interview_service.create_interview(
                subagent_id=str(agent.id),
                lead_id=None
            )
             print(f"INTERVIEW CREATED: {interview['id']}")
        except Exception as e:
            print(f"ERROR CREATING INTERVIEW: {e}")
            traceback.print_exc()
            return

        print("3. Processing Message...")
        try:
            response = await interview_service.process_message_with_agent(
                interview_id=interview['id'],
                subagent_id=str(agent.id),
                user_message="Olá, teste de debug"
            )
            print("RESPONSE RECEIVED:")
            print(response)
        except Exception as e:
            print(f"ERROR PROCESSING MESSAGE: {e}")
            traceback.print_exc()

    except Exception as e:
        print(f"GENERAL ERROR: {e}")
        traceback.print_exc()
    print("--- END DEBUG ---")

if __name__ == "__main__":
    asyncio.run(debug_renus_flow())
