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

import { isaService } from '@/services/isaService';

interface RenusChatContextType {
  isChatOpen: boolean;
  toggleChat: () => void;
  openChat: () => void;
  closeChat: () => void;
  messages: ChatMessage[];
  sendMessage: (text: string) => Promise<void>;
  isTyping: boolean;
  activeAgent: 'renus' | 'isa';
  setActiveAgent: (agent: 'renus' | 'isa') => void;
}

const RenusChatContext = createContext<RenusChatContextType | undefined>(undefined);

export const RenusChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Default welcome messages
  const renusWelcome: ChatMessage = { id: 'welcome_renus', sender: 'renus', text: 'Olá! Eu sou Renus, seu assistente de descoberta. Como posso ajudar a transformar seu negócio hoje?' };
  const isaWelcome: ChatMessage = { id: 'welcome_isa', sender: 'renus', text: 'Olá Admin! Sou a ISA, sua assistente administrativa. Posso gerar relatórios, listar dados e executar comandos no sistema.' }; // sender 'renus' used as generic bot sender for UI compatibility

  // Separate states for each agent
  const [renusMessages, setRenusMessages] = useState<ChatMessage[]>([renusWelcome]);
  const [isaMessages, setIsaMessages] = useState<ChatMessage[]>([isaWelcome]);

  const [activeAgent, setActiveAgent] = useState<'renus' | 'isa'>('renus');

  const [interviewId, setInterviewId] = useState<string | null>(localStorage.getItem('renus_interview_id'));
  const [isTyping, setIsTyping] = useState(false);

  // Load dynamic welcome message for Renus on mount
  useEffect(() => {
    const loadWelcome = async () => {
      try {
        const agentInfo = await publicChatService.getAgentPublicInfo('renus');
        if (agentInfo && agentInfo.welcome_message) {
          setRenusMessages(prev => {
            if (prev.length === 1 && prev[0].id === 'welcome_renus') {
              return [{ ...prev[0], text: agentInfo.welcome_message }];
            }
            return prev;
          });
        }
      } catch (error) {
        console.warn("Using default welcome message for Renus");
      }
    };
    loadWelcome();
  }, []);

  const toggleChat = () => setIsChatOpen(prev => !prev);
  const openChat = () => setIsChatOpen(true);
  const closeChat = () => setIsChatOpen(false);

  // Get current active messages
  const messages = activeAgent === 'renus' ? renusMessages : isaMessages;

  const sendMessage = useCallback(async (text: string) => {
    try {
      // Add user message immediately
      const userMsg: ChatMessage = { id: Date.now().toString(), sender: 'user', text };

      if (activeAgent === 'renus') {
        setRenusMessages(prev => [...prev, userMsg]);
      } else {
        setIsaMessages(prev => [...prev, userMsg]);
      }

      setIsTyping(true);

      if (activeAgent === 'renus') {
        // RENUS LOGIC (Public)
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
        setRenusMessages(prev => [...prev, botMsg]);

      } else {
        // ISA LOGIC (Admin/Private)
        const response = await isaService.sendMessage(text);

        const botMsg: ChatMessage = {
          id: Date.now().toString() + '_isa',
          sender: 'renus', // UI expects 'renus' for bot styling currently, or we update UI
          text: response.content
        };
        setIsaMessages(prev => [...prev, botMsg]);
      }

    } catch (error) {
      console.error('Chat Error:', error);
      toast.error(`Não foi possível conectar ao ${activeAgent === 'renus' ? 'Renus' : 'ISA'}.`);
    } finally {
      setIsTyping(false);
    }
  }, [interviewId, activeAgent]);

  const value = {
    isChatOpen,
    toggleChat,
    openChat,
    closeChat,
    messages,
    sendMessage,
    isTyping,
    activeAgent,
    setActiveAgent
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