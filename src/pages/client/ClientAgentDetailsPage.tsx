
import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Settings, MessageSquare, LayoutDashboard, Terminal, Save, ArrowLeft, BarChart, Pause, Play, Download, MoreVertical, Trash2, Users } from 'lucide-react';
import { toast } from 'sonner';
import PreviewChat from '@/components/agents/PreviewChat';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Loader2 } from 'lucide-react';

// Services
import { clientDashboardService } from '@/services/clientDashboardService';
import { agentService } from '@/services/agentService'; // For direct types/helpers

// Configuration Panel
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel';

// Agent Specific Tabs (Reused from Admin)
import AgentOverviewTab from '@/components/agents/AgentOverviewTab';
import AgentUsersTab from '@/components/agents/AgentUsersTab';
import AgentMetricsTab from '@/components/agents/AgentMetricsTab';
import AgentLogsTab from '@/components/agents/AgentLogsTab';
import { Agent } from '@/types/agent';
import { useAuth } from '@/context/AuthContext';

const ClientAgentDetailsPage: React.FC = () => {
    const { slug } = useParams<{ slug: string }>();
    const navigate = useNavigate();
    const { user } = useAuth(); // Get current user context

    const [agent, setAgent] = useState<Agent | null>(null);
    const [loading, setLoading] = useState(true);
    const [activeMainTab, setActiveMainTab] = useState('overview');
    const [isSaving, setIsSaving] = useState(false);
    // In a real app, track dirty state
    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    useEffect(() => {
        const fetchAgent = async () => {
            if (!slug) return;
            try {
                setLoading(true);
                // Use client service which uses agentService internally but in future could enforce strict client validation
                const data = await clientDashboardService.getAgentBySlug(slug);
                if (data) {
                    setAgent(data);
                } else {
                    toast.error('Agente não encontrado.');
                    navigate('/dashboard/client/agents');
                }
            } catch (error) {
                console.error("Error fetching agent:", error);
                toast.error('Erro ao carregar detalhes do agente.');
                // In mock mode, prevent redirect loop, but in prod redirect
                // navigate('/dashboard/client/agents'); 
            } finally {
                setLoading(false);
            }
        };

        fetchAgent();
    }, [slug, navigate]);

    const handleSaveAndPublish = async () => {
        if (!agent) return;
        setIsSaving(true);
        try {
            // Mock save
            await new Promise(resolve => setTimeout(resolve, 1500));
            setHasUnsavedChanges(false);
            toast.success(`Configuração do agente ${agent.name} salva com sucesso!`);
        } catch (err) {
            toast.error('Erro ao salvar configurações.');
        } finally {
            setIsSaving(false);
        }
    };

    const handleToggleStatus = async () => {
        if (!agent) return;
        try {
            const newStatus = agent.status === 'ativo' ? 'pausado' : 'ativo';
            // In real app: await agentService.changeAgentStatus(agent.id, newStatus);
            // Updating local state for optimistic UI or re-fetching
            setAgent({ ...agent, status: newStatus as any });
            toast.success(`Agente ${agent.name} ${newStatus === 'ativo' ? 'ativado' : 'pausado'}.`);
        } catch (err) {
            toast.error('Erro ao alterar status.');
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'ativo': return 'bg-green-600';
            case 'pausado': return 'bg-yellow-600';
            case 'inativo': return 'bg-gray-500';
            case 'erro': return 'bg-red-600';
            default: return 'bg-gray-500';
        }
    };

    if (loading) {
        return (
            <DashboardLayout>
                <div className="flex justify-center items-center h-screen">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
            </DashboardLayout>
        );
    }

    if (!agent) return null;

    // Define Tabs based on Plan/Type
    // E.g. Users tab only for B2B
    const isB2B = agent.type === 'b2b_empresa';
    // Check if client has addons for SubAgents? (Mock logic for now)
    const hasSubAgentsAddon = false; // user?.plan.addons.includes('subagents')

    const mainTabs = [
        { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: AgentOverviewTab },
        { value: 'config', label: 'Configuração', icon: Settings, component: ConfigRenusPanel },
        { value: 'chat', label: 'Chat de Teste', icon: MessageSquare, component: PreviewChat },
        // Conditional Tabs
        ...(isB2B ? [{ value: 'users', label: 'Usuários', icon: Users, component: AgentUsersTab }] : []),
        { value: 'metrics', label: 'Métricas', icon: BarChart, component: AgentMetricsTab },
        { value: 'logs', label: 'Logs', icon: Terminal, component: AgentLogsTab },
    ];

    return (
        <DashboardLayout>
            <div className="flex items-center mb-4">
                <Link to="/dashboard/client/agents" className="text-muted-foreground hover:text-primary flex items-center text-sm">
                    <ArrowLeft className="h-4 w-4 mr-2" /> Voltar para Meus Agentes
                </Link>
            </div>

            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                <div>
                    <h2 className="text-3xl font-bold flex items-center">
                        <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
                        {agent.name}
                    </h2>
                    <p className="text-muted-foreground ml-10">
                        {agent.domain || 'Sem domínio configurado'} • {agent.model}
                    </p>
                </div>

                <div className="flex items-center space-x-3 flex-wrap gap-y-2">
                    <Badge className={cn("transition-colors text-white", getStatusColor(agent.status))}>
                        {agent.status.toUpperCase()} | {agent.version || 'V1.0'}
                    </Badge>

                    <Button
                        variant="outline"
                        size="sm"
                        onClick={handleToggleStatus}
                        className={cn(agent.status === 'ativo' ? 'text-red-500 border-red-500 hover:bg-red-50' : 'text-green-500 border-green-500 hover:bg-green-50')}
                    >
                        {agent.status === 'ativo' ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                        {agent.status === 'ativo' ? 'Pausar' : 'Ativar'}
                    </Button>

                    {/* Quick Config Actions */}
                    {activeMainTab === 'config' && (
                        <Button
                            onClick={handleSaveAndPublish}
                            disabled={isSaving}
                            className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
                        >
                            <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar'}
                        </Button>
                    )}
                </div>
            </div>

            <Tabs value={activeMainTab} onValueChange={setActiveMainTab} className="w-full">
                <TabsList className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 h-auto p-1 bg-gray-100 dark:bg-gray-800 mb-6">
                    {mainTabs.map(tab => (
                        <TabsTrigger
                            key={tab.value}
                            value={tab.value}
                            className="flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white transition-all"
                        >
                            <tab.icon className="h-4 w-4" />
                            <span className="hidden sm:inline">{tab.label}</span>
                        </TabsTrigger>
                    ))}
                </TabsList>

                <TabsContent value="overview">
                    <AgentOverviewTab agent={agent} />
                </TabsContent>

                <TabsContent value="config">
                    <Card>
                        <CardHeader>
                            <CardTitle>Configuração do Agente</CardTitle>
                            <p className="text-sm text-muted-foreground">
                                Personalize o comportamento e as integrações do seu assistente.
                            </p>
                        </CardHeader>
                        <CardContent>
                            <ConfigRenusPanel
                                isGlobalConfig={false}
                                clientMode={true}
                                hasAddons={hasSubAgentsAddon ? ['subagents'] : []}
                            />
                        </CardContent>
                    </Card>
                </TabsContent>

                {isB2B && (
                    <TabsContent value="users">
                        <AgentUsersTab agentType={agent.type} />
                    </TabsContent>
                )}

                <TabsContent value="chat">
                    <Card>
                        <CardHeader>
                            <CardTitle>Chat de Teste</CardTitle>
                        </CardHeader>
                        <CardContent className="h-[600px] p-0">
                            <PreviewChat
                                agentName={agent.name}
                                agentSlug={agent.slug || ''}
                                systemPrompt={agent.system_prompt}
                                useRealAgent={true}
                            />
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="metrics">
                    <AgentMetricsTab />
                </TabsContent>

                <TabsContent value="logs">
                    <AgentLogsTab />
                </TabsContent>

            </Tabs>
        </DashboardLayout>
    );
};

export default ClientAgentDetailsPage;
