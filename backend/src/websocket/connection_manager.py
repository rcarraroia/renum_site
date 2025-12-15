"""
WebSocket Connection Manager - Sprint 09
Manages active WebSocket connections and presence tracking
"""

from typing import Dict, Set, Optional
from datetime import datetime
from fastapi import WebSocket
from src.utils.logger import logger


class ConnectionManager:
    """
    Manages WebSocket connections for real-time communication
    
    Features:
    - Track active connections per user
    - Send personal messages
    - Broadcast to multiple users
    - Presence tracking (online, offline, away)
    """
    
    def __init__(self):
        """Initialize connection manager"""
        # Active connections: user_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        
        # User presence: user_id -> status
        self.user_presence: Dict[str, str] = {}
        
        # Last activity: user_id -> timestamp
        self.last_activity: Dict[str, datetime] = {}
        
        # Conversation participants: conversation_id -> Set[user_id]
        self.conversation_participants: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """
        Accept and register new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
        """
        await websocket.accept()
        
        # Store connection
        self.active_connections[user_id] = websocket
        
        # Set presence to online
        self.user_presence[user_id] = "online"
        self.last_activity[user_id] = datetime.utcnow()
        
        logger.info(f"WebSocket connected: user_id={user_id}")
        logger.info(f"Active connections: {len(self.active_connections)}")
    
    def disconnect(self, user_id: str) -> None:
        """
        Remove WebSocket connection
        
        Args:
            user_id: User ID
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Set presence to offline
        self.user_presence[user_id] = "offline"
        
        # Remove from conversation participants
        for conversation_id in list(self.conversation_participants.keys()):
            if user_id in self.conversation_participants[conversation_id]:
                self.conversation_participants[conversation_id].remove(user_id)
                
                # Remove empty conversation
                if not self.conversation_participants[conversation_id]:
                    del self.conversation_participants[conversation_id]
        
        logger.info(f"WebSocket disconnected: user_id={user_id}")
        logger.info(f"Active connections: {len(self.active_connections)}")
    
    async def send_personal(self, user_id: str, message: dict) -> bool:
        """
        Send message to specific user
        
        Args:
            user_id: Target user ID
            message: Message data
            
        Returns:
            True if sent successfully, False otherwise
        """
        if user_id not in self.active_connections:
            logger.warning(f"User {user_id} not connected, cannot send message")
            return False
        
        try:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)
            logger.debug(f"Sent personal message to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending personal message to {user_id}: {e}")
            # Remove broken connection
            self.disconnect(user_id)
            return False
    
    async def broadcast(self, user_ids: Set[str], message: dict, exclude: Optional[str] = None) -> int:
        """
        Broadcast message to multiple users
        
        Args:
            user_ids: Set of user IDs to send to
            message: Message data
            exclude: Optional user ID to exclude from broadcast
            
        Returns:
            Number of users who received the message
        """
        sent_count = 0
        
        for user_id in user_ids:
            # Skip excluded user
            if exclude and user_id == exclude:
                continue
            
            # Send to user
            if await self.send_personal(user_id, message):
                sent_count += 1
        
        logger.debug(f"Broadcast to {sent_count}/{len(user_ids)} users")
        return sent_count
    
    async def broadcast_to_conversation(
        self, 
        conversation_id: str, 
        message: dict, 
        exclude: Optional[str] = None
    ) -> int:
        """
        Broadcast message to all participants in a conversation
        
        Args:
            conversation_id: Conversation ID
            message: Message data
            exclude: Optional user ID to exclude
            
        Returns:
            Number of users who received the message
        """
        if conversation_id not in self.conversation_participants:
            logger.warning(f"No participants in conversation {conversation_id}")
            return 0
        
        participants = self.conversation_participants[conversation_id]
        return await self.broadcast(participants, message, exclude)
    
    def join_conversation(self, user_id: str, conversation_id: str) -> None:
        """
        Add user to conversation participants
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID
        """
        if conversation_id not in self.conversation_participants:
            self.conversation_participants[conversation_id] = set()
        
        self.conversation_participants[conversation_id].add(user_id)
        logger.debug(f"User {user_id} joined conversation {conversation_id}")
    
    def leave_conversation(self, user_id: str, conversation_id: str) -> None:
        """
        Remove user from conversation participants
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID
        """
        if conversation_id in self.conversation_participants:
            self.conversation_participants[conversation_id].discard(user_id)
            
            # Remove empty conversation
            if not self.conversation_participants[conversation_id]:
                del self.conversation_participants[conversation_id]
            
            logger.debug(f"User {user_id} left conversation {conversation_id}")
    
    def update_presence(self, user_id: str, status: str) -> None:
        """
        Update user presence status
        
        Args:
            user_id: User ID
            status: Presence status (online, offline, away)
        """
        valid_statuses = ["online", "offline", "away"]
        if status not in valid_statuses:
            logger.warning(f"Invalid presence status: {status}")
            return
        
        self.user_presence[user_id] = status
        self.last_activity[user_id] = datetime.utcnow()
        logger.debug(f"User {user_id} presence updated to {status}")
    
    def get_presence(self, user_id: str) -> str:
        """
        Get user presence status
        
        Args:
            user_id: User ID
            
        Returns:
            Presence status (online, offline, away)
        """
        return self.user_presence.get(user_id, "offline")
    
    def is_connected(self, user_id: str) -> bool:
        """
        Check if user is connected
        
        Args:
            user_id: User ID
            
        Returns:
            True if connected, False otherwise
        """
        return user_id in self.active_connections
    
    def get_conversation_participants(self, conversation_id: str) -> Set[str]:
        """
        Get all participants in a conversation
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Set of user IDs
        """
        return self.conversation_participants.get(conversation_id, set())
    
    def get_stats(self) -> dict:
        """
        Get connection manager statistics
        
        Returns:
            Dict with statistics
        """
        return {
            "active_connections": len(self.active_connections),
            "total_conversations": len(self.conversation_participants),
            "online_users": len([u for u, s in self.user_presence.items() if s == "online"]),
            "away_users": len([u for u, s in self.user_presence.items() if s == "away"]),
        }


# Singleton instance
_connection_manager = None

def get_connection_manager() -> ConnectionManager:
    """Get singleton instance of ConnectionManager"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager
