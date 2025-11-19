' por '&rarr;'.">
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Shield, Lock, AlertTriangle, Save, TestTube, CheckCircle, XCircle, Settings, ChevronDown, ChevronUp, Mail, Phone, Landmark, MapPin, Tag, Trash2, Brain, Clock, RefreshCw, Plus } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Slider } from '@/components/ui/slider';

type ActionType = 'Bloquear' | 'Sanitizar' | 'Alertar';

interface ValidatorCardProps {
    title: string;
    icon: React.ElementType;
    defaultEnabled: boolean;
    defaultAction: ActionType;
    isPremium?: boolean;
    children: React.ReactNode;
}

const ValidatorCard: React.FC<ValidatorCardProps> = ({ title, icon: Icon, defaultEnabled, defaultAction, isPremium, children }) => {
    const [isEnabled, setIsEnabled] = useState(defaultEnabled);
    const [action, setAction] = useState<ActionType>(defaultAction);
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <Card className={cn("transition-all", isEnabled ? "border-[#4e4ea8] dark:border-[#0ca7d2]" : "border-dashed border-gray-300 dark:border-gray-700")}>
            <CardHeader className="p-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <Icon className={cn("h-6 w-6", isEnabled ? "text-[#FF6B35]" : "text-muted-foreground")} />
                        <CardTitle className="text-lg">{title}</CardTitle>
                        {isPremium && <Badge className="bg-yellow-500 text-gray-900">Premium</Badge>}
                    </div>
                    <Switch checked={isEnabled} onCheckedChange={setIsEnabled} className={cn(isEnabled ? 'data-[state=checked]:bg-[#4e4ea8]' : '')} />
                </div>
            </CardHeader>
            <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
                <CollapsibleTrigger asChild>
                    <Button variant="ghost" className="w-full justify-between px-4 py-2 text-sm text-muted-foreground hover:bg-gray-50 dark:hover:bg-gray-800">
                        Detalhes e Configuração
                        {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </Button>
                </CollapsibleTrigger>
                <CollapsibleContent>
                    <Separator />
                    <CardContent className="p-4 space-y-4">
                        <div className="grid grid-cols-2 gap-4 items-center">
                            <Label>Ação em Caso de Violação</Label>
                            <Select value={action} onValueChange={(v) => setAction(v as ActionType)} disabled={!isEnabled}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Ação" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="Bloquear">Bloquear Mensagem</SelectItem>
                                    <SelectItem value="Sanitizar">Sanitizar Conteúdo</SelectItem>
                                    <SelectItem value="Alertar">Apenas Alertar</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        {children}
                    </CardContent>
                </CollapsibleContent>
            </Collapsible>
        </Card>
    );
};

const GuardrailsTab: React.FC = () => {
    const [isGuardrailsEnabled, setIsGuardrailsEnabled] = useState(true);
    const [securityLevel, setSecurityLevel] = useState('Intermediário');
    const [testMessage, setTestMessage] = useState('');
    const [testResult, setTestResult] = useState<any>(null);
    const [isTesting, setIsTesting] = useState(false);
    const [blockedWords, setBlockedWords] = useState(['preço', 'concorrente', 'fraude']);
    const [newBlockedWord, setNewBlockedWord] = useState('');

    const handleSave = () => {
        toast.success("Configurações de Guardrails salvas e prontas para publicação.");
    };

    const handlePublish = () => {
        toast.success("Configuração de Guardrails publicada com sucesso!");
    };

    const handleTest = () => {
        if (!testMessage) return;
        setIsTesting(true);
        setTestResult(null);
        toast.info("Executando teste de Guardrails...");

        setTimeout(() => {
            const violations = [];
            if (testMessage.toLowerCase().includes('api-key')) {
                violations.push({ type: 'Secret Detector', detail: 'API Key detectada.', action: 'Bloquear' });
            }
            if (testMessage.toLowerCase().includes('renato carraro')) {
                violations.push({ type: 'PII Detector', detail: 'Nome completo detectado.', action: 'Sanitizar' });
            }
            if (testMessage.toLowerCase().includes('como burlar')) {
                violations.push({ type: 'Jailbreak Protection', detail: 'Tentativa de desvio detectada.', action: 'Bloquear' });
            }

            setTestResult({
                status: violations.length === 0 ? 'PASS' : 'FAIL',
                violations,
                sanitizedText: violations.length > 0 ? testMessage.replace(/api-key/gi, '[REDACTED]').replace(/renato carraro/gi, 'RC') : testMessage,
                latency: (Math.random() * 500 + 100).toFixed(0) + 'ms',
            });
            setIsTesting(false);
            if (violations.length > 0) {
                toast.error(`Teste falhou: ${violations.length} violações encontradas.`);
            } else {
                toast.success("Teste bem-sucedido! Nenhuma violação encontrada.");
            }
        }, 1500);
    };

    const handleAddBlockedWord = () => {
        const word = newBlockedWord.trim().toLowerCase();
        if (word && !blockedWords.includes(word)) {
            setBlockedWords([...blockedWords, word]);
            setNewBlockedWord('');
            toast.info(`Palavra-chave '${word}' adicionada.`);
        }
    };

    const handleRemoveBlockedWord = (wordToRemove: string) => {
        setBlockedWords(blockedWords.filter(word => word !== wordToRemove));
        toast.warning(`Palavra-chave '${wordToRemove}' removida.`);
    };

    return (
        <div className="space-y-8">
            {/* Header and Global Toggle */}
            <Card className="p-6 border-2 border-[#0ca7d2] dark:border-[#4e4ea8]">
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-2xl font-bold flex items-center text-[#4e4ea8] dark:text-[#0ca7d2]">
                            <Shield className="h-6 w-6 mr-3" /> Guardrails de Segurança
                        </h2>
                        <p className="text-sm text-muted-foreground mt-1">
                            Defina limites e políticas de segurança para o agente Renus, protegendo contra conteúdo impróprio e vazamento de dados.
                        </p>
                    </div>
                    <div className="flex flex-col items-end space-y-2">
                        <Switch checked={isGuardrailsEnabled} onCheckedChange={setIsGuardrailsEnabled} className={cn(isGuardrailsEnabled ? 'data-[state=checked]:bg-[#FF6B35]' : '')} />
                        <Badge className={cn(isGuardrailsEnabled ? 'bg-green-500' : 'bg-red-500', 'text-white')}>
                            {isGuardrailsEnabled ? 'Ativo' : 'Inativo'}
                        </Badge>
                    </div>
                </div>
                <Separator className="my-4" />
                <div className="grid grid-cols-2 gap-4">
                    <Label className="flex items-center">Nível de Segurança Global</Label>
                    <Select value={securityLevel} onValueChange={setSecurityLevel}>
                        <SelectTrigger><SelectValue placeholder="Nível" /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="Básico">Básico</SelectItem>
                            <SelectItem value="Intermediário">Intermediário</SelectItem>
                            <SelectItem value="Avançado">Avançado</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </Card>

            {/* Validator Cards Grid */}
            <div className="grid md:grid-cols-2 gap-6">
                
                {/* 1. PII Detector */}
                <ValidatorCard title="Detector de Informações Pessoais (PII)" icon={Mail} defaultEnabled={true} defaultAction="Sanitizar">
                    <div className="space-y-3">
                        <Label>Tipos de PII a Detectar:</Label>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                            <div className="flex items-center space-x-2"><Switch defaultChecked /><Label>Email</Label></div>
                            <div className="flex items-center space-x-2"><Switch defaultChecked /><Label>Telefone</Label></div>
                            <div className="flex items-center space-x-2"><Switch defaultChecked /><Label>CPF/CNPJ</Label></div>
                            <div className="flex items-center space-x-2"><Switch defaultChecked /><Label>Endereço</Label></div>
                        </div>
                        <p className="text-xs text-muted-foreground italic">Exemplo: "Meu email é joao@exemplo.com" &rarr; "Meu email é [REDACTED]"</p>
                    </div>
                </ValidatorCard>

                {/* 2. Secret Detector */}
                <ValidatorCard title="Detector de Credenciais e API Keys" icon={Lock} defaultEnabled={true} defaultAction="Bloquear">
                    <div className="space-y-3">
                        <Label>Padrões de Detecção:</Label>
                        <p className="text-xs text-muted-foreground">Detecta chaves de API, tokens de acesso e senhas em formatos comuns (ex: JWT, AWS Key).</p>
                        <Label htmlFor="sensitivity">Nível de Sensibilidade</Label>
                        <Slider id="sensitivity" defaultValue={[70]} max={100} step={10} className="w-[90%]" />
                    </div>
                </ValidatorCard>

                {/* 3. Jailbreak Protection */}
                <ValidatorCard title="Proteção contra Jailbreak" icon={Brain} defaultEnabled={true} defaultAction="Bloquear" isPremium>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <Label>Análise Avançada (LLM)</Label>
                            <Switch defaultChecked />
                        </div>
                        <p className="text-xs text-muted-foreground italic">Bloqueia tentativas de desviar o Renus de sua persona e instruções de sistema.</p>
                    </div>
                </ValidatorCard>

                {/* 4. Keyword Filter */}
                <ValidatorCard title="Filtro de Palavras-chave" icon={Tag} defaultEnabled={true} defaultAction="Alertar">
                    <div className="space-y-3">
                        <Label>Lista de Palavras Bloqueadas:</Label>
                        <div className="flex space-x-2">
                            <Input 
                                placeholder="Adicionar palavra..." 
                                value={newBlockedWord} 
                                onChange={(e) => setNewBlockedWord(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleAddBlockedWord()}
                            />
                            <Button type="button" onClick={handleAddBlockedWord} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                                <Plus className="h-4 w-4" />
                            </Button>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {blockedWords.map(word => (
                                <Badge key={word} variant="secondary" className="text-sm cursor-pointer hover:bg-red-100 dark:hover:bg-red-900/50" onClick={() => handleRemoveBlockedWord(word)}>
                                    {word} <Trash2 className="h-3 w-3 ml-1" />
                                </Badge>
                            ))}
                        </div>
                    </div>
                </ValidatorCard>

                {/* 5. Topic Alignment (Premium) */}
                <ValidatorCard title="Alinhamento de Tópico" icon={Settings} defaultEnabled={false} defaultAction="Alertar" isPremium>
                    <div className="space-y-3">
                        <Label>Tópicos Permitidos (separados por vírgula):</Label>
                        <Input placeholder="Ex: Vendas, Automação, Discovery" disabled />
                        <Label htmlFor="strictness">Rigor da Detecção</Label>
                        <Slider id="strictness" defaultValue={[50]} max={100} step={10} className="w-[90%]" disabled />
                        <p className="text-xs text-yellow-600 dark:text-yellow-400">Recurso Premium. Faça upgrade para configurar o alinhamento de tópico.</p>
                    </div>
                </ValidatorCard>

                {/* 6. NSFW Detector (Premium) */}
                <ValidatorCard title="Filtro de Conteúdo Impróprio" icon={AlertTriangle} defaultEnabled={false} defaultAction="Bloquear" isPremium>
                    <div className="space-y-3">
                        <Label>Nível de Sensibilidade:</Label>
                        <Select disabled>
                            <SelectTrigger><SelectValue placeholder="Moderado" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="low">Baixo</SelectItem>
                                <SelectItem value="moderate">Moderado</SelectItem>
                                <SelectItem value="high">Alto</SelectItem>
                            </SelectContent>
                        </Select>
                        <p className="text-xs text-yellow-600 dark:text-yellow-400">Recurso Premium. Faça upgrade para ativar a filtragem NSFW.</p>
                    </div>
                </ValidatorCard>
            </div>

            {/* Testing Area */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><TestTube className="h-5 w-5 mr-2" /> Área de Teste</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <Textarea 
                        placeholder="Digite uma mensagem para testar as políticas de Guardrails..."
                        rows={3}
                        value={testMessage}
                        onChange={(e) => setTestMessage(e.target.value)}
                    />
                    <Button onClick={handleTest} disabled={isTesting} className="bg-[#0ca7d2] hover:bg-[#0987a8]">
                        <TestTube className="h-4 w-4 mr-2" /> {isTesting ? 'Testando...' : 'Testar Guardrails'}
                    </Button>

                    {testResult && (
                        <div className="mt-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800 space-y-2">
                            <div className="flex justify-between items-center">
                                <span className="font-semibold">Status do Teste:</span>
                                <Badge className={cn(testResult.status === 'PASS' ? 'bg-green-500' : 'bg-red-500', 'text-white')}>
                                    {testResult.status}
                                </Badge>
                            </div>
                            <p className="text-sm text-muted-foreground">Latência de Processamento: {testResult.latency}</p>
                            
                            {testResult.violations.length > 0 ? (
                                <div className="space-y-2 pt-2 border-t dark:border-gray-700">
                                    <p className="font-semibold text-red-500 flex items-center"><XCircle className="h-4 w-4 mr-2" /> Violações Encontradas:</p>
                                    <ul className="list-disc pl-5 text-sm space-y-1">
                                        {testResult.violations.map((v: any, i: number) => (
                                            <li key={i}>[{v.type}] {v.detail} (Ação: {v.action})</li>
                                        ))}
                                    </ul>
                                    <p className="font-semibold text-sm mt-3">Texto Sanitizado (Simulação):</p>
                                    <p className="text-xs font-mono bg-white dark:bg-gray-900 p-2 rounded border">{testResult.sanitizedText}</p>
                                </div>
                            ) : (
                                <p className="text-sm text-green-500 flex items-center"><CheckCircle className="h-4 w-4 mr-2" /> Nenhuma violação detectada.</p>
                            )}
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Advanced Settings */}
            <Collapsible>
                <CollapsibleTrigger asChild>
                    <Button variant="outline" className="w-full justify-between">
                        <span className="flex items-center"><Settings className="h-4 w-4 mr-2" /> Configurações Avançadas</span>
                        <ChevronDown className="h-4 w-4" />
                    </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="mt-4">
                    <Card>
                        <CardContent className="p-6 space-y-4">
                            <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                    <Label>Cache TTL (Tempo de Vida do Cache)</Label>
                                    <Select defaultValue="1h">
                                        <SelectTrigger><SelectValue placeholder="1 hora" /></SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="15min">15 minutos</SelectItem>
                                            <SelectItem value="1h">1 hora</SelectItem>
                                            <SelectItem value="6h">6 horas</SelectItem>
                                            <SelectItem value="24h">24 horas</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div>
                                    <Label>Comportamento de Fallback</Label>
                                    <Select defaultValue="default_msg">
                                        <SelectTrigger><SelectValue placeholder="Mensagem Padrão" /></SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="default_msg">Mensagem Padrão</SelectItem>
                                            <SelectItem value="transfer_human">Transferir para Humano</SelectItem>
                                            <SelectItem value="end_conv">Encerrar Conversa</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                            <div>
                                <Label>Mensagem de Erro Customizada</Label>
                                <Input placeholder="Ex: Desculpe, não posso discutir esse tópico." />
                            </div>
                        </CardContent>
                    </Card>
                </CollapsibleContent>
            </Collapsible>

            <div className="flex justify-end space-x-3">
                <Button onClick={handleSave} variant="outline">
                    <Save className="h-4 w-4 mr-2" /> Salvar Rascunho
                </Button>
                <Button onClick={handlePublish} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                    <Zap className="h-4 w-4 mr-2" /> Publicar Configuração
                </Button>
            </div>
        </div>
    );
};

export default GuardrailsTab;