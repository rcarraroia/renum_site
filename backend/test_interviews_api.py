"""
Test script for Interviews API
Sprint 08 - FASE 5: Interviews Validation
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

# Test data
test_interview_id = None
test_message_ids = []


def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_result(test_name, success, details=""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")


def test_1_start_interview():
    """Test 1: Start new interview"""
    global test_interview_id
    
    print_section("TEST 1: Start New Interview")
    
    try:
        response = requests.post(
            f"{API_URL}/interviews/start",
            json={
                "lead_id": None,
                "subagent_id": None
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            test_interview_id = data.get('id')
            
            # Validate response structure
            assert 'id' in data, "Missing 'id' in response"
            assert 'status' in data, "Missing 'status' in response"
            assert data['status'] == 'in_progress', f"Expected status 'in_progress', got '{data['status']}'"
            assert 'started_at' in data, "Missing 'started_at' in response"
            
            print_result("Start Interview", True, f"Interview ID: {test_interview_id}")
            return True
        else:
            print_result("Start Interview", False, f"Expected 201, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Start Interview", False, str(e))
        return False


def test_2_list_interviews():
    """Test 2: List interviews"""
    print_section("TEST 2: List Interviews")
    
    try:
        response = requests.get(f"{API_URL}/interviews")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            assert 'interviews' in data, "Missing 'interviews' in response"
            assert 'total' in data, "Missing 'total' in response"
            assert 'page' in data, "Missing 'page' in response"
            assert 'page_size' in data, "Missing 'page_size' in response"
            assert 'total_pages' in data, "Missing 'total_pages' in response"
            assert isinstance(data['interviews'], list), "'interviews' should be a list"
            
            print_result("List Interviews", True, f"Found {data['total']} interviews")
            return True
        else:
            print_result("List Interviews", False, f"Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("List Interviews", False, str(e))
        return False


def test_3_get_interview_details():
    """Test 3: Get interview details"""
    print_section("TEST 3: Get Interview Details")
    
    if not test_interview_id:
        print_result("Get Interview Details", False, "No interview ID available")
        return False
    
    try:
        response = requests.get(f"{API_URL}/interviews/{test_interview_id}")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            assert 'interview' in data, "Missing 'interview' in response"
            assert 'messages' in data, "Missing 'messages' in response"
            assert 'progress' in data, "Missing 'progress' in response"
            
            interview = data['interview']
            assert interview['id'] == test_interview_id, "Interview ID mismatch"
            
            progress = data['progress']
            assert 'collected' in progress, "Missing 'collected' in progress"
            assert 'total' in progress, "Missing 'total' in progress"
            assert 'percentage' in progress, "Missing 'percentage' in progress"
            
            print_result("Get Interview Details", True, f"Progress: {progress['collected']}/{progress['total']} ({progress['percentage']}%)")
            return True
        else:
            print(f"Response: {response.text}")
            print_result("Get Interview Details", False, f"Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Get Interview Details", False, str(e))
        return False


def test_4_send_message():
    """Test 4: Send message to interview"""
    print_section("TEST 4: Send Message")
    
    if not test_interview_id:
        print_result("Send Message", False, "No interview ID available")
        return False
    
    try:
        response = requests.post(
            f"{API_URL}/interviews/{test_interview_id}/messages",
            json={
                "content": "Olá! Meu nome é João Silva e trabalho na empresa TechCorp."
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            assert 'user_message' in data, "Missing 'user_message' in response"
            assert 'agent_response' in data, "Missing 'agent_response' in response"
            assert 'progress' in data, "Missing 'progress' in response"
            assert 'is_complete' in data, "Missing 'is_complete' in response"
            
            user_msg = data['user_message']
            agent_msg = data['agent_response']
            
            assert user_msg['role'] == 'user', "User message role should be 'user'"
            assert agent_msg['role'] == 'assistant', "Agent message role should be 'assistant'"
            
            print_result("Send Message", True, f"Agent responded: {agent_msg['content'][:100]}...")
            return True
        else:
            print(f"Response: {response.text}")
            print_result("Send Message", False, f"Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Send Message", False, str(e))
        return False


def test_5_get_messages():
    """Test 5: Get interview messages"""
    print_section("TEST 5: Get Interview Messages")
    
    if not test_interview_id:
        print_result("Get Messages", False, "No interview ID available")
        return False
    
    try:
        response = requests.get(f"{API_URL}/interviews/{test_interview_id}/messages")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            assert 'messages' in data, "Missing 'messages' in response"
            assert 'total' in data, "Missing 'total' in response"
            assert isinstance(data['messages'], list), "'messages' should be a list"
            
            # Should have at least 2 messages (user + agent from test 4)
            assert len(data['messages']) >= 2, f"Expected at least 2 messages, got {len(data['messages'])}"
            
            print_result("Get Messages", True, f"Found {data['total']} messages")
            return True
        else:
            print(f"Response: {response.text}")
            print_result("Get Messages", False, f"Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Get Messages", False, str(e))
        return False


def test_6_update_interview():
    """Test 6: Update interview data"""
    print_section("TEST 6: Update Interview")
    
    if not test_interview_id:
        print_result("Update Interview", False, "No interview ID available")
        return False
    
    try:
        response = requests.put(
            f"{API_URL}/interviews/{test_interview_id}",
            json={
                "contact_name": "João Silva",
                "email": "joao.silva@techcorp.com",
                "company": "TechCorp"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate updated fields
            assert data['contact_name'] == "João Silva", "contact_name not updated"
            assert data['email'] == "joao.silva@techcorp.com", "email not updated"
            assert data['company'] == "TechCorp", "company not updated"
            
            print_result("Update Interview", True, "Interview data updated successfully")
            return True
        else:
            print(f"Response: {response.text}")
            print_result("Update Interview", False, f"Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Update Interview", False, str(e))
        return False


def cleanup():
    """Cleanup: Delete test interview"""
    print_section("CLEANUP: Delete Test Interview")
    
    if not test_interview_id:
        print("No interview to cleanup")
        return
    
    try:
        # Note: There's no DELETE endpoint in the routes, so we'll leave it
        # In production, you might want to add a DELETE endpoint or mark as deleted
        print(f"⚠️  Note: Interview {test_interview_id} left in database (no DELETE endpoint)")
        print("   You may want to manually delete it or add a DELETE endpoint")
        
    except Exception as e:
        print(f"Cleanup error: {e}")


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("  INTERVIEWS API VALIDATION - SPRINT 08 FASE 5")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Start Interview", test_1_start_interview()))
    results.append(("List Interviews", test_2_list_interviews()))
    results.append(("Get Interview Details", test_3_get_interview_details()))
    results.append(("Send Message", test_4_send_message()))
    results.append(("Get Messages", test_5_get_messages()))
    results.append(("Update Interview", test_6_update_interview()))
    
    # Cleanup
    cleanup()
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"  TOTAL: {passed}/{total} tests passed ({int(passed/total*100)}%)")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Interviews API is working correctly.")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
