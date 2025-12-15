"""
Client Supabase Client - Sprint 07A
Client for connecting to client's own Supabase database
"""

from supabase import create_client, Client
from typing import Dict, Any, Optional, List
from ..utils.logger import logger
import re


class ClientSupabaseClient:
    """
    Client for querying client's own Supabase database.
    Enforces read-only mode and table whitelist for security.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize client Supabase client.
        
        Args:
            config: Configuration dict with keys:
                - supabase_url: Client's Supabase project URL
                - supabase_key: Client's Supabase service key
                - read_only: Restrict to read-only queries (default: True)
                - allowed_tables: Whitelist of allowed tables (default: all)
        """
        self.supabase_url = config['supabase_url']
        self.supabase_key = config['supabase_key']
        self.read_only = config.get('read_only', True)
        self.allowed_tables = config.get('allowed_tables', [])
        
        # Create Supabase client
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
        logger.info(f"[ClientSupabase] Client initialized (read_only={self.read_only})")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        return bool(self.supabase_url and self.supabase_key)
    
    def _validate_table(self, table: str) -> bool:
        """
        Validate table name against whitelist.
        
        Args:
            table: Table name to validate
        
        Returns:
            True if valid, False otherwise
        """
        # If no whitelist, allow all tables
        if not self.allowed_tables:
            return True
        
        return table in self.allowed_tables
    
    def _validate_query_safety(self, operation: str) -> bool:
        """
        Validate query operation for safety.
        
        Args:
            operation: Operation type (select, insert, update, delete)
        
        Returns:
            True if safe, False otherwise
        """
        # If read_only, only allow SELECT
        if self.read_only and operation.lower() != 'select':
            return False
        
        return True
    
    async def execute_query(
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
        Execute query on client's database.
        
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
            dict with success status and data/error
        """
        # Validate table
        if not self._validate_table(table):
            return {
                "success": False,
                "error": f"Table '{table}' is not in allowed tables list"
            }
        
        # Validate operation
        if not self._validate_query_safety(operation):
            return {
                "success": False,
                "error": f"Operation '{operation}' not allowed in read-only mode"
            }
        
        logger.info(f"[ClientSupabase] Executing {operation} on table {table}")
        
        try:
            if operation.lower() == 'select':
                query = self.client.table(table).select(columns)
                
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
            
            elif operation.lower() == 'insert':
                if not data:
                    return {"success": False, "error": "Data is required for insert operation"}
                
                result = self.client.table(table).insert(data).execute()
                
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            elif operation.lower() == 'update':
                if not data:
                    return {"success": False, "error": "Data is required for update operation"}
                if not filters:
                    return {"success": False, "error": "Filters are required for update operation"}
                
                query = self.client.table(table).update(data)
                
                # Apply filters
                for key, value in filters.items():
                    query = query.eq(key, value)
                
                result = query.execute()
                
                return {
                    "success": True,
                    "data": result.data,
                    "count": len(result.data)
                }
            
            elif operation.lower() == 'delete':
                if not filters:
                    return {"success": False, "error": "Filters are required for delete operation"}
                
                query = self.client.table(table).delete()
                
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
            logger.error(f"[ClientSupabase] Error executing query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to client's database.
        
        Returns:
            dict with success status and message
        """
        import time
        start_time = time.time()
        
        try:
            # Try to execute a simple query
            result = self.client.rpc('version').execute()
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"[ClientSupabase] Connection test successful ({latency_ms}ms)")
            
            return {
                "success": True,
                "message": "Connection successful",
                "latency_ms": latency_ms
            }
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.error(f"[ClientSupabase] Connection test failed: {str(e)}")
            
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "latency_ms": latency_ms
            }
