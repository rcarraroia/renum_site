import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Zap, Save, History, Play, Send } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { publicChatService } from '@/services/publicChatService';

interface InstructionsConfig {
  systemPrompt: string;
  persona: string;
  capabilities: string;
  limitations: string;
  welcomeMessage: string;
}

const MOCK_INSTRUCTIONS: InstructionsConfig = {
  systemPrompt: "Você é Renus, um agente de descoberta de IA da Renum Tech Agency. Seu objetivo é mapear os desafios de negócios do usuário e sugerir soluções de IA personalizadas (Sistemas AI Native, Workflows ou Agentes Solo). Mantenha um tom profissional, empático e focado em ROI.",
  persona: "Profissional, empático, focado em resultados e com conhecimento profundo em automação e IA.",
  capabilities: "Mapeamento de desafios, sugestão de soluções, geração de relatórios preliminares.",
  limitations: "Não pode realizar transações financeiras ou acessar dados confidenciais de clientes.",
  welcomeMessage: "Olá! Sou Renus, seu agente de descoberta de IA da Renum Tech Agency. Estou aqui para ajudar a mapear seus desafios de negócios e sugerir soluções de IA personalizadas. Como posso te ajudar hoje?"
};

const InstructionsTab: React.FC = () => {
  const [config, setConfig] = useState<InstructionsConfig>({
    systemPrompt: '',
    persona: '',
    capabilities: '',
    limitations: '',
    welcomeMessage: ''
  });
  const [agentId, setAgentId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  // Test Chat State
  const [testInput, setTestInput] = useState('');
  const [testResponse, setTestResponse] = useState<string | null>(null);
  const [isTesting, setIsTesting] = useState(false);

  // Import agentService (dynamic import or use global if available, assuming import works)
  // We need to add query import at the top? No, we will assume imports are handled by the environment or add them if missing.
  // Actually, I need to add the import statement at the top of the file as well.

  useEffect(() => {
    loadAgentConfig();
  }, []);

  const loadAgentConfig = async () => {
    try {
      setIsLoading(true);
      // Fetch the main 'renus' agent
      // We assume publicChatService is redundant here, we use agentService directly for config
      const agentService = (await import('@/services/agentService')).default;

      let agent;
      try {
        agent = await agentService.getAgentBySlug('renus');
      } catch (e) {
        console.warn("Agent 'renus' not found by slug, trying to find by role or list...");
        // Fallback: List agents and find system_orchestrator
        const agents = await agentService.listAgents();
        agent = agents.find(a => a.slug === 'renus' || a.role === 'system_orchestrator');
      }

      if (agent) {
        setAgentId(agent.id);
        const identity = agent.config?.identity || {};
        setConfig({
          systemPrompt: identity.system_prompt || agent.config?.system_prompt || '',
          persona: identity.persona || '',
          capabilities: identity.capabilities || '',
          limitations: identity.limitations || '',
          welcomeMessage: identity.welcome_message || ''
        });
      } else {
        toast.error("Agente Renus não encontrado.");
      }
    } catch (error) {
      console.error("Error loading agent:", error);
      toast.error("Erro ao carregar configurações do agente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!agentId) return;

    setIsSaving(true);
    try {
      const agentService = (await import('@/services/agentService')).default;

      // Get current agent to preserve other config
      const currentAgent = await agentService.getAgent(agentId);
      const currentConfig = currentAgent.config || {};

      // Update config structure
      const newConfig = {
        ...currentConfig,
        identity: {
          ...currentConfig.identity, // preserve other identity fields if any
          system_prompt: config.systemPrompt,
          persona: config.persona,
          capabilities: config.capabilities,
          limitations: config.limitations,
          welcome_message: config.welcomeMessage
        },
        // Also update root system_prompt for compatibility if needed, 
        // but Phase 1 spec says we use identity.system_prompt
        // We can sync them to be safe
        system_prompt: config.systemPrompt
      };

      await agentService.updateAgent(agentId, {
        config: newConfig
      });

      toast.success("Instruções salvas e aplicadas ao Agente Real!");
    } catch (error) {
      console.error("Error saving agent:", error);
      toast.error("Erro ao salvar configurações.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleTest = async () => {
    if (!testInput.trim()) {
      toast.warning("Digite uma mensagem para testar.");
      return;
    }

    setIsTesting(true);
    setTestResponse(null);
    try {
      // Usa o slug 'renus' para testar o agente principal
      const response = await publicChatService.sendMessage('renus', testInput);
      setTestResponse(response.message);
      toast.success("Resposta recebida do Agente Real!");
    } catch (error) {
      console.error(error);
      toast.error("Erro ao conectar com o agente Renus.");
    } finally {
      setIsTesting(false);
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-muted-foreground">Carregando configurações do Agente Renus...</div>;
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Prompt Principal do Sistema (Backend Real)</CardTitle>
          <CardDescription>
            Defina a função, o tom e as regras fundamentais do agente Renus.
            <br />
            <span className="text-xs text-orange-600 font-semibold">
              Alterações aqui impactam IMEDIATAMENTE o agente "Jonas" (Renus).
            </span>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Label htmlFor="system-prompt" className="mb-2 block">Prompt de Comportamento (System Prompt)</Label>
          <Textarea
            id="system-prompt"
            rows={8}
            value={config.systemPrompt}
            onChange={(e) => setConfig({ ...config, systemPrompt: e.target.value })}
            className="font-mono text-sm"
          />
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Detalhes da Persona</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="welcome" className="mb-1 block text-green-600 font-medium">Mensagem de Boas-Vindas</Label>
              <Textarea
                id="welcome"
                rows={2}
                placeholder="Ex: Olá! Sou Jonas..."
                value={config.welcomeMessage}
                onChange={(e) => setConfig({ ...config, welcomeMessage: e.target.value })}
                className="border-green-200 focus:border-green-500"
              />
              <p className="text-xs text-muted-foreground mt-1">Aparece antes do usuário digitar.</p>
            </div>

            <div>
              <Label htmlFor="persona" className="mb-1 block">Tom e Personalidade</Label>
              <Input
                id="persona"
                value={config.persona}
                onChange={(e) => setConfig({ ...config, persona: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="capabilities" className="mb-1 block">Capacidades Principais</Label>
              <Textarea
                id="capabilities"
                rows={3}
                value={config.capabilities}
                onChange={(e) => setConfig({ ...config, capabilities: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="limitations" className="mb-1 block">Restrições e Limitações</Label>
              <Textarea
                id="limitations"
                rows={3}
                value={config.limitations}
                onChange={(e) => setConfig({ ...config, limitations: e.target.value })}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center text-[#0ca7d2]">
              <Play className="h-5 w-5 mr-2" /> Preview de Conversa (Real)
            </CardTitle>
            <CardDescription>Teste o comportamento atual do agente Renus (versão salva).</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm flex-grow flex flex-col">
            <div className="flex-grow space-y-3">
              <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-semibold text-[#FF6B35] mb-1">Entrada de Teste:</p>
                <div className="flex gap-2">
                  <Input
                    value={testInput}
                    onChange={(e) => setTestInput(e.target.value)}
                    placeholder="Ex: Quero automatizar minhas vendas..."
                    className="bg-white dark:bg-gray-900"
                    onKeyDown={(e) => e.key === 'Enter' && handleTest()}
                  />
                </div>
              </div>

              {testResponse && (
                <div className="p-3 bg-[#4e4ea8]/10 dark:bg-[#0ca7d2]/10 rounded-lg border border-[#4e4ea8] animate-in fade-in slide-in-from-bottom-2">
                  <p className="font-semibold text-[#4e4ea8] dark:text-[#0ca7d2] mb-1">Renus (Real):</p>
                  <p>{testResponse}</p>
                </div>
              )}
            </div>

            <Button className="w-full mt-4 bg-[#0ca7d2] hover:bg-[#0989ac] text-white" onClick={handleTest} disabled={isTesting}>
              {isTesting ? (
                <>
                  <Zap className="h-4 w-4 mr-2 animate-spin" /> Testando...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" /> Enviar Teste
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <History className="h-5 w-5 mr-2" /> Meta-Informação (Real Backend)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-muted-foreground">
            <p>Agent ID: <span className="font-mono text-zinc-500">{agentId}</span></p>
            <p className="mt-1">Config Mode: <span className="text-green-600 font-medium font-mono">Dynamic JSONB</span></p>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button onClick={handleSave} disabled={isSaving || !agentId} className="bg-[#FF6B35] hover:bg-[#e55f30]">
          <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Configuração'}
        </Button>
      </div>
    </div>
  );
};

export default InstructionsTab;