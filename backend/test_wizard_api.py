"""
Sprint 06 - Wizard API Integration Tests
Tests all wizard endpoints to ensure functionality
"""

import requests
import json
from uuid import uuid4

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_CLIENT_ID = str(uuid4())  # Mock client ID for testing

# Test results tracking
tests_passed = 0
tests_failed = 0
test_results = []

def log_test(name: str, passed: bool, details: str = ""):
    """Log test result"""
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        status = "✅ PASS"
    else:
        tests_failed += 1
        status = "❌ FAIL"
    
    result = f"{status} - {name}"
    if details:
        result += f"\n    {details}"
    test_results.append(result)
    print(result)

def get_auth_token():
    """Get authentication token (mock for now)"""
    # In production, this would authenticate with real credentials
    # For testing, we'll use a mock token or skip auth
    return None

# Test 1: List Templates
print("\n=== TEST 1: List Templates ===")
try:
    response = requests.get(f"{BASE_URL}/agents/wizard/templates/list")
    if response.status_code == 200:
        templates = response.json()
        if len(templates) == 5:
            log_test("List Templates", True, f"Found {len(templates)} templates")
        else:
            log_test("List Templates", False, f"Expected 5 templates, got {len(templates)}")
    else:
        log_test("List Templates", False, f"Status code: {response.status_code}")
except Exception as e:
    log_test("List Templates", False, f"Exception: {str(e)}")

# Test 2: Get Specific Template
print("\n=== TEST 2: Get Template Details ===")
try:
    response = requests.get(f"{BASE_URL}/agents/wizard/templates/customer_service")
    if response.status_code == 200:
        template = response.json()
        required_fields = ['name', 'description', 'personality', 'system_prompt_base']
        has_all_fields = all(field in template for field in required_fields)
        if has_all_fields:
            log_test("Get Template Details", True, f"Template: {template.get('name')}")
        else:
            log_test("Get Template Details", False, "Missing required fields")
    else:
        log_test("Get Template Details", False, f"Status code: {response.status_code}")
except Exception as e:
    log_test("Get Template Details", False, f"Exception: {str(e)}")

# Test 3: Start Wizard
print("\n=== TEST 3: Start Wizard ===")
wizard_id = None
try:
    payload = {"client_id": TEST_CLIENT_ID}
    response = requests.post(f"{BASE_URL}/agents/wizard/start", json=payload)
    if response.status_code == 201:
        session = response.json()
        wizard_id = session.get('id')
        if wizard_id:
            log_test("Start Wizard", True, f"Wizard ID: {wizard_id}")
        else:
            log_test("Start Wizard", False, "No wizard ID returned")
    else:
        log_test("Start Wizard", False, f"Status code: {response.status_code}, Response: {response.text}")
except Exception as e:
    log_test("Start Wizard", False, f"Exception: {str(e)}")

