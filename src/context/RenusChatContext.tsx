import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { publicChatService, ChatMessage } from '@/services/publicChatService';
import { toast } from 'sonner';

interface RenusChatContextType {
  isChatOpen: boolean;
  toggleChat: () => void;
  openChat: () => void;
  closeChat: () => void;
  messages: ChatMessage[];
  sendMessage: (text: string) => Promise<void>;
  isTyping: boolean;
}

const RenusChatContext = createContext<RenusChatContextType | undefined>(undefined);

export const RenusChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  // Default welcome message (fallback)
  const defaultWelcome: ChatMessage = { id: 'welcome', sender: 'renus', text: 'Olá! Eu sou Renus, seu assistente de descoberta. Como posso ajudar a transformar seu negócio hoje?' };
  const [messages, setMessages] = useState<ChatMessage[]>([defaultWelcome]);

  const [interviewId, setInterviewId] = useState<string | null>(localStorage.getItem('renus_interview_id'));
  const [isTyping, setIsTyping] = useState(false);

  // Load dynamic welcome message on mount via PUBLIC endpoint
  useEffect(() => {
    const loadWelcome = async () => {
      try {
        const agentInfo = await publicChatService.getAgentPublicInfo('renus');

        if (agentInfo && agentInfo.welcome_message) {
          setMessages(prev => {
            // Only replace if the first message is the default welcome and hasn't been changed/added to
            if (prev.length === 1 && prev[0].id === 'welcome') {
              return [{ ...prev[0], text: agentInfo.welcome_message }];
            }
            return prev;
          });
        }
      } catch (error) {
        // Silent fail - keep default welcome
        console.warn("Using default welcome message (renus agent not found or public API error)");
      }
    };

    loadWelcome();
  }, []);

  const toggleChat = () => setIsChatOpen(prev => !prev);
  const openChat = () => setIsChatOpen(true);
  const closeChat = () => setIsChatOpen(false);

  const sendMessage = useCallback(async (text: string) => {
    try {
      // Add user message immediately
      const userMsg: ChatMessage = { id: Date.now().toString(), sender: 'user', text };
      setMessages(prev => [...prev, userMsg]);
      setIsTyping(true);

      // Call API (assuming slug 'renus' for the main orchestrator)
      // If 'renus' doesn't exist, we might need 'renus-discovery' or similar. 
      // Ideally this comes from config.
      const slug = 'renus';

      const response = await publicChatService.sendMessage(slug, text, interviewId);

      if (response.interview_id && response.interview_id !== interviewId) {
        setInterviewId(response.interview_id);
        localStorage.setItem('renus_interview_id', response.interview_id);
      }

      const botMsg: ChatMessage = {
        id: Date.now().toString() + '_bot',
        sender: 'renus',
        text: response.message
      };

      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      console.error('Chat Error:', error);
      toast.error('Não foi possível conectar ao Renus. Tente novamente mais tarde.');
    } finally {
      setIsTyping(false);
    }
  }, [interviewId]);

  // Restore history if interviewId exists
  useEffect(() => {
    if (interviewId && messages.length === 1) { // Only welcome message present
      /* 
      // Optional: Restore history logic
      publicChatService.getHistory('renus', interviewId).then(data => {
        // Map history to local format
      });
      */
    }
  }, [interviewId]);

  const value = {
    isChatOpen,
    toggleChat,
    openChat,
    closeChat,
    messages,
    sendMessage,
    isTyping
  };

  return (
    <RenusChatContext.Provider value={value}>
      {children}
    </RenusChatContext.Provider>
  );
};

export const useRenusChat = () => {
  const context = useContext(RenusChatContext);
  if (context === undefined) {
    throw new Error('useRenusChat must be used within a RenusChatProvider');
  }
  return context;
};