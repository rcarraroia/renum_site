import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders, FileText, MessageSquare, LayoutDashboard, Terminal, Save, ArrowLeft, Server, BarChart } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link, useParams } from 'react-router-dom';

// Configuration Sub-Tabs (Reused from RenusConfigPage)
import InstructionsTab from '@/components/renus-config/InstructionsTab';
import ToolsTab from '@/components/renus-config/ToolsTab';
import KnowledgeTab from '@/components/renus-config/KnowledgeTab';
import TriggersTab from '@/components/renus-config/TriggersTab';
import GuardrailsTab from '@/components/renus-config/GuardrailsTab';
import { SubAgentsTab } from '@/components/renus-config/SubAgentsTab';
import { AdvancedTab } from '@/components/renus-config/AdvancedTab';

// Agent Specific Tabs
import AgentIntegrationsTab from '@/components/agents/AgentIntegrationsTab';
import ApiWebhooksTab from '@/components/agents/ApiWebhooksTab';
import AgentOverviewTab from '@/components/agents/AgentOverviewTab';
import AgentInstancesTab from '@/components/agents/AgentInstancesTab';
import AgentMetricsTab from '@/components/agents/AgentMetricsTab';
import AgentLogsTab from '@/components/agents/AgentLogsTab';

const MOCK_AGENT_DATA = {
    id: 'slim-vendas',
    name: 'Agente de Vendas Slim',
    status: 'Ativo',
    lastPublished: '2025-01-20 14:35',
    version: 'V1.3',
};

const AgentDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeMainTab, setActiveMainTab] = useState('overview');
  const [activeConfigTab, setActiveConfigTab] = useState('instructions');
  const [isSaving, setIsSaving] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(true); // Mock state

  const agent = MOCK_AGENT_DATA; // Use mock data for now

  const mainTabs = [
    { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: AgentOverviewTab },
    { value: 'config', label: 'Configuração', icon: Settings, component: null }, // Special tab for sub-tabs
    { value: 'instances', label: 'Instâncias', icon: Server, component: AgentInstancesTab },
    { value: 'metrics', label: 'Métricas', icon: BarChart, component: AgentMetricsTab },
    { value: 'logs', label: 'Logs', icon: Terminal, component: AgentLogsTab },
  ];

  const configSubTabs = [
    { value: 'instructions', label: 'Instruções', icon: Settings, component: InstructionsTab },
    { value: 'tools', label: 'Ferramentas', icon: Wrench, component: ToolsTab },
    { value: 'integrations', label: 'Integrações', icon: RefreshCw, component: AgentIntegrationsTab },
    { value: 'knowledge', label: 'Conhecimento', icon: BookOpen, component: KnowledgeTab },
    { value: 'triggers', label: 'Gatilhos', icon: Clock, component: TriggersTab },
    { value: 'guardrails', label: 'Guardrails', icon: Shield, component: GuardrailsTab },
    { value: 'subagents', label: 'Sub-Agentes', icon: Users, component: SubAgentsTab },
    { value: 'advanced', label: 'Avançado', icon: Sliders, component: AdvancedTab },
    { value: 'api-webhooks', label: 'API & Webhooks', icon: FileText, component: ApiWebhooksTab },
  ];

  const handleSaveAndPublish = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      setHasUnsavedChanges(false);
      toast.success(`Configuração do agente ${agent.name} publicada com sucesso!`);
    }, 1500);
  };

  const ActiveMainComponent = useMemo(() => {
    const tab = mainTabs.find(t => t.value === activeMainTab);
    return tab?.component;
  }, [activeMainTab]);

  const ActiveConfigComponent = useMemo(() => {
    const tab = configSubTabs.find(t => t.value === activeConfigTab);
    return tab?.component;
  }, [activeConfigTab]);

  return (
    <DashboardLayout>
      <div className="flex items-center mb-4">
        <Link to="/dashboard/admin/renus-config" className="text-muted-foreground hover:text-primary flex items-center text-sm">
            <ArrowLeft className="h-4 w-4 mr-2" /> Voltar aos Agentes
        </Link>
      </div>
      
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          {agent.name}
        </h2>
        <div className="flex items-center space-x-4">
            <Badge variant="secondary" className={cn(
                "transition-colors",
                agent.status === 'Ativo' ? "bg-green-500 text-white" : "bg-red-500 text-white"
            )}>
                {agent.status} | {agent.version}
            </Badge>
            {activeMainTab === 'config' && (
                <Button 
                    onClick={handleSaveAndPublish} 
                    disabled={isSaving || !hasUnsavedChanges} 
                    className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
                >
                    <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Publicando...' : 'Salvar e Publicar'}
                </Button>
            )}
        </div>
      </div>

      {/* Main Tabs */}
      <Tabs value={activeMainTab} onValueChange={setActiveMainTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
          {mainTabs.map(tab => (
            <TabsTrigger 
              key={tab.value} 
              value={tab.value} 
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white data-[state=active]:shadow-md transition-all",
                activeMainTab === tab.value && 'bg-[#FF6B35] text-white'
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {/* Tab Content: Configuration (Nested Tabs) */}
        <TabsContent value="config" className="mt-6">
            <Card>
                <CardHeader>
                    <CardTitle className="text-xl">Configuração Detalhada do Agente</CardTitle>
                    <p className="text-sm text-muted-foreground">Ajuste as instruções, ferramentas e políticas de segurança específicas para este agente.</p>
                </CardHeader>
                <CardContent>
                    <Tabs value={activeConfigTab} onValueChange={setActiveConfigTab} className="w-full">
                        <TabsList className="grid w-full grid-cols-3 md:grid-cols-9 h-auto p-1 bg-gray-100 dark:bg-gray-800">
                            {configSubTabs.map(tab => (
                                <TabsTrigger 
                                    key={tab.value} 
                                    value={tab.value} 
                                    className={cn(
                                        "flex items-center space-x-1 text-xs md:text-sm data-[state=active]:bg-[#0ca7d2] data-[state=active]:text-white transition-all"
                                    )}
                                >
                                    <tab.icon className="h-4 w-4" />
                                    <span className="hidden lg:inline">{tab.label}</span>
                                </TabsTrigger>
                            ))}
                        </TabsList>

                        {configSubTabs.map(tab => (
                            <TabsContent key={tab.value} value={tab.value} className="mt-6">
                                <tab.component />
                            </TabsContent>
                        ))}
                    </Tabs>
                </CardContent>
            </Card>
        </TabsContent>

        {/* Other Main Tab Contents */}
        {mainTabs.filter(t => t.value !== 'config').map(tab => (
            <TabsContent key={tab.value} value={tab.value} className="mt-6">
                {tab.component && <tab.component />}
            </TabsContent>
        ))}
      </Tabs>
    </DashboardLayout>
  );
};

export default AgentDetailsPage;