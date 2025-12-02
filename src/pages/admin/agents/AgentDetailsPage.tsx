import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Settings, MessageSquare, LayoutDashboard, Terminal, Save, ArrowLeft, Server, BarChart, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link, useParams } from 'react-router-dom';
import { mockAgents } from '@/mocks/agents.mock';

// Configuration Panel
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel';

// Agent Specific Tabs
import AgentOverviewTab from '@/components/agents/AgentOverviewTab';
import AgentInstancesTab from '@/components/agents/InstanceList'; // Using the new InstanceList
import AgentMetricsTab from '@/components/agents/AgentMetricsTab';
import AgentLogsTab from '@/components/agents/AgentLogsTab';
import ApiWebhooksTab from '@/components/agents/ApiWebhooksTab'; // Still needed for the main tabs

const AgentDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeMainTab, setActiveMainTab] = useState('overview');
  const [isSaving, setIsSaving] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(true); // Mock state

  const agent = mockAgents.find(a => a.id === id) || {
    id: 'mock-100',
    name: 'Novo Agente (Mock)',
    status: 'inativo',
    version: 'V1.0', // Added version to mock fallback
    lastPublished: 'N/A'
  };

  const mainTabs = [
    { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: AgentOverviewTab },
    { value: 'config', label: 'Configuração', icon: Settings, component: null }, // Special tab for sub-tabs
    { value: 'api-webhooks', label: 'API & Webhooks', icon: RefreshCw, component: ApiWebhooksTab },
    { value: 'instances', label: 'Instâncias', icon: Server, component: AgentInstancesTab },
    { value: 'metrics', label: 'Métricas', icon: BarChart, component: AgentMetricsTab },
    { value: 'logs', label: 'Logs', icon: Terminal, component: AgentLogsTab },
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

  return (
    <DashboardLayout>
      <div className="flex items-center mb-4">
        <Link to="/dashboard/admin/agents" className="text-muted-foreground hover:text-primary flex items-center text-sm">
            <ArrowLeft className="h-4 w-4 mr-2" /> Voltar à Lista de Agentes
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
                agent.status === 'ativo' ? "bg-green-500 text-white" : "bg-red-500 text-white"
            )}>
                {agent.status.toUpperCase()} | {agent.version}
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
        <TabsList className="grid w-full grid-cols-6 h-auto p-1 bg-gray-100 dark:bg-gray-800">
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
                    <ConfigRenusPanel isGlobalConfig={false} />
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