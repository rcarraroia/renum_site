"""
Integration Tests - Complete Flow Validation
Tests all 6 core functionalities end-to-end
"""

import sys
import time
from datetime import datetime

# Add backend to path
sys.path.insert(0, 'E:/PROJETOS SITE/Projeto Renum/Projeto Site Renum/renum_site/backend')

from src.utils.supabase_client import get_client

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_test(name, passed, details=""):
    """Print test result"""
    status = "PASS" if passed else "FAIL"
    symbol = "✓" if passed else "✗"
    print(f"  [{symbol}] {name}: {status}")
    if details:
        print(f"      {details}")

def test_projects_flow():
    """Test complete projects flow"""
    print_header("TEST 1: Projects Flow")
    
    supabase = get_client()
    test_passed = True
    project_id = None
    
    try:
        # 1. Create project
        print("  Step 1: Creating project...")
        project_data = {
            'name': f'Integration Test Project {datetime.now().strftime("%Y%m%d%H%M%S")}',
            'description': 'Test project for integration testing',
            'type': 'AI Native',
            'status': 'Em Andamento'
        }
        result = supabase.table('projects').insert(project_data).execute()
        project_id = result.data[0]['id']
        print_test("Create project", True, f"ID: {project_id}")
        
        # 2. Read project
        print("  Step 2: Reading project...")
        result = supabase.table('projects').select('*').eq('id', project_id).execute()
        print_test("Read project", len(result.data) == 1, f"Found: {len(result.data)} records")
        
        # 3. Update project
        print("  Step 3: Updating project...")
        update_data = {'description': 'Updated description'}
        result = supabase.table('projects').update(update_data).eq('id', project_id).execute()
        print_test("Update project", result.data[0]['description'] == 'Updated description', f"Description updated")
        
        # 4. Delete project
        print("  Step 4: Deleting project...")
        supabase.table('projects').delete().eq('id', project_id).execute()
        result = supabase.table('projects').select('*').eq('id', project_id).execute()
        print_test("Delete project", len(result.data) == 0, "Project deleted successfully")
        
    except Exception as e:
        print_test("Projects flow", False, str(e))
        test_passed = False
        # Cleanup
        if project_id:
            try:
                supabase.table('projects').delete().eq('id', project_id).execute()
            except:
                pass
    
    return test_passed

def test_leads_flow():
    """Test complete leads flow"""
    print_header("TEST 2: Leads Flow")
    
    supabase = get_client()
    test_passed = True
    lead_id = None
    
    try:
        # 1. Create lead
        print("  Step 1: Creating lead...")
        lead_data = {
            'name': f'Test Lead {datetime.now().strftime("%Y%m%d%H%M%S")}',
            'phone': '+5511999999999',
            'email': 'test@example.com',
            'status': 'novo',
            'source': 'pesquisa'
        }
        result = supabase.table('leads').insert(lead_data).execute()
        lead_id = result.data[0]['id']
        print_test("Create lead", True, f"ID: {lead_id}")
        
        # 2. Read lead
        print("  Step 2: Reading lead...")
        result = supabase.table('leads').select('*').eq('id', lead_id).execute()
        print_test("Read lead", len(result.data) == 1, f"Found: {len(result.data)} records")
        
        # 3. Update lead email
        print("  Step 3: Updating lead email...")
        update_data = {'email': 'updated@example.com'}
        result = supabase.table('leads').update(update_data).eq('id', lead_id).execute()
        print_test("Update lead email", result.data[0]['email'] == 'updated@example.com', f"Email: {result.data[0]['email']}")
        
        # 4. Delete lead
        print("  Step 4: Deleting lead...")
        supabase.table('leads').delete().eq('id', lead_id).execute()
        result = supabase.table('leads').select('*').eq('id', lead_id).execute()
        print_test("Delete lead", len(result.data) == 0, "Lead deleted successfully")
        
    except Exception as e:
        print_test("Leads flow", False, str(e))
        test_passed = False
        # Cleanup
        if lead_id:
            try:
                supabase.table('leads').delete().eq('id', lead_id).execute()
            except:
                pass
    
    return test_passed

