import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Zap, Info, DollarSign, Activity, Save, Loader2 } from 'lucide-react';
import { monitoringService, MonitoringStats } from '@/services/monitoringService';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import agentService from '@/services/agentService';

export const AdvancedTab = () => {
  const [agent, setAgent] = useState<any>(null);
  const [config, setConfig] = useState({
    provider: 'openai',
    model: 'gpt-4o',
    temperature: 0.7,
    maxTokens: 4000,
    apiKey: ''
  });

  const [monitoringStats, setMonitoringStats] = useState<MonitoringStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(false);
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
      try {
        agentData = await agentService.getAgentBySlug('renus');
      } catch {
        const agents = await agentService.listAgents();
        agentData = agents.find((a: any) => a.slug === 'renus' || a.role === 'system_orchestrator');
      }

      if (agentData) {
        setAgent(agentData);
        // Load config from agent
        setConfig({
          provider: agentData.config?.provider || 'openai',
          model: agentData.config?.model || 'gpt-4o',
          temperature: agentData.config?.temperature || 0.7,
          maxTokens: agentData.config?.max_tokens || 4000,
          apiKey: '' // Never show API key
        });
      }

      // Load monitoring stats
      setLoadingStats(true);
      try {
        const stats = await monitoringService.getStats();
        setMonitoringStats(stats);
      } catch (error) {
        console.error("Failed to load LangSmith stats", error);
      }
      setLoadingStats(false);
    } catch (error) {
      console.error("Error loading advanced config:", error);
      toast.error("Erro ao carregar configurações avançadas.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!agent) return;
    setIsSaving(true);
    try {
      const updatedConfig = {
        ...agent.config,
        provider: config.provider,
        model: config.model,
        temperature: config.temperature,
        max_tokens: config.maxTokens
      };

      await agentService.updateAgent(agent.id, { config: updatedConfig });
      setAgent({ ...agent, config: updatedConfig });
      toast.success("Configurações avançadas salvas!");
    } catch (error) {
      toast.error("Erro ao salvar configurações.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <div className="flex justify-center p-8"><Loader2 className="animate-spin h-8 w-8 text-primary" /></div>;
  }

  const modelOptions = [
    {
      value: 'anthropic/claude-sonnet-4',
      label: 'Claude Sonnet 4',
      tier: 'premium',
      cost: '$15/1M tokens'
    },
    {
      value: 'openai/gpt-4o',
      label: 'GPT-4o',
      tier: 'premium',
      cost: '$10/1M tokens'
    },
    {
      value: 'openai/gpt-4o-mini',
      label: 'GPT-4o Mini',
      tier: 'standard',
      cost: '$0.15/1M tokens'
    },
    {
      value: 'google/gemini-pro-1.5',
      label: 'Gemini Pro 1.5',
      tier: 'standard',
      cost: '$7/1M tokens'
    },
    {
      value: 'meta-llama/llama-3.1-8b-instruct:free',
      label: 'Llama 3.1 8B',
      tier: 'free',
      cost: 'FREE'
    },
    {
      value: 'meta-llama/llama-3.1-70b-instruct',
      label: 'Llama 3.1 70B',
      tier: 'standard',
      cost: '$0.80/1M tokens'
    }
  ];

  const selectedModelInfo = modelOptions.find(m => m.value === config.model);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-[#4e4ea8] flex items-center gap-2">
          <Zap className="h-6 w-6" />
          Configurações Avançadas
        </h2>
        <p className="text-muted-foreground mt-1">
          Configure o modelo de IA, parâmetros e integrações avançadas
        </p>
      </div>

      {/* Provider Section */}
      <Card>
        <CardHeader>
          <CardTitle>Provider de IA</CardTitle>
          <CardDescription>
            OpenRouter oferece acesso unificado a múltiplos modelos de IA
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Provider</Label>
            <Select value={config.provider} onValueChange={(value) => setConfig({ ...config, provider: value })}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="openrouter">
                  <div className="flex items-center gap-2">
                    <span>OpenRouter</span>
                    <Badge variant="secondary" className="text-xs">Recomendado</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="openai">OpenAI Direto</SelectItem>
                <SelectItem value="anthropic">Anthropic Direto</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>API Key do OpenRouter</Label>
            <Input
              type="password"
              placeholder="sk-or-v1-..."
              value={config.apiKey}
              onChange={(e) => setConfig({ ...config, apiKey: e.target.value })}
            />
            <p className="text-xs text-muted-foreground">
              Obtenha sua chave em: <a href="https://openrouter.ai/keys" target="_blank" className="text-[#0ca7d2] hover:underline">openrouter.ai/keys</a>
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Model Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Modelo Padrão (Agente Principal)</CardTitle>
          <CardDescription>
            Este modelo será usado pelo agente Renus principal. Sub-agentes podem ter modelos diferentes.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Modelo de IA</Label>
            <Select value={config.model} onValueChange={(value) => setConfig({ ...config, model: value })}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {modelOptions.map((model) => (
                  <SelectItem key={model.value} value={model.value}>
                    <div className="flex items-center justify-between w-full">
                      <span>{model.label}</span>
                      <div className="flex items-center gap-2 ml-4">
                        <Badge
                          variant="outline"
                          className={
                            model.tier === 'premium' ? 'border-purple-500 text-purple-700' :
                              model.tier === 'free' ? 'border-green-500 text-green-700' :
                                'border-blue-500 text-blue-700'
                          }
                        >
                          {model.tier}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{model.cost}</span>
                      </div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {selectedModelInfo && (
            <Alert>
              <DollarSign className="h-4 w-4" />
              <AlertDescription>
                <strong>{selectedModelInfo.label}</strong> • {selectedModelInfo.cost}
              </AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Temperature</Label>
              <span className="text-sm text-muted-foreground">{config.temperature}</span>
            </div>
            <Slider
              value={[config.temperature]}
              onValueChange={(value) => setConfig({ ...config, temperature: value[0] })}
              min={0}
              max={2}
              step={0.1}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground">
              Menor = mais preciso e consistente | Maior = mais criativo e variado
            </p>
          </div>

          <div className="space-y-2">
            <Label>Max Tokens</Label>
            <Input
              type="number"
              value={config.maxTokens}
              onChange={(e) => setConfig({ ...config, maxTokens: parseInt(e.target.value) })}
              min={100}
              max={8000}
            />
            <p className="text-xs text-muted-foreground">
              Limite de tokens por resposta (recomendado: 2000-4000)
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Info Box */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          <strong>Dica:</strong> Modelos diferentes têm custos e capacidades variadas.
          Use modelos premium (Claude Sonnet 4, GPT-4) para tarefas críticas e modelos
          mais baratos ou FREE para testes e tarefas simples.
        </AlertDescription>
      </Alert>

      {/* Monitoring Section (LangSmith) */}
      <Card className="border-blue-200 dark:border-blue-900 bg-blue-50/20 dark:bg-blue-950/10">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-blue-500" />
                Observabilidade LangSmith
              </CardTitle>
              <CardDescription>Monitoramento em tempo real das execuções do agente</CardDescription>
            </div>
            {monitoringStats?.status === 'active' && (
              <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
                Ativo: {monitoringStats.project}
              </Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {loadingStats ? (
            <div className="text-sm text-muted-foreground flex items-center gap-2">
              <span className="animate-spin">⌛</span> Carregando métricas...
            </div>
          ) : monitoringStats?.status === 'active' ? (
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div className="p-3 bg-white dark:bg-gray-800 rounded-lg border">
                  <div className="text-xs text-muted-foreground">Total Runs (100)</div>
                  <div className="text-2xl font-bold">{monitoringStats.total_runs_in_window}</div>
                </div>
                <div className="p-3 bg-white dark:bg-gray-800 rounded-lg border">
                  <div className="text-xs text-muted-foreground">Taxa de Erro</div>
                  <div className={cn("text-2xl font-bold", monitoringStats.error_rate > 0 ? "text-red-500" : "text-green-500")}>
                    {monitoringStats.error_rate}%
                  </div>
                </div>
                <div className="p-3 bg-white dark:bg-gray-800 rounded-lg border">
                  <div className="text-xs text-muted-foreground">Sucesso</div>
                  <div className="text-2xl font-bold text-green-600">{monitoringStats.success_rate}%</div>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-semibold mb-2">Últimas 5 Execuções</h4>
                <div className="space-y-2">
                  {monitoringStats.recent_runs.slice(0, 5).map(run => (
                    <div key={run.id} className="text-xs flex items-center justify-between p-2 bg-white dark:bg-gray-800 rounded border">
                      <div className="flex items-center gap-2">
                        <div className={cn("w-2 h-2 rounded-full", run.status === 'success' ? "bg-green-500" : "bg-red-500")} />
                        <span className="font-medium truncate max-w-[150px]">{run.name}</span>
                      </div>
                      <div className="flex items-center gap-3 text-muted-foreground">
                        <span>{run.latency}s</span>
                        <span>{run.timestamp ? new Date(run.timestamp).toLocaleTimeString() : '-'}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-sm text-yellow-600 bg-yellow-50 p-3 rounded border border-yellow-200">
              LangSmith não está configurado ou ativo neste ambiente.
              <br />
              Verifique as variáveis de ambiente LANGSMITH_API_KEY.
            </div>
          )}
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end pt-4">
        <Button onClick={handleSave} disabled={isSaving} className="gap-2 bg-[#FF6B35] hover:bg-[#e55f30]">
          {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
          {isSaving ? 'Salvando...' : 'Salvar Configurações'}
        </Button>
      </div>

    </div>
  );
};