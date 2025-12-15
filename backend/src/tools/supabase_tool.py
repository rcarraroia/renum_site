"""
Supabase Tool - LangChain Tool for Database Queries
Sprint 07A - Integrações Core (Updated)

Tool that allows agents to query the CLIENT'S Supabase database.
Uses ClientSupabaseClient for secure, read-only access.
"""

from typing import Any, Dict, Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from uuid import UUID
import asyncio

from ..integrations.client_supabase import ClientSupabaseClient
from ..services.integration_service import IntegrationService


class SupabaseQueryInput(BaseModel):
    """Input schema for Supabase queries"""
    
    table: str = Field(..., description="Table name to query (e.g., 'leads', 'clients', 'interviews')")
    operation: str = Field(..., description="Operation: 'select', 'insert', 'update', 'delete'")
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Filter conditions as key-value pairs (e.g., {'status': 'active'})"
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Data for insert/update operations"
    )
    columns: Optional[str] = Field(
        default="*",
        description="Columns to select (default: '*' for all columns)"
    )
    limit: Optional[int] = Field(
        default=None,
        description="Maximum number of records to return"
    )
    order_by: Optional[str] = Field(
        default=None,
        description="Column to order by (e.g., 'created_at')"
    )
    order_desc: bool = Field(
        default=False,
        description="Whether to order descending"
    )


class SupabaseTool(BaseTool):
    """
    Tool for querying CLIENT'S Supabase database.
    
    Supports read-only select operations on whitelisted tables.
    Uses ClientSupabaseClient for secure access.
    """
    
    name: str = "query_client_database"
    description: str = """Query the client's Supabase database (read-only).
    
    Use this tool to fetch data from the client's database.
    Only SELECT operations are allowed on whitelisted tables.
    
    Examples:
    - Select all active leads: table='leads', operation='select', filters={'status': 'active'}
    - Count interviews: table='interviews', operation='select', columns='count(*)'
    - Get recent orders: table='orders', operation='select', order_by='created_at', order_desc=True, limit=10
    """
    args_schema: Type[BaseModel] = SupabaseQueryInput
    
    client_id: Optional[UUID] = None
    
    def __init__(self, client_id: Optional[UUID] = None, **kwargs):
        """
        Initialize Supabase Tool.
        
        Args:
            client_id: Client ID for loading database integration config
            **kwargs: Additional arguments for BaseTool
        """
        super().__init__(**kwargs)
        self.client_id = client_id
    
    def _run(
        self,
        table: str,
        operation: str,
        filters: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        columns: str = "*",
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """Synchronous version"""
        return asyncio.run(self._arun(table, operation, filters, data, columns, limit, order_by, order_desc))
    
    async def _arun(
        self,
        table: str,
        operation: str,
        filters: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        columns: str = "*",
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Execute async query on client's database.
        
        Args:
            table: Table name
            operation: Operation type (only 'select' is allowed)
            filters: Filter conditions
            data: Data (not used for read-only)
            columns: Columns to select
            limit: Maximum records to return
            order_by: Column to order by
            order_desc: Order descending
        
        Returns:
            Dictionary with success status and data/error
        """
        try:
            # Validate operation (read-only)
            if operation != "select":
                return {
                    "success": False,
                    "error": f"Operation '{operation}' not allowed. Only 'select' is permitted (read-only mode)"
                }
            
            # Load integration config
            if not self.client_id:
                return {
                    "success": False,
                    "error": "client_id is required to query database"
                }
            
            integration_service = IntegrationService()
            integration = await integration_service.get_integration(self.client_id, "database")
            
            if not integration:
                return {
                    "success": False,
                    "error": "Database integration not configured for this client"
                }
            
            if integration.status != "active":
                return {
                    "success": False,
                    "error": f"Database integration is {integration.status}, not active"
                }
            
            # Get decrypted config
            config = await integration_service.decrypt_credentials(integration.config)
            
            # Create ClientSupabaseClient
            client = ClientSupabaseClient(
                supabase_url=config.get("supabase_url"),
                supabase_key=config.get("supabase_key"),
                read_only=True,  # Enforce read-only
                allowed_tables=config.get("allowed_tables", [])
            )
            
            # Execute query
            result = await client.execute_query(
                table=table,
                operation=operation,
                filters=filters,
                columns=columns,
                limit=limit,
                order_by=order_by,
                order_desc=order_desc
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }


def create_supabase_tool(client_id: Optional[UUID] = None) -> SupabaseTool:
    """
    Factory function to create a Supabase Tool with client_id.
    
    Args:
        client_id: Client ID for loading database integration config
    
    Returns:
        Configured SupabaseTool instance
    """
    return SupabaseTool(client_id=client_id)
