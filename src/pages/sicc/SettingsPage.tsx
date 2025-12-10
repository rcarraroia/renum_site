import React, { useState, useEffect, useCallback, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge'; // <-- Importação adicionada
import { Settings, Brain, Zap, Shield, Clock, Database, Users, AlertTriangle, Save, RefreshCw, Trash2, History, CheckCircle, XCircle, Info, Loader2 } from 'lucide-react';
import { siccService } from '@/services/siccService';
import { AgentSettings, LearningMode, AnalysisFrequency, Snapshot } from '@/types/sicc';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Label } from '@/components/ui/label';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { Skeleton } from '@/components/ui/skeleton';

// --- Constantes ---
const DEFAULT_SETTINGS: AgentSettings = {
    agent_id: '',
    learning_mode: 'active',
    analysis_frequency: 'hourly',
    auto_approve_threshold: 0.80,
    manual_review_threshold: 0.50,
    auto_reject_threshold: 0.30,
    max_memories: 10000,
    max_pending_learnings: 500,
    snapshot_retention_days: 90,
    auto_archive_days: 365,
    layer_base_enabled: true,
    layer_company_enabled: true,
    layer_individual_enabled: true,
    audio_retention_days: 30,
    anonymization_enabled: true,
    multi_tenant_isolation: true,
    updated_at: new Date().toISOString(),
    updated_by: 'System',
};

const FREQUENCY_OPTIONS: { value: AnalysisFrequency; label: string }[] = [
    { value: 'realtime', label: 'Realtime' },
    { value: 'hourly', label: 'Hourly' },
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
];

// --- Componente Principal ---

