"""
Stress Test for BUG #10 - Server Freezing
Tests server stability under load to validate fix
"""

import httpx
import asyncio
import time
import psutil
import os
from typing import List, Dict

BASE_URL = "http://localhost:8000"
TIMEOUT = 5.0


class StressTestResults:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.timeouts = 0
        self.errors: List[str] = []
        self.response_times: List[float] = []
        self.memory_samples: List[float] = []
        self.start_time = None
        self.end_time = None
    
    def add_success(self, response_time: float):
        self.total_requests += 1
        self.successful_requests += 1
        self.response_times.append(response_time)
    
    def add_failure(self, error: str):
        self.total_requests += 1
        self.failed_requests += 1
        self.errors.append(error)
    
    def add_timeout(self):
        self.total_requests += 1
        self.timeouts += 1
    
    def add_memory_sample(self, memory_mb: float):
        self.memory_samples.append(memory_mb)
    
    def get_summary(self) -> Dict:
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        min_response_time = min(self.response_times) if self.response_times else 0
        max_response_time = max(self.response_times) if self.response_times else 0
        
        avg_memory = sum(self.memory_samples) / len(self.memory_samples) if self.memory_samples else 0
        min_memory = min(self.memory_samples) if self.memory_samples else 0
        max_memory = max(self.memory_samples) if self.memory_samples else 0
        memory_growth = max_memory - min_memory if self.memory_samples else 0
        
        return {
            "duration_seconds": round(duration, 2),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "timeouts": self.timeouts,
            "success_rate": round(self.successful_requests / self.total_requests * 100, 2) if self.total_requests > 0 else 0,
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "min_response_time_ms": round(min_response_time * 1000, 2),
            "max_response_time_ms": round(max_response_time * 1000, 2),
            "avg_memory_mb": round(avg_memory, 2),
            "min_memory_mb": round(min_memory, 2),
            "max_memory_mb": round(max_memory, 2),
            "memory_growth_mb": round(memory_growth, 2),
            "requests_per_second": round(self.total_requests / duration, 2) if duration > 0 else 0
        }


async def make_request(client: httpx.AsyncClient, endpoint: str) -> tuple[bool, float, str]:
    """
    Make single HTTP request.
    
    Returns:
        (success, response_time, error_message)
    """
    try:
        start = time.time()
        response = await client.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
        response_time = time.time() - start
        
        if response.status_code == 200:
            return (True, response_time, "")
        else:
            return (False, response_time, f"HTTP {response.status_code}")
    
    except httpx.TimeoutException:
        return (False, TIMEOUT, "TIMEOUT")
    
    except Exception as e:
        return (False, 0, str(e))


async def stress_test_sequential(num_requests: int = 100) -> StressTestResults:
    """
    Sequential stress test - one request at a time.
    
    Args:
        num_requests: Number of requests to make
    
    Returns:
        Test results
    """
    print(f"\n🔄 Sequential Stress Test ({num_requests} requests)")
    print("=" * 60)
    
    results = StressTestResults()
    results.start_time = time.time()
    
    # Get backend process
    backend_pid = None
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'uvicorn' in ' '.join(cmdline) and 'src.main:app' in ' '.join(cmdline):
                backend_pid = proc.info['pid']
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if backend_pid:
        backend_process = psutil.Process(backend_pid)
        print(f"✅ Backend process found (PID: {backend_pid})")
    else:
        print("⚠️  Backend process not found - memory monitoring disabled")
        backend_process = None
    
    async with httpx.AsyncClient() as client:
        for i in range(num_requests):
            # Make request
            success, response_time, error = await make_request(client, "/health")
            
            if success:
                results.add_success(response_time)
            elif error == "TIMEOUT":
                results.add_timeout()
            else:
                results.add_failure(error)
            
            # Sample memory every 10 requests
            if backend_process and i % 10 == 0:
                try:
                    memory_info = backend_process.memory_info()
                    memory_mb = memory_info.rss / 1024 / 1024
                    results.add_memory_sample(memory_mb)
                except:
                    pass
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Progress: {i + 1}/{num_requests} requests", end="\r")
    
    results.end_time = time.time()
    
    print(f"\nProgress: {num_requests}/{num_requests} requests ✅")
    
    return results


