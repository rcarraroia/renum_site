import React, { useState, useEffect, useMemo, useCallback } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Brain, Search, Edit, Trash2, Eye, Filter, Users, ChevronDown, ChevronUp, Loader2, CheckCircle, XCircle, Copy, Clock, ArrowLeft, ArrowRight, Save, Sliders, Plus } from 'lucide-react';
import { siccService } from '@/services/siccService';
import { Memory, MemoryLayer, MemoryChunkType } from '@/types/sicc';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Skeleton } from '@/components/ui/skeleton';

// --- Tipos de Modais ---
type ModalType = 'view' | 'edit' | 'none';

// --- Constantes de Filtro ---
const MEMORY_TYPES: MemoryChunkType[] = ['FAQ', 'Business Term', 'Response Strategy', 'Script'];
const MEMORY_LAYERS: MemoryLayer[] = ['base', 'company', 'niche', 'individual'];
const CONFIDENCE_OPTIONS = ['0.9', '0.8', '0.7'];

// --- Componente Principal ---
const MemoryManagerPage: React.FC = () => {
  const [agents, setAgents] = useState<{ id: string; name: string }[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>(undefined);
  
  const [memories, setMemories] = useState<Memory[]>([]);
  const [totalMemories, setTotalMemories] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [perPage, setPerPage] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    chunk_type: 'all',
    layer: 'all',
    is_active: 'true', // Default to active
    quality_score: 'all',
  });
  const [isFilterExpanded, setIsFilterExpanded] = useState(false);
  
  const [selectedMemoryIds, setSelectedMemoryIds] = useState<string[]>([]);
  const [activeModal, setActiveModal] = useState<ModalType>('none');
  const [currentMemory, setCurrentMemory] = useState<Memory | null>(null);
  const [editFormData, setEditFormData] = useState<Partial<Memory>>({});

  // --- Handlers de Dados e API ---

  const fetchMemories = useCallback(async (page: number, search: string, currentFilters: typeof filters) => {
    if (!selectedAgentId) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await siccService.listMemories(selectedAgentId, page, perPage, search, currentFilters);
      setMemories(response.data);
      setTotalMemories(response.total);
    } catch (err) {
      setError("Falha ao carregar memórias.");
      toast.error("Falha ao carregar memórias.");
    } finally {
      setIsLoading(false);
    }
  }, [selectedAgentId, perPage]);

  // Fetch agents on mount
  useEffect(() => {
    siccService.getAgents().then(data => {
      setAgents(data);
      if (data.length > 0) {
        setSelectedAgentId(data[0].id);
      }
    }).catch(() => toast.error("Não foi possível carregar a lista de agentes."));
  }, []);

  // Fetch memories when agent, page, or filters change
  useEffect(() => {
    if (selectedAgentId) {
      fetchMemories(currentPage, searchTerm, filters);
    }
  }, [selectedAgentId, currentPage, filters, fetchMemories]);

  // Debounce search term
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      setCurrentPage(1);
      fetchMemories(1, searchTerm, filters);
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  // --- Handlers de Ações ---

  const handleFilterChange = (key: keyof typeof filters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedMemoryIds(memories.map(m => m.id));
    } else {
      setSelectedMemoryIds([]);
    }
  };

  const handleSelectOne = (id: string, checked: boolean) => {
    if (checked) {
      setSelectedMemoryIds(prev => [...prev, id]);
    } else {
      setSelectedMemoryIds(prev => prev.filter(mid => mid !== id));
    }
  };

  const handleOpenModal = async (type: ModalType, memory: Memory) => {
    setCurrentMemory(memory);
    setActiveModal(type);
    if (type === 'edit') {
      setEditFormData(memory);
    }
    // Fetch full details for view/edit (mocked)
    try {
        const details = await siccService.getMemoryDetails(memory.id);
        setCurrentMemory(details);
        if (type === 'edit') {
            setEditFormData(details);
        }
    } catch (e) {
        toast.error("Erro ao carregar detalhes da memória.");
    }
  };

  const handleCloseModal = () => {
    setActiveModal('none');
    setCurrentMemory(null);
    setEditFormData({});
  };

  const handleSaveEdit = async () => {
    if (!currentMemory) return;
    try {
      await siccService.updateMemory(currentMemory.id, editFormData);
      toast.success("Memória atualizada com sucesso!");
      handleCloseModal();
      fetchMemories(currentPage, searchTerm, filters); // Refresh list
    } catch (e) {
      toast.error("Falha ao salvar edição.");
    }
  };

  const handleArchive = async (id: string) => {
    if (window.confirm("Tem certeza que deseja arquivar esta memória?")) {
      try {
        await siccService.deleteMemory(id);
        toast.warning("Memória arquivada com sucesso.");
        fetchMemories(currentPage, searchTerm, filters); // Refresh list
      } catch (e) {
        toast.error("Falha ao arquivar memória.");
      }
    }
  };

  const handleBulkArchive = async () => {
    if (selectedMemoryIds.length === 0) return;
    if (window.confirm(`Tem certeza que deseja arquivar ${selectedMemoryIds.length} memórias selecionadas?`)) {
      setIsLoading(true);
      try {
        // Simulate bulk operation
        for (const id of selectedMemoryIds) {
          await siccService.deleteMemory(id);
        }
        toast.success(`${selectedMemoryIds.length} memórias arquivadas.`);
        setSelectedMemoryIds([]);
        fetchMemories(currentPage, searchTerm, filters);
      } catch (e) {
        toast.error("Falha ao arquivar em massa.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  // --- Renderização Auxiliar ---

  const getLayerBadge = (layer: MemoryLayer) => {
    const colors = {
      base: 'bg-gray-500',
      company: 'bg-purple-600',
      niche: 'bg-indigo-600',
      individual: 'bg-cyan-500',
    };
    return <Badge className={cn("capitalize text-white", colors[layer])}>{layer}</Badge>;
  };

  const getChunkTypeBadge = (type: MemoryChunkType) => {
    return <Badge variant="outline" className="text-sm">{type}</Badge>;
  };

  const totalPages = Math.ceil(totalMemories / perPage);
  const activeMemoriesCount = totalMemories; // Mock: assuming total is active for simplicity

  // --- Modais ---

  const ViewModal: React.FC = () => (
    <Dialog open={activeModal === 'view'} onOpenChange={handleCloseModal}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-purple-600">
            <Eye className="h-5 w-5 mr-2" /> Visualizar Memória
          </DialogTitle>
          <CardDescription>ID: {currentMemory?.id} | Criado em: {currentMemory?.created_at ? format(new Date(currentMemory.created_at), 'dd/MM/yyyy HH:mm', { locale: ptBR }) : 'N/A'}</CardDescription>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
            <h4 className="text-lg font-semibold flex items-center text-indigo-600"><Brain className="h-4 w-4 mr-2" /> Conteúdo</h4>
            <Textarea readOnly rows={8} defaultValue={currentMemory?.content} className="font-mono text-sm" />
            
            <div className="grid grid-cols-3 gap-4">
                <div><Label>Tipo</Label>{currentMemory && getChunkTypeBadge(currentMemory.chunk_type)}</div>
                <div><Label>Camada</Label>{currentMemory && getLayerBadge(currentMemory.layer)}</div>
                <div><Label>Confiança</Label><Badge className="bg-cyan-500 text-white">{currentMemory?.quality_score.toFixed(2)}</Badge></div>
            </div>

            <h4 className="text-lg font-semibold flex items-center text-cyan-500"><Sliders className="h-4 w-4 mr-2" /> Metadados Técnicos</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
                <div><Label>Uso (Contagem)</Label><p className="font-medium">{currentMemory?.usage_count}</p></div>
                <div><Label>Status</Label><p className="font-medium">{currentMemory?.is_active ? 'Ativa' : 'Arquivada'}</p></div>
                <div><Label>Embedding (Primeiros 5)</Label><p className="font-mono text-xs break-all">{currentMemory?.embedding?.slice(0, 5).join(', ')}...</p></div>
                <div><Label>Histórico</Label><p className="text-xs text-muted-foreground">{currentMemory?.history?.join('; ')}</p></div>
            </div>
            
            <h4 className="text-lg font-semibold flex items-center text-purple-600"><Search className="h-4 w-4 mr-2" /> Memórias Similares (Mock)</h4>
            <ul className="space-y-2 text-sm">
                <li className="p-2 border rounded-lg">Memória 456: FAQ sobre Garantia (Score: 0.95)</li>
                <li className="p-2 border rounded-lg">Memória 789: Termo de Serviço (Score: 0.89)</li>
            </ul>
        </div>
        <DialogFooter>
            <Button variant="outline" onClick={handleCloseModal}>Fechar</Button>
            <Button onClick={() => handleOpenModal('edit', currentMemory!)} className="bg-purple-600 hover:bg-purple-700">
                <Edit className="h-4 w-4 mr-2" /> Editar
            </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const EditModal: React.FC = () => (
    <Dialog open={activeModal === 'edit'} onOpenChange={handleCloseModal}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-purple-600">
            <Edit className="h-5 w-5 mr-2" /> Editar Memória
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
            <div className="space-y-2">
                <Label htmlFor="content">Conteúdo da Memória *</Label>
                <Textarea 
                    id="content" 
                    rows={10} 
                    value={editFormData.content} 
                    onChange={(e) => setEditFormData({...editFormData, content: e.target.value})}
                    className="font-mono text-sm"
                />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="chunk_type">Tipo</Label>
                    <Select value={editFormData.chunk_type} onValueChange={(v) => setEditFormData({...editFormData, chunk_type: v as MemoryChunkType})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            {MEMORY_TYPES.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}
                        </SelectContent>
                    </Select>
                </div>
                <div className="space-y-2">
                    <Label htmlFor="layer">Camada</Label>
                    <Select value={editFormData.layer} onValueChange={(v) => setEditFormData({...editFormData, layer: v as MemoryLayer})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            {MEMORY_LAYERS.map(layer => <SelectItem key={layer} value={layer}>{layer}</SelectItem>)}
                        </SelectContent>
                    </Select>
                </div>
            </div>
            
            <div className="space-y-2">
                <Label htmlFor="quality_score">Confiança (Qualidade)</Label>
                <Input 
                    id="quality_score" 
                    type="number" 
                    step="0.01" 
                    min="0" 
                    max="1" 
                    value={editFormData.quality_score} 
                    onChange={(e) => setEditFormData({...editFormData, quality_score: parseFloat(e.target.value)})}
                />
            </div>
        </div>
        <DialogFooter>
            <Button variant="outline" onClick={handleCloseModal}>Cancelar</Button>
            <Button onClick={handleSaveEdit} className="bg-purple-600 hover:bg-purple-700">
                <Save className="h-4 w-4 mr-2" /> Salvar Alterações
            </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center text-purple-600 dark:text-white">
          <Brain className="h-7 w-7 mr-3" />
          Gerenciador de Memórias
        </h2>
        <div className="flex space-x-4">
            <Select value={selectedAgentId} onValueChange={setSelectedAgentId} disabled={isLoading || agents.length === 0}>
                <SelectTrigger className="w-[200px] bg-white dark:bg-gray-800 border-indigo-600 dark:border-purple-600">
                    <Users className="h-4 w-4 mr-2 text-indigo-600" />
                    <SelectValue placeholder="Selecione o Agente" />
                </SelectTrigger>
                <SelectContent>
                    {agents.map(agent => (
                        <SelectItem key={agent.id} value={agent.id}>{agent.name}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
      </div>
      
      <Card className="mb-6">
        <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                <div className="relative flex-grow w-full md:w-auto">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input 
                        placeholder="Buscar memórias por conteúdo..." 
                        className="pl-10" 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        disabled={isLoading}
                    />
                </div>
                <div className="flex space-x-2 flex-shrink-0 w-full md:w-auto">
                    <Button variant="outline" onClick={() => setIsFilterExpanded(prev => !prev)}>
                        <Filter className="h-4 w-4 mr-2" /> Filtros
                        {isFilterExpanded ? <ChevronUp className="h-4 w-4 ml-2" /> : <ChevronDown className="h-4 w-4 ml-2" />}
                    </Button>
                    <Button className="bg-purple-600 hover:bg-purple-700">
                        <Plus className="h-4 w-4 mr-2" /> Nova
                    </Button>
                </div>
            </div>
            
            {isFilterExpanded && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-900">
                    <Select value={filters.chunk_type} onValueChange={(v) => handleFilterChange('chunk_type', v)}>
                        <SelectTrigger><SelectValue placeholder="Tipo" /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Todos os Tipos</SelectItem>
                            {MEMORY_TYPES.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}
                        </SelectContent>
                    </Select>
                    <Select value={filters.layer} onValueChange={(v) => handleFilterChange('layer', v)}>
                        <SelectTrigger><SelectValue placeholder="Camada" /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Todas as Camadas</SelectItem>
                            {MEMORY_LAYERS.map(layer => <SelectItem key={layer} value={layer}>{layer.charAt(0).toUpperCase() + layer.slice(1)}</SelectItem>)}
                        </SelectContent>
                    </Select>
                    <Select value={filters.is_active} onValueChange={(v) => handleFilterChange('is_active', v)}>
                        <SelectTrigger><SelectValue placeholder="Status" /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Todos os Status</SelectItem>
                            <SelectItem value="true">Ativa</SelectItem>
                            <SelectItem value="false">Arquivada</SelectItem>
                        </SelectContent>
                    </Select>
                    <Select value={filters.quality_score} onValueChange={(v) => handleFilterChange('quality_score', v)}>
                        <SelectTrigger><SelectValue placeholder="Confiança" /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Todas</SelectItem>
                            {CONFIDENCE_OPTIONS.map(score => <SelectItem key={score} value={score}>{`> ${score}`}</SelectItem>)}
                        </SelectContent>
                    </Select>
                </div>
            )}
            
            {selectedMemoryIds.length > 0 && (
                <div className="mt-4 flex items-center space-x-3 p-3 bg-indigo-50 dark:bg-indigo-900/50 rounded-lg">
                    <span className="text-sm font-medium text-indigo-700 dark:text-indigo-300">{selectedMemoryIds.length} memórias selecionadas.</span>
                    <Button variant="destructive" size="sm" onClick={handleBulkArchive} disabled={isLoading}>
                        <Trash2 className="h-4 w-4 mr-2" /> Arquivar Selecionadas
                    </Button>
                </div>
            )}
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
            <div className="rounded-md border overflow-x-auto">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[50px]">
                                <Checkbox 
                                    checked={selectedMemoryIds.length === memories.length && memories.length > 0}
                                    onCheckedChange={(checked) => handleSelectAll(checked as boolean)}
                                    disabled={isLoading || memories.length === 0}
                                />
                            </TableHead>
                            <TableHead className="min-w-[300px]">Conteúdo</TableHead>
                            <TableHead>Tipo</TableHead>
                            <TableHead>Camada</TableHead>
                            <TableHead>Confiança</TableHead>
                            <TableHead>Uso</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Ações</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            Array.from({ length: perPage }).map((_, i) => (
                                <TableRow key={i}>
                                    <TableCell colSpan={8}><Skeleton className="h-6 w-full" /></TableCell>
                                </TableRow>
                            ))
                        ) : memories.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} className="h-24 text-center text-muted-foreground">
                                    <Brain className="h-6 w-6 mx-auto mb-2" />
                                    Nenhuma memória encontrada com os filtros atuais.
                                </TableCell>
                            </TableRow>
                        ) : (
                            memories.map((memory) => (
                                <TableRow key={memory.id} className={cn(!memory.is_active && 'opacity-50')}>
                                    <TableCell>
                                        <Checkbox 
                                            checked={selectedMemoryIds.includes(memory.id)}
                                            onCheckedChange={(checked) => handleSelectOne(memory.id, checked as boolean)}
                                        />
                                    </TableCell>
                                    <TableCell className="font-medium max-w-[300px] truncate hover:whitespace-normal hover:overflow-visible cursor-pointer" onClick={() => handleOpenModal('view', memory)}>
                                        {memory.content}
                                    </TableCell>
                                    <TableCell>{getChunkTypeBadge(memory.chunk_type)}</TableCell>
                                    <TableCell>{getLayerBadge(memory.layer)}</TableCell>
                                    <TableCell className="font-semibold text-cyan-500">{memory.quality_score.toFixed(2)}</TableCell>
                                    <TableCell>{memory.usage_count}</TableCell>
                                    <TableCell>
                                        {memory.is_active ? (
                                            <CheckCircle className="h-4 w-4 text-green-500" />
                                        ) : (
                                            <XCircle className="h-4 w-4 text-red-500" />
                                        )}
                                    </TableCell>
                                    <TableCell className="text-right space-x-1">
                                        <Button variant="ghost" size="icon" onClick={() => handleOpenModal('view', memory)}><Eye className="h-4 w-4" /></Button>
                                        <Button variant="ghost" size="icon" onClick={() => handleOpenModal('edit', memory)}><Edit className="h-4 w-4" /></Button>
                                        <Button variant="destructive" size="icon" onClick={() => handleArchive(memory.id)} disabled={!memory.is_active}><Trash2 className="h-4 w-4" /></Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </CardContent>
        <CardFooter className="flex justify-between items-center border-t pt-4">
            <div className="text-sm text-muted-foreground">
                📊 {totalMemories.toLocaleString()} memórias • {activeMemoriesCount} ativas.
            </div>
            <div className="flex items-center space-x-2">
                <Button 
                    variant="outline" 
                    size="icon" 
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1 || isLoading}
                >
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <span className="text-sm text-muted-foreground">Página {currentPage} de {totalPages}</span>
                <Button 
                    variant="outline" 
                    size="icon" 
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages || isLoading}
                >
                    <ArrowRight className="h-4 w-4" />
                </Button>
            </div>
        </CardFooter>
      </Card>

      {/* Modals */}
      {currentMemory && activeModal === 'view' && <ViewModal />}
      {currentMemory && activeModal === 'edit' && <EditModal />}
    </DashboardLayout>
  );
};

export default MemoryManagerPage;