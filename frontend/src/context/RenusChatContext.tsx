import React, { createContext, useContext, useState, useMemo } from 'react';

interface RenusChatContextType {
  isChatOpen: boolean;
  toggleChat: () => void;
  openChat: () => void;
  closeChat: () => void;
}

const RenusChatContext = createContext<RenusChatContextType | undefined>(undefined);

export const RenusChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => setIsChatOpen(prev => !prev);
  const openChat = () => setIsChatOpen(true);
  const closeChat = () => setIsChatOpen(false);

  const value = useMemo(() => ({ isChatOpen, toggleChat, openChat, closeChat }), [isChatOpen]);

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