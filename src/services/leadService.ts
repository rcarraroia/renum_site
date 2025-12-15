/**
 * Lead Service
 * Handles all lead-related API calls
 */

import { apiClient } from './api';
import { Lead, LeadCreate, LeadUpdate, LeadList, LeadConvertRequest } from '../types/lead';

export const leadService = {
  /**
   * Get all leads with pagination and filters
   */
  async getAll(params?: {
    page?: number;
    limit?: number;
    search?: string;
    status?: string;
    source?: string;
  }): Promise<LeadList> {
    const { data } = await apiClient.get<LeadList>('/api/leads', params);
    return data;
  },

  /**
   * Get lead by ID
   */
  async getById(id: string): Promise<Lead> {
    const { data } = await apiClient.get<Lead>(`/api/leads/${id}`);
    return data;
  },

  /**
   * Create new lead
   */
  async create(lead: LeadCreate): Promise<Lead> {
    const { data } = await apiClient.post<Lead>('/api/leads', lead);
    return data;
  },

  /**
   * Update existing lead
   */
  async update(id: string, lead: LeadUpdate): Promise<Lead> {
    const { data } = await apiClient.put<Lead>(`/api/leads/${id}`, lead);
    return data;
  },

  /**
   * Delete lead
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/api/leads/${id}`);
  },

  /**
   * Convert lead to client
   */
  async convertToClient(id: string, data: LeadConvertRequest): Promise<any> {
    const { data: client } = await apiClient.post(`/api/leads/${id}/convert`, data);
    return client;
  },
};
