import { useState, useCallback } from 'react';

/**
 * Hook for managing optimistic updates with rollback capability
 * 
 * @template T - The type of data being managed
 * @param initialData - Initial data state
 * @returns Object with data, optimistic update function, and rollback function
 */
export function useOptimisticUpdate<T>(initialData: T) {
  const [data, setData] = useState<T>(initialData);
  const [previousData, setPreviousData] = useState<T>(initialData);
  const [isOptimistic, setIsOptimistic] = useState(false);

  /**
   * Perform an optimistic update
   * Updates the UI immediately, then calls the async operation
   * Rolls back if the operation fails
   */
  const optimisticUpdate = useCallback(
    async (
      newData: T,
      asyncOperation: () => Promise<T>
    ): Promise<{ success: boolean; data?: T; error?: Error }> => {
      // Save current state for potential rollback
      setPreviousData(data);
      
      // Apply optimistic update immediately
      setData(newData);
      setIsOptimistic(true);

      try {
        // Execute the async operation
        const result = await asyncOperation();
        
        // Update with real data from server
        setData(result);
        setIsOptimistic(false);
        
        return { success: true, data: result };
      } catch (error) {
        // Rollback to previous state on error
        setData(previousData);
        setIsOptimistic(false);
        
        return { 
          success: false, 
          error: error instanceof Error ? error : new Error('Unknown error') 
        };
      }
    },
    [data, previousData]
  );

  /**
   * Manually rollback to previous state
   */
  const rollback = useCallback(() => {
    setData(previousData);
    setIsOptimistic(false);
  }, [previousData]);

  /**
   * Update data without optimistic behavior
   */
  const updateData = useCallback((newData: T) => {
    setData(newData);
    setIsOptimistic(false);
  }, []);

  return {
    data,
    isOptimistic,
    optimisticUpdate,
    rollback,
    updateData,
  };
}
