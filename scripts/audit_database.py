"""
Database Audit Script for RENUM System
This script connects to the actual Supabase database and performs comprehensive analysis.
"""

import os
import sys
from supabase import create_client, Client
import json
from datetime import datetime

# Database configuration
SUPABASE_URL = "https://grmwexchkfuztjikxtlp.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdybXdleGNoa2Z1enRqaWt4dGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMTk3NDAxOSwiZXhwIjoyMDQ3NTUwMDE5fQ.1YOHcY46xUo87_bwi8xrWHKL7tE7v_BQcGDCCGLMgEI"

def create_supabase_client() -> Client:
    """Create Supabase client with service role key"""
    return create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

def count_rows_in_table(supabase: Client, table_name: str) -> int:
    """Count rows in a specific table"""
    try:
        result = supabase.table(table_name).select("*", count="exact").limit(0).execute()
        return result.count if result.count is not None else 0
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    """Main audit function"""
    print("=" * 60)
    print("RENUM DATABASE AUDIT")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    try:
        supabase = create_supabase_client()
        print("\n[OK] Successfully connected to Supabase!")
        
        # List of expected tables based on migrations and analysis
        expected_tables = [
            'clients', 'leads', 'projects', 'agents', 'sub_agents',
            'conversations', 'messages', 'interviews', 'interview_messages',
            'integrations', 'triggers', 'trigger_executions', 'interaction_logs',
            'sicc_memories', 'sicc_learnings', 'sicc_patterns', 'sicc_snapshots',
            'sicc_evolution_entries'
        ]
        
        print("\n" + "=" * 60)
        print("TABLE INVENTORY AND ROW COUNTS")
        print("=" * 60)
        
        results = {}
        for table in expected_tables:
            count = count_rows_in_table(supabase, table)
            results[table] = count
            status = "[OK]" if isinstance(count, int) else "[ERR]"
            print(f"{status} {table}: {count}")
        
        # Also try some additional tables that might exist
        additional_tables = [
            'users', 'profiles', 'categories', 'tools', 'agent_tools',
            'renus_config', 'webhooks'
        ]
        
        print("\n" + "=" * 60)
        print("CHECKING ADDITIONAL TABLES")
        print("=" * 60)
        
        for table in additional_tables:
            count = count_rows_in_table(supabase, table)
            if not isinstance(count, str) or "does not exist" not in str(count):
                results[table] = count
                status = "[OK]" if isinstance(count, int) else "[WARN]"
                print(f"{status} {table}: {count}")
        
        print("\n" + "=" * 60)
        print("SAMPLE DATA FROM KEY TABLES")
        print("=" * 60)
        
        # Sample data from key tables
        sample_tables = ['clients', 'leads', 'agents', 'projects']
        for table in sample_tables:
            try:
                result = supabase.table(table).select("*").limit(3).execute()
                if result.data:
                    print(f"\n[DATA] {table} (first 3 records):")
                    for record in result.data:
                        # Show just id and name/title if available
                        id_val = record.get('id', 'N/A')
                        name_val = record.get('name', record.get('title', record.get('email', 'N/A')))
                        print(f"   - ID: {id_val}, Name/Title: {name_val}")
                else:
                    print(f"\n[DATA] {table}: No data found")
            except Exception as e:
                print(f"\n[DATA] {table}: Error - {str(e)[:100]}")
        
        # Save results to JSON
        output = {
            'timestamp': datetime.now().isoformat(),
            'connection': 'SUCCESS',
            'table_counts': results
        }
        
        with open('audit_database_results.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print("\n" + "=" * 60)
        print("[OK] Audit complete! Results saved to audit_database_results.json")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERR] Error connecting to database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
