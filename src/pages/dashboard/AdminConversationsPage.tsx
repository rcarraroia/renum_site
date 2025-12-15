import React, { useState, useMemo, useCallback, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { MessageSquare, Zap, Clock, CheckCircle, Mail, Globe, Users } from 'lucide-react';
// Mock conversations data (local fallback)
const MOCK_CONVERSATIONS = [
  {
    id: '1',
    leadId: '1',
    status: 'active' as ConversationStatus,
    lastMessage: 'Olá, preciso de ajuda com meu pedido',
    lastMessageAt: new Date('2024-12-10T10:30:00'),
    unreadCount: 2,
    channel: 'whatsapp',
    leadName: 'João Silva',
    leadPhone: '+5511999999999'
  }
];
import { Conversation, ConversationStatus, MessageSender } from '@/types/conversation';
import ConversationListPanel from '@/components/conversations/ConversationListPanel';
import ConversationDetailPanel from '@/components/conversations/ConversationDetailPanel';
import { WebSocketIndicator } from '@/components/conversations/WebSocketIndicator';
import { useWebSocket } from '@/hooks/useWebSocket';
import { conversationService } from '@/services/conversationService';
import { toast } from 'sonner';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

// WebSocket URL from environment or default
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
const USE_WEBSOCKET = import.meta.env.VITE_USE_WEBSOCKET === 'true';

const AdminConversationsPage: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>(MOCK_CONVERSATIONS);
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(MOCK_CONVERSATIONS[0]?.id || null);
  const [useMockData, setUseMockData] = useState(!USE_WEBSOCKET);

  // Get JWT token from localStorage
  const token = localStorage.getItem('token') || '';

  // Initialize WebSocket (only if enabled)
  const {
    isConnected,
    connectionStatus,
    lastError,
    sendMessage: wsSendMessage,
    sendTyping,
    joinConversation,
    leaveConversation,
  } = useWebSocket({
    url: WS_URL,
    token,
    autoConnect: USE_WEBSOCKET && !!token,
    
    onMessage: (data) => {
      console.log('WebSocket message received:', data);
      // Update conversations with new message
      toast.info('Nova mensagem recebida');
    },
    
    onTyping: (data) => {
      console.log('Typing indicator:', data);
    },
    
    onError: (data) => {
      console.error('WebSocket error:', data);
      toast.error(`Erro WebSocket: ${data.error}`);
    },
  });

  // Load real conversations if WebSocket is enabled
  useEffect(() => {
    if (USE_WEBSOCKET && isConnected) {
      loadConversations();
    }
  }, [isConnected]);

  // Join conversation when selected
  useEffect(() => {
    if (USE_WEBSOCKET && selectedConversationId && isConnected) {
      joinConversation(selectedConversationId);
      
      return () => {
        leaveConversation(selectedConversationId);
      };
    }
  }, [selectedConversationId, isConnected]);

  const loadConversations = async () => {
    try {
      const data = await conversationService.getAll();
      setConversations(data.items as any);
      setUseMockData(false);
    } catch (error) {
      console.error('Error loading conversations:', error);
      toast.error('Erro ao carregar conversas. Usando dados de exemplo.');
      setUseMockData(true);
    }
  };

  const selectedConversation = useMemo(() => 
    conversations.find(c => c.id === selectedConversationId) || null
  , [conversations, selectedConversationId]);

  const metrics = useMemo(() => ({
    total: conversations.length,
    unread: conversations.reduce((sum, conv) => sum + conv.unreadCount, 0),
    newToday: conversations.filter(c => c.status === 'Nova').length,
  }), [conversations]);

  const handleUpdateStatus = useCallback((id: string, status: ConversationStatus) => {
    setConversations(prev => prev.map(conv => 
      conv.id === id ? { ...conv, status, lastUpdate: new Date() } : conv
    ));
    toast.success(`Status da conversa ${id} alterado para ${status}.`);
  }, []);

  const handleSendMessage = useCallback((id: string, content: string, isInternal: boolean, sender: MessageSender = 'admin') => {
    // If WebSocket is enabled and connected, send via WebSocket
    if (USE_WEBSOCKET && isConnected && !isInternal) {
      wsSendMessage(id, content);
      toast.success("Mensagem enviada via WebSocket.");
      return;
    }

    // Fallback to local state update (MOCK mode or internal notes)
    const newMessage = {
      id: `m${Date.now()}`,
      sender: sender,
      type: 'text' as const,
      content: content,
      timestamp: new Date(),
      read: true,
      metadata: {
        internal_note: isInternal,
        intent: isInternal ? 'Nota Interna' : 'Resposta Manual',
      }
    };

    setConversations(prev => prev.map(conv => {
      if (conv.id === id) {
        return {
          ...conv,
          messages: [...conv.messages, newMessage],
          lastUpdate: newMessage.timestamp,
          unreadCount: 0, // Admin interaction marks as read
          status: conv.status === 'Nova' ? 'Em Andamento' : conv.status,
        };
      }
      return conv;
    }));
    
    if (isInternal) {
        toast.info("Nota interna adicionada.");
    } else {
        toast.success("Mensagem enviada ao cliente.");
    }
  }, [USE_WEBSOCKET, isConnected, wsSendMessage]);

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <MessageSquare className="h-7 w-7 mr-3 text-[#FF6B35]" />
          Conversas
        </h2>
        <div className="flex items-center space-x-3">
          {/* WebSocket Status Indicator (only if enabled) */}
          {USE_WEBSOCKET && <WebSocketIndicator status={connectionStatus} />}
          
          {/* Mock Data Badge */}
          {useMockData && (
            <span className="px-3 py-1.5 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
              Dados de Exemplo
            </span>
          )}
          
          <Button variant="outline">
            <Users className="h-4 w-4 mr-2" /> Gerenciar Agentes
          </Button>
        </div>
      </div>
      
      {/* WebSocket Error Alert */}
      {USE_WEBSOCKET && lastError && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <p className="font-medium">Erro de conexão WebSocket:</p>
          <p className="text-sm">{lastError}</p>
          <p className="text-sm mt-2">Usando dados de exemplo como fallback.</p>
        </div>
      )}
      
      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Conversas</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Mensagens Não Lidas</CardTitle>
            <Mail className="h-4 w-4 text-[#FF6B35]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#FF6B35]">{metrics.unread}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Novas Hoje</CardTitle>
            <Clock className="h-4 w-4 text-[#0ca7d2]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#0ca7d2]">{metrics.newToday}</div>
          </CardContent>
        </Card>
      </div>

      {/* Split View Container */}
      <Card className="flex flex-grow h-[calc(100vh-280px)] min-h-[600px] overflow-hidden">
        <div className="w-full md:w-80 flex-shrink-0 h-full">
          <ConversationListPanel
            conversations={conversations}
            selectedConversationId={selectedConversationId}
            onSelectConversation={setSelectedConversationId}
          />
        </div>
        
        <Separator orientation="vertical" className="hidden md:block" />

        <div className="flex-grow h-full hidden md:block">
          {selectedConversation ? (
            <ConversationDetailPanel 
                conversation={selectedConversation} 
                onUpdateStatus={handleUpdateStatus}
                onSendMessage={handleSendMessage}
            />
          ) : (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              <p>Selecione uma conversa para visualizar os detalhes.</p>
            </div>
          )}
        </div>
        
        {/* Mobile View: Show only list or detail */}
        <div className={cn("flex-grow h-full md:hidden", selectedConversation ? 'block' : 'hidden')}>
            {selectedConversation && (
                <ConversationDetailPanel 
                    conversation={selectedConversation} 
                    onUpdateStatus={handleUpdateStatus}
                    onSendMessage={handleSendMessage}
                />
            )}
        </div>
        <div className={cn("w-full h-full md:hidden", selectedConversation ? 'hidden' : 'block')}>
            <ConversationListPanel
                conversations={conversations}
                selectedConversationId={selectedConversationId}
                onSelectConversation={setSelectedConversationId}
            />
        </div>
      </Card>
    </DashboardLayout>
  );
};

export default AdminConversationsPage;