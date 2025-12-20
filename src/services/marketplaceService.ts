/**
 * Marketplace Service
 * Service for marketplace operations (templates, cloning, etc)
 */

import { apiClient } from './api';
import type { Agent } from '@/types/agent';

/**
 * List marketplace templates
 * Automatically filters by client category (B2B/B2C)
 */
export async function listMarketplaceTemplates(params: { niche?: string } = {}): Promise<Agent[]> {
    const response = await apiClient.get<Agent[]>('/api/marketplace/templates', params);
    return response.data;
}

/**
 * Clone template for current client
 */
export async function cloneTemplate(templateId: string, customName?: string): Promise<Agent> {
    const response = await apiClient.post<Agent>(`/api/marketplace/templates/${templateId}/clone`, {
        custom_name: customName
    });
    return response.data;
}

/**
 * Get template details
 */
export async function getTemplate(templateId: string): Promise<Agent> {
    const response = await apiClient.get<Agent>(`/api/agents/${templateId}`);
    return response.data;
}

export const marketplaceService = {
    listMarketplaceTemplates,
    cloneTemplate,
    getTemplate,
};

export default marketplaceService;
