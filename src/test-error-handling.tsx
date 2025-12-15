/**
 * Test Error Handling
 * Component to test error boundary and error handling
 */

import React, { useState } from 'react';
import { apiClient } from './services/api';

export function TestErrorHandling() {
  const [result, setResult] = useState<string>('');

  const testComponentError = () => {
    throw new Error('Test component error!');
  };

  const testApiError = async () => {
    try {
      await apiClient.get('/api/nonexistent-endpoint');
    } catch (error) {
      setResult(`API Error caught: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const testAuthError = async () => {
    try {
      // Remove token to trigger auth error
      localStorage.removeItem('token');
      await apiClient.get('/api/projects');
    } catch (error) {
      setResult(`Auth Error caught: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  return (
    <div className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">Test Error Handling</h1>
      
      <div className="space-x-4">
        <button
          onClick={testComponentError}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Test Component Error (will show error boundary)
        </button>

        <button
          onClick={testApiError}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Test API Error
        </button>

        <button
          onClick={testAuthError}
          className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
        >
          Test Auth Error
        </button>
      </div>

      {result && (
        <div className="p-4 bg-gray-100 rounded">
          <p className="font-mono text-sm">{result}</p>
        </div>
      )}
    </div>
  );
}
