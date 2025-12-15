/**
 * Project Service
 * Handles all project-related API calls
 */

import { apiClient } from './api';
import { Project, ProjectCreate, ProjectUpdate, ProjectList } from '../types/project';

export const projectService = {
  /**
   * Get all projects with pagination and filters
   */
  async getAll(params?: {
    page?: number;
    limit?: number;
    search?: string;
    status?: string;
    type?: string;
    client_id?: string;
  }): Promise<ProjectList> {
    const { data } = await apiClient.get<ProjectList>('/api/projects', params);
    return data;
  },

  /**
   * Get project by ID
   */
  async getById(id: string): Promise<Project> {
    const { data } = await apiClient.get<Project>(`/api/projects/${id}`);
    return data;
  },

  /**
   * Create new project
   */
  async create(project: ProjectCreate): Promise<Project> {
    const { data } = await apiClient.post<Project>('/api/projects', project);
    return data;
  },

  /**
   * Update existing project
   */
  async update(id: string, project: ProjectUpdate): Promise<Project> {
    const { data } = await apiClient.put<Project>(`/api/projects/${id}`, project);
    return data;
  },

  /**
   * Delete project
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/api/projects/${id}`);
  },
};
