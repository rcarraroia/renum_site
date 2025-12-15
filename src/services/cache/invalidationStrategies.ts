import { cacheManager } from './cacheManager';

/**
 * Cache invalidation strategies for different resources
 * Defines which cache entries should be invalidated when data changes
 */

export const invalidationStrategies = {
  /**
   * Projects invalidation
   */
  projects: {
    onCreate: () => {
      cacheManager.invalidateResource('projects');
      cacheManager.invalidateResource('reports'); // Reports depend on projects
    },
    onUpdate: (projectId: string) => {
      cacheManager.invalidate(`projects:${projectId}`);
      cacheManager.invalidateResource('projects');
      cacheManager.invalidateResource('reports');
    },
    onDelete: (projectId: string) => {
      cacheManager.invalidate(`projects:${projectId}`);
      cacheManager.invalidateResource('projects');
      cacheManager.invalidateResource('reports');
      // Also invalidate related interviews
      cacheManager.invalidatePattern(`interviews.*project:${projectId}`);
    },
  },

  /**
   * Leads invalidation
   */
  leads: {
    onCreate: () => {
      cacheManager.invalidateResource('leads');
      cacheManager.invalidateResource('reports');
    },
    onUpdate: (leadId: string) => {
      cacheManager.invalidate(`leads:${leadId}`);
      cacheManager.invalidateResource('leads');
      cacheManager.invalidateResource('reports');
    },
    onDelete: (leadId: string) => {
      cacheManager.invalidate(`leads:${leadId}`);
      cacheManager.invalidateResource('leads');
      cacheManager.invalidateResource('reports');
      // Also invalidate related conversations and interviews
      cacheManager.invalidatePattern(`conversations.*lead:${leadId}`);
      cacheManager.invalidatePattern(`interviews.*lead:${leadId}`);
    },
    onConvert: (leadId: string, clientId: string) => {
      cacheManager.invalidate(`leads:${leadId}`);
      cacheManager.invalidateResource('leads');
      cacheManager.invalidateResource('clients');
      cacheManager.invalidate(`clients:${clientId}`);
      cacheManager.invalidateResource('reports');
    },
    onStageChange: (leadId: string) => {
      cacheManager.invalidate(`leads:${leadId}`);
      cacheManager.invalidateResource('leads');
      cacheManager.invalidateResource('reports');
    },
  },

  /**
   * Clients invalidation
   */
  clients: {
    onCreate: () => {
      cacheManager.invalidateResource('clients');
      cacheManager.invalidateResource('reports');
    },
    onUpdate: (clientId: string) => {
      cacheManager.invalidate(`clients:${clientId}`);
      cacheManager.invalidateResource('clients');
      cacheManager.invalidateResource('reports');
    },
    onDelete: (clientId: string) => {
      cacheManager.invalidate(`clients:${clientId}`);
      cacheManager.invalidateResource('clients');
      cacheManager.invalidateResource('reports');
      // Also invalidate related data
      cacheManager.invalidatePattern(`leads.*client:${clientId}`);
      cacheManager.invalidatePattern(`projects.*client:${clientId}`);
    },
  },

  /**
   * Conversations invalidation
   */
  conversations: {
    onCreate: () => {
      cacheManager.invalidateResource('conversations');
      cacheManager.invalidateResource('reports');
    },
    onUpdate: (conversationId: string) => {
      cacheManager.invalidate(`conversations:${conversationId}`);
      cacheManager.invalidateResource('conversations');
    },
    onNewMessage: (conversationId: string) => {
      cacheManager.invalidate(`conversations:${conversationId}`);
      cacheManager.invalidate(`conversations:${conversationId}:messages`);
      cacheManager.invalidateResource('conversations');
      cacheManager.invalidateResource('reports');
    },
    onStatusChange: (conversationId: string) => {
      cacheManager.invalidate(`conversations:${conversationId}`);
      cacheManager.invalidateResource('conversations');
      cacheManager.invalidateResource('reports');
    },
  },

  /**
   * Interviews invalidation
   */
  interviews: {
    onCreate: () => {
      cacheManager.invalidateResource('interviews');
      cacheManager.invalidateResource('reports');
    },
    onUpdate: (interviewId: string) => {
      cacheManager.invalidate(`interviews:${interviewId}`);
      cacheManager.invalidateResource('interviews');
    },
    onNewMessage: (interviewId: string) => {
      cacheManager.invalidate(`interviews:${interviewId}`);
      cacheManager.invalidate(`interviews:${interviewId}:messages`);
      cacheManager.invalidateResource('interviews');
    },
    onComplete: (interviewId: string) => {
      cacheManager.invalidate(`interviews:${interviewId}`);
      cacheManager.invalidate(`interviews:${interviewId}:results`);
      cacheManager.invalidateResource('interviews');
      cacheManager.invalidateResource('reports');
    },
  },

  /**
   * Reports invalidation
   */
  reports: {
    onFilterChange: () => {
      cacheManager.invalidateResource('reports');
    },
    onDataChange: () => {
      // Reports should be invalidated when any data changes
      cacheManager.invalidateResource('reports');
    },
  },

  /**
   * Global invalidation
   */
  global: {
    onLogout: () => {
      cacheManager.clear();
    },
    onAuthError: () => {
      cacheManager.clear();
    },
  },
};

export default invalidationStrategies;
