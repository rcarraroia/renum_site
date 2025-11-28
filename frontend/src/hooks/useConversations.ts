/**
 * useConversations Hook
 * React Query hooks for conversation operations
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  conversationService,
  ConversationFilters,
  ConversationCreate,
  ConversationUpdate,
  ConversationResponse,
} from '../services/conversationService';

// Query keys
export const conversationKeys = {
  all: ['conversations'] as const,
  lists: () => [...conversationKeys.all, 'list'] as const,
  list: (page: number, limit: number, filters?: ConversationFilters) =>
    [...conversationKeys.lists(), { page, limit, filters }] as const,
  details: () => [...conversationKeys.all, 'detail'] as const,
  detail: (id: string) => [...conversationKeys.details(), id] as const,
};

/**
 * Hook to fetch conversations list
 */
export function useConversations(
  page: number = 1,
  limit: number = 20,
  filters?: ConversationFilters
) {
  return useQuery({
    queryKey: conversationKeys.list(page, limit, filters),
    queryFn: () => conversationService.getConversations(page, limit, filters),
    staleTime: 30000, // 30 seconds
  });
}

/**
 * Hook to fetch single conversation
 */
export function useConversation(id: string) {
  return useQuery({
    queryKey: conversationKeys.detail(id),
    queryFn: () => conversationService.getConversationById(id),
    enabled: !!id,
    staleTime: 30000,
  });
}

/**
 * Hook to create conversation
 */
export function useCreateConversation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ConversationCreate) =>
      conversationService.createConversation(data),
    onSuccess: () => {
      // Invalidate conversations list
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
  });
}

/**
 * Hook to update conversation
 */
export function useUpdateConversation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ConversationUpdate }) =>
      conversationService.updateConversation(id, data),
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: conversationKeys.detail(id) });

      // Snapshot previous value
      const previousConversation = queryClient.getQueryData<ConversationResponse>(
        conversationKeys.detail(id)
      );

      // Optimistically update
      if (previousConversation) {
        queryClient.setQueryData<ConversationResponse>(
          conversationKeys.detail(id),
          { ...previousConversation, ...data }
        );
      }

      return { previousConversation };
    },
    onError: (err, { id }, context) => {
      // Rollback on error
      if (context?.previousConversation) {
        queryClient.setQueryData(
          conversationKeys.detail(id),
          context.previousConversation
        );
      }
    },
    onSettled: (data, error, { id }) => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: conversationKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
  });
}

/**
 * Hook to update conversation status
 */
export function useUpdateStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: 'active' | 'closed' | 'pending' }) =>
      conversationService.updateStatus(id, status),
    onMutate: async ({ id, status }) => {
      await queryClient.cancelQueries({ queryKey: conversationKeys.detail(id) });

      const previousConversation = queryClient.getQueryData<ConversationResponse>(
        conversationKeys.detail(id)
      );

      if (previousConversation) {
        queryClient.setQueryData<ConversationResponse>(
          conversationKeys.detail(id),
          { ...previousConversation, status }
        );
      }

      return { previousConversation };
    },
    onError: (err, { id }, context) => {
      if (context?.previousConversation) {
        queryClient.setQueryData(
          conversationKeys.detail(id),
          context.previousConversation
        );
      }
    },
    onSettled: (data, error, { id }) => {
      queryClient.invalidateQueries({ queryKey: conversationKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
  });
}

/**
 * Hook to delete conversation
 */
export function useDeleteConversation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => conversationService.deleteConversation(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
  });
}

/**
 * Hook to mark conversation as read
 */
export function useMarkAsRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => conversationService.markAsRead(id),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: conversationKeys.detail(id) });

      const previousConversation = queryClient.getQueryData<ConversationResponse>(
        conversationKeys.detail(id)
      );

      if (previousConversation) {
        queryClient.setQueryData<ConversationResponse>(
          conversationKeys.detail(id),
          { ...previousConversation, unread_count: 0 }
        );
      }

      return { previousConversation };
    },
    onError: (err, id, context) => {
      if (context?.previousConversation) {
        queryClient.setQueryData(
          conversationKeys.detail(id),
          context.previousConversation
        );
      }
    },
    onSettled: (data, error, id) => {
      queryClient.invalidateQueries({ queryKey: conversationKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
  });
}
