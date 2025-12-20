
import React, { useState, useMemo, useCallback, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { MessageSquare, Clock, Mail } from 'lucide-react';
// Mock conversations updated for client view context
const MOCK_CONVERSATIONS_CLIENT = [
    {
        id: '1',
        leadId: '1',
        status: 'active' as const,
        lastMessage: 'Olá, gostaria de saber mais sobre o plano.',
        lastMessageAt: new Date('2024-12-19T09:30:00'),
        unreadCount: 1,
        channel: 'whatsapp',
        leadName: 'Cliente Exemplo',
        leadPhone: '+5511988888888'
    },
    {
        id: '2',
        leadId: '2',
        status: 'closed' as const,
        lastMessage: 'Obrigado pelo atendimento!',
        lastMessageAt: new Date('2024-12-18T16:20:00'),
        unreadCount: 0,
        channel: 'web',
        leadName: 'Visitante Site',
        leadPhone: ''
    }
];
import { Conversation, ConversationStatus, MessageSender } from '@/types/conversation';
import ConversationListPanel from '@/components/conversations/ConversationListPanel';
import ConversationDetailPanel from '@/components/conversations/ConversationDetailPanel';
import { WebSocketIndicator } from '@/components/conversations/WebSocketIndicator';
import { useWebSocket } from '@/hooks/useWebSocket';
import { conversationService } from '@/services/conversationService'; // Assuming this service handles RLS correctly
import { toast } from 'sonner';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';

// WebSocket URL
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
const USE_WEBSOCKET = import.meta.env.VITE_USE_WEBSOCKET === 'true';

const ClientConversationsPage: React.FC = () => {
    // Use mock initially, switch to API later
    const [conversations, setConversations] = useState<Conversation[]>(MOCK_CONVERSATIONS_CLIENT as any);
    const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
    const [useMockData, setUseMockData] = useState(!USE_WEBSOCKET);

    const token = localStorage.getItem('token') || '';

    const {
        isConnected,
        connectionStatus,
        lastError,
        sendMessage: wsSendMessage,
        joinConversation,
        leaveConversation,
    } = useWebSocket({
        url: WS_URL,
        token,
        autoConnect: USE_WEBSOCKET && !!token,

        onMessage: (data) => {
            console.log('Client WS message:', data);
            toast.info('Nova mensagem recebida');
            // In real implementation: update conversation list
        },

        onError: (data) => {
            console.error('WebSocket error:', data);
        },
    });

    useEffect(() => {
        if (USE_WEBSOCKET && isConnected) {
            loadConversations();
        }
    }, [isConnected]);

    // Join/Leave rooms logic
    useEffect(() => {
        if (USE_WEBSOCKET && selectedConversationId && isConnected) {
            joinConversation(selectedConversationId);
            return () => leaveConversation(selectedConversationId);
        }
    }, [selectedConversationId, isConnected]);

    const loadConversations = async () => {
        try {
            // In the future: ensure this service calls an endpoint filtered by client token
            const data = await conversationService.getAll();
            setConversations(data.items as any);
            setUseMockData(false);
        } catch (error) {
            console.error('Error loading conversations:', error);
            // Keep mock data on error for demo purposes
            setUseMockData(true);
        }
    };

    const selectedConversation = useMemo(() =>
        conversations.find(c => c.id === selectedConversationId) || null
        , [conversations, selectedConversationId]);

    const metrics = useMemo(() => ({
        total: conversations.length,
        unread: conversations.reduce((sum, conv) => sum + conv.unreadCount, 0),
        active: conversations.filter(c => c.status === 'active' || c.status === 'Em Andamento').length,
    }), [conversations]);

    const handleUpdateStatus = useCallback((id: string, status: ConversationStatus) => {
        setConversations(prev => prev.map(conv =>
            conv.id === id ? { ...conv, status, lastUpdate: new Date() } : conv
        ));
        toast.success(`Conversa ${status}.`);
    }, []);

    const handleSendMessage = useCallback((id: string, content: string, isInternal: boolean, sender: MessageSender = 'user') => {
        if (USE_WEBSOCKET && isConnected && !isInternal) {
            wsSendMessage(id, content);
            return;
        }

        // Optimistic Update (Mock)
        const newMessage = {
            id: `m${Date.now()}`,
            sender: sender,
            type: 'text' as const,
            content: content,
            timestamp: new Date(),
            read: true,
            metadata: { internal_note: isInternal }
        };

        setConversations(prev => prev.map(conv => {
            if (conv.id === id) {
                return {
                    ...conv,
                    messages: [...(conv.messages || []), newMessage],
                    lastUpdate: newMessage.timestamp,
                    unreadCount: 0
                };
            }
            return conv;
        }));
    }, [USE_WEBSOCKET, isConnected, wsSendMessage]);

    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold flex items-center">
                    <MessageSquare className="h-7 w-7 mr-3 text-[#FF6B35]" />
                    Minhas Conversas
                </h2>

                {USE_WEBSOCKET && <WebSocketIndicator status={connectionStatus} />}
            </div>

            {/* Metrics Cards */}
            <div className="grid gap-4 md:grid-cols-3 mb-8">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Atendimentos</CardTitle>
                        <MessageSquare className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics.total}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Não Lidas</CardTitle>
                        <Mail className="h-4 w-4 text-[#FF6B35]" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-[#FF6B35]">{metrics.unread}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Ativas Agora</CardTitle>
                        <Clock className="h-4 w-4 text-[#0ca7d2]" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-[#0ca7d2]">{metrics.active}</div>
                    </CardContent>
                </Card>
            </div>

            <Card className="flex flex-grow h-[calc(100vh-280px)] min-h-[600px] overflow-hidden">
                <div className="w-full md:w-80 flex-shrink-0 h-full border-r">
                    <ConversationListPanel
                        conversations={conversations}
                        selectedConversationId={selectedConversationId}
                        onSelectConversation={setSelectedConversationId}
                    />
                </div>

                <div className="hidden md:flex flex-grow h-full flex-col">
                    {selectedConversation ? (
                        <ConversationDetailPanel
                            conversation={selectedConversation}
                            onUpdateStatus={handleUpdateStatus}
                            onSendMessage={handleSendMessage}
                            readOnly={false} // Client can reply? Yes, usually.
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full text-muted-foreground bg-gray-50/50">
                            <div className="text-center">
                                <MessageSquare className="h-12 w-12 mx-auto mb-3 opacity-20" />
                                <p>Selecione uma conversa para iniciar o atendimento.</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Mobile View Support (Simplified) */}
                {!selectedConversation && (
                    <div className="md:hidden w-full">
                        {/* List already rendered above, but logic would need to toggle visibility like admin page */}
                    </div>
                )}
            </Card>
        </DashboardLayout>
    );
};

export default ClientConversationsPage;
