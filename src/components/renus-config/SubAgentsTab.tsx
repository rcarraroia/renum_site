import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Plus, Edit, Trash2, MessageSquare, Globe, ChevronDown, ChevronUp, Users, Zap, FileText, Upload, Info } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useToast } from '@/hooks/use-toast';

interface SubAgent {
  id: string;
  name: string;
  description: string;
  channel: 'site' | 'whatsapp';
  systemPrompt: string;
  topics: string[];
  isActive: boolean;
  // 🆕 NOVOS CAMPOS
  useFineTuning?: boolean;
  fineTuneStatus?: 'none' | 'preparing' | 'training' | 'ready' | 'failed';
  fineTuneModelId?: string;
  trainingExamplesCount?: number;
}

export const SubAgentsTab = () => {
  const { toast } = useToast();
  
  // Mock data inicial
  const [subAgents, setSubAgents] = useState<SubAgent[]>([
    {
      id: '1',
      name: 'Pesquisa MMN',
      description: 'Agente especializado em entrevistar distribuidores de Marketing Multinível',
      channel: 'whatsapp',
      systemPrompt: 'Você é um pesquisador especializado em Marketing Multinível. Conduza entrevistas para entender as dores e necessidades dos distribuidores.',
      topics: ['Prospecção', 'Atendimento', 'Treinamento', 'Automação', 'Investimento'],
      isActive: true,
      useFineTuning: false,
      fineTuneStatus: 'none',
    },
    {
      id: '2',
      name: 'Atendimento Clínicas',
      description: 'Agente para atendimento 24/7 de pacientes de clínicas médicas',
      channel: 'site',
      systemPrompt: 'Você é um assistente virtual de clínica médica. Ajude pacientes com agendamentos, dúvidas sobre procedimentos e informações gerais.',
      topics: ['Agendamentos', 'Procedimentos', 'Convênios', 'Localização'],
      isActive: false,
      useFineTuning: false,
      fineTuneStatus: 'none',
    },
    {
      id: '3',
      name: 'Vendas E-commerce',
      description: 'Agente de vendas para loja online de roupas',
      channel: 'whatsapp',
      systemPrompt: 'Você é um consultor de vendas especializado em moda. Ajude clientes a encontrar produtos, tire dúvidas e finalize vendas.',
      topics: ['Produtos', 'Tamanhos', 'Pagamento', 'Entrega'],
      isActive: true,
      useFineTuning: false,
      fineTuneStatus: 'none',
    }
  ]);

  // Estados do modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingAgent, setEditingAgent] = useState<SubAgent | null>(null);
  const [isExpanded, setIsExpanded] = useState<{[key: string]: boolean}>({});

  // Estado do formulário
  const [formData, setFormData] = useState<Partial<SubAgent>>({
    name: '',
    description: '',
    channel: 'whatsapp',
    systemPrompt: '',
    topics: [],
    isActive: true,
    useFineTuning: false,
    fineTuneStatus: 'none',
  });

  const handleOpenModal = (agent?: SubAgent) => {
    if (agent) {
      setEditingAgent(agent);
      setFormData(agent);
    } else {
      setEditingAgent(null);
      setFormData({
        name: '',
        description: '',
        channel: 'whatsapp',
        systemPrompt: '',
        topics: [],
        isActive: true,
        useFineTuning: false,
        fineTuneStatus: 'none',
      });
    }
    setIsModalOpen(true);
  };

  const handleSave = () => {
    if (!formData.name || !formData.systemPrompt) {
      toast({
        title: "Erro",
        description: "Nome e Prompt são obrigatórios",
        variant: "destructive"
      });
      return;
    }

    if (editingAgent) {
      // Editar existente
      setSubAgents(prev => 
        prev.map(agent => 
          agent.id === editingAgent.id 
            ? { ...agent, ...formData } as SubAgent
            : agent
        )
      );
      toast({
        title: "Sub-Agente atualizado!",
        description: `${formData.name} foi atualizado com sucesso.`
      });
    } else {
      // Criar novo
      const newAgent: SubAgent = {
        id: Date.now().toString(),
        ...formData as SubAgent
      };
      setSubAgents(prev => [...prev, newAgent]);
      toast({
        title: "Sub-Agente criado!",
        description: `${formData.name} foi criado com sucesso.`
      });
    }

    setIsModalOpen(false);
  };

  const handleDelete = (id: string) => {
    setSubAgents(prev => prev.filter(agent => agent.id !== id));
    toast({
      title: "Sub-Agente removido",
      description: "O sub-agente foi removido com sucesso."
    });
  };

  const handleToggleActive = (id: string) => {
    setSubAgents(prev =>
      prev.map(agent =>
        agent.id === id
          ? { ...agent, isActive: !agent.isActive }
          : agent
      )
    );
  };

  const addTopic = () => {
    const topicInput = prompt('Digite o nome do tópico:');
    if (topicInput) {
      setFormData(prev => ({
        ...prev,
        topics: [...(prev.topics || []), topicInput]
      }));
    }
  };

  const removeTopic = (index: number) => {
    setFormData(prev => ({
      ...prev,
      topics: (prev.topics || []).filter((_, i) => i !== index)
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[#4e4ea8]">Sub-Agentes Especializados</h2>
          <p className="text-muted-foreground mt-1">
            Crie agentes especializados para diferentes nichos, tipos e canais de atendimento
          </p>
        </div>
        <Button 
          onClick={() => handleOpenModal()}
          className="bg-[#FF6B35] hover:bg-[#e55f30]"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Sub-Agente
        </Button>
      </div>

      {/* Lista de Sub-Agentes */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {subAgents.map(agent => (
          <Card 
            key={agent.id}
            className={cn(
              "transition-all hover:shadow-lg",
              agent.isActive 
                ? "border-[#0ca7d2]" 
                : "border-dashed opacity-60"
            )}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="space-y-1 flex-1">
                  <CardTitle className="flex items-center gap-2 text-lg">
                    {agent.name}
                    {agent.isActive ? (
                      <Badge className="bg-green-500 text-xs">Ativo</Badge>
                    ) : (
                      <Badge variant="secondary" className="text-xs">Inativo</Badge>
                    )}
                  </CardTitle>
                  <CardDescription className="text-sm">
                    {agent.description}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-3">
              {/* Canal */}
              <div className="flex items-center gap-2 text-sm">
                {agent.channel === 'whatsapp' ? (
                  <>
                    <MessageSquare className="h-4 w-4 text-green-600" />
                    <span className="text-muted-foreground">WhatsApp</span>
                  </>
                ) : (
                  <>
                    <Globe className="h-4 w-4 text-blue-600" />
                    <span className="text-muted-foreground">Site</span>
                  </>
                )}
              </div>

              {/* Tópicos (expansível) */}
              <div>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-between p-0 h-auto hover:bg-transparent"
                  onClick={() => setIsExpanded(prev => ({
                    ...prev,
                    [agent.id]: !prev[agent.id]
                  }))}
                >
                  <span className="text-sm text-muted-foreground">
                    🔖 {agent.topics.length} tópicos configurados
                  </span>
                  {isExpanded[agent.id] ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </Button>
                
                {isExpanded[agent.id] && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {agent.topics.map((topic, i) => (
                      <Badge key={i} variant="outline" className="text-xs">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            </CardContent>

            <CardFooter className="flex gap-2 pt-3 border-t">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleOpenModal(agent)}
                className="flex-1"
              >
                <Edit className="h-3 w-3 mr-1" />
                Editar
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleToggleActive(agent.id)}
                className="flex-1"
              >
                {agent.isActive ? 'Pausar' : 'Ativar'}
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(agent.id)}
              >
                <Trash2 className="h-3 w-3" />
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {subAgents.length === 0 && (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Users className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhum sub-agente criado</h3>
            <p className="text-muted-foreground text-center mb-4">
              Crie seu primeiro sub-agente especializado para começar
            </p>
            <Button 
              onClick={() => handleOpenModal()}
              className="bg-[#FF6B35] hover:bg-[#e55f30]"
            >
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeiro Sub-Agente
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Modal de Criação/Edição */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-[#4e4ea8]">
              {editingAgent ? 'Editar Sub-Agente' : 'Novo Sub-Agente'}
            </DialogTitle>
            <DialogDescription>
              Configure um agente especializado para um nicho e tipo específico
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Nome */}
            <div className="space-y-2">
              <Label htmlFor="name">Nome do Sub-Agente *</Label>
              <Input
                id="name"
                placeholder="Ex: Pesquisa MMN, Atendimento Clínicas, Vendas E-commerce"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({...prev, name: e.target.value}))}
              />
              <p className="text-xs text-muted-foreground">
                Escolha um nome descritivo que identifique o nicho e tipo
              </p>
            </div>

            {/* Descrição */}
            <div className="space-y-2">
              <Label htmlFor="description">Descrição</Label>
              <Textarea
                id="description"
                placeholder="Breve descrição do objetivo e público-alvo deste sub-agente..."
                rows={3}
                value={formData.description}
                onChange={(e) => setFormData(prev => ({...prev, description: e.target.value}))}
              />
            </div>

            {/* Canal */}
            <div className="space-y-2">
              <Label>Canal de Atendimento *</Label>
              <RadioGroup
                value={formData.channel}
                onValueChange={(value) => setFormData(prev => ({...prev, channel: value as 'site' | 'whatsapp'}))}
              >
                <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer">
                  <RadioGroupItem value="whatsapp" id="whatsapp" />
                  <Label htmlFor="whatsapp" className="flex items-center gap-2 cursor-pointer flex-1">
                    <MessageSquare className="h-4 w-4 text-green-600" />
                    <div>
                      <div className="font-medium">WhatsApp</div>
                      <div className="text-xs text-muted-foreground">Atendimento via WhatsApp Business</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer">
                  <RadioGroupItem value="site" id="site" />
                  <Label htmlFor="site" className="flex items-center gap-2 cursor-pointer flex-1">
                    <Globe className="h-4 w-4 text-blue-600" />
                    <div>
                      <div className="font-medium">Site</div>
                      <div className="text-xs text-muted-foreground">Widget de chat no website</div>
                    </div>
                  </Label>
                </div>
              </RadioGroup>
            </div>

            {/* System Prompt */}
            <div className="space-y-2">
              <Label htmlFor="systemPrompt">Prompt Base (System Prompt) *</Label>
              <Textarea
                id="systemPrompt"
                placeholder="Você é um assistente especializado em... Seu objetivo é... Mantenha um tom..."
                rows={8}
                className="font-mono text-sm"
                value={formData.systemPrompt}
                onChange={(e) => setFormData(prev => ({...prev, systemPrompt: e.target.value}))}
              />
              <p className="text-xs text-muted-foreground">
                💡 Defina claramente: função, comportamento, tom e objetivo do agente
              </p>
            </div>

            {/* Tópicos Obrigatórios */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Tópicos/Contextos Principais</Label>
                  <p className="text-xs text-muted-foreground">
                    Principais assuntos que o agente deve dominar
                  </p>
                </div>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={addTopic}
                >
                  <Plus className="h-3 w-3 mr-1" />
                  Adicionar
                </Button>
              </div>
              <div className="flex flex-wrap gap-2 min-h-[40px] p-3 border rounded-lg">
                {(formData.topics || []).length === 0 ? (
                  <span className="text-sm text-muted-foreground">
                    Nenhum tópico adicionado
                  </span>
                ) : (
                  (formData.topics || []).map((topic, index) => (
                    <Badge
                      key={index}
                      variant="secondary"
                      className="flex items-center gap-1"
                    >
                      {topic}
                      <button
                        onClick={() => removeTopic(index)}
                        className="hover:text-destructive ml-1"
                      >
                        ×
                      </button>
                    </Badge>
                  ))
                )}
              </div>
            </div>
            
            {/* Seção Fine-tuning */}
            <div className="space-y-4 p-4 border-2 border-dashed border-blue-300 dark:border-blue-700 rounded-lg bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-blue-600" />
                    <Label className="text-lg font-semibold text-blue-900 dark:text-blue-100">
                      ⚡ Fine-tuning (Otimização Avançada)
                    </Label>
                    <Badge variant="secondary" className="text-xs">
                      Em Breve
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1 ml-7">
                    Economize até 90% em tokens e melhore a qualidade das respostas
                  </p>
                </div>
                <Switch
                  checked={formData.useFineTuning || false}
                  onCheckedChange={(checked) => setFormData(prev => ({...prev, useFineTuning: checked}))}
                  disabled={true}
                  className="opacity-50"
                />
              </div>

              {/* Área expansível (sempre visível para preview) */}
              <div className="space-y-3 pt-3 border-t border-blue-200 dark:border-blue-800 opacity-60">
                {/* Info cards */}
                <div className="grid grid-cols-3 gap-2">
                  <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                    <div className="text-xs text-muted-foreground">Economia</div>
                    <div className="text-lg font-bold text-blue-600">~90%</div>
                  </div>
                  <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                    <div className="text-xs text-muted-foreground">Tokens/msg</div>
                    <div className="text-lg font-bold text-green-600">50</div>
                    <div className="text-xs line-through text-gray-400">800</div>
                  </div>
                  <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                    <div className="text-xs text-muted-foreground">Exemplos</div>
                    <div className="text-lg font-bold text-purple-600">50+</div>
                  </div>
                </div>

                {/* Upload placeholder */}
                <div className="space-y-2">
                  <Label className="text-sm flex items-center gap-2 opacity-50">
                    <FileText className="h-4 w-4" />
                    Dataset de Treinamento (JSONL)
                  </Label>
                  <div className="border-2 border-dashed rounded-lg p-4 text-center bg-white dark:bg-gray-900 opacity-50">
                    <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">
                      Arraste o arquivo .jsonl aqui ou clique para selecionar
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Mínimo 50 exemplos de conversas
                    </p>
                  </div>
                </div>

                {/* Status placeholder */}
                <div className="p-3 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 opacity-50">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-gray-400"></div>
                    <span className="text-sm text-muted-foreground">
                      Aguardando ativação do fine-tuning...
                    </span>
                  </div>
                </div>

                {/* Info footer */}
                <div className="flex items-start gap-2 p-2 rounded bg-blue-100 dark:bg-blue-900">
                  <Info className="h-4 w-4 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-700 dark:text-blue-300">
                    <strong>Como funciona:</strong> Você treina o modelo uma vez com exemplos reais de conversas. 
                    Depois, ele já sabe como responder naturalmente, sem precisar de prompts gigantes toda vez.
                    Isso reduz drasticamente o consumo de tokens e melhora a qualidade das respostas.
                  </p>
                </div>
              </div>
            </div>

            {/* Status */}
            <div className="flex items-center justify-between p-4 border rounded-lg bg-gray-50 dark:bg-gray-900">
              <div>
                <Label>Status Inicial</Label>
                <p className="text-sm text-muted-foreground">
                  Ativar sub-agente imediatamente após criação
                </p>
              </div>
              <Switch
                checked={formData.isActive}
                onCheckedChange={(checked) => setFormData(prev => ({...prev, isActive: checked}))}
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setIsModalOpen(false)}
            >
              Cancelar
            </Button>
            <Button
              onClick={handleSave}
              className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
            >
              {editingAgent ? 'Salvar Alterações' : 'Criar Sub-Agente'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};