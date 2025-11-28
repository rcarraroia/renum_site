/**
 * useMessages Hook
 * React Query hooks for message operations
 */
import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query';
import {
  messageService,
  MessageCreate,
  MessageResponse,
} from '../services/messageService';

// Query keys
export const messageKeys = {
  all: ['messages'] as const,
  lists: () => [...messageKeys.all, 'list'] as const,
  list: (conversationId: string) => [...messageKeys.lists(), conversationId] as const,
};

/**
 * Hook to fetch messages for a conversation
 */
export function useMessages(conversationId: string, limit: number = 50) {
  return useQuery({
    queryKey: messageKeys.list(conversationId),
    queryFn: () => messageService.getMessages(conversationId, limit),
    enabled: !!conversationId,
    staleTime: 10000, // 10 seconds
  });
}

/**
 * Hook to fetch messages with infinite scroll
 */
export function useInfiniteMessages(conversationId: string, limit: number = 50) {
  return useInfiniteQuery({
    queryKey: messageKeys.list(conversationId),
    queryFn: ({ pageParam }) =>
      messageService.getMessages(conversationId, limit, pageParam),
    getNextPageParam: (lastPage) => {
      // Return the ID of the oldest message for pagination
      if (lastPage.length === 0) return undefined;
      return lastPage[0].id;
    },
    initialPageParam: undefined as string | undefined,
    enabled: !!conversationId,
    staleTime: 10000,
  });
}

/**
 * Hook to send message
 */
export function useSendMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: MessageCreate) => messageService.sendMessage(data),
    onMutate: async (newMessage) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({
        queryKey: messageKeys.list(newMessage.conversation_id),
      });

      // Snapshot previous value
      const previousMessages = queryClient.getQueryData<MessageResponse[]>(
        messageKeys.list(newMessage.conversation_id)
      );

      // Optimistically add new message
      const optimisticMessage: MessageResponse = {
        id: `temp-${Date.now()}`,
        conversation_id: newMessage.conversation_id,
        sender: newMessage.sender,
        type: newMessage.type,
        content: newMessage.content,
        timestamp: new Date().toISOString(),
        is_read: false,
        metadata: newMessage.metadata || null,
        created_at: new Date().toISOString(),
      };

      queryClient.setQueryData<MessageResponse[]>(
        messageKeys.list(newMessage.conversation_id),
        (old) => (old ? [...old, optimisticMessage] : [optimisticMessage])
      );

      return { previousMessages, optimisticMessage };
    },
    onError: (err, newMessage, context) => {
      // Rollback on error
      if (context?.previousMessages) {
        queryClient.setQueryData(
          messageKeys.list(newMessage.conversation_id),
          context.previousMessages
        );
      }
    },
    onSuccess: (data, variables, context) => {
      // Replace optimistic message with real one
      queryClient.setQueryData<MessageResponse[]>(
        messageKeys.list(variables.conversation_id),
        (old) => {
          if (!old) return [data];
          return old.map((msg) =>
            msg.id === context?.optimisticMessage.id ? data : msg
          );
        }
      );
    },
    onSettled: (data, error, variables) => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({
        queryKey: messageKeys.list(variables.conversation_id),
      });
    },
  });
}

/**
 * Hook to mark messages as read
 */
export function useMarkAsRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (messageIds: string[]) =>
      messageService.markMessagesAsRead(messageIds),
    onMutate: async (messageIds) => {
      // Find which conversation these messages belong to
      // (In a real app, you'd pass conversation_id explicitly)
      const queries = queryClient.getQueriesData<MessageResponse[]>({
        queryKey: messageKeys.lists(),
      });

      const updates: Array<{
        queryKey: any;
        previousMessages: MessageResponse[];
      }> = [];

      for (const [queryKey, messages] of queries) {
        if (!messages) continue;

        const hasMessages = messages.some((msg) => messageIds.includes(msg.id));
        if (!hasMessages) continue;

        await queryClient.cancelQueries({ queryKey });

        const previousMessages = messages;

        // Optimistically mark as read
        queryClient.setQueryData<MessageResponse[]>(queryKey, (old) =>
          old
            ? old.map((msg) =>
                messageIds.includes(msg.id) ? { ...msg, is_read: true } : msg
              )
            : []
        );

        updates.push({ queryKey, previousMessages });
      }

      return { updates };
    },
    onError: (err, messageIds, context) => {
      // Rollback on error
      if (context?.updates) {
        for (const { queryKey, previousMessages } of context.updates) {
          queryClient.setQueryData(queryKey, previousMessages);
        }
      }
    },
    onSettled: () => {
      // Refetch all message lists
      queryClient.invalidateQueries({ queryKey: messageKeys.lists() });
    },
  });
}
