
import { agentService } from './agentService';
import { dashboardService } from './dashboardService';
import { paymentService } from './paymentService';
import { Agent, AgentStats } from '@/types/agent';
import { DashboardStats } from './dashboardService';

/**
 * Service for Client Dashboard operations
 * Centralizes calls to underlying services with client-specific context
 * Use this service for all interaction within the Client Panel (/dashboard/client)
 */
export const clientDashboardService = {
    /**
     * Get all agents for the current client
     * RLS ensures only client's agents are returned
     */
    getAgents: async (): Promise<Agent[]> => {
        return agentService.listAgents();
    },

    /**
     * Get specific agent by slug
     */
    getAgentBySlug: async (slug: string): Promise<Agent> => {
        return agentService.getAgentBySlug(slug);
    },

    /**
     * Get agent statistics
     */
    getAgentStats: async (agentId: string): Promise<AgentStats> => {
        return agentService.getAgentStats(agentId);
    },

    /**
     * Get overall client dashboard metrics
     */
    getDashboardMetrics: async (): Promise<DashboardStats> => {
        return dashboardService.getClientMetrics();
    },

    /**
     * Get client subscription details
     */
    getSubscription: async () => {
        return paymentService.getSubscription();
    }
};

export default clientDashboardService;
