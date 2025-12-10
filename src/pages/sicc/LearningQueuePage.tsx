import React, { useState, useEffect, useCallback, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Clock, CheckCircle, XCircle, Eye, AlertTriangle, Users, Loader2, Brain, ArrowRight, MessageSquare } from 'lucide-react';
import { siccService } from '@/services/siccService';
import { Learning, LearningQueueResponse, LearningStatus, LearningType } from '@/types/sicc';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Progress } from '@/components/ui/progress';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';

// --- Constantes ---
const REFRESH_INTERVAL = 30000; // 30 segundos
const LEARNING_TYPES: Record<LearningType, string> = {
    memory_added: 'Nova Memória',
    pattern_detected: 'Padrão Detectado',
    behavior_updated: 'Comportamento Atualizado',
};

// --- Componentes Auxiliares ---

interface LearningCardProps {
    learning: Learning;
    onSelect: (id: string, checked: boolean) => void;
    isSelected: boolean;
    onOpenDetails: (learning: Learning) => void;
    onApprove: (id: string) => void;
    onReject: (learning: Learning) => void;
    activeTab: LearningStatus;
}

const LearningCard: React.FC<LearningCardProps> = ({ learning, onSelect, isSelected, onOpenDetails, onApprove, onReject, activeTab }) => {
    const confidence = Math.round(learning.quality_score * 100);
    const isPending = activeTab === 'pending';
    
    const getConfidenceColor = (score: number) => {
        if (score >= 0.8) return 'bg-green-600';
        if (score >= 0.6) return 'bg-yellow-500';
        return 'bg-orange-500';
    };

    const getStatusIcon = (status: LearningStatus) => {
        switch (status) {
            case 'approved': return <CheckCircle className="h-4 w-4 text-green-600" />;
            case 'rejected': return <XCircle className="h-4 w-4 text-red-600" />;
            default: return <Clock className="h-4 w-4 text-yellow-500" />;
        }
    };

    return (
        <Card className={cn("p-4 transition-all", isSelected && isPending ? "border-2 border-purple-600 dark:border-indigo-600 bg-purple-50/50 dark:bg-gray-800" : "hover:shadow-md")}>
            <div className="flex items-start space-x-3">
                {isPending && (
                    <Checkbox 
                        checked={isSelected} 
                        onCheckedChange={(checked) => onSelect(learning.id, checked as boolean)}
                        className="mt-1 h-5 w-5 flex-shrink-0"
                    />
                )}
                <div className="flex-grow space-y-2">
                    <div className="flex items-center justify-between">
                        <h4 className="font-semibold text-lg flex items-center">
                            {getStatusIcon(learning.status)}
                            <span className="ml-2">{learning.title}</span>
                        </h4>
                        <Badge className={cn("text-white", getConfidenceColor(learning.quality_score))}>
                            Confiança: {confidence}%
                        </Badge>
                    </div>
                    
                    <div className="text-sm text-muted-foreground">
                        <p>Tipo: <Badge variant="secondary">{LEARNING_TYPES[learning.learning_type]}</Badge></p>
                        <p className="mt-1 line-clamp-2">
                            <Brain className="h-4 w-4 mr-1 inline text-indigo-600" /> 
                            Análise ISA: {learning.analysis}
                        </p>
                    </div>
                    
                    <div className="flex justify-between items-center text-xs pt-2 border-t dark:border-gray-700">
                        <p>
                            {learning.status === 'pending' 
                                ? `Criado ${formatDistanceToNow(new Date(learning.created_at), { addSuffix: true, locale: ptBR })}`
                                : `Revisado por ${learning.reviewed_by} ${formatDistanceToNow(new Date(learning.reviewed_at!), { addSuffix: true, locale: ptBR })}`
                            }
                        </p>
                        <div className="flex space-x-2">
                            <Button variant="outline" size="sm" onClick={() => onOpenDetails(learning)}>
                                <Eye className="h-4 w-4 mr-1" /> Ver Detalhes
                            </Button>
                            {isPending && (
                                <>
                                    <Button size="sm" className="bg-green-600 hover:bg-green-700" onClick={() => onApprove(learning.id)}>
                                        <CheckCircle className="h-4 w-4 mr-1" /> Aprovar
                                    </Button>
                                    <Button size="sm" className="bg-red-600 hover:bg-red-700" onClick={() => onReject(learning)}>
                                        <XCircle className="h-4 w-4 mr-1" /> Rejeitar
                                    </Button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </Card>
    );
};

// --- Componente Principal ---

const LearningQueuePage: React.FC = () => {
    const [agents, setAgents] = useState<{ id: string; name: string }[]>([]);
    const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>(undefined);
    const [activeTab, setActiveTab] = useState<LearningStatus>('pending');
    
    const [queueData, setQueueData] = useState<LearningQueueResponse>({ data: [], stats: { pending: 0, approved: 0, rejected: 0, approval_rate: 0 } });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const [selectedLearnings, setSelectedLearnings] = useState<string[]>([]);
    
    const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
    const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
    const [currentLearning, setCurrentLearning] = useState<Learning | null>(null);
    const [rejectionReason, setRejectionReason] = useState('');

    // --- Fetch Data ---
    const fetchQueue = useCallback(async (agentId: string, status: LearningStatus) => {
        if (!agentId) return;
        setIsLoading(true);
        setError(null);
        try {
            const response = await siccService.getLearningQueue(agentId, status);
            setQueueData(response);
        } catch (err) {
            setError("Falha ao carregar a fila de aprendizados.");
            toast.error("Falha ao carregar a fila de aprendizados.");
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Fetch agents on mount
    useEffect(() => {
        siccService.getAgents().then(data => {
            setAgents(data);
            if (data.length > 0) {
                setSelectedAgentId(data[0].id);
            }
        });
    }, []);

    // Fetch queue when agent or tab changes
    useEffect(() => {
        if (selectedAgentId) {
            fetchQueue(selectedAgentId, activeTab);
            setSelectedLearnings([]); // Clear selection on tab change
        }
    }, [selectedAgentId, activeTab, fetchQueue]);

    // Auto-refresh for pending tab
    useEffect(() => {
        if (activeTab === 'pending' && selectedAgentId) {
            const interval = setInterval(() => {
                fetchQueue(selectedAgentId, 'pending');
            }, REFRESH_INTERVAL);
            return () => clearInterval(interval);
        }
    }, [activeTab, selectedAgentId, fetchQueue]);

    // --- Handlers de Ações ---

    const handleApprove = async (id: string) => {
        try {
            await siccService.approveLearning(id);
            toast.success(`Aprendizado ${id} aprovado e adicionado à memória.`);
            fetchQueue(selectedAgentId!, activeTab);
        } catch (e) {
            toast.error("Falha ao aprovar.");
        }
    };

    const handleReject = (learning: Learning) => {
        setCurrentLearning(learning);
        setRejectionReason('');
        setIsRejectModalOpen(true);
    };

    const handleConfirmReject = async () => {
        if (rejectionReason.length < 10) {
            toast.error("O motivo da rejeição deve ter no mínimo 10 caracteres.");
            return;
        }
        try {
            await siccService.rejectLearning(currentLearning!.id, rejectionReason);
            toast.warning(`Aprendizado ${currentLearning!.id} rejeitado.`);
            setIsRejectModalOpen(false);
            fetchQueue(selectedAgentId!, activeTab);
        } catch (e) {
            toast.error("Falha ao rejeitar.");
        }
    };

    const handleBatchApprove = async () => {
        if (selectedLearnings.length === 0) return;
        if (window.confirm(`Aprovar ${selectedLearnings.length} aprendizados?`)) {
            try {
                await siccService.batchApproveLearning(selectedLearnings);
                toast.success(`${selectedLearnings.length} aprendizados aprovados em lote.`);
                setSelectedLearnings([]);
                fetchQueue(selectedAgentId!, activeTab);
            } catch (e) {
                toast.error("Falha ao aprovar em lote.");
            }
        }
    };

    const handleBatchReject = () => {
        if (selectedLearnings.length === 0) return;
        setCurrentLearning(null); // Use null to indicate batch action
        setRejectionReason('');
        setIsRejectModalOpen(true);
    };

    const handleConfirmBatchReject = async () => {
        if (rejectionReason.length < 10) {
            toast.error("O motivo da rejeição deve ter no mínimo 10 caracteres.");
            return;
        }
        try {
            await siccService.batchRejectLearning(selectedLearnings, rejectionReason);
            toast.warning(`${selectedLearnings.length} aprendizados rejeitados em lote.`);
            setSelectedLearnings([]);
            setIsRejectModalOpen(false);
            fetchQueue(selectedAgentId!, activeTab);
        } catch (e) {
            toast.error("Falha ao rejeitar em lote.");
        }
    };

    const handleSelectOne = (id: string, checked: boolean) => {
        setSelectedLearnings(prev => 
            checked ? [...prev, id] : prev.filter(lid => lid !== id)
        );
    };

    const handleSelectAll = (checked: boolean) => {
        if (checked) {
            setSelectedLearnings(queueData.data.map(l => l.id));
        } else {
            setSelectedLearnings([]);
        }
    };

    const isAllSelected = queueData.data.length > 0 && selectedLearnings.length === queueData.data.length;

    // --- Modais ---

    const DetailsModal: React.FC = () => {
        if (!currentLearning) return null;
        const confidence = Math.round(currentLearning.quality_score * 100);
        
        return (
            <Dialog open={isDetailsModalOpen} onOpenChange={setIsDetailsModalOpen}>
                <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
                    <DialogHeader>
                        <DialogTitle className="flex items-center text-purple-600">
                            <Eye className="h-5 w-5 mr-2" /> Detalhes do Aprendizado
                        </DialogTitle>
                        <CardDescription>{currentLearning.title}</CardDescription>
                    </DialogHeader>
                    
                    <div className="space-y-4 py-4">
                        <div className="grid grid-cols-3 gap-4">
                            <div><Label>Tipo</Label><Badge variant="secondary">{LEARNING_TYPES[currentLearning.learning_type]}</Badge></div>
                            <div><Label>Criado em</Label><p className="text-sm">{format(new Date(currentLearning.created_at), 'dd/MM/yyyy HH:mm')}</p></div>
                            <div><Label>Status</Label><Badge className={cn("text-white", currentLearning.status === 'approved' ? 'bg-green-600' : currentLearning.status === 'rejected' ? 'bg-red-600' : 'bg-yellow-500')}>{currentLearning.status.toUpperCase()}</Badge></div>
                        </div>

                        <div className="space-y-2">
                            <Label>Confiança ISA ({confidence}%)</Label>
                            <Progress value={confidence} className="h-3 [&>div]:bg-cyan-500" />
                        </div>

                        <h4 className="text-lg font-semibold flex items-center text-indigo-600"><Brain className="h-4 w-4 mr-2" /> Análise ISA Completa</h4>
                        <Textarea readOnly rows={6} defaultValue={currentLearning.analysis} className="font-mono text-sm" />
                        
                        <h4 className="text-lg font-semibold flex items-center text-cyan-500"><AlertTriangle className="h-4 w-4 mr-2" /> Impacto Estimado</h4>
                        <p className="text-sm text-muted-foreground">{currentLearning.source_data.impact_estimate}</p>

                        <h4 className="text-lg font-semibold flex items-center text-purple-600"><MessageSquare className="h-4 w-4 mr-2" /> Conversas de Origem ({currentLearning.source_data.conversations.length})</h4>
                        <ul className="space-y-1 text-sm">
                            {currentLearning.source_data.conversations.map(conv => (
                                <li key={conv.id} className="flex justify-between p-2 border rounded-lg">
                                    <span>Conversa #{conv.id}</span>
                                    <span className="text-xs text-muted-foreground">{conv.date}</span>
                                </li>
                            ))}
                        </ul>
                        
                        {currentLearning.status === 'rejected' && currentLearning.rejection_reason && (
                            <div className="p-3 bg-red-50 dark:bg-red-900/50 border border-red-300 rounded-lg">
                                <Label className="text-red-600">Motivo da Rejeição:</Label>
                                <p className="text-sm text-red-700 dark:text-red-300">{currentLearning.rejection_reason}</p>
                            </div>
                        )}
                    </div>
                    
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsDetailsModalOpen(false)}>Fechar</Button>
                        {currentLearning.status === 'pending' && (
                            <>
                                <Button className="bg-red-600 hover:bg-red-700" onClick={() => { setIsDetailsModalOpen(false); handleReject(currentLearning); }}>
                                    <XCircle className="h-4 w-4 mr-2" /> Rejeitar
                                </Button>
                                <Button className="bg-green-600 hover:bg-green-700" onClick={() => { setIsDetailsModalOpen(false); handleApprove(currentLearning.id); }}>
                                    <CheckCircle className="h-4 w-4 mr-2" /> Aprovar
                                </Button>
                            </>
                        )}
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        );
    };

    const RejectModal: React.FC = () => {
        const isBatch = selectedLearnings.length > 0 && !currentLearning;
        const title = isBatch ? `Rejeitar ${selectedLearnings.length} Aprendizados` : `Rejeitar Aprendizado: ${currentLearning?.title}`;
        
        return (
            <Dialog open={isRejectModalOpen} onOpenChange={setIsRejectModalOpen}>
                <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                        <DialogTitle className="flex items-center text-red-600">
                            <XCircle className="h-5 w-5 mr-2" /> {title}
                        </DialogTitle>
                    </DialogHeader>
                    
                    <div className="space-y-4 py-4">
                        <Label htmlFor="rejection-reason">Motivo da rejeição: *</Label>
                        <Textarea 
                            id="rejection-reason" 
                            rows={5} 
                            value={rejectionReason} 
                            onChange={(e) => setRejectionReason(e.target.value)}
                            placeholder="Explique o motivo da rejeição (mínimo 10 caracteres)..."
                        />
                        <p className="text-xs text-muted-foreground">Esta informação será usada para treinar a ISA a evitar erros futuros.</p>
                    </div>
                    
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsRejectModalOpen(false)}>Cancelar</Button>
                        <Button 
                            onClick={isBatch ? handleConfirmBatchReject : handleConfirmReject} 
                            disabled={rejectionReason.length < 10}
                            className="bg-red-600 hover:bg-red-700"
                        >
                            <XCircle className="h-4 w-4 mr-2" /> Confirmar Rejeição
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        );
    };

    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold flex items-center text-purple-600 dark:text-white">
                    <Clock className="h-7 w-7 mr-3" />
                    Fila de Aprendizados
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
                    <div className="flex justify-between items-center">
                        <h3 className="text-xl font-semibold">Estatísticas de Revisão</h3>
                        <Badge className="bg-indigo-600 text-white">
                            Aprovação: {queueData.stats.approval_rate}% (30 dias)
                        </Badge>
                    </div>
                    <div className="grid grid-cols-3 gap-4 mt-4">
                        <Card className="p-4 text-center border-l-4 border-yellow-500">
                            <p className="text-sm text-muted-foreground">Pendentes</p>
                            <p className="text-3xl font-bold text-yellow-500">{queueData.stats.pending}</p>
                        </Card>
                        <Card className="p-4 text-center border-l-4 border-green-600">
                            <p className="text-sm text-muted-foreground">Aprovados</p>
                            <p className="text-3xl font-bold text-green-600">{queueData.stats.approved}</p>
                        </Card>
                        <Card className="p-4 text-center border-l-4 border-red-600">
                            <p className="text-sm text-muted-foreground">Rejeitados</p>
                            <p className="text-3xl font-bold text-red-600">{queueData.stats.rejected}</p>
                        </Card>
                    </div>
                </CardContent>
            </Card>

            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as LearningStatus)} className="w-full">
                <TabsList className="grid w-full grid-cols-3 h-auto p-1 bg-gray-100 dark:bg-gray-800">
                    <TabsTrigger value="pending" className={cn("flex items-center space-x-2 data-[state=active]:bg-yellow-500 data-[state=active]:text-gray-900")}>
                        <Clock className="h-4 w-4" />
                        <span>Pendentes</span>
                        <Badge className="bg-white text-yellow-500">{queueData.stats.pending}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="approved" className={cn("flex items-center space-x-2 data-[state=active]:bg-green-600 data-[state=active]:text-white")}>
                        <CheckCircle className="h-4 w-4" />
                        <span>Aprovados</span>
                        <Badge className="bg-white text-green-600">{queueData.stats.approved}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="rejected" className={cn("flex items-center space-x-2 data-[state=active]:bg-red-600 data-[state=active]:text-white")}>
                        <XCircle className="h-4 w-4" />
                        <span>Rejeitados</span>
                        <Badge className="bg-white text-red-600">{queueData.stats.rejected}</Badge>
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="pending" className="mt-6 space-y-4">
                    {selectedLearnings.length > 0 && (
                        <Card className="p-4 bg-purple-50 dark:bg-indigo-900/50 border-2 border-purple-600">
                            <div className="flex justify-between items-center">
                                <span className="text-lg font-semibold text-purple-800 dark:text-purple-200">
                                    {selectedLearnings.length} aprendizados selecionados
                                </span>
                                <div className="flex space-x-3">
                                    <Button className="bg-green-600 hover:bg-green-700" onClick={handleBatchApprove}>
                                        <CheckCircle className="h-4 w-4 mr-2" /> Aprovar Todos
                                    </Button>
                                    <Button className="bg-red-600 hover:bg-red-700" onClick={handleBatchReject}>
                                        <XCircle className="h-4 w-4 mr-2" /> Rejeitar Todos
                                    </Button>
                                </div>
                            </div>
                        </Card>
                    )}
                    
                    {isLoading ? (
                        Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-32 w-full" />)
                    ) : queueData.data.length === 0 ? (
                        <div className="text-center p-12 border-2 border-dashed rounded-lg">
                            <CheckCircle className="h-10 w-10 mx-auto text-green-600 mb-4" />
                            <p className="text-lg text-muted-foreground">Nenhum aprendizado pendente de revisão. Bom trabalho!</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                                <Checkbox 
                                    checked={isAllSelected}
                                    onCheckedChange={(checked) => handleSelectAll(checked as boolean)}
                                />
                                <Label>Selecionar todos ({queueData.data.length})</Label>
                            </div>
                            {queueData.data.map(learning => (
                                <LearningCard 
                                    key={learning.id} 
                                    learning={learning} 
                                    onSelect={handleSelectOne}
                                    isSelected={selectedLearnings.includes(learning.id)}
                                    onOpenDetails={() => { setCurrentLearning(learning); setIsDetailsModalOpen(true); }}
                                    onApprove={handleApprove}
                                    onReject={handleReject}
                                    activeTab={activeTab}
                                />
                            ))}
                        </div>
                    )}
                </TabsContent>

                <TabsContent value="approved" className="mt-6 space-y-4">
                    {isLoading ? (
                        Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-24 w-full" />)
                    ) : queueData.data.length === 0 ? (
                        <div className="text-center p-12 border-2 border-dashed rounded-lg">
                            <Clock className="h-10 w-10 mx-auto text-muted-foreground mb-4" />
                            <p className="text-lg text-muted-foreground">Nenhum histórico de aprendizados aprovados.</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {queueData.data.map(learning => (
                                <LearningCard 
                                    key={learning.id} 
                                    learning={learning} 
                                    onSelect={() => {}}
                                    isSelected={false}
                                    onOpenDetails={() => { setCurrentLearning(learning); setIsDetailsModalOpen(true); }}
                                    onApprove={() => {}}
                                    onReject={() => {}}
                                    activeTab={activeTab}
                                />
                            ))}
                        </div>
                    )}
                </TabsContent>
                
                <TabsContent value="rejected" className="mt-6 space-y-4">
                    {isLoading ? (
                        Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-24 w-full" />)
                    ) : queueData.data.length === 0 ? (
                        <div className="text-center p-12 border-2 border-dashed rounded-lg">
                            <Clock className="h-10 w-10 mx-auto text-muted-foreground mb-4" />
                            <p className="text-lg text-muted-foreground">Nenhum histórico de aprendizados rejeitados.</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {queueData.data.map(learning => (
                                <LearningCard 
                                    key={learning.id} 
                                    learning={learning} 
                                    onSelect={() => {}}
                                    isSelected={false}
                                    onOpenDetails={() => { setCurrentLearning(learning); setIsDetailsModalOpen(true); }}
                                    onApprove={() => {}}
                                    onReject={() => {}}
                                    activeTab={activeTab}
                                />
                            ))}
                        </div>
                    )}
                </TabsContent>
            </Tabs>

            {/* Modals */}
            {isDetailsModalOpen && <DetailsModal />}
            {isRejectModalOpen && <RejectModal />}
        </DashboardLayout>
    );
};

export default LearningQueuePage;