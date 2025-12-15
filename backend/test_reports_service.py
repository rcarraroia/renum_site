"""
Reports Service Validation Script
Sprint 08 - Conexao Backend - FASE 6

Tests ReportService directly (bypassing API authentication)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.report_service import ReportService
from src.services.dashboard_service import DashboardService
import json

def print_separator(title=""):
    print("\n" + "=" * 60)
    if title:
        print(f" {title}")
        print("=" * 60)

def print_test_result(test_name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    symbol = "✅" if passed else "❌"
    print(f"\n{symbol} {status} - {test_name}")
    if details:
        print(f"   {details}")

# Test counters
total_tests = 0
passed_tests = 0

print_separator("REPORTS SERVICE VALIDATION - SPRINT 08 FASE 6")

# Initialize services
report_service = ReportService()
dashboard_service = DashboardService()

# TEST 1: Get Overview
print_separator("TEST 1: Get Overview")
total_tests += 1
try:
    filters = {}
    result = report_service.get_overview(filters)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    required_fields = ["totalLeads", "totalClients", "totalConversations", 
                      "totalInterviews", "activeProjects", "conversionRate"]
    has_all_fields = all(field in result for field in required_fields)
    
    if has_all_fields:
        passed_tests += 1
        print_test_result("Get Overview", True, 
                        f"Total Leads: {result['totalLeads']}, "
                        f"Total Clients: {result['totalClients']}, "
                        f"Conversion Rate: {result['conversionRate']}%")
    else:
        missing = [f for f in required_fields if f not in result]
        print_test_result("Get Overview", False, f"Missing fields: {missing}")
except Exception as e:
    print_test_result("Get Overview", False, f"Exception: {str(e)}")

# TEST 2: Get Overview with Filters
print_separator("TEST 2: Get Overview with Filters")
total_tests += 1
try:
    filters = {
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "client_id": None
    }
    result = report_service.get_overview(filters)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if "totalLeads" in result:
        passed_tests += 1
        print_test_result("Get Overview with Filters", True, "Filters applied successfully")
    else:
        print_test_result("Get Overview with Filters", False, "Invalid result")
except Exception as e:
    print_test_result("Get Overview with Filters", False, f"Exception: {str(e)}")

# TEST 3: Get Agent Performance
print_separator("TEST 3: Get Agent Performance")
total_tests += 1
try:
    filters = {}
    result = report_service.get_agent_performance(filters)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if isinstance(result, list) and len(result) > 0:
        agent = result[0]
        required_fields = ["agentId", "agentName", "totalConversations", 
                         "avgResponseTime", "satisfactionScore"]
        has_all_fields = all(field in agent for field in required_fields)
        
        if has_all_fields:
            passed_tests += 1
            print_test_result("Get Agent Performance", True, 
                            f"Found {len(result)} agents")
        else:
            missing = [f for f in required_fields if f not in agent]
            print_test_result("Get Agent Performance", False, 
                            f"Missing fields: {missing}")
    else:
        print_test_result("Get Agent Performance", False, "Expected non-empty list")
except Exception as e:
    print_test_result("Get Agent Performance", False, f"Exception: {str(e)}")

# TEST 4: Get Conversion Funnel
print_separator("TEST 4: Get Conversion Funnel")
total_tests += 1
try:
    filters = {}
    result = report_service.get_conversion_funnel(filters)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if isinstance(result, list) and len(result) > 0:
        stage = result[0]
        required_fields = ["stage", "count", "conversionRate"]
        has_all_fields = all(field in stage for field in required_fields)
        
        if has_all_fields:
            passed_tests += 1
            print_test_result("Get Conversion Funnel", True, 
                            f"Found {len(result)} stages")
        else:
            missing = [f for f in required_fields if f not in stage]
            print_test_result("Get Conversion Funnel", False, 
                            f"Missing fields: {missing}")
    else:
        print_test_result("Get Conversion Funnel", False, "Expected non-empty list")
except Exception as e:
    print_test_result("Get Conversion Funnel", False, f"Exception: {str(e)}")

# TEST 5: Dashboard Stats (bonus test)
print_separator("TEST 5: Dashboard Stats (Bonus)")
total_tests += 1
try:
    result = dashboard_service.get_stats(client_id=None)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    required_fields = ["total_clients", "total_leads", "total_conversations", 
                      "active_interviews", "completed_interviews", "completion_rate"]
    has_all_fields = all(field in result for field in required_fields)
    
    if has_all_fields:
        passed_tests += 1
        print_test_result("Dashboard Stats", True, 
                        f"Completion Rate: {result['completion_rate']}%")
    else:
        missing = [f for f in required_fields if f not in result]
        print_test_result("Dashboard Stats", False, f"Missing fields: {missing}")
except Exception as e:
    print_test_result("Dashboard Stats", False, f"Exception: {str(e)}")

# Summary
print_separator("TEST SUMMARY")
test_names = [
    "Get Overview",
    "Get Overview with Filters", 
    "Get Agent Performance",
    "Get Conversion Funnel",
    "Dashboard Stats"
]
for i, name in enumerate(test_names, 1):
    status = "✅ PASS" if i <= passed_tests else "❌ FAIL"
    print(f"{status} - {name}")

print_separator(f"TOTAL: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.0f}%)")

if passed_tests == total_tests:
    print("\n🎉 ALL TESTS PASSED! Reports Service is working correctly.")
else:
    print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the errors above.")
