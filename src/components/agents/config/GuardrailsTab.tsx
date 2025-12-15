import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Shield, Lock, AlertTriangle, Save, Tag, UserX, Copy, Eye } from 'lucide-react';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import agentService from '@/services/agentService';

const GuardrailsTab: React.FC = () => {
    const [agent, setAgent] = useState<any>(null);
    const [config, setConfig] = useState<any>({
        enabled: true,
        input: { keywords: [], pii: { enabled: true, types: ['email', 'phone'] }, jailbreak: { enabled: true } },
        output: { keywords: [], secrets: { enabled: true }, hallucination: { enabled: false } }
    });
    const [isLoading, setIsLoading] = useState(true);
    const [keywordInput, setKeywordInput] = useState('');

    useEffect(() => {
        loadAgent();
    }, []);

    const loadAgent = async () => {
        try {
            setIsLoading(true);
            const agents = await agentService.listAgents({ role: 'system_orchestrator' });
            // Fallback default
            let foundAgent = agents[0];
            if (!foundAgent) {
                const all = await agentService.listAgents();
                foundAgent = all.find((a: any) => a.slug === 'renus') || all[0];
            }

            if (foundAgent) {
                // Fetch full details
                const fullAgent = await agentService.getAgent(foundAgent.id);
                setAgent(fullAgent);

                // Load guardrails config or use defaults
                if (fullAgent.config?.guardrails) {
                    setConfig(fullAgent.config.guardrails);
                }
            }
        } catch (error) {
            toast.error("Erro ao carregar configurações.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSave = async () => {
        if (!agent) return;
        try {
            const updatedConfig = {
                ...agent.config,
                guardrails: config
            };
            await agentService.updateAgent(agent.id, { config: updatedConfig });
            setAgent({ ...agent, config: updatedConfig });
            toast.success("Políticas de segurança salvas!");
        } catch (error) {
            toast.error("Erro ao salvar.");
        }
    };

    const addKeyword = (list: 'input' | 'output') => {
        if (!keywordInput) return;
        const current = config[list]?.keywords || [];
        const updated = {
            ...config,
            [list]: {
                ...config[list],
                keywords: [...current, keywordInput]
            }
        };
        setConfig(updated);
        setKeywordInput('');
    };

    const removeKeyword = (list: 'input' | 'output', word: string) => {
        const current = config[list]?.keywords || [];
        const updated = {
            ...config,
            [list]: {
                ...config[list],
                keywords: current.filter((w: string) => w !== word)
            }
        };
        setConfig(updated);
    };

    const toggleFeature = (path: string, value: boolean) => {
        const parts = path.split('.');
        const newConfig = { ...config };
        let current = newConfig;
        for (let i = 0; i < parts.length - 1; i++) {
            if (!current[parts[i]]) current[parts[i]] = {};
            current = current[parts[i]];
        }
        current[parts[parts.length - 1]] = value;
        setConfig(newConfig);
    };

    if (isLoading) return <div>Carregando Guardrails...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <Shield className="h-8 w-8 text-primary" />
                    <div>
                        <h3 className="text-xl font-bold">Segurança e Guardrails</h3>
                        <p className="text-sm text-muted-foreground">Sistema de proteção em 2 camadas (Entrada e Saída).</p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <Label>Ativar Sistema de Segurança</Label>
                    <Switch
                        checked={config.enabled}
                        onCheckedChange={(v: boolean) => toggleFeature('enabled', v)}
                    />
                </div>
            </div>

            <Tabs defaultValue="input" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="input" className="flex gap-2"><UserX className="h-4 w-4" /> Camada 1: Entrada (Usuário)</TabsTrigger>
                    <TabsTrigger value="output" className="flex gap-2"><Eye className="h-4 w-4" /> Camada 2: Saída (Agente)</TabsTrigger>
                </TabsList>

                {/* INPUT LAYER */}
                <TabsContent value="input" className="space-y-4 mt-4">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <Lock className="h-5 w-5 text-orange-500" /> Proteção de Dados (PII)
                            </CardTitle>
                            <CardDescription>Detectar e anonimizar dados sensíveis antes de processar.</CardDescription>
                        </CardHeader>
                        <CardContent className="flex items-center justify-between">
                            <div className="space-y-1">
                                <Label>Anonimizar Email e Telefone</Label>
                                <p className="text-xs text-muted-foreground">Substitui dados reais por [REDACTED]</p>
                            </div>
                            <Switch
                                checked={config.input?.pii?.enabled}
                                onCheckedChange={(v: boolean) => toggleFeature('input.pii.enabled', v)}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <AlertTriangle className="h-5 w-5 text-red-500" /> Proteção contra Jailbreak
                            </CardTitle>
                            <CardDescription>Bloqueia tentativas de manipular as instruções do sistema ("Ignore previous instructions").</CardDescription>
                        </CardHeader>
                        <CardContent className="flex items-center justify-between">
                            <Label>Ativar Proteção Heurística</Label>
                            <Switch
                                checked={config.input?.jailbreak?.enabled}
                                onCheckedChange={(v: boolean) => toggleFeature('input.jailbreak.enabled', v)}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <Tag className="h-5 w-5 text-blue-500" /> Palavras Proibidas (Input)
                            </CardTitle>
                            <CardDescription>Bloqueia mensagens do usuário contendo estes termos.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex gap-2">
                                <Input
                                    placeholder="Adicionar palavra..."
                                    value={keywordInput}
                                    onChange={e => setKeywordInput(e.target.value)}
                                />
                                <Button onClick={() => addKeyword('input')}>Adicionar</Button>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {(config.input?.keywords || []).map((word: string) => (
                                    <Badge key={word} variant="secondary" className="cursor-pointer hover:bg-destructive/20" onClick={() => removeKeyword('input', word)}>
                                        {word} x
                                    </Badge>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* OUTPUT LAYER */}
                <TabsContent value="output" className="space-y-4 mt-4">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <Lock className="h-5 w-5 text-purple-500" /> Vazamento de Segredos
                            </CardTitle>
                            <CardDescription>Impede que o agente vaze API Keys ou credenciais (formato sk-...).</CardDescription>
                        </CardHeader>
                        <CardContent className="flex items-center justify-between">
                            <Label>Bloquear Padrões de API Key</Label>
                            <Switch
                                checked={config.output?.secrets?.enabled}
                                onCheckedChange={(v: boolean) => toggleFeature('output.secrets.enabled', v)}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <Copy className="h-5 w-5 text-yellow-500" /> Palavras Proibidas (Output)
                            </CardTitle>
                            <CardDescription>Garante que o agente nunca use estes termos na resposta.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex gap-2">
                                <Input
                                    placeholder="Adicionar palavra..."
                                    value={keywordInput}
                                    onChange={e => setKeywordInput(e.target.value)}
                                />
                                <Button onClick={() => addKeyword('output')}>Adicionar</Button>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {(config.output?.keywords || []).map((word: string) => (
                                    <Badge key={word} variant="outline" className="cursor-pointer hover:bg-destructive/20" onClick={() => removeKeyword('output', word)}>
                                        {word} x
                                    </Badge>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>

            <div className="flex justify-end pt-4">
                <Button onClick={handleSave} className="gap-2 bg-green-600 hover:bg-green-700">
                    <Save className="h-4 w-4" /> Salvar Configurações de Segurança
                </Button>
            </div>
        </div>
    );
};

export default GuardrailsTab;