async def stress_test_concurrent(num_requests: int = 100, concurrency: int = 10) -> StressTestResults:
    """
    Concurrent stress test - multiple requests in parallel.
    
    Args:
        num_requests: Total number of requests
        concurrency: Number of concurrent requests
    
    Returns:
        Test results
    """
    print(f"\n🚀 Concurrent Stress Test ({num_requests} requests, {concurrency} concurrent)")
    print("=" * 60)
    
    results = StressTestResults()
    results.start_time = time.time()
    
    # Get backend process
    backend_pid = None
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'uvicorn' in ' '.join(cmdline) and 'src.main:app' in ' '.join(cmdline):
                backend_pid = proc.info['pid']
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if backend_pid:
        backend_process = psutil.Process(backend_pid)
        print(f"✅ Backend process found (PID: {backend_pid})")
    else:
        print("⚠️  Backend process not found - memory monitoring disabled")
        backend_process = None
    
    async with httpx.AsyncClient() as client:
        # Create batches
        batches = [num_requests // concurrency] * concurrency
        batches[-1] += num_requests % concurrency  # Add remainder to last batch
        
        completed = 0
        
        for batch_size in batches:
            # Create concurrent tasks
            tasks = [make_request(client, "/health") for _ in range(batch_size)]
            batch_results = await asyncio.gather(*tasks)
            
            # Process results
            for success, response_time, error in batch_results:
                if success:
                    results.add_success(response_time)
                elif error == "TIMEOUT":
                    results.add_timeout()
                else:
                    results.add_failure(error)
            
            completed += batch_size
            
            # Sample memory
            if backend_process:
                try:
                    memory_info = backend_process.memory_info()
                    memory_mb = memory_info.rss / 1024 / 1024
                    results.add_memory_sample(memory_mb)
                except:
                    pass
            
            # Progress indicator
            print(f"Progress: {completed}/{num_requests} requests", end="\r")
    
    results.end_time = time.time()
    
    print(f"\nProgress: {num_requests}/{num_requests} requests ✅")
    
    return results


def print_results(results: StressTestResults, test_name: str):
    """Print test results"""
    summary = results.get_summary()
    
    print(f"\n📊 {test_name} Results")
    print("=" * 60)
    print(f"Duration: {summary['duration_seconds']}s")
    print(f"Total Requests: {summary['total_requests']}")
    print(f"Successful: {summary['successful_requests']} ({summary['success_rate']}%)")
    print(f"Failed: {summary['failed_requests']}")
    print(f"Timeouts: {summary['timeouts']}")
    print(f"Requests/sec: {summary['requests_per_second']}")
    print()
    print(f"Response Time:")
    print(f"  - Average: {summary['avg_response_time_ms']}ms")
    print(f"  - Min: {summary['min_response_time_ms']}ms")
    print(f"  - Max: {summary['max_response_time_ms']}ms")
    print()
    print(f"Memory Usage:")
    print(f"  - Average: {summary['avg_memory_mb']} MB")
    print(f"  - Min: {summary['min_memory_mb']} MB")
    print(f"  - Max: {summary['max_memory_mb']} MB")
    print(f"  - Growth: {summary['memory_growth_mb']} MB")
    print()
    
    # Verdict
    if summary['timeouts'] == 0 and summary['success_rate'] >= 95:
        print("✅ PASS - Server is stable")
    elif summary['timeouts'] > 0:
        print(f"❌ FAIL - {summary['timeouts']} timeouts detected (BUG #10 present)")
    else:
        print(f"⚠️  WARNING - Success rate {summary['success_rate']}% (expected >= 95%)")


async def main():
    """Run all stress tests"""
    print("\n" + "=" * 60)
    print("🧪 BUG #10 STRESS TEST - Server Freezing Validation")
    print("=" * 60)
    
    # Test 1: Sequential (100 requests)
    results1 = await stress_test_sequential(100)
    print_results(results1, "Sequential Test (100 requests)")
    
    # Test 2: Concurrent (100 requests, 10 concurrent)
    results2 = await stress_test_concurrent(100, 10)
    print_results(results2, "Concurrent Test (100 requests, 10 concurrent)")
    
    # Test 3: Heavy load (1000 requests, 20 concurrent)
    results3 = await stress_test_concurrent(1000, 20)
    print_results(results3, "Heavy Load Test (1000 requests, 20 concurrent)")
    
    # Final verdict
    print("\n" + "=" * 60)
    print("📋 FINAL VERDICT")
    print("=" * 60)
    
    all_results = [results1, results2, results3]
    total_timeouts = sum(r.timeouts for r in all_results)
    avg_success_rate = sum(r.get_summary()['success_rate'] for r in all_results) / len(all_results)
    total_memory_growth = sum(r.get_summary()['memory_growth_mb'] for r in all_results)
    
    print(f"Total Requests: {sum(r.total_requests for r in all_results)}")
    print(f"Total Timeouts: {total_timeouts}")
    print(f"Average Success Rate: {round(avg_success_rate, 2)}%")
    print(f"Total Memory Growth: {round(total_memory_growth, 2)} MB")
    print()
    
    if total_timeouts == 0 and avg_success_rate >= 95 and total_memory_growth < 100:
        print("✅ BUG #10 FIXED - Server is stable under load")
        return 0
    else:
        print("❌ BUG #10 STILL PRESENT - Server has issues")
        if total_timeouts > 0:
            print(f"   - {total_timeouts} timeouts detected")
        if avg_success_rate < 95:
            print(f"   - Success rate {round(avg_success_rate, 2)}% (expected >= 95%)")
        if total_memory_growth >= 100:
            print(f"   - Memory growth {round(total_memory_growth, 2)} MB (expected < 100 MB)")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