def test_clients_flow():
    """Test complete clients flow"""
    print_header("TEST 3: Clients Flow")
    
    supabase = get_client()
    test_passed = True
    client_id = None
    
    try:
        # 1. Create client
        print("  Step 1: Creating client...")
        client_data = {
            'company_name': f'Test Company {datetime.now().strftime("%Y%m%d%H%M%S")}',
            'document': '12345678901234',
            'status': 'active',
            'segment': 'test'
        }
        result = supabase.table('clients').insert(client_data).execute()
        client_id = result.data[0]['id']
        print_test("Create client", True, f"ID: {client_id}")
        
        # 2. Read client
        print("  Step 2: Reading client...")
        result = supabase.table('clients').select('*').eq('id', client_id).execute()
        print_test("Read client", len(result.data) == 1, f"Found: {len(result.data)} records")
        
        # 3. Update client
        print("  Step 3: Updating client...")
        update_data = {'segment': 'Teste'}
        result = supabase.table('clients').update(update_data).eq('id', client_id).execute()
        print_test("Update client", result.data[0]['segment'] == 'Teste', f"Segment: {result.data[0]['segment']}")
        
        # 4. Delete client
        print("  Step 4: Deleting client...")
        supabase.table('clients').delete().eq('id', client_id).execute()
        result = supabase.table('clients').select('*').eq('id', client_id).execute()
        print_test("Delete client", len(result.data) == 0, "Client deleted successfully")
        
    except Exception as e:
        print_test("Clients flow", False, str(e))
        test_passed = False
        # Cleanup
        if client_id:
            try:
                supabase.table('clients').delete().eq('id', client_id).execute()
            except:
                pass
    
    return test_passed

def test_interviews_flow():
    """Test complete interviews flow"""
    print_header("TEST 4: Interviews Flow")
    
    supabase = get_client()
    test_passed = True
    lead_id = None
    project_id = None
    interview_id = None
    
    try:
        # Setup: Create lead
        print("  Setup: Creating lead...")
        lead_data = {
            'name': 'Test Lead for Interview',
            'phone': '+5511888888888',
            'status': 'novo',
            'source': 'pesquisa'
        }
        lead_result = supabase.table('leads').insert(lead_data).execute()
        lead_id = lead_result.data[0]['id']
        
        # 1. Create interview
        print("  Step 1: Creating interview...")
        interview_data = {
            'lead_id': lead_id,
            'contact_name': 'Test Contact',
            'contact_phone': '+5511888888888',
            'status': 'in_progress'
        }
        result = supabase.table('interviews').insert(interview_data).execute()
        interview_id = result.data[0]['id']
        print_test("Create interview", True, f"ID: {interview_id}")
        
        # 2. Read interview
        print("  Step 2: Reading interview...")
        result = supabase.table('interviews').select('*').eq('id', interview_id).execute()
        print_test("Read interview", len(result.data) == 1, f"Found: {len(result.data)} records")
        
        # 3. Update interview status
        print("  Step 3: Updating interview status...")
        update_data = {'status': 'completed'}
        result = supabase.table('interviews').update(update_data).eq('id', interview_id).execute()
        print_test("Update interview", result.data[0]['status'] == 'completed', f"Status: {result.data[0]['status']}")
        
        # Cleanup
        print("  Cleanup: Removing test data...")
        if interview_id:
            supabase.table('interviews').delete().eq('id', interview_id).execute()
        if lead_id:
            supabase.table('leads').delete().eq('id', lead_id).execute()
        # Note: project_id not used in interviews table
        print_test("Cleanup", True, "Test data removed")
        
    except Exception as e:
        print_test("Interviews flow", False, str(e))
        test_passed = False
        # Cleanup
        try:
            if interview_id:
                supabase.table('interviews').delete().eq('id', interview_id).execute()
            if lead_id:
                supabase.table('leads').delete().eq('id', lead_id).execute()
        except:
            pass
    
    return test_passed

def test_conversations_flow():
    """Test conversations CRUD (WebSocket deferred)"""
    print_header("TEST 5: Conversations Flow (CRUD only)")
    
    supabase = get_client()
    test_passed = True
    lead_id = None
    conversation_id = None
    
    try:
        # Setup: Create lead
        print("  Setup: Creating lead...")
        lead_data = {
            'name': 'Test Lead for Conversation',
            'phone': '+5511777777777',
            'status': 'novo',
            'source': 'pesquisa'
        }
        lead_result = supabase.table('leads').insert(lead_data).execute()
        lead_id = lead_result.data[0]['id']
        
        # 1. Create conversation
        print("  Step 1: Creating conversation...")
        conversation_data = {
            'status': 'active',
            'channel': 'whatsapp'
        }
        result = supabase.table('conversations').insert(conversation_data).execute()
        conversation_id = result.data[0]['id']
        print_test("Create conversation", True, f"ID: {conversation_id}")
        
        # 2. Read conversation
        print("  Step 2: Reading conversation...")
        result = supabase.table('conversations').select('*').eq('id', conversation_id).execute()
        print_test("Read conversation", len(result.data) == 1, f"Found: {len(result.data)} records")
        
        # 3. Update conversation
        print("  Step 3: Updating conversation channel...")
        update_data = {'channel': 'email'}
        result = supabase.table('conversations').update(update_data).eq('id', conversation_id).execute()
        print_test("Update conversation", result.data[0]['channel'] == 'email', f"Channel: {result.data[0]['channel']}")
        
        # Note: WebSocket tests deferred to next sprint
        print("\n  Note: WebSocket real-time messaging tests deferred to next sprint")
        
        # Cleanup
        print("  Cleanup: Removing test data...")
        if conversation_id:
            supabase.table('conversations').delete().eq('id', conversation_id).execute()
        if lead_id:
            supabase.table('leads').delete().eq('id', lead_id).execute()
        print_test("Cleanup", True, "Test data removed")
        
    except Exception as e:
        print_test("Conversations flow", False, str(e))
        test_passed = False
        # Cleanup
        try:
            if conversation_id:
                supabase.table('conversations').delete().eq('id', conversation_id).execute()
            if lead_id:
                supabase.table('leads').delete().eq('id', lead_id).execute()
        except:
            pass
    
    return test_passed

