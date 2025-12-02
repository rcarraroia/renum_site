"""
ISA Command Service - Audit logging for ISA commands
Sprint 04 - Sistema Multi-Agente

Service for logging and retrieving ISA administrative commands.
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..config.supabase import supabase_admin
from ..models.isa_command import IsaCommandCreate, IsaCommandResponse
from ..utils.logger import logger


class IsaCommandService:
    """Service for managing ISA command audit logs"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = supabase_admin
    
    async def log_command(
        self,
        admin_id: UUID,
        user_message: str,
        assistant_response: str,
        command_executed: bool = False,
        command_type: Optional[str] = None,
        execution_result: Optional[dict] = None
    ) -> IsaCommandResponse:
        """
        Log an ISA command execution for audit purposes.
        
        Args:
            admin_id: UUID of the admin who executed the command
            user_message: The command message from admin
            assistant_response: ISA's response
            command_executed: Whether a command was actually executed
            command_type: Type of command (query, report, etc)
            execution_result: Result of command execution
        
        Returns:
            IsaCommandResponse with logged command
        
        Raises:
            Exception: If logging fails
        """
        try:
            logger.info(f"Logging ISA command from admin {admin_id}")
            
            # Prepare command data
            command_data = {
                'admin_id': str(admin_id),
                'user_message': user_message,
                'assistant_response': assistant_response,
                'command_executed': command_executed,
                'executed_at': datetime.now().isoformat()
            }
            
            # Add optional fields
            if command_type:
                command_data['command_type'] = command_type
            
            if execution_result:
                command_data['execution_result'] = execution_result
            
            # Insert into database
            response = self.supabase.table('isa_commands').insert(command_data).execute()
            
            if not response.data:
                raise Exception("Failed to log ISA command")
            
            logged_command = IsaCommandResponse(**response.data[0])
            logger.info(f"ISA command logged: {logged_command.id}")
            
            return logged_command
            
        except Exception as e:
            logger.error(f"Error logging ISA command: {e}")
            raise
    
    async def get_command(self, command_id: UUID) -> Optional[IsaCommandResponse]:
        """
        Get a specific ISA command by ID.
        
        Args:
            command_id: UUID of the command
        
        Returns:
            IsaCommandResponse or None if not found
        """
        try:
            response = self.supabase.table('isa_commands')\
                .select('*')\
                .eq('id', str(command_id))\
                .execute()
            
            if not response.data:
                return None
            
            return IsaCommandResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Error getting ISA command {command_id}: {e}")
            raise
    
    async def list_commands(
        self,
        admin_id: Optional[UUID] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[IsaCommandResponse]:
        """
        List ISA commands with optional filtering.
        
        Args:
            admin_id: Filter by admin ID (optional)
            limit: Number of results per page
            offset: Offset for pagination
        
        Returns:
            List of IsaCommandResponse objects
        """
        try:
            # Build query
            query = self.supabase.table('isa_commands').select('*')
            
            # Apply filters
            if admin_id:
                query = query.eq('admin_id', str(admin_id))
            
            # Order by executed_at DESC (most recent first)
            query = query.order('executed_at', desc=True)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1)
            
            # Execute query
            response = query.execute()
            
            return [IsaCommandResponse(**cmd) for cmd in response.data]
            
        except Exception as e:
            logger.error(f"Error listing ISA commands: {e}")
            raise
    
    async def get_admin_history(
        self,
        admin_id: UUID,
        limit: int = 20
    ) -> List[IsaCommandResponse]:
        """
        Get command history for a specific admin.
        
        Args:
            admin_id: UUID of the admin
            limit: Number of recent commands to return
        
        Returns:
            List of recent commands from this admin
        """
        return await self.list_commands(admin_id=admin_id, limit=limit, offset=0)
    
    async def get_recent_commands(self, limit: int = 10) -> List[IsaCommandResponse]:
        """
        Get most recent ISA commands across all admins.
        
        Args:
            limit: Number of recent commands to return
        
        Returns:
            List of most recent commands
        """
        return await self.list_commands(limit=limit, offset=0)
    
    async def count_commands(
        self,
        admin_id: Optional[UUID] = None,
        command_executed_only: bool = False
    ) -> int:
        """
        Count ISA commands with optional filtering.
        
        Args:
            admin_id: Filter by admin ID (optional)
            command_executed_only: Only count commands that were executed
        
        Returns:
            Count of commands
        """
        try:
            # Build query
            query = self.supabase.table('isa_commands').select('id', count='exact')
            
            # Apply filters
            if admin_id:
                query = query.eq('admin_id', str(admin_id))
            
            if command_executed_only:
                query = query.eq('command_executed', True)
            
            # Execute query
            response = query.execute()
            
            return response.count or 0
            
        except Exception as e:
            logger.error(f"Error counting ISA commands: {e}")
            raise
