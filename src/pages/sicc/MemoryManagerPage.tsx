import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { agentService } from '@/services/agentService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Brain, Search, Plus, Filter, FileText, Lightbulb, BookOpen, ArrowLeft, Edit, Trash2 } from 'lucide-react';
import { toast } from 'sonner';

export default function MemoryManagerPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [memories, setMemories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [agent, setAgent] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Modal states - Bug #1 e #2
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedMemory, setSelectedMemory] = useState<any>(null);
  const [formData, setFormData] = useState({
    content: '',
    type: 'general',
    confidence: 0.8
  });
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const init = async () => {
      if (!slug) {
        setError('Slug do agente não fornecido');
        setLoading(false);
        return;
      }
      
      try {
        // Busca agente pelo slug da URL
        const agentData = await agentService.getAgentBySlug(slug);
        if (agentData) {
          setAgent(agentData);
          loadMemories(agentData.id);
        } else {
          setError(`Agente "${slug}" não encontrado`);
          setLoading(false);
        }
      } catch (error) {
        console.error('Error fetching agent:', error);
        setError('Erro ao carregar agente');
        setLoading(false);
      }
    };
    init();
  }, [slug]);

  const loadMemories = async (id: string) => {
    try {
      setLoading(true);
      const data: any = await siccService.listMemories(id);
      setMemories(Array.isArray(data) ? data : (data?.items || []));
    } catch (error) {
      console.error('Erro ao carregar memórias:', error);
      setMemories([]);
    } finally {
      setLoading(false);
    }
  };

  const getMemoryIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'faq': return <FileText className="h-4 w-4" />;
      case 'strategy': return <Lightbulb className="h-4 w-4" />;
      case 'business_term': return <BookOpen className="h-4 w-4" />;
      default: return <Brain className="h-4 w-4" />;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'faq': return 'FAQ';
      case 'strategy': return 'Estratégia';
      case 'business_term': return 'Termo Negócio';
      default: return 'Geral';
    }
  };

  // Bug #1 - Função para abrir modal de edição
  const handleEditMemory = (memory: any) => {
    setSelectedMemory(memory);
    setFormData({
      content: memory.content || '',
      type: memory.type || 'general',
      confidence: memory.confidence || 0.8
    });
    setIsEditModalOpen(true);
  };

  // Bug #2 - Função para abrir modal de criação
  const handleCreateMemory = () => {
    setSelectedMemory(null);
    setFormData({
      content: '',
      type: 'general',
      confidence: 0.8
    });
    setIsCreateModalOpen(true);
  };

  // Salvar memória (criar ou editar)
  const handleSaveMemory = async () => {
    // Validação robusta do agent_id
    if (!agent?.id) {
      toast.error('Erro: Agente não carregado corretamente');
      console.error('Agent ID is missing:', agent);
      return;
    }
    
    if (!formData.content.trim()) {
      toast.error('Conteúdo da memória é obrigatório');
      return;
    }

    setIsSaving(true);
    try {
      if (selectedMemory) {
        // Editar memória existente - Bug #1 corrigido
        await siccService.updateMemory(selectedMemory.id, {
          content: formData.content,
          chunk_type: formData.type,
          confidence_score: formData.confidence  // Backend espera confidence_score
        });
        toast.success('Memória atualizada com sucesso!');
      } else {
        // Criar nova memória - Garantir que agent.id é válido
        console.log('Creating memory with agent_id:', agent.id);
        await siccService.createMemory(agent.id, {
          content: formData.content,
          chunk_type: formData.type,
          confidence_score: formData.confidence  // Backend espera confidence_score
        });
        toast.success('Memória criada com sucesso!');
      }
      
      // Recarregar lista
      loadMemories(agent.id);
      setIsCreateModalOpen(false);
      setIsEditModalOpen(false);
    } catch (error) {
      console.error('Erro ao salvar memória:', error);
      toast.error('Erro ao salvar memória');
    } finally {
      setIsSaving(false);
    }
  };

  // Deletar memória
  const handleDeleteMemory = async (memoryId: string) => {
    if (!confirm('Tem certeza que deseja excluir esta memória?')) return;
    
    try {
      await siccService.deleteMemory(memoryId);
      toast.success('Memória excluída com sucesso!');
      if (agent?.id) loadMemories(agent.id);
    } catch (error) {
      console.error('Erro ao excluir memória:', error);
      toast.error('Erro ao excluir memória');
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6 flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="text-center py-12">
            <p className="text-red-500 mb-4">{error}</p>
            <Button onClick={() => navigate('/dashboard/admin/agents')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para Agentes
            </Button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            {/* Bug #3 - Corrigido: Voltar para aba Inteligência, não config geral */}
            <Button variant="ghost" size="sm" onClick={() => navigate(`/dashboard/admin/agents/${slug}?tab=intelligence`)}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar
            </Button>
            <div>
              <h1 className="text-3xl font-bold">🧠 Gerenciador de Memórias</h1>
              <p className="text-muted-foreground">{agent?.name || slug}</p>
            </div>
          </div>
          {/* Bug #2 - Corrigido: onClick para Nova Memória */}
          <Button className="bg-purple-600 hover:bg-purple-700" onClick={handleCreateMemory}>
            <Plus className="h-4 w-4 mr-2" />
            Nova Memória
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Memórias</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{memories.length}</div>
              <Badge variant="secondary" className="mt-1">Ativas</Badge>
            </CardContent>
          </Card>
          {/* Placeholder stats - In a real app we'd compute these or get from stats API */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Tipos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground">
                Estatísticas detalhadas por tipo serão carregadas aqui.
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>📋 Lista de Memórias</CardTitle>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  Buscar
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtrar
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {memories.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground border border-dashed rounded-lg">
                  <Brain className="h-12 w-12 mx-auto mb-3 opacity-20" />
                  <p>Nenhuma memória encontrada no banco de dados.</p>
                  <p className="text-xs">O agente ainda não aprendeu nada ou o banco foi resetado.</p>
                </div>
              ) : (
                memories.map((memory: any) => (
                  <div key={memory.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="secondary" className="flex items-center gap-1">
                            {getMemoryIcon(memory.type)}
                            {getTypeLabel(memory.type)}
                          </Badge>
                          <Badge variant="outline">Confiança: {(memory.confidence * 100).toFixed(0)}%</Badge>
                        </div>
                        <p className="text-sm font-medium mb-1">
                          {memory.content}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Usado {memory.usage_count || 0} vezes • Criado em {new Date(memory.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      {/* Bug #1 - Corrigido: onClick para Editar */}
                      <div className="flex gap-2">
                        <Button variant="ghost" size="sm" onClick={() => handleEditMemory(memory)}>
                          <Edit className="h-4 w-4 mr-1" />
                          Editar
                        </Button>
                        <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-700" onClick={() => handleDeleteMemory(memory.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        {/* Modal de Criação - Bug #2 */}
        <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>🧠 Nova Memória</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Conteúdo</label>
                <Textarea
                  placeholder="Digite o conteúdo da memória..."
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  rows={4}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Tipo</label>
                <Select value={formData.type} onValueChange={(value) => setFormData({ ...formData, type: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">Geral</SelectItem>
                    <SelectItem value="faq">FAQ</SelectItem>
                    <SelectItem value="strategy">Estratégia</SelectItem>
                    <SelectItem value="business_term">Termo de Negócio</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Confiança ({Math.round(formData.confidence * 100)}%)</label>
                <Input
                  type="range"
                  min="0"
                  max="100"
                  value={formData.confidence * 100}
                  onChange={(e) => setFormData({ ...formData, confidence: parseInt(e.target.value) / 100 })}
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateModalOpen(false)}>Cancelar</Button>
              <Button onClick={handleSaveMemory} disabled={isSaving} className="bg-purple-600 hover:bg-purple-700">
                {isSaving ? 'Salvando...' : 'Criar Memória'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Modal de Edição - Bug #1 */}
        <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>✏️ Editar Memória</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Conteúdo</label>
                <Textarea
                  placeholder="Digite o conteúdo da memória..."
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  rows={4}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Tipo</label>
                <Select value={formData.type} onValueChange={(value) => setFormData({ ...formData, type: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">Geral</SelectItem>
                    <SelectItem value="faq">FAQ</SelectItem>
                    <SelectItem value="strategy">Estratégia</SelectItem>
                    <SelectItem value="business_term">Termo de Negócio</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Confiança ({Math.round(formData.confidence * 100)}%)</label>
                <Input
                  type="range"
                  min="0"
                  max="100"
                  value={formData.confidence * 100}
                  onChange={(e) => setFormData({ ...formData, confidence: parseInt(e.target.value) / 100 })}
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditModalOpen(false)}>Cancelar</Button>
              <Button onClick={handleSaveMemory} disabled={isSaving} className="bg-purple-600 hover:bg-purple-700">
                {isSaving ? 'Salvando...' : 'Salvar Alterações'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
}