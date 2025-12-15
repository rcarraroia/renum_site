/**
 * Test Component for State Synchronization
 * Tests cache invalidation, optimistic updates, and rollback
 */

import React, { useState } from 'react';
import { useOptimisticUpdate } from './hooks/useOptimisticUpdate';
import { useCachedData } from './hooks/useCachedData';
import { cacheManager } from './services/cache/cacheManager';
import { invalidationStrategies } from './services/cache/invalidationStrategies';

interface TestData {
  id: string;
  name: string;
  value: number;
}

export function TestStateSync() {
  const [testResults, setTestResults] = useState<string[]>([]);

  const addResult = (result: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${result}`]);
  };

  // Test 1: Cache Manager Basic Operations
  const testCacheBasics = () => {
    addResult('🧪 Testing Cache Basics...');
    
    // Set data
    cacheManager.set('test:1', { id: '1', name: 'Test', value: 100 });
    addResult('✅ Set cache data');
    
    // Get data
    const data = cacheManager.get<TestData>('test:1');
    if (data && data.name === 'Test') {
      addResult('✅ Retrieved cache data correctly');
    } else {
      addResult('❌ Failed to retrieve cache data');
    }
    
    // Invalidate
    cacheManager.invalidate('test:1');
    const invalidated = cacheManager.get('test:1');
    if (invalidated === null) {
      addResult('✅ Cache invalidation works');
    } else {
      addResult('❌ Cache invalidation failed');
    }
  };

  // Test 2: Cache Pattern Invalidation
  const testPatternInvalidation = () => {
    addResult('🧪 Testing Pattern Invalidation...');
    
    // Set multiple entries
    cacheManager.set('projects:1', { id: '1', name: 'Project 1' });
    cacheManager.set('projects:2', { id: '2', name: 'Project 2' });
    cacheManager.set('leads:1', { id: '1', name: 'Lead 1' });
    addResult('✅ Set multiple cache entries');
    
    // Invalidate pattern
    cacheManager.invalidatePattern('^projects');
    
    const project1 = cacheManager.get('projects:1');
    const project2 = cacheManager.get('projects:2');
    const lead1 = cacheManager.get('leads:1');
    
    if (project1 === null && project2 === null && lead1 !== null) {
      addResult('✅ Pattern invalidation works correctly');
    } else {
      addResult('❌ Pattern invalidation failed');
    }
    
    // Cleanup
    cacheManager.clear();
  };

  // Test 3: Cache Subscription
  const testCacheSubscription = () => {
    addResult('🧪 Testing Cache Subscription...');
    
    let notified = false;
    
    const unsubscribe = cacheManager.subscribe('test:sub', (data) => {
      if (data && data.name === 'Updated') {
        notified = true;
        addResult('✅ Subscription notification received');
      }
    });
    
    cacheManager.set('test:sub', { id: '1', name: 'Updated' });
    
    setTimeout(() => {
      if (notified) {
        addResult('✅ Subscription works correctly');
      } else {
        addResult('❌ Subscription failed');
      }
      unsubscribe();
    }, 100);
  };

  // Test 4: Optimistic Update Success
  const testOptimisticSuccess = async () => {
    addResult('🧪 Testing Optimistic Update (Success)...');
    
    const initialData: TestData = { id: '1', name: 'Initial', value: 0 };
    const { optimisticUpdate } = useOptimisticUpdate(initialData);
    
    const newData: TestData = { id: '1', name: 'Updated', value: 100 };
    
    const result = await optimisticUpdate(
      newData,
      async () => {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        return { id: '1', name: 'Server Response', value: 100 };
      }
    );
    
    if (result.success && result.data?.name === 'Server Response') {
      addResult('✅ Optimistic update succeeded');
    } else {
      addResult('❌ Optimistic update failed');
    }
  };

  // Test 5: Optimistic Update Rollback
  const testOptimisticRollback = async () => {
    addResult('🧪 Testing Optimistic Update (Rollback)...');
    
    const initialData: TestData = { id: '1', name: 'Initial', value: 0 };
    const { optimisticUpdate } = useOptimisticUpdate(initialData);
    
    const newData: TestData = { id: '1', name: 'Updated', value: 100 };
    
    const result = await optimisticUpdate(
      newData,
      async () => {
        // Simulate API error
        await new Promise(resolve => setTimeout(resolve, 500));
        throw new Error('API Error');
      }
    );
    
    if (!result.success && result.error) {
      addResult('✅ Optimistic update rolled back on error');
    } else {
      addResult('❌ Rollback failed');
    }
  };

  // Test 6: Invalidation Strategies
  const testInvalidationStrategies = () => {
    addResult('🧪 Testing Invalidation Strategies...');
    
    // Setup cache
    cacheManager.set('projects:all', [{ id: '1' }]);
    cacheManager.set('projects:1', { id: '1', name: 'Project 1' });
    cacheManager.set('reports:overview', { total: 10 });
    
    // Test project update invalidation
    invalidationStrategies.projects.onUpdate('1');
    
    const projectsAll = cacheManager.get('projects:all');
    const project1 = cacheManager.get('projects:1');
    const reports = cacheManager.get('reports:overview');
    
    if (projectsAll === null && project1 === null && reports === null) {
      addResult('✅ Invalidation strategy works correctly');
    } else {
      addResult('❌ Invalidation strategy failed');
    }
  };

  // Test 7: Cache Statistics
  const testCacheStats = () => {
    addResult('🧪 Testing Cache Statistics...');
    
    cacheManager.clear();
    
    cacheManager.set('test:1', { id: '1' });
    cacheManager.set('test:2', { id: '2' });
    cacheManager.set('test:3', { id: '3' });
    
    const stats = cacheManager.getStats();
    
    if (stats.total === 3 && stats.active === 3) {
      addResult(`✅ Cache stats correct: ${stats.total} total, ${stats.active} active`);
    } else {
      addResult('❌ Cache stats incorrect');
    }
  };

  // Run all tests
  const runAllTests = async () => {
    setTestResults([]);
    addResult('🚀 Starting State Synchronization Tests...');
    addResult('');
    
    testCacheBasics();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    testPatternInvalidation();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    testCacheSubscription();
    await new Promise(resolve => setTimeout(resolve, 300));
    
    await testOptimisticSuccess();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    await testOptimisticRollback();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    testInvalidationStrategies();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    testCacheStats();
    await new Promise(resolve => setTimeout(resolve, 200));
    
    addResult('');
    addResult('✅ All tests completed!');
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold mb-4">State Synchronization Tests</h1>
        
        <div className="mb-6">
          <button
            onClick={runAllTests}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Run All Tests
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold mb-2">Test Results:</h2>
            <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm max-h-96 overflow-y-auto">
              {testResults.length === 0 ? (
                <p className="text-gray-500">Click "Run All Tests" to start...</p>
              ) : (
                testResults.map((result, index) => (
                  <div key={index} className="mb-1">
                    {result}
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="border-t pt-4">
            <h2 className="text-lg font-semibold mb-2">Cache Statistics:</h2>
            <button
              onClick={() => {
                const stats = cacheManager.getStats();
                addResult(`📊 Stats: ${JSON.stringify(stats, null, 2)}`);
              }}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
            >
              Show Cache Stats
            </button>
          </div>

          <div className="border-t pt-4">
            <h2 className="text-lg font-semibold mb-2">Manual Actions:</h2>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  cacheManager.clear();
                  addResult('🗑️ Cache cleared');
                }}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
              >
                Clear Cache
              </button>
              
              <button
                onClick={() => {
                  cacheManager.cleanup();
                  addResult('🧹 Expired entries cleaned up');
                }}
                className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700 transition-colors"
              >
                Cleanup Expired
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TestStateSync;
