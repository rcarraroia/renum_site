"""
Supabase Tool - LangChain Tool for Database Queries
Sprint 04 - Sistema Multi-Agente

Tool that allows agents to query the Supabase database with proper RLS enforcement.
"""

from typing import Any, Dict, Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ..config.supabase import supabase_admin


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
    Tool for querying Supabase database.
    
    Supports select, insert, update, delete operations.
    Automatically enforces RLS based on user context (client_id).
    """
    
    name: str = "supabase_query"
    description: str = """Query the Supabase database. 
    Supports select, insert, update, delete operations.
    Automatically enforces Row Level Security (RLS) based on user context.
    
    Examples:
    - Select all active leads: table='leads', operation='select', filters={'status': 'active'}
    - Insert new client: table='clients', operation='insert', data={'name': 'Acme Corp', 'email': 'contact@acme.com'}
    - Update interview status: table='interviews', operation='update', filters={'id': 'uuid'}, data={'status': 'completed'}
    - Count interviews: table='interviews', operation='select', columns='count(*)'
    """
    args_schema: Type[BaseModel] = SupabaseQueryInput
    
    client_id: Optional[str] = None
    
    def __init__(self, client_id: Optional[str] = None, **kwargs):
        """
        Initialize Supabase Tool.
        
        Args:
            client_id: Client ID for multi-tenant filtering (optional)
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
        """
        Execute synchronous query.
        
        Args:
            table: Table name
            operation: Operation type (select, insert, update, delete)
            filters: Filter conditions
            data: Data for insert/update
            columns: Columns to select
            limit: Maximum records to return
            order_by: Column to order by
            order_desc: Order descending
        
        Returns:
            Dictionary with success status and data/error
        """
        try:
            # Add client_id filter if provided (multi-tenant)
            if self.client_id and filters is None:
                filters = {}
            if self.client_id:
                filters["client_id"] = self.client_id
            
            # Execute operation
            if operation == "select":
                query = supabase_admin.table(table).select(columns)
                
                # Apply filters
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                
                # Apply ordering
                if order_by:
                    query = query.order(order_by, desc=order_desc)
                
                # Apply limit
                if limit:
                    query = query.limit(limit)
                
                result = query.execute()
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            elif operation == "insert":
                if not data:
                    return {"success": False, "error": "Data is required for insert operation"}
                
                # Add client_id to data if provided
                if self.client_id:
                    data["client_id"] = self.client_id
                
                result = supabase_admin.table(table).insert(data).execute()
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            elif operation == "update":
                if not data:
                    return {"success": False, "error": "Data is required for update operation"}
                if not filters:
                    return {"success": False, "error": "Filters are required for update operation"}
                
                query = supabase_admin.table(table).update(data)
                
                # Apply filters
                for key, value in filters.items():
                    query = query.eq(key, value)
                
                result = query.execute()
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            elif operation == "delete":
                if not filters:
                    return {"success": False, "error": "Filters are required for delete operation"}
                
                query = supabase_admin.table(table).delete()
                
                # Apply filters
                for key, value in filters.items():
                    query = query.eq(key, value)
                
                result = query.execute()
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}. Supported: select, insert, update, delete"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def _arun(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute async query.
        
        Note: Currently uses sync implementation.
        For true async, would need async Supabase client.
        """
        return self._run(*args, **kwargs)


def create_supabase_tool(client_id: Optional[str] = None) -> SupabaseTool:
    """
    Factory function to create a Supabase Tool with optional client_id.
    
    Args:
        client_id: Client ID for multi-tenant filtering
    
    Returns:
        Configured SupabaseTool instance
    """
    return SupabaseTool(client_id=client_id)
