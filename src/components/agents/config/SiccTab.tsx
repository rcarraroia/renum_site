import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { Brain, Activity, TrendingUp, ExternalLink, Zap } from 'lucide-react';
import { toast } from 'sonner';
import { Link } from 'react-router-dom';
import { siccService } from '@/services/siccService';
import agentService from '@/services/agentService';

const SiccTab: React.FC = () => {
    const [agent, setAgent] = useState<any>(null);
    const [stats, setStats] = useState<any>(null);
    const [settings, setSettings] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setIsLoading(true);
            // 1. Get Agent to know ID
            let agentData;
            try {
                agentData = await agentService.getAgentBySlug('renus');
            } catch {
                const agents = await agentService.listAgents();
                agentData = agents.find((a: any) => a.slug === 'renus' || a.role === 'system_orchestrator');
            }

            if (agentData) {
                setAgent(agentData);
                // 2. Get SICC Data
                const [statsData, settingsData] = await Promise.all([
                    siccService.getEvolutionStats(agentData.id),
                    siccService.getSettings(agentData.id)
                ]);
                setStats(statsData);
                setSettings(settingsData);
            } else {
                toast.error('Agente Renus não encontrado');
            }
        } catch (error) {
            console.error(error);
            toast.error('Erro ao carregar dados do SICC');
        } finally {
            setIsLoading(false);
        }
    };

    const handleToggleSicc = async (enabled: boolean) => {
        if (!agent) return;
        try {
            // Update Agent Config (Master Switch)
            const updatedConfig = {
                ...agent.config,
                sicc: {
                    ...agent.config?.sicc,
                    enabled: enabled
                }
            };
            await agentService.updateAgent(agent.id, { config: updatedConfig });
            setAgent({ ...agent, config: updatedConfig });

            // Also update SICC Settings
            if (settings) {
                const newSettings = { ...settings, learning_enabled: enabled };
                await siccService.updateSettings(agent.id, newSettings);
                setSettings(newSettings);
            }

            toast.success(`SICC ${enabled ? 'Ativado' : 'Desativado'} com sucesso!`);
        } catch (error) {
            toast.error('Erro ao atualizar status do SICC');
        }
    };

    const handleSaveSettings = async () => {
        if (!agent || !settings) return;
        setIsSaving(true);
        try {
            await siccService.updateSettings(agent.id, settings);
            toast.success('Configurações de Inteligência salvas!');
        } catch (error) {
            toast.error('Erro ao salvar configurações');
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) return <div className="p-8 text-center text-muted-foreground">Carregando inteligência...</div>;
    if (!agent) return <div className="p-8 text-center text-red-500">Agente não encontrado.</div>;

    const siccEnabled = agent.config?.sicc?.enabled ?? true; // Default true for demo

    return (
        <div className="space-y-6">
            {/* Master Toggle Banner */}
            <Card className={`border-l-4 ${siccEnabled ? 'border-l-purple-600' : 'border-l-gray-300'}`}>
                <CardContent className="flex items-center justify-between p-6">
                    <div className="flex items-center space-x-4">
                        <div className={`p-3 rounded-full ${siccEnabled ? 'bg-purple-100' : 'bg-gray-100'}`}>
                            <Brain className={`h-6 w-6 ${siccEnabled ? 'text-purple-600' : 'text-gray-400'}`} />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                                Sistema de Inteligência e Contexto Contínuo (SICC)
                            </h3>
                            <p className="text-sm text-muted-foreground">
                                Permite que o Renus aprenda com conversas, detecte padrões e evolua autonomamente.
                            </p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-muted-foreground">Status:</span>
                        <Switch
                            checked={siccEnabled}
                            onCheckedChange={handleToggleSicc}
                        />
                        <Badge variant={siccEnabled ? 'default' : 'secondary'} className={siccEnabled ? 'bg-purple-600' : ''}>
                            {siccEnabled ? 'ATIVO' : 'PAUSADO'}
                        </Badge>
                    </div>
                </CardContent>
            </Card>

            {/* Stats Overview */}
            <div className="grid md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Memórias Totais</CardTitle>
                        <Brain className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.total_memories || 0}</div>
                        <p className="text-xs text-muted-foreground flex items-center mt-1">
                            <TrendingUp className="h-3 w-3 mr-1 text-green-500" /> +{stats?.total_memories_change || 0}% este mês
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Taxa de Auto-Aprovação</CardTitle>
                        <Activity className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.auto_approved_rate || 0}%</div>
                        <p className="text-xs text-muted-foreground flex items-center mt-1">
                            Confiança do sistema
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Novos Padrões</CardTitle>
                        <Zap className="h-4 w-4 text-amber-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.new_patterns || 0}</div>
                        <p className="text-xs text-muted-foreground flex items-center mt-1">
                            Detectados na última semana
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Basic Settings */}
            <div className="grid md:grid-cols-3 gap-6">
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Configurações Rápidas de Aprendizado</CardTitle>
                        <CardDescription>Ajustes finos do comportamento evolutivo.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        {settings && (
                            <>
                                <div className="flex items-center justify-between">
                                    <div className="space-y-0.5">
                                        <label className="text-base font-medium">Auto-Aprovação</label>
                                        <p className="text-sm text-muted-foreground">Permitir que o sistema aprove memórias com alta confiança sem revisão humana.</p>
                                    </div>
                                    <Switch
                                        checked={settings.auto_approval_threshold < 1.0} // Simplification: if threshold < 1, it implies auto approval is possible
                                        onCheckedChange={(checked) => setSettings({ ...settings, auto_approval_threshold: checked ? 0.8 : 1.0 })}
                                    />
                                </div>
                                <div className="space-y-4">
                                    <div className="flex justify-between">
                                        <label className="text-base font-medium">Limite de Confiança ({Math.round((settings.auto_approval_threshold || 0.8) * 100)}%)</label>
                                    </div>
                                    <Slider
                                        value={[(settings.auto_approval_threshold || 0.8) * 100]}
                                        min={50}
                                        max={100}
                                        step={5}
                                        onValueChange={(val) => setSettings({ ...settings, auto_approval_threshold: val[0] / 100 })}
                                    />
                                </div>
                                <div className="flex justify-end pt-4">
                                    <Button onClick={handleSaveSettings} disabled={isSaving}>
                                        {isSaving ? 'Salvando...' : 'Aplicar Alterações'}
                                    </Button>
                                </div>
                            </>
                        )}
                    </CardContent>
                </Card>

                {/* Deep Link to Full Dashboard */}
                <Card className="bg-gradient-to-br from-purple-900 to-indigo-900 text-white border-none">
                    <CardHeader>
                        <CardTitle className="text-white">Painel Avançado SICC</CardTitle>
                        <CardDescription className="text-purple-200">
                            Acesse o dashboard completo para gerenciar memórias individuais, visualizar gráficos de evolução e ajustar a arquitetura neural.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button className="w-full bg-white text-purple-900 hover:bg-gray-100" asChild>
                            <Link to="/intelligence/evolution">
                                Abrir Dashboard SICC <ExternalLink className="ml-2 h-4 w-4" />
                            </Link>
                        </Button>
                    </CardContent>
                </Card>
            </div>

        </div>
    );
};

export default SiccTab;