const SettingsPage: React.FC = () => {
    const [agents, setAgents] = useState<{ id: string; name: string }[]>([]);
    const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>(undefined);
    
    const [settings, setSettings] = useState<AgentSettings>(DEFAULT_SETTINGS);
    const [originalSettings, setOriginalSettings] = useState<AgentSettings>(DEFAULT_SETTINGS);
    const [usageStats, setUsageStats] = useState({ memories: 0, pending_learnings: 0 });
    
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Modals
    const [isResetModalOpen, setIsResetModalOpen] = useState(false);
    const [isSnapshotModalOpen, setIsSnapshotModalOpen] = useState(false);
    const [isRestoreModalOpen, setIsRestoreModalOpen] = useState(false);
    const [isPurgeModalOpen, setIsPurgeModalOpen] = useState(false);
    const [snapshotName, setSnapshotName] = useState('');
    const [purgeConfirmation, setPurgeConfirmation] = useState('');
    const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
    const [selectedSnapshotId, setSelectedSnapshotId] = useState<string | undefined>(undefined);

    // --- Data Fetching ---

    const fetchSettings = useCallback(async (agentId: string) => {
        if (!agentId) return;
        setIsLoading(true);
        setError(null);
        try {
            const [fetchedSettings, stats] = await Promise.all([
                siccService.getSettings(agentId),
                siccService.getCurrentUsageStats(agentId)
            ]);
            setSettings(fetchedSettings);
            setOriginalSettings(fetchedSettings);
            setUsageStats(stats);
        } catch (err) {
            setError("Falha ao carregar configurações.");
            toast.error("Falha ao carregar configurações.");
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        siccService.getAgents().then(data => {
            setAgents(data);
            if (data.length > 0) {
                setSelectedAgentId(data[0].id);
            }
        });
    }, []);

    useEffect(() => {
        if (selectedAgentId) {
            fetchSettings(selectedAgentId);
        }
    }, [selectedAgentId, fetchSettings]);

    // --- State Management & Validation ---

    const isDirty = useMemo(() => {
        return JSON.stringify(settings) !== JSON.stringify(originalSettings);
    }, [settings, originalSettings]);

    const handleSettingChange = (key: keyof AgentSettings, value: any) => {
        setSettings(prev => ({ ...prev, [key]: value }));
    };

    const validateThresholds = () => {
        if (settings.auto_approve_threshold <= settings.manual_review_threshold) {
            return "O Threshold de Auto-Aprovação deve ser maior que o de Revisão Humana.";
        }
        if (settings.manual_review_threshold <= settings.auto_reject_threshold) {
            return "O Threshold de Revisão Humana deve ser maior que o de Descarte Automático.";
        }
        return null;
    };

    const validationError = useMemo(validateThresholds, [settings]);

    // --- Action Handlers ---

    const handleSave = async () => {
        if (!selectedAgentId || validationError) {
            toast.error(validationError || "Selecione um agente.");
            return;
        }
        setIsSaving(true);
        try {
            const updatedSettings = await siccService.saveSettings(selectedAgentId, settings);
            setSettings(updatedSettings);
            setOriginalSettings(updatedSettings);
            toast.success("Configurações salvas com sucesso!");
        } catch (e) {
            toast.error("Falha ao salvar configurações.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleReset = async () => {
        if (!selectedAgentId) return;
        setIsResetModalOpen(false);
        setIsSaving(true);
        try {
            await siccService.resetSettings(selectedAgentId);
            await fetchSettings(selectedAgentId); // Refetch defaults
            toast.warning("Configurações restauradas para o padrão.");
        } catch (e) {
            toast.error("Falha ao resetar configurações.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleCreateSnapshot = async () => {
        if (!selectedAgentId) return;
        setIsSnapshotModalOpen(false);
        setIsSaving(true);
        try {
            await siccService.createSnapshot(selectedAgentId, snapshotName);
            toast.success("Snapshot criado com sucesso!");
            setSnapshotName('');
        } catch (e) {
            toast.error("Falha ao criar snapshot.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleOpenRestoreModal = async () => {
        if (!selectedAgentId) return;
        try {
            const list = await siccService.listSnapshots(selectedAgentId);
            setSnapshots(list);
            setIsRestoreModalOpen(true);
        } catch (e) {
            toast.error("Falha ao listar snapshots.");
        }
    };

    const handleRestoreSnapshot = async () => {
        if (!selectedSnapshotId || !selectedAgentId) return;
        if (!window.confirm("ATENÇÃO: Restaurar um snapshot pode reverter o comportamento do agente. Confirma a restauração?")) return;

        setIsRestoreModalOpen(false);
        setIsSaving(true);
        try {
            await siccService.restoreSnapshot(selectedSnapshotId);
            await fetchSettings(selectedAgentId); // Refetch settings after restore
            toast.success("Snapshot restaurado com sucesso!");
        } catch (e) {
            toast.error("Falha ao restaurar snapshot.");
        } finally {
            setIsSaving(false);
            setSelectedSnapshotId(undefined);
        }
    };

    const handlePurgeMemories = async () => {
        if (!selectedAgentId || purgeConfirmation !== 'CONFIRMAR') {
            toast.error("Você deve digitar 'CONFIRMAR' para prosseguir.");
            return;
        }
        setIsPurgeModalOpen(false);
        setIsSaving(true);
        try {
            await siccService.purgeMemories(selectedAgentId);
            await fetchSettings(selectedAgentId); // Update usage stats
            toast.error("Todas as memórias foram permanentemente removidas.");
        } catch (e) {
            toast.error("Falha ao limpar memórias.");
        } finally {
            setPurgeConfirmation('');
            setIsSaving(false);
        }
    };

    // --- Renderização Auxiliar ---

    const renderSlider = (key: keyof AgentSettings, label: string, description: string, color: string, min: number, max: number, step: number) => {
        const value = settings[key] as number;
        const percentage = (value - min) / (max - min) * 100;

        return (
            <div className="space-y-3 p-3 border rounded-lg">
                <div className="flex justify-between items-center">
                    <Label className="font-medium">{label}</Label>
                    <Badge className={cn("text-white", color)}>{value.toFixed(2)}</Badge>
                </div>
                <Slider
                    min={min}
                    max={max}
                    step={step}
                    value={[value]}
                    onValueChange={(v) => handleSettingChange(key, v[0])}
                    className="w-full"
                    style={{ '--slider-track-background': `linear-gradient(to right, ${color} ${percentage}%, #e5e7eb ${percentage}%)` } as React.CSSProperties}
                />
                <p className="text-xs text-muted-foreground">{description}</p>
            </div>
        );
    };

    const renderInputWithUsage = (key: keyof AgentSettings, label: string, description: string, currentUsage: number, maxLimit: number) => {
        const value = settings[key] as number;
        const percentageUsed = maxLimit > 0 ? ((currentUsage / maxLimit) * 100).toFixed(1) : '0';

        return (
            <div className="space-y-2">
                <Label>{label}</Label>
                <div className="flex space-x-2">
                    <Input
                        type="number"
                        value={value}
                        onChange={(e) => handleSettingChange(key, parseInt(e.target.value) || 0)}
                        min={0}
                    />
                </div>
                <p className="text-xs text-muted-foreground">
                    {description}
                    <span className="block mt-1 font-medium text-blue-600 dark:text-blue-400">
                        Atual: {currentUsage.toLocaleString()} / {value.toLocaleString()} ({percentageUsed}% usado)
                    </span>
                </p>
            </div>
        );
    };

    if (isLoading) {
        return (
            <DashboardLayout>
                <h2 className="text-3xl font-bold flex items-center text-purple-600 mb-6"><Settings className="h-7 w-7 mr-3" /> Configurações IA</h2>
                <div className="space-y-6">
                    <Skeleton className="h-40 w-full" />
                    <Skeleton className="h-60 w-full" />
                    <Skeleton className="h-40 w-full" />
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold flex items-center text-purple-600 dark:text-white">
                    <Settings className="h-7 w-7 mr-3" />
                    Configurações IA
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

            {isDirty && (
                <Alert variant="default" className="mb-6 border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
                    <AlertTriangle className="h-4 w-4 text-yellow-600" />
                    <AlertTitle className="text-yellow-700">Configurações Não Salvas</AlertTitle>
                    <AlertDescription className="text-yellow-600">
                        Você possui alterações pendentes. Clique em "Salvar Configurações" no rodapé para aplicá-las.
                    </AlertDescription>
                </Alert>
            )}
            
            {validationError && (
                <Alert variant="destructive" className="mb-6">
                    <XCircle className="h-4 w-4" />
                    <AlertTitle>Erro de Validação</AlertTitle>
                    <AlertDescription>{validationError}</AlertDescription>
                </Alert>
            )}

            <div className="grid lg:grid-cols-3 gap-6">
                {/* CARD 1: Sistema de Aprendizado */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle className="flex items-center text-purple-600"><Brain className="h-5 w-5 mr-2" /> Sistema de Aprendizado</CardTitle>
                        <CardDescription>Controle o modo de operação e a frequência de análise da ISA.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <Label>Modo de Aprendizado</Label>
                                <Select 
                                    value={settings.learning_mode} 
                                    onValueChange={(v) => handleSettingChange('learning_mode', v as LearningMode)}
                                >
                                    <SelectTrigger><SelectValue /></SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="active">Ativo (Aprende e Sugere)</SelectItem>
                                        <SelectItem value="observe_only">Apenas Observação (Não Sugere)</SelectItem>
                                        <SelectItem value="disabled">Desativado (Não Analisa)</SelectItem>
                                    </SelectContent>
                                </Select>
                                <p className="text-xs text-muted-foreground">Define se a ISA pode gerar novos aprendizados.</p>
                            </div>
                            <div className="space-y-2">
                                <Label>Frequência de Análise</Label>
                                <Select 
                                    value={settings.analysis_frequency} 
                                    onValueChange={(v) => handleSettingChange('analysis_frequency', v as AnalysisFrequency)}
                                >
                                    <SelectTrigger><SelectValue /></SelectTrigger>
                                    <SelectContent>
                                        {FREQUENCY_OPTIONS.map(opt => (
                                            <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                                <p className="text-xs text-muted-foreground">Com que frequência a ISA analisa conversas para detectar padrões.</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* CARD 4: Camadas de Conhecimento (Lateral) */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center text-indigo-600"><Database className="h-5 w-5 mr-2" /> Camadas de Conhecimento</CardTitle>
                        <CardDescription>Ative ou desative o acesso a diferentes fontes de memória.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <Label htmlFor="layer_base">Camada Base (Nicho)</Label>
                            <Switch 
                                id="layer_base" 
                                checked={settings.layer_base_enabled} 
                                onCheckedChange={(checked) => handleSettingChange('layer_base_enabled', checked)}
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <Label htmlFor="layer_company">Camada Empresa</Label>
                            <Switch 
                                id="layer_company" 
                                checked={settings.layer_company_enabled} 
                                onCheckedChange={(checked) => handleSettingChange('layer_company_enabled', checked)}
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <Label htmlFor="layer_individual">Camada Individual</Label>
                            <Switch 
                                id="layer_individual" 
                                checked={settings.layer_individual_enabled} 
                                onCheckedChange={(checked) => handleSettingChange('layer_individual_enabled', checked)}
                            />
                        </div>
                        <Alert className="border-blue-500 bg-blue-50 dark:bg-blue-950">
                            <Info className="h-4 w-4 text-blue-600" />
                            <AlertDescription className="text-xs">
                                Desativar camadas remove o acesso do agente às memórias contidas nelas.
                            </AlertDescription>
                        </Alert>
                    </CardContent>
                </Card>

                {/* CARD 2: Thresholds de Aprovação */}
                <Card className="lg:col-span-3">
                    <CardHeader>
                        <CardTitle className="flex items-center text-cyan-500"><Zap className="h-5 w-5 mr-2" /> Thresholds de Aprovação</CardTitle>
                        <CardDescription>Defina os níveis de confiança que determinam a aprovação automática ou a necessidade de revisão humana.</CardDescription>
                    </CardHeader>
                    <CardContent className="grid md:grid-cols-3 gap-4">
                        {renderSlider(
                            'auto_approve_threshold',
                            'Auto-Aprovação (≥)',
                            `Aprendizados com confiança ≥${settings.auto_approve_threshold.toFixed(2)} são aprovados automaticamente.`,
                            '#10b981', // Green
                            0, 1, 0.01
                        )}
                        {renderSlider(
                            'manual_review_threshold',
                            'Revisão Humana (≥)',
                            `Aprendizados entre ${settings.manual_review_threshold.toFixed(2)} e ${settings.auto_approve_threshold.toFixed(2)} requerem aprovação manual.`,
                            '#f59e0b', // Amber
                            0, 1, 0.01
                        )}
                        {renderSlider(
                            'auto_reject_threshold',
                            'Descarte Automático (<)',
                            `Aprendizados com confiança <${settings.auto_reject_threshold.toFixed(2)} são descartados automaticamente.`,
                            '#ef4444', // Red
                            0, 1, 0.01
                        )}
                    </CardContent>
                </Card>

                {/* CARD 3: Quotas e Limites */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle className="flex items-center text-purple-600"><Clock className="h-5 w-5 mr-2" /> Quotas e Limites</CardTitle>
                        <CardDescription>Gerencie o volume de dados e a retenção de memórias e aprendizados.</CardDescription>
                    </CardHeader>
                    <CardContent className="grid md:grid-cols-2 gap-6">
                        {renderInputWithUsage(
                            'max_memories',
                            'Máximo de Memórias por Agente',
                            'Limite total de chunks de memória que o agente pode armazenar.',
                            usageStats.memories,
                            settings.max_memories
                        )}
                        {renderInputWithUsage(
                            'max_pending_learnings',
                            'Máximo de Aprendizados Pendentes',
                            'Limite de itens na fila de revisão humana.',
                            usageStats.pending_learnings,
                            settings.max_pending_learnings
                        )}
                        <div className="space-y-2">
                            <Label>Retenção de Snapshots (dias)</Label>
                            <Input
                                type="number"
                                value={settings.snapshot_retention_days}
                                onChange={(e) => handleSettingChange('snapshot_retention_days', parseInt(e.target.value) || 0)}
                                min={0}
                            />
                            <p className="text-xs text-muted-foreground">Período de retenção dos backups de configuração.</p>
                        </div>
                        <div className="space-y-2">
                            <Label>Auto-Arquivar Memórias Antigas (dias)</Label>
                            <Input
                                type="number"
                                value={settings.auto_archive_days}
                                onChange={(e) => handleSettingChange('auto_archive_days', parseInt(e.target.value) || 0)}
                                min={0}
                            />
                            <p className="text-xs text-muted-foreground">Memórias não usadas por este período são arquivadas (0 = nunca).</p>
                        </div>
                    </CardContent>
                </Card>

                {/* CARD 5: Segurança e Privacidade (Lateral) */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center text-green-600"><Shield className="h-5 w-5 mr-2" /> Segurança e Privacidade</CardTitle>
                        <CardDescription>Configurações de conformidade e retenção de dados brutos.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label>Retenção de Áudio (dias)</Label>
                            <Input
                                type="number"
                                value={settings.audio_retention_days}
                                onChange={(e) => handleSettingChange('audio_retention_days', parseInt(e.target.value) || 0)}
                                min={0}
                            />
                            <p className="text-xs text-muted-foreground">Arquivos de transcrição brutos são deletados após este período.</p>
                        </div>
                        <div className="flex items-center justify-between">
                            <Label htmlFor="anonymization">Anonimização Automática</Label>
                            <Switch 
                                id="anonymization" 
                                checked={settings.anonymization_enabled} 
                                onCheckedChange={(checked) => handleSettingChange('anonymization_enabled', checked)}
                            />
                        </div>
                        <div className="flex items-center justify-between opacity-70">
                            <Label htmlFor="multi_tenant">Isolamento Multi-Tenant</Label>
                            <Switch 
                                id="multi_tenant" 
                                checked={settings.multi_tenant_isolation} 
                                disabled 
                            />
                        </div>
                        <Alert className="border-green-500 bg-green-50 dark:bg-green-950">
                            <CheckCircle className="h-4 w-4 text-green-600" />
                            <AlertDescription className="text-xs">
                                Sistema em conformidade com LGPD/GDPR.
                            </AlertDescription>
                        </Alert>
                    </CardContent>
                </Card>

                {/* CARD 6: Ações Perigosas */}
                <Card className="lg:col-span-3">
                    <CardHeader>
                        <CardTitle className="flex items-center text-red-600"><AlertTriangle className="h-5 w-5 mr-2" /> Ações Perigosas</CardTitle>
                        <CardDescription>Operações que afetam permanentemente o estado do agente. Use com cautela.</CardDescription>
                    </CardHeader>
                    <CardContent className="grid md:grid-cols-4 gap-4">
                        <Button variant="outline" onClick={() => setIsResetModalOpen(true)} disabled={isSaving}>
                            <RefreshCw className="h-4 w-4 mr-2" /> Resetar Configurações
                        </Button>
                        <Button variant="outline" onClick={() => setIsSnapshotModalOpen(true)} disabled={isSaving}>
                            <History className="h-4 w-4 mr-2" /> Criar Snapshot Manual
                        </Button>
                        <Button variant="outline" onClick={handleOpenRestoreModal} disabled={isSaving}>
                            <History className="h-4 w-4 mr-2" /> Restaurar Snapshot
                        </Button>
                        <Button variant="destructive" onClick={() => setIsPurgeModalOpen(true)} disabled={isSaving}>
                            <Trash2 className="h-4 w-4 mr-2" /> Limpar Todas Memórias
                        </Button>
                    </CardContent>
                </Card>
            </div>

            <CardFooter className="mt-6 flex justify-between items-center border-t pt-4">
                <div className="text-sm text-muted-foreground">
                    Última atualização: {format(new Date(settings.updated_at), 'dd/MM/yyyy HH:mm', { locale: ptBR })} por {settings.updated_by}
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline" onClick={() => setSettings(originalSettings)} disabled={!isDirty || isSaving}>
                        Cancelar
                    </Button>
                    <Button 
                        onClick={handleSave} 
                        disabled={!isDirty || !!validationError || isSaving}
                        className="bg-purple-600 hover:bg-purple-700"
                    >
                        {isSaving ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Save className="h-4 w-4 mr-2" />}
                        Salvar Configurações
                    </Button>
                </div>
            </CardFooter>

            {/* Modals */}
            
            {/* Reset Modal */}
            <Dialog open={isResetModalOpen} onOpenChange={setIsResetModalOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle className="text-red-600 flex items-center"><RefreshCw className="h-5 w-5 mr-2" /> Confirmar Reset</DialogTitle>
                    </DialogHeader>
                    <p>Tem certeza que deseja restaurar todas as configurações para os valores padrão? Isso não afetará as memórias existentes.</p>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsResetModalOpen(false)}>Cancelar</Button>
                        <Button variant="destructive" onClick={handleReset}>Resetar</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Snapshot Modal */}
            <Dialog open={isSnapshotModalOpen} onOpenChange={setIsSnapshotModalOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle className="text-purple-600 flex items-center"><History className="h-5 w-5 mr-2" /> Criar Snapshot</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <Label htmlFor="snapshot-name">Nome do Snapshot (Opcional)</Label>
                        <Input 
                            id="snapshot-name" 
                            value={snapshotName} 
                            onChange={(e) => setSnapshotName(e.target.value)} 
                            placeholder="Ex: Configuração antes do lançamento Q2"
                        />
                        <p className="text-sm text-muted-foreground">Um snapshot salva o estado atual das configurações do agente.</p>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsSnapshotModalOpen(false)}>Cancelar</Button>
                        <Button onClick={handleCreateSnapshot} className="bg-purple-600 hover:bg-purple-700">Criar Snapshot</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Restore Modal */}
            <Dialog open={isRestoreModalOpen} onOpenChange={setIsRestoreModalOpen}>
                <DialogContent className="sm:max-w-[600px]">
                    <DialogHeader>
                        <DialogTitle className="text-red-600 flex items-center"><History className="h-5 w-5 mr-2" /> Restaurar Snapshot</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <Label>Selecione o Snapshot para Restaurar:</Label>
                        <Select value={selectedSnapshotId} onValueChange={setSelectedSnapshotId}>
                            <SelectTrigger><SelectValue placeholder="Selecione um snapshot..." /></SelectTrigger>
                            <SelectContent>
                                {snapshots.map(snap => (
                                    <SelectItem key={snap.id} value={snap.id}>
                                        {snap.name} ({format(new Date(snap.created_at), 'dd/MM/yyyy')})
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        {selectedSnapshotId && (
                            <Alert variant="destructive">
                                <AlertTriangle className="h-4 w-4" />
                                <AlertDescription>
                                    A restauração reverterá as configurações para o estado salvo. Isso pode causar mudanças imediatas no comportamento do agente.
                                </AlertDescription>
                            </Alert>
                        )}
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsRestoreModalOpen(false)}>Cancelar</Button>
                        <Button variant="destructive" onClick={handleRestoreSnapshot} disabled={!selectedSnapshotId}>Restaurar</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Purge Modal (Triple Confirmation) */}
            <Dialog open={isPurgeModalOpen} onOpenChange={setIsPurgeModalOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle className="text-red-700 flex items-center"><Trash2 className="h-5 w-5 mr-2" /> Limpar Todas Memórias (IRREVERSÍVEL)</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <Alert variant="destructive">
                            <AlertTriangle className="h-4 w-4" />
                            <AlertDescription>
                                Esta ação removerá permanentemente TODAS as memórias do agente, incluindo FAQ, termos de negócio e padrões. O agente voltará a um estado de conhecimento zero.
                            </AlertDescription>
                        </Alert>
                        <Label htmlFor="purge-confirm">Para confirmar, digite a palavra "CONFIRMAR" abaixo:</Label>
                        <Input 
                            id="purge-confirm" 
                            value={purgeConfirmation} 
                            onChange={(e) => setPurgeConfirmation(e.target.value)} 
                            className="font-bold text-red-600"
                        />
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsPurgeModalOpen(false)}>Cancelar</Button>
                        <Button 
                            variant="destructive" 
                            onClick={handlePurgeMemories} 
                            disabled={purgeConfirmation !== 'CONFIRMAR'}
                        >
                            <Trash2 className="h-4 w-4 mr-2" /> Limpar Memórias Permanentemente
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </DashboardLayout>
    );
};

export default SettingsPage;