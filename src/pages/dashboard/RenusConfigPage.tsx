import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Save, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel'; // Using the new consolidated panel
import agentService from '@/services/agentService';
import { Agent } from '@/types/agent';
import { cn } from '@/lib/utils';

const RenusConfigPage: React.FC = () => {
  const [isSaving, setIsSaving] = useState(false);
  const [isUnsaved, setIsUnsaved] = useState(false);
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Carregar configuração do Agente Orquestrador
  const loadConfig = async () => {
    try {
      setLoading(true);
      setError(null);
      // Busca o agente orquestrador do sistema
      const agents = await agentService.listAgents({ role: 'system_orchestrator' });

      if (agents.length > 0) {
        // Precisamos dos detalhes completos, então buscamos pelo ID
        // listAgents retorna AgentListItem, getAgent retorna Agent
        const fullAgent = await agentService.getAgent(agents[0].id);
        setAgent(fullAgent);
      } else {
        setError('Agente Renus (Orquestrador) não encontrado no sistema.');
        toast.error('Agente Renus não configurado no Backend.');
      }

    } catch (err) {
      setError('Erro ao carregar configuração. Tente novamente.');
      console.error('Erro ao carregar config:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  const handleSaveAll = async () => {
    if (!agent) return;

    try {
      setIsSaving(true);
      // Aqui, idealmente, pegaríamos o estado atual do ConfigRenusPanel
      // Como o panel ainda não expõe onChange, vamos apenas simular o update do agente
      // para garantir a conexão com o endpoint /agents/{id}
      // TODO: Conectar estado dos filhos (ConfigRenusPanel) ao estado pai (agent.config)

      await agentService.updateAgent(agent.id, {
        config: agent.config || {}, // Preserva ou atualiza config JSONB
        // is_active: agent.is_active // Se quiséssemos alterar status
      });

      setIsUnsaved(false);
      toast.success("Configuração do Renus sincronizada com o Agente Real!");
    } catch (err) {
      toast.error('Erro ao salvar configuração.');
      console.error('Erro ao salvar config:', err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          Configuração Global do Renus
        </h2>
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className={cn(
            "transition-colors",
            isUnsaved ? "bg-yellow-500 text-white" : "bg-green-500 text-white"
          )}>
            {isUnsaved ? 'Alterações Não Salvas' : 'Configuração Publicada'}
          </Badge>
          <Button
            onClick={handleSaveAll}
            disabled={isSaving}
            className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
          >
            <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Publicando...' : 'Salvar e Publicar'}
          </Button>
        </div>
      </div>

      {/* Status Bar - Moved from Sidebar to Top for better space utilization */}
      <Card className="mb-6 bg-gray-50/50 dark:bg-gray-800/50 border-dashed">
        <CardContent className="p-4 flex flex-wrap gap-4 items-center justify-between text-sm">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">Versão:</span>
              <Badge variant="outline" className="font-mono">V1.3</Badge>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">Última Publicação:</span>
              <span className="font-medium">2 min atrás</span>
            </div>
          </div>

          <div className="h-4 w-px bg-gray-300 dark:bg-gray-700 hidden md:block" />

          <div className="flex items-center gap-6 flex-wrap">
            <div className="flex items-center gap-2" title="Ferramentas Ativas">
              <Wrench className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Ferramentas:</span>
              <span className="font-semibold text-green-600 dark:text-green-400">2/3</span>
            </div>
            <div className="flex items-center gap-2" title="Integrações Conectadas">
              <RefreshCw className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Integrações:</span>
              <span className="font-semibold text-yellow-600 dark:text-yellow-400">3/4</span>
            </div>
            <div className="flex items-center gap-2" title="Gatilhos Ativos">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Gatilhos:</span>
              <span className="font-semibold text-green-600 dark:text-green-400">2</span>
            </div>
            <div className="flex items-center gap-2" title="Guardrails Ativos">
              <Shield className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Guardrails:</span>
              <span className="font-semibold text-green-600 dark:text-green-400">3/6</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Configuration Tabs - Now Full Width */}
      <div className="w-full">
        <ConfigRenusPanel 
          agentId={agent?.id} 
          isGlobalConfig={true}
          hasAddons={['subagents']}
        />
      </div>
    </DashboardLayout>
  );
};

export default RenusConfigPage;