/**
 * Task 23: Pesquisas Contextual Interface - IMPLEMENTAÇÃO REAL
 * Dashboard de entrevistas com análises de IA
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FileText, BarChart3, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient } from '@/services/api';

interface Interview {
    id: string;
    title: string;
    status: 'active' | 'completed' | 'analyzing';
    responses_count: number;
    created_at: string;
    ai_insights?: string;
}

export const PesquisasInterface: React.FC = () => {
    const [activeInterviews, setActiveInterviews] = useState<Interview[]>([]);
    const [completedInterviews, setCompletedInterviews] = useState<Interview[]>([]);

    useEffect(() => {
        loadInterviews();
    }, []);

    const loadInterviews = async () => {
        try {
            const { data } = await apiClient.get<Interview[]>('/api/interviews');
            const interviews = data || [];

            setActiveInterviews(interviews.filter((i: Interview) => i.status === 'active'));
            setCompletedInterviews(interviews.filter((i: Interview) => i.status === 'completed'));
        } catch (error) {
            console.error('Erro ao carregar entrevistas:', error);
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">Pesquisas - Agente de Entrevistas</h1>
                    <p className="text-muted-foreground">Dashboard de Entrevistas e Análises de IA</p>
                </div>
                <Link to="/dashboard/admin/agents/pesquisas/config">
                    <button className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-md">
                        <Settings className="h-4 w-4" />
                        Configuração Técnica
                    </button>
                </Link>
            </div>

            <Tabs defaultValue="active">
                <TabsList>
                    <TabsTrigger value="active">Entrevistas Ativas ({activeInterviews.length})</TabsTrigger>
                    <TabsTrigger value="completed">Completadas ({completedInterviews.length})</TabsTrigger>
                    <TabsTrigger value="reports">Relatórios IA</TabsTrigger>
                </TabsList>

                <TabsContent value="active" className="space-y-4">
                    {activeInterviews.map(interview => (
                        <Card key={interview.id}>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <FileText className="h-5 w-5" />
                                    {interview.title}
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex justify-between">
                                    <span className="text-sm">{interview.responses_count} respostas</span>
                                    <span className="text-sm text-muted-foreground">
                                        {new Date(interview.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </TabsContent>

                <TabsContent value="completed">
                    {completedInterviews.map(interview => (
                        <Card key={interview.id} className="mb-4">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <BarChart3 className="h-5 w-5 text-green-600" />
                                    {interview.title}
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                {interview.ai_insights && (
                                    <div className="p-4 bg-blue-50 rounded-md">
                                        <p className="text-sm font-semibold mb-2">Insights da IA:</p>
                                        <p className="text-sm">{interview.ai_insights}</p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    ))}
                </TabsContent>

                <TabsContent value="reports">
                    <Card>
                        <CardContent className="p-6">
                            <p className="text-center text-muted-foreground">Relatórios de análise de IA</p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default PesquisasInterface;
