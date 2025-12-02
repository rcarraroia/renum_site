import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Zap, Save, History, Play } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

interface InstructionsConfig {
  systemPrompt: string;
  persona: string;
  capabilities: string;
  limitations: string;
}

const MOCK_INSTRUCTIONS: InstructionsConfig = {
  systemPrompt: "Você é Renus, um agente de descoberta de IA da Renum Tech Agency. Seu objetivo é mapear os desafios de negócios do usuário e sugerir soluções de IA personalizadas (Sistemas AI Native, Workflows ou Agentes Solo). Mantenha um tom profissional, empático e focado em ROI.",
  persona: "Profissional, empático, focado em resultados e com conhecimento profundo em automação e IA.",
  capabilities: "Mapeamento de desafios, sugestão de soluções, geração de relatórios preliminares.",
  limitations: "Não pode realizar transações financeiras ou acessar dados confidenciais de clientes.",
};

const InstructionsTab: React.FC = () => {
  const [config, setConfig] = useState<InstructionsConfig>(MOCK_INSTRUCTIONS);
  const [isSaving, setIsSaving] = useState(false);
  const [isTesting, setIsTesting] = useState(false);

  useEffect(() => {
    const storedConfig = localStorage.getItem('renus_instructions');
    if (storedConfig) {
      setConfig(JSON.parse(storedConfig));
    }
  }, []);

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => {
      localStorage.setItem('renus_instructions', JSON.stringify(config));
      setIsSaving(false);
      toast.success("Instruções salvas com sucesso!");
    }, 1000);
  };

  const handleTest = () => {
    setIsTesting(true);
    toast.info("Simulando teste de prompt...");
    setTimeout(() => {
      setIsTesting(false);
      toast.success("Teste concluído. Renus respondeu conforme a persona.");
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Prompt Principal do Sistema</CardTitle>
          <CardDescription>Defina a função, o tom e as regras fundamentais do agente Renus.</CardDescription>
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

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center text-[#0ca7d2]">
                <Play className="h-5 w-5 mr-2" /> Preview de Conversa
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-semibold text-[#FF6B35]">Usuário:</p>
                <p>Quero automatizar minhas vendas.</p>
            </div>
            <div className="p-3 bg-[#4e4ea8]/10 dark:bg-[#0ca7d2]/10 rounded-lg border border-[#4e4ea8]">
                <p className="font-semibold text-[#4e4ea8] dark:text-[#0ca7d2]">Renus (Preview):</p>
                <p>Compreendo. Para mapear a solução ideal, preciso entender seu funil atual e os KPIs que deseja otimizar. Qual é o seu principal gargalo hoje?</p>
            </div>
            <Button variant="outline" className="w-full mt-4" onClick={handleTest} disabled={isTesting}>
                {isTesting ? 'Testando...' : 'Simular e Testar'}
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
            <CardTitle className="flex items-center">
                <History className="h-5 w-5 mr-2" /> Histórico de Versões (Mock)
            </CardTitle>
        </CardHeader>
        <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex justify-between"><span>V1.2 - Foco em ROI</span><span className="text-xs">2024-10-20</span></li>
                <li className="flex justify-between"><span>V1.1 - Adição de Empatia</span><span className="text-xs">2024-09-15</span></li>
            </ul>
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button onClick={handleSave} disabled={isSaving} className="bg-[#FF6B35] hover:bg-[#e55f30]">
          <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Configuração'}
        </Button>
      </div>
    </div>
  );
};

export default InstructionsTab;