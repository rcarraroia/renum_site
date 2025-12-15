/**
 * Client Service
 * Handles all client-related API calls
 */

import { apiClient } from './api';
import { Client, ClientCreate, ClientUpdate, ClientList } from '../types/client';

export const clientService = {
  /**
   * Get all clients with pagination and filters
   */
  async getAll(params?: {
    page?: number;
    limit?: number;
    search?: string;
    status?: string;
    plan?: string;
  }): Promise<ClientList> {
    const { data } = await apiClient.get<ClientList>('/api/clients', params);
    return data;
  },

  /**
   * Get client by ID
   */
  async getById(id: string): Promise<Client> {
    const { data } = await apiClient.get<Client>(`/api/clients/${id}`);
    return data;
  },

  /**
   * Create new client
   */
  async create(client: ClientCreate): Promise<Client> {
    const { data } = await apiClient.post<Client>('/api/clients', client);
    return data;
  },

  /**
   * Update existing client
   */
  async update(id: string, client: ClientUpdate): Promise<Client> {
    const { data } = await apiClient.put<Client>(`/api/clients/${id}`, client);
    return data;
  },

  /**
   * Delete client
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/api/clients/${id}`);
  },
};
