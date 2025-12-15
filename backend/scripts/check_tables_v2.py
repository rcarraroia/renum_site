import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from src.config.supabase import supabase_admin
print("Tables Check:")

def check_table(name):
    try:
        # We try to select 1 row just to check existence
        res = supabase_admin.table(name).select('count', count='exact').limit(1).execute()
        print(f"{name}: EXISTS")
    except Exception as e:
        # If table doesn't exist, Supabase/PostgREST usually throws error
        if '404' in str(e) or 'does not exist' in str(e):
             print(f"{name}: MISSING")
        else:
             print(f"{name}: ERROR ({str(e)})")

check_table('agents')
check_table('agent_integrations')
check_table('credentials')
check_table('connections')
