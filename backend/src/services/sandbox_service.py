"""
Sandbox Service - Sprint 06
Manages sandbox testing for agents before publication
"""

from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from src.config.supabase import supabase_admin
from src.models.wizard import SandboxSession, SandboxMessageResponse
from src.services.template_service import get_template_service


class SandboxService:
    """Service for managing sandbox testing"""
    
    def __init__(self):
        self.supabase = supabase_admin
        self.template_service = get_template_service()
    
    def create_sandbox(self, wizard_id: UUID) -> SandboxSession:
        """
        Create temporary sandbox conversation
        
        Args:
            wizard_id: Wizard session ID
            
        Returns:
            Created sandbox session
        """
        # Get wizard session
        wizard_result = self.supabase.table('sub_agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .eq('status', 'draft')\
            .single()\
            .execute()
        
        if not wizard_result.data:
            raise ValueError(f"Wizard session {wizard_id} not found")
        
        # Create sandbox conversation
        conversation_id = uuid4()
        sandbox_id = uuid4()
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=1)  # Sandbox expires in 1 hour
        
        conversation_data = {
            'id': str(conversation_id),
            'client_id': wizard_result.data['client_id'],
            'status': 'Nova',  # Must match CHECK constraint: 'Nova', 'Em Andamento', etc.
            'channel': 'Web',  # Must match CHECK constraint: 'WhatsApp', 'Web', 'Email', 'API'
            'summary': f'Sandbox test for wizard {wizard_id}',
            'tags': ['sandbox', 'test'],
            'created_at': now.isoformat(),
            'updated_at': now.isoformat(),
        }
        
        conv_result = self.supabase.table('conversations').insert(conversation_data).execute()
        
        if not conv_result.data:
            raise Exception("Failed to create sandbox conversation")
        
        # Store sandbox session info in wizard config
        wizard_config = wizard_result.data.get('config', {})
        wizard_config['sandbox'] = {
            'sandbox_id': str(sandbox_id),
            'conversation_id': str(conversation_id),
            'created_at': now.isoformat(),
            'expires_at': expires_at.isoformat(),
            'is_sandbox': True,
        }
        
        self.supabase.table('sub_agents')\
            .update({'config': wizard_config})\
            .eq('id', str(wizard_id))\
            .execute()
        
        return SandboxSession(
            id=sandbox_id,
            wizard_id=wizard_id,
            conversation_id=conversation_id,
            created_at=now,
            expires_at=expires_at,
        )
    
    async def process_message(
        self,
        wizard_id: UUID,
        message: str
    ) -> SandboxMessageResponse:
        """
        Process message in sandbox
        
        Args:
            wizard_id: Wizard session ID
            message: User message
            
        Returns:
            Assistant response with collected data
        """
        # Get wizard session and sandbox info
        wizard_result = self.supabase.table('sub_agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .single()\
            .execute()
        
        if not wizard_result.data:
            raise ValueError(f"Wizard session {wizard_id} not found")
        
        wizard_config = wizard_result.data.get('config', {})
        sandbox_info = wizard_config.get('sandbox')
        
        if not sandbox_info:
            raise ValueError("Sandbox not initialized. Call create_sandbox first.")
        
        conversation_id = UUID(sandbox_info['conversation_id'])
        
        # Save messages using direct SQL to bypass Supabase cache issues
        now = datetime.utcnow()
        
        import psycopg2
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        try:
            # Save user message (sender must be: 'client', 'renus', 'admin', or 'system')
            cur.execute("""
                INSERT INTO messages (conversation_id, sender, type, content, channel, timestamp, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(conversation_id),
                'client',  # User is 'client' in the CHECK constraint
                'text',
                message,
                'Web',
                now,
                now
            ))
            
            conn.commit()
            
            # Generate assistant response based on wizard configuration
            assistant_response = await self._generate_sandbox_response(
                wizard_config,
                conversation_id,
                message
            )
            
            # Save assistant message (assistant is 'renus' in the CHECK constraint)
            cur.execute("""
                INSERT INTO messages (conversation_id, sender, type, content, channel, timestamp, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(conversation_id),
                'renus',  # Assistant is 'renus' in the CHECK constraint
                'text',
                assistant_response['content'],
                'Web',
                now,
                now
            ))
            
            conn.commit()
            
        finally:
            cur.close()
            conn.close()
        
        return SandboxMessageResponse(
            role='assistant',
            content=assistant_response['content'],
            timestamp=now,
            collected_data=assistant_response.get('collected_data'),
        )
    
    def get_sandbox_history(self, wizard_id_or_conversation_id: UUID) -> List[Dict[str, Any]]:
        """
        Get conversation history from sandbox
        
        Args:
            wizard_id_or_conversation_id: Wizard session ID or conversation ID
            
        Returns:
            List of messages
        """
        # Try as conversation_id first (for internal use)
        messages_result = self.supabase.table('messages')\
            .select('*')\
            .eq('conversation_id', str(wizard_id_or_conversation_id))\
            .order('timestamp')\
            .execute()
        
        if messages_result.data:
            return messages_result.data
        
        # If no messages, try as wizard_id
        wizard_result = self.supabase.table('sub_agents')\
            .select('config')\
            .eq('id', str(wizard_id_or_conversation_id))\
            .single()\
            .execute()
        
        if not wizard_result.data:
            return []
        
        sandbox_info = wizard_result.data.get('config', {}).get('sandbox')
        if not sandbox_info:
            return []
        
        conversation_id = sandbox_info['conversation_id']
        
        # Get messages
        messages_result = self.supabase.table('messages')\
            .select('*')\
            .eq('conversation_id', conversation_id)\
            .order('timestamp')\
            .execute()
        
        return messages_result.data or []
    
    def get_collected_data(self, wizard_id: UUID) -> Dict[str, Any]:
        """
        Get information collected during sandbox
        
        Args:
            wizard_id: Wizard session ID
            
        Returns:
            Collected data
        """
        # Get conversation history
        history = self.get_sandbox_history(wizard_id)
        
        # Extract collected data from messages metadata
        collected = {}
        
        for msg in history:
            if msg.get('role') == 'assistant':
                metadata = msg.get('metadata', {})
                if 'collected_field' in metadata:
                    field_name = metadata['collected_field']
                    field_value = metadata.get('field_value')
                    if field_value:
                        collected[field_name] = field_value
        
        return collected
    
    def cleanup_sandbox(self, wizard_id: UUID) -> bool:
        """
        Delete sandbox data
        
        Args:
            wizard_id: Wizard session ID
            
        Returns:
            True if cleaned up successfully
        """
        # Get sandbox info
        wizard_result = self.supabase.table('sub_agents')\
            .select('config')\
            .eq('id', str(wizard_id))\
            .single()\
            .execute()
        
        if not wizard_result.data:
            return False
        
        sandbox_info = wizard_result.data.get('config', {}).get('sandbox')
        if not sandbox_info:
            return True  # Already cleaned up
        
        conversation_id = sandbox_info['conversation_id']
        
        # Delete messages
        self.supabase.table('messages')\
            .delete()\
            .eq('conversation_id', conversation_id)\
            .execute()
        
        # Delete conversation
        self.supabase.table('conversations')\
            .delete()\
            .eq('id', conversation_id)\
            .execute()
        
        # Remove sandbox info from wizard config
        wizard_config = wizard_result.data.get('config', {})
        if 'sandbox' in wizard_config:
            del wizard_config['sandbox']
            
            self.supabase.table('sub_agents')\
                .update({'config': wizard_config})\
                .eq('id', str(wizard_id))\
                .execute()
        
        return True
    
    async def _generate_sandbox_response(
        self,
        wizard_config: Dict[str, Any],
        conversation_id: UUID,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Generate sandbox response using WizardAgent with LangGraph.
        
        Creates temporary agent instance from wizard configuration and
        processes message through LangGraph for real behavior testing.
        """
        from src.agents.wizard_agent import create_wizard_agent
        from langchain_core.messages import HumanMessage, AIMessage
        
        # Create agent from wizard configuration
        agent = create_wizard_agent(wizard_config)
        
        # Load conversation history
        history_data = self.get_sandbox_history(conversation_id)
        
        # Convert to LangChain messages
        messages = []
        for msg in history_data:
            sender = msg.get('sender', 'client')
            content = msg.get('content', '')
            
            if sender == 'client':
                messages.append(HumanMessage(content=content))
            elif sender == 'renus':
                messages.append(AIMessage(content=content))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        # Process through agent
        result = await agent.invoke(
            messages=messages,
            context={
                'conversation_id': str(conversation_id),
                'is_sandbox': True,
            }
        )
        
        return {
            'content': result['response'],
            'metadata': {
                'is_complete': result.get('is_complete', False),
                'remaining_fields': result.get('remaining_fields', []),
            },
            'collected_data': result.get('collected_data', {}),
        }


# Singleton instance
_sandbox_service = None

def get_sandbox_service() -> SandboxService:
    """Get singleton instance of SandboxService"""
    global _sandbox_service
    if _sandbox_service is None:
        _sandbox_service = SandboxService()
    return _sandbox_service