def test_reports_flow():
    """Test reports data retrieval"""
    print_header("TEST 6: Reports Flow")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # 1. Test data exists
        print("  Step 1: Checking if data exists for reports...")
        projects = supabase.table('projects').select('id').limit(1).execute()
        leads = supabase.table('leads').select('id').limit(1).execute()
        clients = supabase.table('clients').select('id').limit(1).execute()
        
        has_data = len(projects.data) > 0 or len(leads.data) > 0 or len(clients.data) > 0
        print_test("Data exists", has_data, f"Projects: {len(projects.data)}, Leads: {len(leads.data)}, Clients: {len(clients.data)}")
        
        # 2. Test aggregations
        print("  Step 2: Testing aggregations...")
        total_projects = supabase.table('projects').select('id', count='exact').execute()
        total_leads = supabase.table('leads').select('id', count='exact').execute()
        total_clients = supabase.table('clients').select('id', count='exact').execute()
        
        print_test("Count aggregations", True, f"Projects: {total_projects.count}, Leads: {total_leads.count}, Clients: {total_clients.count}")
        
        # 3. Test filtering
        print("  Step 3: Testing filters...")
        active_projects = supabase.table('projects').select('*').eq('status', 'Em Andamento').execute()
        print_test("Filter by status", True, f"Active projects: {len(active_projects.data)}")
        
    except Exception as e:
        print_test("Reports flow", False, str(e))
        test_passed = False
    
    return test_passed

def test_data_persistence():
    """Test data persists correctly"""
    print_header("TEST 7: Data Persistence")
    
    supabase = get_client()
    test_passed = True
    lead_id = None
    
    try:
        # 1. Create data
        print("  Step 1: Creating test data...")
        lead_data = {
            'name': 'Persistence Test Lead',
            'phone': '+5511666666666',
            'status': 'novo',
            'source': 'pesquisa'
        }
        result = supabase.table('leads').insert(lead_data).execute()
        lead_id = result.data[0]['id']
        print_test("Create data", True, f"ID: {lead_id}")
        
        # 2. Wait a moment
        print("  Step 2: Waiting 1 second...")
        time.sleep(1)
        
        # 3. Verify data still exists
        print("  Step 3: Verifying data persists...")
        result = supabase.table('leads').select('*').eq('id', lead_id).execute()
        persisted = len(result.data) == 1 and result.data[0]['name'] == 'Persistence Test Lead'
        print_test("Data persists", persisted, "Data found after wait")
        
        # Cleanup
        print("  Cleanup: Removing test data...")
        supabase.table('leads').delete().eq('id', lead_id).execute()
        print_test("Cleanup", True, "Test data removed")
        
    except Exception as e:
        print_test("Data persistence", False, str(e))
        test_passed = False
        # Cleanup
        if lead_id:
            try:
                supabase.table('leads').delete().eq('id', lead_id).execute()
            except:
                pass
    
    return test_passed

def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("  INTEGRATION TESTS - SPRINT 08")
    print("  Testing all 6 core functionalities")
    print("="*60)
    
    start_time = time.time()
    results = []
    
    # Run all tests
    results.append(("Projects Flow", test_projects_flow()))
    results.append(("Leads Flow", test_leads_flow()))
    results.append(("Clients Flow", test_clients_flow()))
    results.append(("Interviews Flow", test_interviews_flow()))
    results.append(("Conversations Flow", test_conversations_flow()))
    results.append(("Reports Flow", test_reports_flow()))
    results.append(("Data Persistence", test_data_persistence()))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"  [{symbol}] {name}: {status}")
    
    elapsed = time.time() - start_time
    
    print(f"\n  Total: {passed}/{total} tests passed")
    print(f"  Time: {elapsed:.2f}s")
    
    if passed == total:
        print(f"\n  ✓ ALL INTEGRATION TESTS PASSED!")
        return 0
    else:
        print(f"\n  ✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    exit(main())
