import React, { useState } from 'react';
import { Users, Plus } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useToast } from '@/hooks/use-toast';
import { SubAgent } from './types';
import { SubAgentCard } from './SubAgentCard';
import { SubAgentModal } from './SubAgentModal';

const initialMockAgents: SubAgent[] = [
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
];

export const SubAgentsTab = () => {
  const { toast } = useToast();
  
  const [subAgents, setSubAgents] = useState<SubAgent[]>(initialMockAgents);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingAgent, setEditingAgent] = useState<SubAgent | null>(null);
  const [isExpanded, setIsExpanded] = useState<{[key: string]: boolean}>({});

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
  
  const handleToggleExpand = (id: string) => {
    setIsExpanded(prev => ({
        ...prev,
        [id]: !prev[id]
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
          <SubAgentCard
            key={agent.id}
            agent={agent}
            onEdit={handleOpenModal}
            onDelete={handleDelete}
            onToggleActive={handleToggleActive}
            isExpanded={!!isExpanded[agent.id]}
            onToggleExpand={handleToggleExpand}
          />
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
      <SubAgentModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        formData={formData}
        setFormData={setFormData}
        onSave={handleSave}
        editingAgent={editingAgent}
        addTopic={addTopic}
        removeTopic={removeTopic}
      />
    </div>
  );
};