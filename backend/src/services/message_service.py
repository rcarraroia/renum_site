"""
Message service for business logic
"""
from typing import Optional, List
from uuid import UUID
from src.config.supabase import supabase_admin
from src.models.message import MessageCreate, MessageResponse
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


class MessageService:
    """Service for message operations"""
    
    async def send_message(
        self,
        data: MessageCreate
    ) -> MessageResponse:
        """
        Send and persist message
        
        Args:
            data: Message data
            
        Returns:
            Created message
            
        Raises:
            ValidationError: Invalid data
        """
        try:
            # Prepare data
            message_data = data.model_dump()
            
            # Convert UUID to string for Supabase
            message_data['conversation_id'] = str(message_data['conversation_id'])
            
            # Validate content is not empty
            if not message_data['content'].strip():
                raise ValidationError("Message content cannot be empty")
            
            # Insert into database
            response = supabase_admin.table("messages").insert(
                message_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to send message")
            
            created = response.data[0]
            
            # Update conversation last_update timestamp
            await self._update_conversation_timestamp(message_data['conversation_id'])
            
            # Increment unread_count if sender is not admin
            if message_data['sender'] != 'admin':
                await self._increment_unread_count(message_data['conversation_id'])
            
            logger.info(f"Sent message: {created['id']} in conversation {message_data['conversation_id']}")
            
            return MessageResponse(**created)
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise ValidationError(f"Failed to send message: {str(e)}")
    
    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        before_id: Optional[str] = None
    ) -> List[MessageResponse]:
        """
        Get message history with pagination
        
        Args:
            conversation_id: Conversation ID
            limit: Number of messages to retrieve
            before_id: Get messages before this message ID (for pagination)
            
        Returns:
            List of messages ordered by timestamp ascending
        """
        try:
            # Base query
            query = supabase_admin.table("messages").select("*").eq(
                "conversation_id", conversation_id
            )
            
            # If before_id is provided, get messages before that timestamp
            if before_id:
                # Get the timestamp of the before_id message
                before_msg = supabase_admin.table("messages").select("timestamp").eq(
                    "id", before_id
                ).single().execute()
                
                if before_msg.data:
                    query = query.lt("timestamp", before_msg.data['timestamp'])
            
            # Order by timestamp descending (most recent first) for limit
            query = query.order("timestamp", desc=True).limit(limit)
            
            # Execute query
            response = query.execute()
            
            # Reverse to get ascending order (oldest first)
            messages = [MessageResponse(**item) for item in reversed(response.data)]
            
            logger.info(f"Retrieved {len(messages)} messages for conversation {conversation_id}")
            
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving messages for conversation {conversation_id}: {str(e)}")
            raise
    
    async def mark_messages_as_read(
        self,
        message_ids: List[str]
    ) -> int:
        """
        Mark messages as read
        
        Args:
            message_ids: List of message IDs to mark as read
            
        Returns:
            Number of messages marked as read
        """
        try:
            if not message_ids:
                return 0
            
            # Update is_read to True for all message IDs
            response = supabase_admin.table("messages").update({
                "is_read": True
            }).in_("id", message_ids).execute()
            
            count = len(response.data) if response.data else 0
            
            # Decrement unread_count for affected conversations
            if count > 0:
                # Get unique conversation IDs
                conversations = set()
                for msg_id in message_ids:
                    msg = supabase_admin.table("messages").select("conversation_id").eq(
                        "id", msg_id
                    ).single().execute()
                    if msg.data:
                        conversations.add(msg.data['conversation_id'])
                
                # Decrement unread_count for each conversation
                for conv_id in conversations:
                    await self._decrement_unread_count(conv_id, count)
            
            logger.info(f"Marked {count} messages as read")
            
            return count
            
        except Exception as e:
            logger.error(f"Error marking messages as read: {str(e)}")
            raise
    
    async def _update_conversation_timestamp(
        self,
        conversation_id: str
    ) -> None:
        """
        Update conversation last_update timestamp
        
        Args:
            conversation_id: Conversation ID
        """
        try:
            supabase_admin.table("conversations").update({
                "last_update": "now()"
            }).eq("id", conversation_id).execute()
            
        except Exception as e:
            logger.error(f"Error updating conversation timestamp {conversation_id}: {str(e)}")
            # Don't raise, this is a non-critical operation
    
    async def _increment_unread_count(
        self,
        conversation_id: str
    ) -> None:
        """
        Increment conversation unread_count
        
        Args:
            conversation_id: Conversation ID
        """
        try:
            # Get current unread_count
            response = supabase_admin.table("conversations").select("unread_count").eq(
                "id", conversation_id
            ).single().execute()
            
            if response.data:
                current_count = response.data.get('unread_count', 0)
                
                # Increment
                supabase_admin.table("conversations").update({
                    "unread_count": current_count + 1
                }).eq("id", conversation_id).execute()
            
        except Exception as e:
            logger.error(f"Error incrementing unread count {conversation_id}: {str(e)}")
            # Don't raise, this is a non-critical operation
    
    async def _decrement_unread_count(
        self,
        conversation_id: str,
        count: int = 1
    ) -> None:
        """
        Decrement conversation unread_count
        
        Args:
            conversation_id: Conversation ID
            count: Number to decrement
        """
        try:
            # Get current unread_count
            response = supabase_admin.table("conversations").select("unread_count").eq(
                "id", conversation_id
            ).single().execute()
            
            if response.data:
                current_count = response.data.get('unread_count', 0)
                
                # Decrement (don't go below 0)
                new_count = max(0, current_count - count)
                
                supabase_admin.table("conversations").update({
                    "unread_count": new_count
                }).eq("id", conversation_id).execute()
            
        except Exception as e:
            logger.error(f"Error decrementing unread count {conversation_id}: {str(e)}")
            # Don't raise, this is a non-critical operation
    
    # Aliases para consistência
    async def create(self, data: MessageCreate) -> MessageResponse:
        """Alias for send_message"""
        return await self.send_message(data)


# Global instance
message_service = MessageService()
