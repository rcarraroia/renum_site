"""
Conversation service for business logic
"""
from typing import Optional, List
from uuid import UUID
from src.config.supabase import supabase_admin
from src.models.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse
)
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


class ConversationService:
    """Service for conversation operations"""
    
    async def create_conversation(
        self,
        data: ConversationCreate
    ) -> ConversationResponse:
        """
        Create new conversation
        
        Args:
            data: Conversation data
            
        Returns:
            Created conversation
            
        Raises:
            ValidationError: Invalid data
        """
        try:
            # Prepare data
            conversation_data = data.model_dump()
            
            # Convert UUID to string for Supabase
            conversation_data['client_id'] = str(conversation_data['client_id'])
            if conversation_data.get('assigned_agent_id'):
                conversation_data['assigned_agent_id'] = str(conversation_data['assigned_agent_id'])
            
            # Insert into database
            response = supabase_admin.table("conversations").insert(
                conversation_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create conversation")
            
            created = response.data[0]
            logger.info(f"Created conversation: {created['id']}")
            
            return ConversationResponse(**created)
            
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise ValidationError(f"Failed to create conversation: {str(e)}")
    
    async def list_conversations(
        self,
        page: int = 1,
        limit: int = 20,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> dict:
        """
        List conversations with filters and pagination
        
        Args:
            page: Page number
            limit: Items per page
            client_id: Filter by client
            status: Filter by status
            priority: Filter by priority
            search: Search in summary
            
        Returns:
            Paginated list of conversations
        """
        try:
            # Base query
            query = supabase_admin.table("conversations").select("*", count="exact")
            
            # Apply filters
            if client_id:
                query = query.eq("client_id", client_id)
            
            if status:
                query = query.eq("status", status)
            
            if priority:
                query = query.eq("priority", priority)
            
            if search:
                query = query.ilike("summary", f"%{search}%")
            
            # Pagination
            offset = (page - 1) * limit
            query = query.range(offset, offset + limit - 1)
            
            # Order by last_update (most recent first)
            query = query.order("last_update", desc=True)
            
            # Execute query
            response = query.execute()
            
            total = response.count or 0
            items = [ConversationResponse(**item) for item in response.data]
            has_next = total > (page * limit)
            
            logger.info(f"Listed {len(items)} conversations (page {page}/{limit})")
            
            return {
                "items": items,
                "total": total,
                "page": page,
                "limit": limit,
                "has_next": has_next
            }
            
        except Exception as e:
            logger.error(f"Error listing conversations: {str(e)}")
            raise
    
    async def get_conversation_by_id(
        self,
        conversation_id: str
    ) -> ConversationResponse:
        """
        Get conversation by ID
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation data
            
        Raises:
            NotFoundError: Conversation not found
        """
        try:
            response = supabase_admin.table("conversations").select("*").eq(
                "id", conversation_id
            ).single().execute()
            
            if not response.data:
                raise NotFoundError(f"Conversation {conversation_id} not found")
            
            logger.info(f"Retrieved conversation: {conversation_id}")
            
            return ConversationResponse(**response.data)
            
        except Exception as e:
            logger.error(f"Error retrieving conversation {conversation_id}: {str(e)}")
            if "not found" in str(e).lower() or "No rows found" in str(e):
                raise NotFoundError(f"Conversation {conversation_id} not found")
            raise
    
    async def update_status(
        self,
        conversation_id: str,
        status: str
    ) -> ConversationResponse:
        """
        Update conversation status
        
        Args:
            conversation_id: Conversation ID
            status: New status ('active', 'closed', 'pending')
            
        Returns:
            Updated conversation
            
        Raises:
            NotFoundError: Conversation not found
            ValidationError: Invalid status
        """
        try:
            # Validate status
            valid_statuses = ['active', 'closed', 'pending']
            if status not in valid_statuses:
                raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
            
            # Verify conversation exists
            await self.get_conversation_by_id(conversation_id)
            
            # Update status
            response = supabase_admin.table("conversations").update({
                "status": status
            }).eq("id", conversation_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Conversation {conversation_id} not found")
            
            updated = response.data[0]
            logger.info(f"Updated conversation status: {conversation_id} -> {status}")
            
            return ConversationResponse(**updated)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating conversation status {conversation_id}: {str(e)}")
            raise ValidationError(f"Failed to update status: {str(e)}")
    
    async def update_conversation(
        self,
        conversation_id: str,
        data: ConversationUpdate
    ) -> ConversationResponse:
        """
        Update conversation
        
        Args:
            conversation_id: Conversation ID
            data: Data to update
            
        Returns:
            Updated conversation
            
        Raises:
            NotFoundError: Conversation not found
        """
        try:
            # Verify conversation exists
            await self.get_conversation_by_id(conversation_id)
            
            # Prepare data (only non-None fields)
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                raise ValidationError("No data to update")
            
            # Convert UUIDs to strings
            if 'assigned_agent_id' in update_data and update_data['assigned_agent_id']:
                update_data['assigned_agent_id'] = str(update_data['assigned_agent_id'])
            
            # Update
            response = supabase_admin.table("conversations").update(
                update_data
            ).eq("id", conversation_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Conversation {conversation_id} not found")
            
            updated = response.data[0]
            logger.info(f"Updated conversation: {conversation_id}")
            
            return ConversationResponse(**updated)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating conversation {conversation_id}: {str(e)}")
            raise ValidationError(f"Failed to update conversation: {str(e)}")
    
    async def delete_conversation(
        self,
        conversation_id: str
    ) -> bool:
        """
        Delete conversation (soft delete by setting status to 'closed')
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundError: Conversation not found
        """
        try:
            # Soft delete: set status to closed
            await self.update_status(conversation_id, 'closed')
            
            logger.info(f"Soft deleted conversation: {conversation_id}")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
            raise
    
    async def mark_as_read(
        self,
        conversation_id: str
    ) -> ConversationResponse:
        """
        Mark all messages in conversation as read (set unread_count to 0)
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Updated conversation
            
        Raises:
            NotFoundError: Conversation not found
        """
        try:
            # Verify conversation exists
            await self.get_conversation_by_id(conversation_id)
            
            # Update unread_count to 0
            response = supabase_admin.table("conversations").update({
                "unread_count": 0
            }).eq("id", conversation_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Conversation {conversation_id} not found")
            
            updated = response.data[0]
            logger.info(f"Marked conversation as read: {conversation_id}")
            
            return ConversationResponse(**updated)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error marking conversation as read {conversation_id}: {str(e)}")
            raise


# Global instance
conversation_service = ConversationService()
