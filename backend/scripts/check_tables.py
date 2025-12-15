from src.config.supabase import supabase_admin
print("Tables:")
try:
    # Not all supabase clients support listing tables directly via API reliably without SQL extension
    # But we can try to infer from common tables
    res = supabase_admin.table('agents').select('count', count='exact').limit(1).execute()
    print("agents: OK")
except: print("agents: Missing")

try:
    res = supabase_admin.table('agent_integrations').select('count', count='exact').limit(1).execute()
    print("agent_integrations: OK")
except: print("agent_integrations: Missing")

try:
    res = supabase_admin.table('credentials').select('count', count='exact').limit(1).execute()
    print("credentials: OK")
except: print("credentials: Missing")
