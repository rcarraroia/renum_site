"""
WebSocket Connection Manager
Manages active WebSocket connections and broadcasting
"""
from typing import Dict, List, Set, Optional
from fastapi import WebSocket
from src.utils.logger import logger


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        # Active connections: {conversation_id: [websockets]}
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
        # User presence: {user_id: {conversation_ids}}
        self.user_presence: Dict[str, Set[str]] = {}
    
    async def connect(
        self,
        websocket: WebSocket,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Register new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            conversation_id: Conversation ID
            user_id: User ID
        """
        # NOTE: websocket.accept() is called in ws_handler before this
        # Do NOT call accept() here to avoid "websocket.accept already called" error
        
        # Add to active connections
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        
        self.active_connections[conversation_id].append(websocket)
        
        # Track user presence
        if user_id not in self.user_presence:
            self.user_presence[user_id] = set()
        
        self.user_presence[user_id].add(conversation_id)
        
        logger.info(
            f"WebSocket connected: user={user_id}, conversation={conversation_id}, "
            f"total_connections={len(self.active_connections[conversation_id])}"
        )
    
    async def disconnect(
        self,
        websocket: WebSocket,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Remove WebSocket connection
        
        Args:
            websocket: WebSocket connection
            conversation_id: Conversation ID
            user_id: User ID
        """
        # Remove from active connections
        if conversation_id in self.active_connections:
            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)
            
            # Clean up empty conversation lists
            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]
        
        # Update user presence
        if user_id in self.user_presence:
            self.user_presence[user_id].discard(conversation_id)
            
            # Clean up empty user presence
            if not self.user_presence[user_id]:
                del self.user_presence[user_id]
        
        logger.info(
            f"WebSocket disconnected: user={user_id}, conversation={conversation_id}"
        )
    
    async def broadcast_to_conversation(
        self,
        conversation_id: str,
        message: dict
    ) -> int:
        """
        Send message to all connections in a conversation
        
        Args:
            conversation_id: Conversation ID
            message: Message to broadcast
            
        Returns:
            Number of successful broadcasts
        """
        if conversation_id not in self.active_connections:
            logger.debug(f"No active connections for conversation {conversation_id}")
            return 0
        
        connections = self.active_connections[conversation_id].copy()
        successful = 0
        failed_connections = []
        
        for connection in connections:
            try:
                await connection.send_json(message)
                successful += 1
            except Exception as e:
                logger.error(f"Failed to broadcast to connection: {str(e)}")
                failed_connections.append(connection)
        
        # Clean up failed connections
        for failed_conn in failed_connections:
            if failed_conn in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(failed_conn)
        
        logger.info(
            f"Broadcast to conversation {conversation_id}: "
            f"successful={successful}, failed={len(failed_connections)}"
        )
        
        return successful
    
    async def broadcast_to_all(
        self,
        message: dict
    ) -> int:
        """
        Send message to all active connections
        
        Args:
            message: Message to broadcast
            
        Returns:
            Number of successful broadcasts
        """
        total_successful = 0
        
        for conversation_id in list(self.active_connections.keys()):
            successful = await self.broadcast_to_conversation(conversation_id, message)
            total_successful += successful
        
        logger.info(f"Broadcast to all: successful={total_successful}")
        
        return total_successful
    
    def get_connections_count(
        self,
        conversation_id: Optional[str] = None
    ) -> int:
        """
        Get number of active connections
        
        Args:
            conversation_id: Optional conversation ID to filter
            
        Returns:
            Number of connections
        """
        if conversation_id:
            return len(self.active_connections.get(conversation_id, []))
        
        return sum(len(conns) for conns in self.active_connections.values())
    
    def is_user_connected(
        self,
        user_id: str,
        conversation_id: Optional[str] = None
    ) -> bool:
        """
        Check if user is connected
        
        Args:
            user_id: User ID
            conversation_id: Optional conversation ID to check
            
        Returns:
            True if user is connected
        """
        if user_id not in self.user_presence:
            return False
        
        if conversation_id:
            return conversation_id in self.user_presence[user_id]
        
        return len(self.user_presence[user_id]) > 0
    
    def get_online_users(
        self,
        conversation_id: str
    ) -> Set[str]:
        """
        Get list of online users in a conversation
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Set of user IDs
        """
        online_users = set()
        
        for user_id, conversations in self.user_presence.items():
            if conversation_id in conversations:
                online_users.add(user_id)
        
        return online_users


# Global instance
connection_manager = ConnectionManager()
