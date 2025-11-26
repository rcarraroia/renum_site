import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Plus, Trash2, Settings, ToggleLeft, ToggleRight, TestTube } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

interface Tool {
  id: number;
  name: string;
  description: string;
  enabled: boolean;
  parameters: { name: string; type: string; description: string }[];
}

const MOCK_TOOLS: Tool[] = [
  {
    id: 1,
    name: 'get_project_status',
    description: 'Busca o status atual de um projeto pelo ID do cliente.',
    enabled: true,
    parameters: [{ name: 'client_id', type: 'string', description: 'ID único do cliente.' }],
  },
  {
    id: 2,
    name: 'schedule_call',
    description: 'Agenda uma call de 30 minutos com um consultor de vendas.',
    enabled: true,
    parameters: [
      { name: 'client_email', type: 'string', description: 'Email do cliente.' },
      { name: 'topic', type: 'string', description: 'Assunto da reunião.' },
    ],
  },
  {
    id: 3,
    name: 'generate_viability_report',
    description: 'Gera um relatório preliminar de viabilidade técnica e ROI.',
    enabled: false,
    parameters: [{ name: 'challenge_summary', type: 'string', description: 'Resumo do desafio do cliente.' }],
  },
];

const ToolsTab: React.FC = () => {
  const [tools, setTools] = useState<Tool[]>(MOCK_TOOLS);
  const [newTool, setNewTool] = useState<Partial<Tool>>({ parameters: [] });
  const [isTesting, setIsTesting] = useState(false);

  const handleToggle = (id: number) => {
    setTools(tools.map(t => (t.id === id ? { ...t, enabled: !t.enabled } : t)));
    toast.info("Status da ferramenta atualizado.");
  };

  const handleAddParameter = () => {
    setNewTool(prev => ({
      ...prev,
      parameters: [...(prev.parameters || []), { name: '', type: 'string', description: '' }],
    }));
  };

  const handleRemoveParameter = (index: number) => {
    setNewTool(prev => ({
      ...prev,
      parameters: prev.parameters?.filter((_, i) => i !== index),
    }));
  };

  const handleCreateTool = () => {
    if (newTool.name && newTool.description) {
      const tool: Tool = {
        id: Date.now(),
        name: newTool.name.toLowerCase().replace(/\s/g, '_'),
        description: newTool.description,
        enabled: true,
        parameters: newTool.parameters || [],
      };
      setTools([...tools, tool]);
      setNewTool({ parameters: [] });
      toast.success(`Ferramenta '${tool.name}' criada e ativada.`);
    } else {
      toast.error("Nome e descrição da ferramenta são obrigatórios.");
    }
  };

  const handleTestTool = (toolName: string) => {
    setIsTesting(true);
    toast.info(`Executando teste simulado para ${toolName}...`);
    setTimeout(() => {
      setIsTesting(false);
      toast.success(`Teste de ${toolName} concluído. Retorno: { success: true, data: 'Mock data' }`);
    }, 1500);
  };

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Ferramentas Ativas ({tools.filter(t => t.enabled).length})</CardTitle>
          <CardDescription>Gerencie as funções externas que o Renus pode chamar durante uma conversa.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {tools.map(tool => (
            <div key={tool.id} className="flex items-center justify-between p-3 border rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <div className="flex-grow">
                <h4 className="font-semibold text-sm text-[#0ca7d2]">{tool.name}</h4>
                <p className="text-xs text-muted-foreground">{tool.description}</p>
                <p className="text-xs mt-1 font-mono">
                  Parâmetros: {tool.parameters.length > 0 ? tool.parameters.map(p => p.name).join(', ') : 'Nenhum'}
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <Button variant="outline" size="sm" onClick={() => handleTestTool(tool.name)} disabled={isTesting}>
                    <TestTube className="h-4 w-4" />
                </Button>
                <Switch
                  checked={tool.enabled}
                  onCheckedChange={() => handleToggle(tool.id)}
                  className={cn(tool.enabled ? 'data-[state=checked]:bg-[#FF6B35]' : '')}
                />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="border-2 border-dashed border-[#4e4ea8] dark:border-[#0ca7d2]">
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Plus className="h-5 w-5 mr-2" /> Criar Nova Ferramenta
          </CardTitle>
          <CardDescription>Defina o nome, descrição e os parâmetros necessários para a nova função.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="tool-name">Nome da Ferramenta (snake_case)</Label>
              <Input
                id="tool-name"
                value={newTool.name || ''}
                onChange={(e) => setNewTool({ ...newTool, name: e.target.value })}
                placeholder="ex: get_client_info"
              />
            </div>
            <div>
              <Label htmlFor="tool-description">Descrição</Label>
              <Input
                id="tool-description"
                value={newTool.description || ''}
                onChange={(e) => setNewTool({ ...newTool, description: e.target.value })}
                placeholder="O que esta ferramenta faz?"
              />
            </div>
          </div>

          <Separator />

          <h5 className="font-semibold text-sm">Parâmetros ({newTool.parameters?.length || 0})</h5>
          <div className="space-y-3">
            {newTool.parameters?.map((param, index) => (
              <div key={index} className="flex space-x-2 items-end">
                <div className="flex-1">
                  <Label>Nome</Label>
                  <Input
                    value={param.name}
                    onChange={(e) => {
                      const params = newTool.parameters || [];
                      params[index].name = e.target.value;
                      setNewTool({ ...newTool, parameters: params });
                    }}
                    placeholder="ex: user_id"
                  />
                </div>
                <div className="flex-1">
                  <Label>Tipo</Label>
                  <Input
                    value={param.type}
                    onChange={(e) => {
                      const params = newTool.parameters || [];
                      params[index].type = e.target.value;
                      setNewTool({ ...newTool, parameters: params });
                    }}
                    placeholder="ex: string, number"
                  />
                </div>
                <div className="flex-1 md:flex-2">
                  <Label>Descrição</Label>
                  <Input
                    value={param.description}
                    onChange={(e) => {
                      const params = newTool.parameters || [];
                      params[index].description = e.target.value;
                      setNewTool({ ...newTool, parameters: params });
                    }}
                    placeholder="Descrição para o modelo de IA"
                  />
                </div>
                <Button variant="destructive" size="icon" onClick={() => handleRemoveParameter(index)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
          <Button variant="outline" onClick={handleAddParameter}>
            <Plus className="h-4 w-4 mr-2" /> Adicionar Parâmetro
          </Button>

          <Button onClick={handleCreateTool} className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80]">
            <Settings className="h-4 w-4 mr-2" /> Salvar Nova Ferramenta
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default ToolsTab;