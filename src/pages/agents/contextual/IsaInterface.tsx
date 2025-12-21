/**
 * Task 24: ISA Contextual Interface - IMPLEMENTAÇÃO REAL
 * Dashboard de supervisão SICC e comandos executados
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Terminal, Activity, Shield, Settings, AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient } from '@/services/api';

interface SiccCommand {
    id: string;
    command: string;
    agent_id: string;
    executed_at: string;
    status: 'success' | 'error' | 'pending';
    result?: string;
}

interface SystemStatus {
    agents_monitored: number;
    commands_today: number;
    error_rate: number;
    sicc_active: boolean;
}

export const IsaInterface: React.FC = () => {
    const [commands, setCommands] = useState<SiccCommand[]>([]);
    const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);

    useEffect(() => {
        loadIsaData();
        const interval = setInterval(loadIsaData, 30000); // Refresh a cada 30s
        return () => clearInterval(interval);
    }, []);

    const loadIsaData = async () => {
        try {
            const { data: commandsData } = await apiClient.get<SiccCommand[]>('/api/sicc/commands', { limit: 50 });
            setCommands(commandsData || []);

            const { data: statusData } = await apiClient.get<SystemStatus>('/api/sicc/status');
            setSystemStatus(statusData);
        } catch (error) {
            console.error('Erro ao carregar dados ISA:', error);
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">ISA - Supervisora de Sistema</h1>
                    <p className="text-muted-foreground">Dashboard de Supervisão SICC e Auditoria</p>
                </div>
                <Link to="/dashboard/admin/agents/isa/config">
                    <button className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-md">
                        <Settings className="h-4 w-4" />
                        Configuração Técnica
                    </button>
                </Link>
            </div>

            {/* Status do Sistema */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">SICC Status</CardTitle>
                        <Shield className={systemStatus?.sicc_active ? "h-4 w-4 text-green-600" : "h-4 w-4 text-red-600"} />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {systemStatus?.sicc_active ? 'ATIVO' : 'INATIVO'}
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flexflex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Comandos Executados</CardTitle>
                        <Terminal className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{systemStatus?.commands_today || 0}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Taxa de Erro</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-yellow-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{systemStatus?.error_rate || 0}%</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Agentes Monitorados</CardTitle>
                        <Activity className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{systemStatus?.agents_monitored || 0}</div>
                    </CardContent>
                </Card>
            </div>

            {/* Comandos SICC */}
            <Tabs defaultValue="recent">
                <TabsList>
                    <TabsTrigger value="recent">Comandos Recentes</TabsTrigger>
                    <TabsTrigger value="errors">Erros</TabsTrigger>
                    <TabsTrigger value="audit">Auditoria</TabsTrigger>
                </TabsList>

                <TabsContent value="recent" className="space-y-4">
                    {commands.map(cmd => (
                        <Card key={cmd.id} className={cmd.status === 'error' ? 'border-red-200' : ''}>
                            <CardHeader>
                                <CardTitle className="text-base flex items-center gap-2">
                                    <Terminal className="h-4 w-4" />
                                    {cmd.command}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className={`px-2 py-1 rounded-full text-xs ${cmd.status === 'success' ? 'bg-green-100 text-green-800' :
                                        cmd.status === 'error' ? 'bg-red-100 text-red-800' :
                                            'bg-yellow-100 text-yellow-800'
                                        }`}>
                                        {cmd.status.toUpperCase()}
                                    </span>
                                    <span className="text-muted-foreground">
                                        {cmd.executed_at ? new Date(cmd.executed_at).toLocaleString() : 'Data indisponível'}
                                    </span>
                                </div>
                                {cmd.result && (
                                    <div className="p-2 bg-gray-50 rounded text-sm font-mono">
                                        {cmd.result}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    ))}
                </TabsContent>

                <TabsContent value="errors">
                    {commands.filter(c => c.status === 'error').length === 0 ? (
                        <Card>
                            <CardContent className="p-6 text-center text-green-600">
                                ✅ Nenhum erro registrado
                            </CardContent>
                        </Card>
                    ) : (
                        commands.filter(c => c.status === 'error').map(cmd => (
                            <Card key={cmd.id} className="mb-4 border-red-200">
                                <CardContent className="p-4">
                                    <p className="font-mono text-sm">{cmd.command}</p>
                                    <p className="text-red-600 text-sm mt-2">{cmd.result}</p>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </TabsContent>

                <TabsContent value="audit">
                    <Card>
                        <CardContent className="p-6">
                            <p className="text-center text-muted-foreground">
                                Logs de auditoria e compliance
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default IsaInterface;