# Test 4: Save Step 1 (Objective)
print("\n=== TEST 4: Save Step 1 (Objective) ===")
if wizard_id:
    try:
        step_data = {
            "data": {
                "template_type": "customer_service",
                "name": "Test Agent",
                "description": "A test agent for validation",
                "niche": "ecommerce"
            }
        }
        response = requests.put(
            f"{BASE_URL}/agents/wizard/{wizard_id}/step/1",
            json=step_data
        )
        if response.status_code == 200:
            session = response.json()
            if session.get('current_step') == 1:
                log_test("Save Step 1", True, "Step 1 data saved")
            else:
                log_test("Save Step 1", False, f"Current step: {session.get('current_step')}")
        else:
            log_test("Save Step 1", False, f"Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        log_test("Save Step 1", False, f"Exception: {str(e)}")
else:
    log_test("Save Step 1", False, "No wizard ID from previous test")

# Test 5: Save Step 2 (Personality)
print("\n=== TEST 5: Save Step 2 (Personality) ===")
if wizard_id:
    try:
        step_data = {
            "data": {
                "personality": "friendly",
                "tone_formal": 30,
                "tone_direct": 70,
                "custom_instructions": "Be helpful and concise"
            }
        }
        response = requests.put(
            f"{BASE_URL}/agents/wizard/{wizard_id}/step/2",
            json=step_data
        )
        if response.status_code == 200:
            log_test("Save Step 2", True, "Step 2 data saved")
        else:
            log_test("Save Step 2", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Save Step 2", False, f"Exception: {str(e)}")
else:
    log_test("Save Step 2", False, "No wizard ID from previous test")

# Test 6: Save Step 3 (Fields)
print("\n=== TEST 6: Save Step 3 (Fields) ===")
if wizard_id:
    try:
        step_data = {
            "data": {
                "standard_fields": {
                    "name": {"enabled": True, "required": True},
                    "email": {"enabled": True, "required": True},
                    "phone": {"enabled": False, "required": False}
                },
                "custom_fields": [
                    {
                        "label": "Company Size",
                        "type": "dropdown",
                        "required": True,
                        "options": ["1-10", "11-50", "51-200", "200+"]
                    }
                ]
            }
        }
        response = requests.put(
            f"{BASE_URL}/agents/wizard/{wizard_id}/step/3",
            json=step_data
        )
        if response.status_code == 200:
            log_test("Save Step 3", True, "Step 3 data saved")
        else:
            log_test("Save Step 3", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Save Step 3", False, f"Exception: {str(e)}")
else:
    log_test("Save Step 3", False, "No wizard ID from previous test")

# Test 7: Save Step 4 (Integrations)
print("\n=== TEST 7: Save Step 4 (Integrations) ===")
if wizard_id:
    try:
        step_data = {
            "data": {
                "integrations": {
                    "whatsapp": {"enabled": True},
                    "email": {"enabled": False},
                    "database": {"enabled": True}
                }
            }
        }
        response = requests.put(
            f"{BASE_URL}/agents/wizard/{wizard_id}/step/4",
            json=step_data
        )
        if response.status_code == 200:
            log_test("Save Step 4", True, "Step 4 data saved")
        else:
            log_test("Save Step 4", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Save Step 4", False, f"Exception: {str(e)}")
else:
    log_test("Save Step 4", False, "No wizard ID from previous test")

# Test 8: Get Wizard Session
print("\n=== TEST 8: Get Wizard Session ===")
if wizard_id:
    try:
        response = requests.get(f"{BASE_URL}/agents/wizard/{wizard_id}")
        if response.status_code == 200:
            session = response.json()
            has_step_data = all([
                session.get('step_1_data'),
                session.get('step_2_data'),
                session.get('step_3_data'),
                session.get('step_4_data')
            ])
            if has_step_data:
                log_test("Get Wizard Session", True, "All step data retrieved")
            else:
                log_test("Get Wizard Session", False, "Missing step data")
        else:
            log_test("Get Wizard Session", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Get Wizard Session", False, f"Exception: {str(e)}")
else:
    log_test("Get Wizard Session", False, "No wizard ID from previous test")

# Test 9: Start Sandbox
print("\n=== TEST 9: Start Sandbox ===")
sandbox_id = None
if wizard_id:
    try:
        response = requests.post(f"{BASE_URL}/agents/wizard/{wizard_id}/sandbox/start")
        if response.status_code == 201:
            sandbox = response.json()
            sandbox_id = sandbox.get('sandbox_id')
            if sandbox_id:
                log_test("Start Sandbox", True, f"Sandbox ID: {sandbox_id}")
            else:
                log_test("Start Sandbox", False, "No sandbox ID returned")
        else:
            log_test("Start Sandbox", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Start Sandbox", False, f"Exception: {str(e)}")
else:
    log_test("Start Sandbox", False, "No wizard ID from previous test")

# Test 10: Send Sandbox Message
print("\n=== TEST 10: Send Sandbox Message ===")
if wizard_id and sandbox_id:
    try:
        payload = {"message": "Hello, I need help"}
        response = requests.post(
            f"{BASE_URL}/agents/wizard/{wizard_id}/sandbox/message",
            json=payload
        )
        if response.status_code == 200:
            message = response.json()
            if message.get('role') == 'assistant' and message.get('content'):
                log_test("Send Sandbox Message", True, "Received agent response")
            else:
                log_test("Send Sandbox Message", False, "Invalid response format")
        else:
            log_test("Send Sandbox Message", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Send Sandbox Message", False, f"Exception: {str(e)}")
else:
    log_test("Send Sandbox Message", False, "No wizard/sandbox ID from previous tests")

# Test 11: Get Sandbox History
print("\n=== TEST 11: Get Sandbox History ===")
if wizard_id:
    try:
        response = requests.get(f"{BASE_URL}/agents/wizard/{wizard_id}/sandbox/history")
        if response.status_code == 200:
            history = response.json()
            if len(history) >= 2:  # User message + agent response
                log_test("Get Sandbox History", True, f"Found {len(history)} messages")
            else:
                log_test("Get Sandbox History", False, f"Expected >= 2 messages, got {len(history)}")
        else:
            log_test("Get Sandbox History", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Get Sandbox History", False, f"Exception: {str(e)}")
else:
    log_test("Get Sandbox History", False, "No wizard ID from previous test")

# Test 12: Get Sandbox Collected Data
print("\n=== TEST 12: Get Sandbox Collected Data ===")
if wizard_id:
    try:
        response = requests.get(f"{BASE_URL}/agents/wizard/{wizard_id}/sandbox/data")
        if response.status_code == 200:
            data = response.json()
            if 'collected_data' in data:
                log_test("Get Sandbox Collected Data", True, "Data retrieved")
            else:
                log_test("Get Sandbox Collected Data", False, "No collected_data field")
        else:
            log_test("Get Sandbox Collected Data", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Get Sandbox Collected Data", False, f"Exception: {str(e)}")
else:
    log_test("Get Sandbox Collected Data", False, "No wizard ID from previous test")

# Test 13: Publish Agent
print("\n=== TEST 13: Publish Agent ===")
if wizard_id:
    try:
        response = requests.post(f"{BASE_URL}/agents/wizard/{wizard_id}/publish")
        if response.status_code == 200:
            result = response.json()
            required_fields = ['agent_id', 'slug', 'public_url', 'embed_code', 'qr_code_url']
            has_all_fields = all(field in result for field in required_fields)
            if has_all_fields:
                log_test("Publish Agent", True, f"Agent published: {result.get('slug')}")
            else:
                log_test("Publish Agent", False, "Missing publication fields")
        else:
            log_test("Publish Agent", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Publish Agent", False, f"Exception: {str(e)}")
else:
    log_test("Publish Agent", False, "No wizard ID from previous test")

# Test 14: Cleanup Sandbox
print("\n=== TEST 14: Cleanup Sandbox ===")
if wizard_id:
    try:
        response = requests.delete(f"{BASE_URL}/agents/wizard/{wizard_id}/sandbox")
        if response.status_code == 204:
            log_test("Cleanup Sandbox", True, "Sandbox cleaned up")
        else:
            log_test("Cleanup Sandbox", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Cleanup Sandbox", False, f"Exception: {str(e)}")
else:
    log_test("Cleanup Sandbox", False, "No wizard ID from previous test")

# Test 15: Delete Wizard (cleanup)
print("\n=== TEST 15: Delete Wizard ===")
if wizard_id:
    try:
        response = requests.delete(f"{BASE_URL}/agents/wizard/{wizard_id}")
        if response.status_code == 204:
            log_test("Delete Wizard", True, "Wizard deleted")
        else:
            log_test("Delete Wizard", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Delete Wizard", False, f"Exception: {str(e)}")
else:
    log_test("Delete Wizard", False, "No wizard ID from previous test")

# Print Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
for result in test_results:
    print(result)
print("="*60)
print(f"Total Tests: {tests_passed + tests_failed}")
print(f"Passed: {tests_passed} ✅")
print(f"Failed: {tests_failed} ❌")
print(f"Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
print("="*60)

# Exit with appropriate code
exit(0 if tests_failed == 0 else 1)
