import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import IntegrationsTab from '@/components/agents/config/IntegrationsTab';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw, Zap, Clock, Search, Wifi, ShieldCheck, Activity, Globe } from 'lucide-react';
import { integrationService } from '@/services/integrationService';
import { cn } from '@/lib/utils';

const AdminIntegrationsPage: React.FC = () => {
    const [stats, setStats] = useState({
        total: 0,
        active: 0,
        errors: 0
    });
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        try {
            setIsLoading(true);
            const data = await integrationService.getIntegrationsStatus();
            setStats({
                total: data.length,
                active: data.filter(i => i.status === 'active').length,
                errors: data.filter(i => i.status === 'error').length
            });
        } catch (error) {
            console.error("Erro ao carregar estatísticas do radar:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <DashboardLayout>
            <div className="space-y-6">
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-3xl font-bold flex items-center tracking-tight">
                            <Wifi className="h-8 w-8 mr-3 text-[#4e4ea8] animate-pulse" />
                            Hub de Integrações
                        </h2>
                        <p className="text-muted-foreground mt-1">Gerencie e monitore todas as conexões externas da rede RENUM.</p>
                    </div>
                    <div className="flex items-center space-x-3">
                        <Button variant="outline" size="sm" onClick={loadStats} disabled={isLoading}>
                            <RefreshCw className={cn("h-4 w-4 mr-2", isLoading && "animate-spin")} />
                            Atualizar Radar
                        </Button>
                        <Badge className="bg-[#4e4ea8] text-white px-3 py-1">Controle Global</Badge>
                    </div>
                </div>

                {/* Radar Status Bar */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Card className="border-l-4 border-l-blue-500 shadow-sm hover:shadow-md transition-shadow">
                        <CardHeader className="pb-2 p-4">
                            <CardTitle className="text-xs font-semibold text-muted-foreground uppercase flex items-center">
                                <Activity className="h-3 w-3 mr-2" /> Total de Conexões
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 pt-0">
                            <div className="text-3xl font-bold">{stats.total}</div>
                        </CardContent>
                    </Card>

                    <Card className="border-l-4 border-l-green-500 shadow-sm hover:shadow-md transition-shadow">
                        <CardHeader className="pb-2 p-4">
                            <CardTitle className="text-xs font-semibold text-muted-foreground uppercase flex items-center text-green-600">
                                <ShieldCheck className="h-3 w-3 mr-2" /> Sistemas Online
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 pt-0">
                            <div className="text-3xl font-bold text-green-600">{stats.active}</div>
                        </CardContent>
                    </Card>

                    <Card className="border-l-4 border-l-red-500 shadow-sm hover:shadow-md transition-shadow">
                        <CardHeader className="pb-2 p-4">
                            <CardTitle className="text-xs font-semibold text-muted-foreground uppercase flex items-center text-red-600">
                                <Search className="h-3 w-3 mr-2" /> Alertas de Falha
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 pt-0">
                            <div className="text-3xl font-bold text-red-600">{stats.errors}</div>
                        </CardContent>
                    </Card>

                    <Card className="border-l-4 border-l-[#FF6B35] shadow-sm hover:shadow-md transition-shadow">
                        <CardHeader className="pb-2 p-4">
                            <CardTitle className="text-xs font-semibold text-muted-foreground uppercase flex items-center text-[#FF6B35]">
                                <Globe className="h-3 w-3 mr-2" /> Webhooks de Saída
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 pt-0">
                            <div className="text-3xl font-bold text-[#FF6B35]">Ativo</div>
                        </CardContent>
                    </Card>
                </div>

                <div className="bg-white dark:bg-gray-900 rounded-xl border shadow-sm overflow-hidden">
                    <div className="p-4 border-b bg-gray-50/50 dark:bg-gray-800/50 flex items-center justify-between">
                        <h3 className="font-semibold flex items-center">
                            <Zap className="h-5 w-5 mr-2 text-yellow-500" />
                            Configurações Globais (Herança para Agentes)
                        </h3>
                    </div>
                    <div className="p-6">
                        <IntegrationsTab globalMode={true} />
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
};

export default AdminIntegrationsPage;
