/**
 * Task 30: Intelligence Dashboard
 * Monitoramento de evolução da IA e memórias
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Brain, Activity, Memory, TrendingUp } from 'lucide-react';
import { apiClient } from '@/services/api';

interface AgentEvolution {
    agent_id: string;
    agent_name: string;
    total_conversations: number;
    avg_satisfaction: number;
    learning_progress: number;
}

interface MemoryEntry {
    id: string;
    type: 'short_term' | 'long_term' | 'episodic';
    content: string;
    created_at: string;
}

export const IntelligenceDashboard: React.FC = () => {
    const [agents, setAgents] = useState<AgentEvolution[]>([]);
    const [memories, setMemories] = useState<MemoryEntry[]>([]);
    const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const { data: agentsData } = await apiClient.get<any[]>('/api/agents', { is_system: false, limit: 20 });

            // Mock evolution data (seria calculado do histórico real)
            const evolution = agentsData.map((a: any) => ({
                agent_id: a.id,
                agent_name: a.name,
                total_conversations: Math.floor(Math.random() * 500),
                avg_satisfaction: 3.5 + Math.random() * 1.5,
                learning_progress: Math.floor(Math.random() * 100)
            }));

            setAgents(evolution);
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold flex items-center gap-2">
                    <Brain className="h-8 w-8" />
                    Intelligence Dashboard
                </h1>
                <p className="text-muted-foreground">
                    Monitore a evolução e performance dos seus agentes
                </p>
            </div>

            <Tabs defaultValue="evolution">
                <TabsList>
                    <TabsTrigger value="evolution">Evolução dos Agentes</TabsTrigger>
                    <TabsTrigger value="memories">Memórias</TabsTrigger>
                    <TabsTrigger value="learning">Fila de Aprendizado</TabsTrigger>
                </TabsList>

                <TabsContent value="evolution" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {agents.map(agent => (
                            <Card key={agent.agent_id} className="cursor-pointer hover:shadow-md">
                                <CardHeader>
                                    <CardTitle className="text-lg">{agent.agent_name}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        <div className="flex justify-between">
                                            <span className="text-sm text-muted-foreground">Conversas</span>
                                            <span className="font-medium">{agent.total_conversations}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-sm text-muted-foreground">Satisfação</span>
                                            <span className="font-medium">{agent.avg_satisfaction.toFixed(1)} ⭐</span>
                                        </div>
                                        <div>
                                            <div className="flex justify-between mb-1">
                                                <span className="text-sm text-muted-foreground">Aprendizado</span>
                                                <span className="text-sm">{agent.learning_progress}%</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                                <div
                                                    className="bg-blue-600 h-2 rounded-full"
                                                    style={{ width: `${agent.learning_progress}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                <TabsContent value="memories">
                    <Card>
                        <CardHeader>
                            <CardTitle>Gestão de Memórias</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground text-center py-8">
                                Selecione um agente para visualizar suas memórias
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="learning">
                    <Card>
                        <CardHeader>
                            <CardTitle>Fila de Aprendizado</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground text-center py-8">
                                Itens pendentes para fine-tuning e aprendizado contínuo
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default IntelligenceDashboard;
