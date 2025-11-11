import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Shield, Lock, AlertTriangle, Save, Settings, CheckCircle, XCircle, Tag, Clock, Download, Mail, Copy, Plus, Trash2 } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Slider } from '@/components/ui/slider';

const MOCK_GLOBAL_SETTINGS = {
    isEnabled: true,
    mandatorySecretDetection: true,
    mandatoryPII: ['Email', 'CPF/CNPJ'],
    defaultKeywords: 'preço, concorrente, ilegal',
    defaultTopicAlignment: 'Vendas, Automação, Discovery',
    auditLogRetention: '90 days',
    billingTier: 'Enterprise',
    creditsUsed: 12000,
    creditLimit: 50000,
};

const GlobalGuardrailsTab: React.FC = () => {
    const [settings, setSettings] = useState(MOCK_GLOBAL_SETTINGS);
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = () => {
        setIsSaving(true);
        setTimeout(() => {
            setIsSaving(false);
            toast.success("Configurações globais de Guardrails salvas!");
        }, 1000);
    };

    const handleApplyTemplate = (template: string) => {
        toast.info(`Aplicando template: ${template}...`);
        // Mock template application
        setTimeout(() => {
            setSettings(prev => ({
                ...prev,
                defaultKeywords: template === 'Maximum Security' ? 'todos, proibido, ilegal, preço' : 'preço, concorrente, ilegal',
            }));
            toast.success(`Template '${template}' aplicado com sucesso.`);
        }, 1000);
    };

    return (
        <div className="space-y-8">
            {/* Global Header and Status */}
            <Card className="p-6 border-2 border-[#4e4ea8] dark:border-[#0ca7d2]">
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-2xl font-bold flex items-center text-[#4e4ea8] dark:text-[#0ca7d2]">
                            <Shield className="h-6 w-6 mr-3" /> Guardrails de Segurança (Global)
                        </h2>
                        <p className="text-sm text-muted-foreground mt-1">
                            Defina políticas de segurança que se aplicam a todos os agentes e clientes.
                        </p>
                        <p className="text-xs mt-2 text-[#FF6B35] font-medium">
                            Hierarquia: <span className="font-bold">Sistema</span> → Conta → Agente
                        </p>
                    </div>
                    <div className="flex flex-col items-end space-y-2">
                        <Switch checked={settings.isEnabled} onCheckedChange={(v) => setSettings({...settings, isEnabled: v})} className={cn(settings.isEnabled ? 'data-[state=checked]:bg-[#FF6B35]' : '')} />
                        <Badge className={cn(settings.isEnabled ? 'bg-green-500' : 'bg-red-500', 'text-white')}>
                            {settings.isEnabled ? 'Ativo Globalmente' : 'Inativo Globalmente'}
                        </Badge>
                    </div>
                </div>
            </Card>

            {/* 1. Mandatory System Policies */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-red-500"><Lock className="h-5 w-5 mr-2" /> Políticas Obrigatórias (Sistema)</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground">Estas políticas são mandatórias e não podem ser desativadas ou sobrescritas em nível de agente.</p>
                    
                    <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-300 dark:border-red-700">
                        <Label htmlFor="mandatorySecretDetection" className="flex flex-col space-y-1">
                            <span>Detecção de Chaves Secretas (API Keys)</span>
                            <span className="font-normal leading-snug text-xs text-muted-foreground">Proteção contra vazamento de credenciais.</span>
                        </Label>
                        <Switch id="mandatorySecretDetection" checked={settings.mandatorySecretDetection} disabled />
                    </div>

                    <div className="space-y-2">
                        <Label>PII Crítico Obrigatório</Label>
                        <div className="flex flex-wrap gap-2">
                            {settings.mandatoryPII.map(pii => (
                                <Badge key={pii} className="bg-[#4e4ea8] text-white flex items-center">
                                    {pii} <Lock className="h-3 w-3 ml-1" />
                                </Badge>
                            ))}
                            <Badge variant="secondary" className="cursor-pointer"><Plus className="h-3 w-3 mr-1" /> Adicionar Tipo</Badge>
                        </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                        <Label>Proteção Básica contra Jailbreak</Label>
                        <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                </CardContent>
            </Card>

            {/* 2. Default Account Policies */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Settings className="h-5 w-5 mr-2" /> Políticas Padrão (Conta)</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground">Estas são as configurações padrão para novos agentes, mas podem ser sobrescritas individualmente.</p>
                    
                    <div>
                        <Label>Filtro de Palavras-chave Padrão</Label>
                        <Textarea rows={2} value={settings.defaultKeywords} onChange={(e) => setSettings({...settings, defaultKeywords: e.target.value})} />
                    </div>
                    
                    <div>
                        <Label>Alinhamento de Tópico Padrão</Label>
                        <Input value={settings.defaultTopicAlignment} onChange={(e) => setSettings({...settings, defaultTopicAlignment: e.target.value})} />
                    </div>
                    
                    <div className="flex items-center justify-between">
                        <Label>Detecção de Conteúdo Impróprio (NSFW)</Label>
                        <Switch defaultChecked={false} />
                    </div>
                </CardContent>
            </Card>

            {/* 3. Policy Templates */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><Copy className="h-5 w-5 mr-2" /> Templates de Políticas</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                        {['Maximum Security', 'Balanced (Default)', 'Basic'].map(template => (
                            <Button key={template} variant="outline" onClick={() => handleApplyTemplate(template)} className="flex flex-col h-auto py-4">
                                <span className="font-semibold">{template}</span>
                                <span className="text-xs text-muted-foreground mt-1">Aplicar</span>
                            </Button>
                        ))}
                    </div>
                    <Button variant="secondary" className="w-full"><Save className="h-4 w-4 mr-2" /> Salvar Configuração Atual como Novo Template</Button>
                </CardContent>
            </Card>

            {/* 4. Billing & Credits */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-green-500"><Zap className="h-5 w-5 mr-2" /> Faturamento e Uso de Créditos</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex justify-between text-sm">
                        <span>Plano Atual:</span>
                        <Badge className="bg-green-600 text-white">{settings.billingTier}</Badge>
                    </div>
                    <div className="space-y-2">
                        <h4 className="font-semibold">Créditos LLM Usados (Mês)</h4>
                        <div className="flex justify-between text-sm">
                            <span>{settings.creditsUsed.toLocaleString()} de {settings.creditLimit.toLocaleString()}</span>
                            <span className="text-muted-foreground">{(settings.creditsUsed / settings.creditLimit * 100).toFixed(0)}% Usado</span>
                        </div>
                        <div className="h-2 w-full bg-gray-200 rounded-full">
                            <div 
                                className="h-2 bg-[#FF6B35] rounded-full" 
                                style={{ width: `${(settings.creditsUsed / settings.creditLimit * 100)}%` }}
                            ></div>
                        </div>
                    </div>
                    <Button variant="outline" className="w-full">Gerenciar Assinatura</Button>
                </CardContent>
            </Card>

            {/* 5. Audit & Logs */}
            <Card>
                <CardHeader><CardTitle className="flex items-center text-muted-foreground"><Clock className="h-5 w-5 mr-2" /> Auditoria e Logs</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Retenção de Logs de Intervenção</Label>
                        <Select value={settings.auditLogRetention} onValueChange={(v) => setSettings({...settings, auditLogRetention: v})}>
                            <SelectTrigger><SelectValue placeholder="90 dias" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="30 days">30 dias</SelectItem>
                                <SelectItem value="90 days">90 dias</SelectItem>
                                <SelectItem value="1 year">1 ano</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="flex space-x-2">
                        <Button variant="outline" className="flex-grow"><Download className="h-4 w-4 mr-2" /> Exportar Logs de Auditoria</Button>
                        <Button variant="outline" className="flex-grow"><Mail className="h-4 w-4 mr-2" /> Agendar Relatório</Button>
                    </div>
                </CardContent>
            </Card>

            <div className="flex justify-end">
                <Button onClick={handleSave} disabled={isSaving} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                    <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Configurações Globais'}
                </Button>
            </div>
        </div>
    );
};

export default GlobalGuardrailsTab;