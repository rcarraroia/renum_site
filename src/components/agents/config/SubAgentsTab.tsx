import React, { useState, useEffect } from 'react';
import { Users, Plus, Zap, Edit, Trash2, MessageSquare, Globe, ChevronDown, ChevronUp, FileText, Upload, Info, Tag, Sliders, RefreshCw, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import agentService from '@/services/agentService';
import { useAuth } from '@/hooks/useAuth'; // Assuming useAuth exists for clientId

interface SubAgent {
  id: string;
  name: string;
  description: string;
  channel: 'site' | 'whatsapp';
  systemPrompt: string;
  topics: string[];
  isActive: boolean;
  useFineTuning?: boolean;
  fineTuneStatus?: 'none' | 'preparing' | 'training' | 'ready' | 'failed';
  model?: string;
}

// --- SubAgentCard Component ---
interface SubAgentCardProps {
  agent: SubAgent;
  onEdit: (agent: SubAgent) => void;
  onDelete: (id: string) => void;
  onToggleActive: (agent: SubAgent) => void;
  isExpanded: boolean;
  onToggleExpand: (id: string) => void;
}

const SubAgentCard: React.FC<SubAgentCardProps> = ({ agent, onEdit, onDelete, onToggleActive, isExpanded, onToggleExpand }) => {
  const getModelLabel = (model?: string) => {
    switch (model) {
      case 'default': return 'Modelo Padrão';
      case 'gpt-4o': return 'GPT-4o';
      case 'gpt-4o-mini': return 'GPT-4o Mini';
      case 'claude-3-5-sonnet-20240620': return 'Claude 3.5 Sonnet';
      case 'llama-3.1-70b-versatile': return 'Llama 3.1 70B';
      default: return model || 'Modelo Padrão';
    }
  };

  return (
    <Card
      className={cn(
        "transition-all hover:shadow-lg",
        agent.isActive
          ? "border-[#4e4ea8] dark:border-[#0ca7d2]"
          : "border-dashed opacity-70"
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
            <CardDescription className="text-sm line-clamp-2">
              {agent.description}
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
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

        <div className="flex items-center gap-2 text-sm">
          <Zap className="h-4 w-4 text-purple-600" />
          <span className="text-muted-foreground">
            {getModelLabel(agent.model)}
          </span>
        </div>

        <div>
          <Button
            variant="ghost"
            size="sm"
            className="w-full justify-between p-0 h-auto hover:bg-transparent"
            onClick={() => onToggleExpand(agent.id)}
          >
            <span className="text-sm text-muted-foreground">
              🔖 {agent.topics.length} tópicos configurados
            </span>
            {isExpanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </Button>

          {isExpanded && (
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
        <Button variant="outline" size="sm" onClick={() => onEdit(agent)} className="flex-1">
          <Edit className="h-3 w-3 mr-1" /> Editar
        </Button>
        <Button variant="outline" size="sm" onClick={() => onToggleActive(agent)} className="flex-1">
          {agent.isActive ? 'Pausar' : 'Ativar'}
        </Button>
        <Button variant="destructive" size="sm" onClick={() => onDelete(agent.id)}>
          <Trash2 className="h-3 w-3" />
        </Button>
      </CardFooter>
    </Card>
  );
};

// --- SubAgentModal Component ---
interface SubAgentModalProps {
  isOpen: boolean;
  onClose: () => void;
  formData: Partial<SubAgent>;
  setFormData: React.Dispatch<React.SetStateAction<Partial<SubAgent>>>;
  onSave: () => void;
  isSaving: boolean;
  editingAgent: SubAgent | null;
  addTopic: () => void;
  removeTopic: (index: number) => void;
}

const SubAgentModal: React.FC<SubAgentModalProps> = ({
  isOpen, onClose, formData, setFormData, onSave, isSaving, editingAgent, addTopic, removeTopic
}) => {
  const isEdit = !!editingAgent;

  const handleBasicChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-[#4e4ea8]">
            {isEdit ? 'Editar Especialista' : 'Novo Agente Especialista'}
          </DialogTitle>
          <DialogDescription>
            Configure um agente que o Renus (Orquestrador) poderá chamar para tarefas específicas.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nome do Especialista *</Label>
            <Input
              id="name"
              placeholder="Ex: Especialista em Vendas, Suporte Técnico"
              value={formData.name || ''}
              onChange={handleBasicChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Descrição (Para o Orquestrador) *</Label>
            <Textarea
              id="description"
              placeholder="Descreva quando esse agente deve ser acionado. Ex: 'Responde dúvidas sobre preços e planos'."
              rows={2}
              value={formData.description || ''}
              onChange={handleBasicChange}
            />
          </div>

          <div className="space-y-2">
            <Label>Canal Principal</Label>
            <RadioGroup
              value={formData.channel}
              onValueChange={(value) => setFormData(prev => ({ ...prev, channel: value as 'site' | 'whatsapp' }))}
              className="flex gap-4"
            >
              <div className="flex items-center space-x-2"><RadioGroupItem value="whatsapp" id="whatsapp" /><Label htmlFor="whatsapp">WhatsApp</Label></div>
              <div className="flex items-center space-x-2"><RadioGroupItem value="site" id="site" /><Label htmlFor="site">Site/Web</Label></div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label>Modelo de IA</Label>
            <Select
              value={formData.model || 'gpt-4o-mini'}
              onValueChange={(value) => setFormData(prev => ({ ...prev, model: value }))}
            >
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="gpt-4o-mini">GPT-4o Mini (Rápido/Econômico)</SelectItem>
                <SelectItem value="gpt-4o">GPT-4o (Inteligente)</SelectItem>
                <SelectItem value="claude-3-5-sonnet-20240620">Claude 3.5 Sonnet</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="systemPrompt">Instruções do Especialista (System Prompt) *</Label>
            <Textarea
              id="systemPrompt"
              placeholder="Você é um especialista em... Seu objetivo é..."
              rows={6}
              className="font-mono text-sm"
              value={formData.systemPrompt || ''}
              onChange={handleBasicChange}
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Tópicos de Especialidade</Label>
              <Button type="button" variant="outline" size="sm" onClick={addTopic}><Plus className="h-3 w-3 mr-1" /> Add</Button>
            </div>
            <div className="flex flex-wrap gap-2 min-h-[40px] p-2 border rounded-lg bg-gray-50 dark:bg-gray-900">
              {(formData.topics || []).length === 0 && <span className="text-sm text-muted-foreground p-1">Nenhum tópico definido</span>}
              {(formData.topics || []).map((topic, index) => (
                <Badge key={index} variant="secondary" className="flex items-center gap-1">
                  {topic}
                  <button type="button" onClick={() => removeTopic(index)} className="hover:text-destructive ml-1">×</button>
                </Badge>
              ))}
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isSaving}>Cancelar</Button>
          <Button onClick={onSave} disabled={isSaving} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
            {isSaving && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
            {isEdit ? 'Salvar Alterações' : 'Criar Agente'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

// --- Main Component ---
export const SubAgentsTab = () => {
  const [subAgents, setSubAgents] = useState<SubAgent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editingAgent, setEditingAgent] = useState<SubAgent | null>(null);
  const [isExpanded, setIsExpanded] = useState<{ [key: string]: boolean }>({});

  const [formData, setFormData] = useState<Partial<SubAgent>>({
    name: '',
    description: '',
    channel: 'whatsapp',
    systemPrompt: '',
    topics: [],
    isActive: true,
    model: 'gpt-4o-mini',
  });

  const { user } = { user: { id: "mock-user" } }; // Placeholder if useAuth is not available
  // To verify: we assume fetching listAgents handles auth via cookies/headers

  useEffect(() => {
    loadSubAgents();
  }, []);

  const loadSubAgents = async () => {
    setIsLoading(true);
    try {
      // Fetch agents where role is 'sub_agent'
      // Using Type Assertion strictly to handle response structure
      const agents: any[] = await agentService.listAgents({ role: 'sub_agent' } as any);

      const mapped: SubAgent[] = agents.map((a: any) => ({
        id: a.id,
        name: a.name,
        description: a.description || '',
        isActive: a.status === 'active' || a.is_active,
        channel: a.config?.channel || 'whatsapp',
        systemPrompt: a.config?.identity?.system_prompt || '',
        topics: a.config?.topics || [],
        model: a.config?.model || 'gpt-4o-mini',
        useFineTuning: false
      }));
      setSubAgents(mapped);
    } catch (error) {
      console.error(error);
      toast.error("Erro ao carregar sub-agentes.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenModal = (agent?: SubAgent) => {
    if (agent) {
      setEditingAgent(agent);
      setFormData(agent);
    } else {
      setEditingAgent(null);
      setFormData({
        name: '', description: '', channel: 'whatsapp', systemPrompt: '',
        topics: [], isActive: true, model: 'gpt-4o-mini'
      });
    }
    setIsModalOpen(true);
  };

  const handleSave = async () => {
    if (!formData.name || !formData.systemPrompt) {
      toast.error("Nome e Prompt são obrigatórios");
      return;
    }
    setIsSaving(true);
    try {
      const payload = {
        name: formData.name,
        description: formData.description,
        role: 'sub_agent',
        status: formData.isActive ? 'active' : 'paused',
        is_active: formData.isActive,
        config: {
          channel: formData.channel,
          model: formData.model,
          topics: formData.topics,
          identity: {
            system_prompt: formData.systemPrompt
          }
        }
      };

      if (editingAgent) {
        await agentService.updateAgent(editingAgent.id, payload as any);
        toast.success("Agente atualizado!");
      } else {
        // Need clientId. If auth context missing, backend *might* infer, or we rely on user context
        // Assuming the createAgent endpoint handles user context.
        await agentService.createAgent(payload as any);
        toast.success("Agente criado!");
      }
      loadSubAgents();
      setIsModalOpen(false);
    } catch (error) {
      console.error(error);
      toast.error("Erro ao salvar agente.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Tem certeza que deseja excluir este especialista?")) return;
    try {
      await agentService.deleteAgent(id);
      setSubAgents(prev => prev.filter(a => a.id !== id));
      toast.success("Agente removido.");
    } catch (error) {
      toast.error("Erro ao excluir.");
    }
  };

  const handleToggleActive = async (agent: SubAgent) => {
    try {
      const newStatus = !agent.isActive;
      const statusStr = newStatus ? 'active' : 'paused';

      // Optimistic update
      setSubAgents(prev => prev.map(a => a.id === agent.id ? { ...a, isActive: newStatus } : a));

      await agentService.changeAgentStatus(agent.id, statusStr);
      toast.success(`Agente ${newStatus ? 'ativado' : 'pausado'}.`);
    } catch (error) {
      toast.error("Erro ao alterar status.");
      loadSubAgents(); // Revert
    }
  };

  const addTopic = () => {
    const topicInput = prompt('Nome do tópico:');
    if (topicInput) {
      setFormData(prev => ({ ...prev, topics: [...(prev.topics || []), topicInput] }));
    }
  };

  const removeTopic = (index: number) => {
    setFormData(prev => ({ ...prev, topics: (prev.topics || []).filter((_, i) => i !== index) }));
  };

  const handleToggleExpand = (id: string) => setIsExpanded(prev => ({ ...prev, [id]: !prev[id] }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[#4e4ea8] dark:text-[#0ca7d2]">Especialistas (Sub-Agentes)</h2>
          <p className="text-muted-foreground mt-1">
            Gerencie o time de agentes especializados que o Renus pode acionar.
          </p>
        </div>
        <Button onClick={() => handleOpenModal()} className="bg-[#FF6B35] hover:bg-[#e55f30]">
          <Plus className="h-4 w-4 mr-2" /> Novo Especialista
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12"><Loader2 className="h-8 w-8 animate-spin text-muted-foreground" /></div>
      ) : (
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
          {subAgents.length === 0 && (
            <Card className="col-span-full border-dashed py-12 text-center text-muted-foreground">
              <p>Nenhum agente especialista encontrado.</p>
              <Button variant="link" onClick={() => handleOpenModal()}>Criar o primeiro</Button>
            </Card>
          )}
        </div>
      )}

      <SubAgentModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        formData={formData}
        setFormData={setFormData}
        onSave={handleSave}
        isSaving={isSaving}
        editingAgent={editingAgent}
        addTopic={addTopic}
        removeTopic={removeTopic}
      />
    </div>
  );
};

export default SubAgentsTab;