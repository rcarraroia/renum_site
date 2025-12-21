import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Loader2, Mail, MessageCircle, Database, Settings, Wrench } from 'lucide-react';
import agentService from '@/services/agentService';
import { toolService, RegistryTool } from '@/services/toolService';

// Icon mapper
const IconMap: Record<string, any> = {
  Mail,
  MessageCircle,
  Database,
  Settings,
  Wrench
};

interface ToolsTabProps {
  agentId?: string;
  clientMode?: boolean;
}

const ToolsTab: React.FC<ToolsTabProps> = ({ agentId: propAgentId }) => {
  const [agent, setAgent] = useState<any>(null);
  const [registryTools, setRegistryTools] = useState<RegistryTool[]>([]);
  const [enabledTools, setEnabledTools] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);

      // Load Agent
      let agentData;
      if (propAgentId) {
        agentData = await agentService.getAgent(propAgentId);
      } else {
        try {
          agentData = await agentService.getAgentBySlug('renus');
        } catch {
          const agents = await agentService.listAgents();
          agentData = agents.find((a: any) => a.slug === 'renus' || a.role === 'system_orchestrator');
        }
      }

      if (agentData) {
        setAgent(agentData);
        // Load config.tools, default to empty list
        setEnabledTools(agentData.config?.tools || []);
      }

      // Load Registry Tools
      const tools = await toolService.getRegistryTools();
      setRegistryTools(tools);

    } catch (error) {
      console.error(error);
      toast.error("Erro ao carregar ferramentas.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleTool = async (toolKey: string, enabled: boolean) => {
    if (!agent) return;

    // Optimistic update
    const newEnabledList = enabled
      ? [...enabledTools, toolKey]
      : enabledTools.filter(k => k !== toolKey);

    setEnabledTools(newEnabledList);

    try {
      setIsSaving(true);
      const updatedConfig = {
        ...agent.config,
        tools: newEnabledList
      };

      await agentService.updateAgent(agent.id, { config: updatedConfig });
      setAgent({ ...agent, config: updatedConfig });
      toast.success(`Ferramenta ${enabled ? 'ativada' : 'desativada'} com sucesso.`);
    } catch (error) {
      // Revert on error
      setEnabledTools(enabledTools);
      toast.error("Erro ao salvar alteração.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <div className="flex justify-center p-8"><Loader2 className="animate-spin h-8 w-8 text-primary" /></div>;
  }

  if (!agent) {
    return <div className="text-red-500 p-4">Agente não encontrado.</div>;
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wrench className="h-5 w-5 text-primary" />
            Ferramentas Nativas
          </CardTitle>
          <CardDescription>
            Habilite as capacidades funcionais que o Renus pode utilizar.
            Essas ferramentas são executadas diretamente pelo backend seguro.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {registryTools.map(tool => {
            const Icon = IconMap[tool.icon] || Wrench;
            const isEnabled = enabledTools.includes(tool.key);

            return (
              <div key={tool.key} className={cn(
                "flex items-center justify-between p-4 border rounded-lg transition-all",
                isEnabled ? "bg-primary/5 border-primary/20" : "bg-card hover:bg-accent/50"
              )}>
                <div className="flex items-start gap-4">
                  <div className={cn("p-2 rounded-lg", isEnabled ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground")}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-base">{tool.name}</h4>
                    <p className="text-sm text-muted-foreground">{tool.description}</p>
                    <div className="flex gap-2 mt-2">
                      <Badge variant="outline" className="text-xs font-mono">{tool.key}</Badge>
                      {isEnabled && <Badge className="bg-green-500/15 text-green-700 hover:bg-green-500/25 border-green-200">Ativo</Badge>}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <Switch
                    checked={isEnabled}
                    onCheckedChange={(checked) => handleToggleTool(tool.key, checked)}
                    disabled={isSaving}
                  />
                </div>
              </div>
            );
          })}

          {registryTools.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              Nenhuma ferramenta registrada no backend.
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="opacity-70 grayscale pointer-events-none border-dashed">
        <CardHeader>
          <CardTitle>Ferramentas Personalizadas (Em Breve)</CardTitle>
          <CardDescription>Criação de ferramentas via API ou scripts Python personalizados.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">Disponível em futuras atualizações (Fase 10).</div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ToolsTab;