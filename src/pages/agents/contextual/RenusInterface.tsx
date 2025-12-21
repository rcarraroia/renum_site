/**
 * Task 22: RENUS Contextual Interface - IMPLEMENTAÇÃO REAL
 * Dashboard de conversas ativas com métricas
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { MessageSquare, TrendingUp, Users, Clock, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient } from '@/services/api';

interface Conversation {
    id: string;
    user_name: string;
    last_message: string;
    status: 'active' | 'waiting' | 'completed';
    created_at: string;
    message_count: number;
}

interface RenusMetrics {
    active_conversations: number;
    total_conversations_today: number;
    avg_response_time: number;
    satisfaction_rate: number;
}

export const RenusInterface: React.FC = () => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [metrics, setMetrics] = useState<RenusMetrics | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadRenusData();
    }, []);

    const loadRenusData = async () => {
        try {
            // Carregar conversas ativas do RENUS
            const { data: conversationsData } = await apiClient.get<Conversation[]>('/api/agents/renus/conversations', { status: 'active' });
            setConversations(conversationsData || []);

            // Carregar métricas
            const { data: metricsData } = await apiClient.get<RenusMetrics>('/api/agents/renus/metrics');
            setMetrics(metricsData);
        } catch (error) {
            console.error('Erro ao carregar dados RENUS:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="p-8 text-center">Carregando dashboard RENUS...</div>;
    }

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">RENUS - Orquestrador de Descoberta</h1>
                    <p className="text-muted-foreground">Dashboard de Conversas e Métricas</p>
                </div>
                <Link to="/dashboard/admin/agents/renus/config">
                    <button className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-md">
                        <Settings className="h-4 w-4" />
                        Configuração Técnica
                    </button>
                </Link>
            </div>

            {/* Métricas */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Conversas Ativas</CardTitle>
                        <MessageSquare className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics?.active_conversations || 0}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Conversas Hoje</CardTitle>
                        <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics?.total_conversations_today || 0}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Tempo Médio Resposta</CardTitle>
                        <Clock className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics?.avg_response_time || 0}s</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Satisfação</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics?.satisfaction_rate || 0}%</div>
                    </CardContent>
                </Card>
            </div>

            {/* Tabs de Conversas */}
            <Tabs defaultValue="active" className="w-full">
                <TabsList>
                    <TabsTrigger value="active">Ativas ({conversations.filter(c => c.status === 'active').length})</TabsTrigger>
                    <TabsTrigger value="waiting">Aguardando ({conversations.filter(c => c.status === 'waiting').length})</TabsTrigger>
                    <TabsTrigger value="history">Histórico</TabsTrigger>
                </TabsList>

                <TabsContent value="active" className="space-y-4">
                    {conversations.filter(c => c.status === 'active').map(conv => (
                        <Card key={conv.id} className="cursor-pointer hover:bg-accent">
                            <CardHeader>
                                <CardTitle className="text-base">{conv.user_name}</CardTitle>
                                <CardDescription>{conv.last_message}</CardDescription>
                            </CardHeader>
                            <CardContent className="flex justify-between text-sm text-muted-foreground">
                                <span>{conv.message_count} mensagens</span>
                                <span>{conv.created_at ? new Date(conv.created_at).toLocaleString() : 'Data indisponível'}</span>
                            </CardContent>
                        </Card>
                    ))}
                </TabsContent>

                <TabsContent value="waiting">
                    <Card>
                        <CardContent className="p-6">
                            <p className="text-center text-muted-foreground">Nenhuma conversa aguardando resposta</p>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="history">
                    <Card>
                        <CardContent className="p-6">
                            <p className="text-center text-muted-foreground">Histórico de conversas</p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default RenusInterface;
