"""
Performance Tests - Sprint 08
Tests response times, pagination, and filtering performance
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

def test_list_performance():
    """Test list loading performance"""
    print_header("TEST 1: List Loading Performance")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # Test Projects
        print("  Testing Projects list...")
        start = time.time()
        result = supabase.table('projects').select('*').execute()
        elapsed = time.time() - start
        passed = elapsed < 2.0
        print_test(f"Projects list ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 2s)")
        test_passed = test_passed and passed
        
        # Test Leads
        print("  Testing Leads list...")
        start = time.time()
        result = supabase.table('leads').select('*').execute()
        elapsed = time.time() - start
        passed = elapsed < 2.0
        print_test(f"Leads list ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 2s)")
        test_passed = test_passed and passed
        
        # Test Clients
        print("  Testing Clients list...")
        start = time.time()
        result = supabase.table('clients').select('*').execute()
        elapsed = time.time() - start
        passed = elapsed < 2.0
        print_test(f"Clients list ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 2s)")
        test_passed = test_passed and passed
        
        # Test Interviews
        print("  Testing Interviews list...")
        start = time.time()
        result = supabase.table('interviews').select('*').execute()
        elapsed = time.time() - start
        passed = elapsed < 2.0
        print_test(f"Interviews list ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 2s)")
        test_passed = test_passed and passed
        
    except Exception as e:
        print_test("List performance", False, str(e))
        test_passed = False
    
    return test_passed

def test_pagination_performance():
    """Test pagination performance"""
    print_header("TEST 2: Pagination Performance")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # Test paginated query
        print("  Testing paginated query (10 items)...")
        start = time.time()
        result = supabase.table('leads').select('*').range(0, 9).execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"Paginated query ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test second page
        print("  Testing second page (10 items)...")
        start = time.time()
        result = supabase.table('leads').select('*').range(10, 19).execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"Second page ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
    except Exception as e:
        print_test("Pagination performance", False, str(e))
        test_passed = False
    
    return test_passed

def test_filter_performance():
    """Test filter performance"""
    print_header("TEST 3: Filter Performance")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # Test status filter
        print("  Testing status filter...")
        start = time.time()
        result = supabase.table('projects').select('*').eq('status', 'Em Andamento').execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"Status filter ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test source filter
        print("  Testing source filter...")
        start = time.time()
        result = supabase.table('leads').select('*').eq('source', 'pesquisa').execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"Source filter ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test segment filter
        print("  Testing segment filter...")
        start = time.time()
        result = supabase.table('clients').select('*').eq('segment', 'test').execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"Segment filter ({len(result.data)} items)", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
    except Exception as e:
        print_test("Filter performance", False, str(e))
        test_passed = False
    
    return test_passed

def test_crud_performance():
    """Test CRUD operation performance"""
    print_header("TEST 4: CRUD Operation Performance")
    
    supabase = get_client()
    test_passed = True
    lead_id = None
    
    try:
        # Test CREATE
        print("  Testing CREATE operation...")
        start = time.time()
        lead_data = {
            'name': f'Performance Test {datetime.now().strftime("%Y%m%d%H%M%S")}',
            'phone': '+5511555555555',
            'status': 'novo',
            'source': 'pesquisa'
        }
        result = supabase.table('leads').insert(lead_data).execute()
        lead_id = result.data[0]['id']
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test("CREATE operation", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test READ
        print("  Testing READ operation...")
        start = time.time()
        result = supabase.table('leads').select('*').eq('id', lead_id).execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test("READ operation", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test UPDATE
        print("  Testing UPDATE operation...")
        start = time.time()
        update_data = {'email': 'performance@test.com'}
        result = supabase.table('leads').update(update_data).eq('id', lead_id).execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test("UPDATE operation", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test DELETE
        print("  Testing DELETE operation...")
        start = time.time()
        supabase.table('leads').delete().eq('id', lead_id).execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test("DELETE operation", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        lead_id = None
        
    except Exception as e:
        print_test("CRUD performance", False, str(e))
        test_passed = False
        # Cleanup
        if lead_id:
            try:
                supabase.table('leads').delete().eq('id', lead_id).execute()
            except:
                pass
    
    return test_passed

def test_aggregation_performance():
    """Test aggregation performance"""
    print_header("TEST 5: Aggregation Performance")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # Test COUNT
        print("  Testing COUNT aggregation...")
        start = time.time()
        result = supabase.table('leads').select('id', count='exact').execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"COUNT aggregation (total: {result.count})", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
        # Test COUNT with filter
        print("  Testing COUNT with filter...")
        start = time.time()
        result = supabase.table('leads').select('id', count='exact').eq('status', 'novo').execute()
        elapsed = time.time() - start
        passed = elapsed < 1.0
        print_test(f"COUNT with filter (total: {result.count})", passed, f"{elapsed:.3f}s (target: < 1s)")
        test_passed = test_passed and passed
        
    except Exception as e:
        print_test("Aggregation performance", False, str(e))
        test_passed = False
    
    return test_passed

def test_concurrent_operations():
    """Test concurrent operations"""
    print_header("TEST 6: Concurrent Operations")
    
    supabase = get_client()
    test_passed = True
    
    try:
        # Simulate concurrent reads
        print("  Testing 5 concurrent reads...")
        start = time.time()
        for i in range(5):
            supabase.table('leads').select('*').limit(10).execute()
        elapsed = time.time() - start
        passed = elapsed < 3.0
        print_test("5 concurrent reads", passed, f"{elapsed:.3f}s (target: < 3s)")
        test_passed = test_passed and passed
        
    except Exception as e:
        print_test("Concurrent operations", False, str(e))
        test_passed = False
    
    return test_passed

def main():
    """Run all performance tests"""
    print("\n" + "="*60)
    print("  PERFORMANCE TESTS - SPRINT 08")
    print("  Testing response times and scalability")
    print("="*60)
    
    start_time = time.time()
    results = []
    
    # Run all tests
    results.append(("List Loading Performance", test_list_performance()))
    results.append(("Pagination Performance", test_pagination_performance()))
    results.append(("Filter Performance", test_filter_performance()))
    results.append(("CRUD Performance", test_crud_performance()))
    results.append(("Aggregation Performance", test_aggregation_performance()))
    results.append(("Concurrent Operations", test_concurrent_operations()))
    
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
        print(f"\n  ✓ ALL PERFORMANCE TESTS PASSED!")
        return 0
    else:
        print(f"\n  ✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    exit(main())
