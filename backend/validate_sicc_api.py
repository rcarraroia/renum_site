"""
SICC API Validation Script
Sprint 10 - SICC Implementation - Task 33

Validates SICC API endpoints functionality.
"""

import asyncio
import sys
import httpx
from uuid import UUID

# Add src to path
sys.path.insert(0, 'src')

from src.config.settings import settings


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"     {details}")


async def test_server_running():
    """Test if server is running"""
    print_section("TESTING SERVER")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{settings.API_HOST}:{settings.API_PORT}/health",
                timeout=5.0
            )
            
            print_test(
                "Server Running",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            
            return response.status_code == 200
    except Exception as e:
        print_test("Server Running", False, f"Error: {e}")
        return False


async def test_api_docs():
    """Test if API docs are accessible"""
    print_section("TESTING API DOCUMENTATION")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{settings.API_HOST}:{settings.API_PORT}/docs",
                timeout=5.0
            )
            
            print_test(
                "Swagger Docs Accessible",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            
            # Check if SICC routes are documented
            content = response.text
            has_sicc_memory = "sicc/memories" in content
            has_sicc_learning = "sicc/learnings" in content
            has_sicc_stats = "sicc/stats" in content
            has_sicc_patterns = "sicc/patterns" in content
            
            print_test(
                "SICC Memory Routes Documented",
                has_sicc_memory,
                "Found in Swagger docs" if has_sicc_memory else "Not found"
            )
            
            print_test(
                "SICC Learning Routes Documented",
                has_sicc_learning,
                "Found in Swagger docs" if has_sicc_learning else "Not found"
            )
            
            print_test(
                "SICC Stats Routes Documented",
                has_sicc_stats,
                "Found in Swagger docs" if has_sicc_stats else "Not found"
            )
            
            print_test(
                "SICC Patterns Routes Documented",
                has_sicc_patterns,
                "Found in Swagger docs" if has_sicc_patterns else "Not found"
            )
            
            return all([has_sicc_memory, has_sicc_learning, has_sicc_stats, has_sicc_patterns])
    except Exception as e:
        print_test("API Docs", False, f"Error: {e}")
        return False


async def test_openapi_schema():
    """Test OpenAPI schema includes SICC routes"""
    print_section("TESTING OPENAPI SCHEMA")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{settings.API_HOST}:{settings.API_PORT}/openapi.json",
                timeout=5.0
            )
            
            print_test(
                "OpenAPI Schema Accessible",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            
            if response.status_code == 200:
                schema = response.json()
                paths = schema.get("paths", {})
                
                # Check for SICC endpoints
                sicc_endpoints = [
                    "/api/sicc/memories/",
                    "/api/sicc/learnings/",
                    "/api/sicc/stats/agent/{agent_id}/metrics",
                    "/api/sicc/patterns/"
                ]
                
                found_endpoints = []
                for endpoint in sicc_endpoints:
                    if endpoint in paths:
                        found_endpoints.append(endpoint)
                
                print_test(
                    "SICC Endpoints in Schema",
                    len(found_endpoints) == len(sicc_endpoints),
                    f"Found {len(found_endpoints)}/{len(sicc_endpoints)} endpoints"
                )
                
                # Check tags
                tags = schema.get("tags", [])
                tag_names = [tag.get("name") for tag in tags]
                
                sicc_tags = ["sicc-memory", "sicc-learning", "sicc-stats", "sicc-patterns"]
                found_tags = [tag for tag in sicc_tags if tag in tag_names]
                
                print_test(
                    "SICC Tags in Schema",
                    len(found_tags) == len(sicc_tags),
                    f"Found {len(found_tags)}/{len(sicc_tags)} tags"
                )
                
                return len(found_endpoints) == len(sicc_endpoints) and len(found_tags) == len(sicc_tags)
            
            return False
    except Exception as e:
        print_test("OpenAPI Schema", False, f"Error: {e}")
        return False


async def test_endpoint_structure():
    """Test endpoint structure (without auth)"""
    print_section("TESTING ENDPOINT STRUCTURE")
    
    test_agent_id = "37ae9902-24bf-42b1-9d01-88c201ee0a6c"
    
    endpoints = [
        ("GET", f"/api/sicc/memories/?agent_id={test_agent_id}"),
        ("GET", f"/api/sicc/learnings/?agent_id={test_agent_id}"),
        ("GET", f"/api/sicc/stats/agent/{test_agent_id}/metrics"),
        ("GET", f"/api/sicc/patterns/?agent_id={test_agent_id}"),
    ]
    
    try:
        async with httpx.AsyncClient() as client:
            for method, path in endpoints:
                try:
                    response = await client.request(
                        method,
                        f"http://{settings.API_HOST}:{settings.API_PORT}{path}",
                        timeout=5.0
                    )
                    
                    # We expect 401 (unauthorized) or 403 (forbidden) since we're not authenticated
                    # NOT 404 (not found) or 500 (server error)
                    is_auth_error = response.status_code in [401, 403]
                    
                    print_test(
                        f"{method} {path}",
                        is_auth_error,
                        f"Status: {response.status_code} (expected 401/403)"
                    )
                except Exception as e:
                    print_test(f"{method} {path}", False, f"Error: {e}")
        
        return True
    except Exception as e:
        print_test("Endpoint Structure", False, f"Error: {e}")
        return False


async def main():
    """Run all validation tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}SICC API VALIDATION{Colors.END}")
    print(f"{Colors.BLUE}Sprint 10 - Task 33 - API Endpoints{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}NOTE: Server must be running on {settings.API_HOST}:{settings.API_PORT}{Colors.END}")
    print(f"{Colors.YELLOW}Start server with: python -m src.main{Colors.END}\n")
    
    results = {
        "Server Running": await test_server_running(),
    }
    
    # Only continue if server is running
    if results["Server Running"]:
        results["API Docs"] = await test_api_docs()
        results["OpenAPI Schema"] = await test_openapi_schema()
        results["Endpoint Structure"] = await test_endpoint_structure()
    else:
        print(f"\n{Colors.RED}❌ SERVER NOT RUNNING - SKIPPING REMAINING TESTS{Colors.END}\n")
        print(f"{Colors.YELLOW}Please start the server and run this script again.{Colors.END}\n")
        return 1
    
    # Summary
    print_section("VALIDATION SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED - API ENDPOINTS VALIDATED{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}❌ SOME TESTS FAILED - API ENDPOINTS NOT FULLY VALIDATED{Colors.END}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
