/**
 * Project Service with Cache and Optimistic Updates
 * Example implementation showing how to use cache manager and optimistic updates
 */

import { apiClient } from '../api';
import { cacheManager } from '../cache/cacheManager';
import { invalidationStrategies } from '../cache/invalidationStrategies';
import type { Project, ProjectCreate, ProjectUpdate } from '../../types/project';

export const projectServiceWithCache = {
  /**
   * Get all projects (with caching)
   */
  async getAll(): Promise<Project[]> {
    const cacheKey = 'projects:all';
    
    // Check cache first
    const cached = cacheManager.get<Project[]>(cacheKey);
    if (cached) {
      return cached;
    }

    // Fetch from API
    const response = await apiClient.get<Project[]>('/api/projects');
    
    // Cache the result
    cacheManager.set(cacheKey, response.data, 5 * 60 * 1000); // 5 minutes
    
    return response.data;
  },

  /**
   * Get project by ID (with caching)
   */
  async getById(id: string): Promise<Project> {
    const cacheKey = `projects:${id}`;
    
    // Check cache first
    const cached = cacheManager.get<Project>(cacheKey);
    if (cached) {
      return cached;
    }

    // Fetch from API
    const response = await apiClient.get<Project>(`/api/projects/${id}`);
    
    // Cache the result
    cacheManager.set(cacheKey, response.data, 5 * 60 * 1000);
    
    return response.data;
  },

  /**
   * Create project (with cache invalidation)
   */
  async create(data: ProjectCreate): Promise<Project> {
    const response = await apiClient.post<Project>('/api/projects', data);
    
    // Invalidate related caches
    invalidationStrategies.projects.onCreate();
    
    return response.data;
  },

  /**
   * Update project (with optimistic update)
   */
  async update(id: string, data: ProjectUpdate): Promise<Project> {
    // Get current cached data for rollback
    const cacheKey = `projects:${id}`;
    const previousData = cacheManager.get<Project>(cacheKey);

    try {
      // Optimistically update cache
      if (previousData) {
        const optimisticData = { ...previousData, ...data };
        cacheManager.set(cacheKey, optimisticData);
      }

      // Make API call
      const response = await apiClient.put<Project>(`/api/projects/${id}`, data);
      
      // Update cache with real data
      cacheManager.set(cacheKey, response.data);
      
      // Invalidate related caches
      invalidationStrategies.projects.onUpdate(id);
      
      return response.data;
    } catch (error) {
      // Rollback on error
      if (previousData) {
        cacheManager.set(cacheKey, previousData);
      }
      throw error;
    }
  },

  /**
   * Delete project (with cache invalidation)
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/api/projects/${id}`);
    
    // Invalidate related caches
    invalidationStrategies.projects.onDelete(id);
  },

  /**
   * Manually invalidate project cache
   */
  invalidateCache(id?: string): void {
    if (id) {
      cacheManager.invalidate(`projects:${id}`);
    } else {
      cacheManager.invalidateResource('projects');
    }
  },
};

export default projectServiceWithCache;
