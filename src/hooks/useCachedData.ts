import { useState, useEffect, useCallback } from 'react';
import { cacheManager } from '../services/cache/cacheManager';

interface UseCachedDataOptions<T> {
  key: string;
  fetcher: () => Promise<T>;
  ttl?: number;
  enabled?: boolean;
  onError?: (error: Error) => void;
}

interface UseCachedDataReturn<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  invalidate: () => void;
}

/**
 * Hook for managing cached data with automatic invalidation
 * 
 * @template T - The type of data being cached
 * @param options - Configuration options
 * @returns Object with data, loading state, error, and control functions
 */
export function useCachedData<T>({
  key,
  fetcher,
  ttl,
  enabled = true,
  onError,
}: UseCachedDataOptions<T>): UseCachedDataReturn<T> {
  const [data, setData] = useState<T | null>(() => cacheManager.get<T>(key));
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * Fetch data from source
   */
  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await fetcher();
      
      // Update cache
      cacheManager.set(key, result, ttl);
      
      // Update local state
      setData(result);
      
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      
      if (onError) {
        onError(error);
      }
      
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [key, fetcher, ttl, onError]);

  /**
   * Refetch data (bypass cache)
   */
  const refetch = useCallback(async () => {
    // Invalidate cache first
    cacheManager.invalidate(key);
    
    // Fetch fresh data
    await fetchData();
  }, [key, fetchData]);

  /**
   * Invalidate cache for this key
   */
  const invalidate = useCallback(() => {
    cacheManager.invalidate(key);
    setData(null);
  }, [key]);

  /**
   * Initial fetch
   */
  useEffect(() => {
    if (!enabled) {
      return;
    }

    // Check cache first
    const cachedData = cacheManager.get<T>(key);
    
    if (cachedData) {
      setData(cachedData);
    } else {
      // Fetch if not in cache
      fetchData();
    }
  }, [key, enabled, fetchData]);

  /**
   * Subscribe to cache changes
   */
  useEffect(() => {
    const unsubscribe = cacheManager.subscribe(key, (newData) => {
      setData(newData);
    });

    return unsubscribe;
  }, [key]);

  return {
    data,
    isLoading,
    error,
    refetch,
    invalidate,
  };
}
