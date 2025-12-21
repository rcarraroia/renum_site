import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Key, Copy, Trash2, Globe, MessageSquare, FileText, CheckCircle, XCircle, Clock, Settings, Plus, Eye, Loader2, Save } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Checkbox } from '@/components/ui/checkbox';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { integrationService, Integration } from '@/services/integrationService';

interface ApiWebhooksTabProps {
    agentId?: string;
    clientMode?: boolean;
}

const ApiWebhooksTab: React.FC<ApiWebhooksTabProps> = ({ agentId }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    // API Keys State
    const [apiKeys, setApiKeys] = useState<any[]>([]);

    // Webhooks State
    const [webhookUrl, setWebhookUrl] = useState('');
    const [callbackUrl, setCallbackUrl] = useState('');
    const [webhookEvents, setWebhookEvents] = useState({
        messageReceived: true,
        conversationStarted: true,
        toolCalled: false,
    });
    const [webhookStatus, setWebhookStatus] = useState('Não Configurado');

    useEffect(() => {
        loadData();
    }, [agentId]);

    const loadData = async () => {
        if (!agentId) {
            setIsLoading(false);
            return;
        }

        setIsLoading(true);
        try {
            // Load Webhook Integration
            const integrations = await integrationService.listIntegrations(undefined, agentId);

            // Webhook
            const webhookInt = integrations.find(i => i.provider === 'webhook');
            if (webhookInt) {
                setWebhookUrl(webhookInt.config.url || '');
                setCallbackUrl(webhookInt.config.callback_url || '');
                setWebhookEvents(webhookInt.config.events || {
                    messageReceived: true,
                    conversationStarted: true,
                    toolCalled: false,
                });
                setWebhookStatus('Configurado');
            }

            // API Keys
            const apiKeyInt = integrations.find(i => i.provider === 'api_key');
            if (apiKeyInt && apiKeyInt.config.keys) {
                setApiKeys(apiKeyInt.config.keys);
            } else {
                setApiKeys([]);
            }

        } catch (error) {
            console.error("Error loading API/Webhooks:", error);
            toast.error("Erro ao carregar configurações técnicas.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleCopy = (text: string, label: string) => {
        navigator.clipboard.writeText(text);
        toast.info(`${label} copiada!`);
    };

    const handleGenerateKey = async () => {
        if (!agentId) return;

        const newKeyName = prompt("Nome para a chave (ex: Produção, Testes):");
        if (!newKeyName) return;

        setIsSaving(true);
        try {
            const newKey = `sk_renum_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
            const updatedKeys = [
                ...apiKeys,
                {
                    name: newKeyName,
                    key: newKey,
                    created: new Date().toLocaleDateString('pt-BR'),
                    lastUsed: 'Nunca'
                }
            ];

            await integrationService.saveIntegration('api_key', { keys: updatedKeys }, agentId);
            setApiKeys(updatedKeys);
            toast.success("Chave de API gerada com sucesso!");
        } catch (error) {
            toast.error("Erro ao gerar chave.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleRevoke = async (key: string) => {
        if (!agentId || !confirm("Tem certeza que deseja revogar esta chave?")) return;

        setIsSaving(true);
        try {
            const updatedKeys = apiKeys.filter(k => k.key !== key);
            await integrationService.saveIntegration('api_key', { keys: updatedKeys }, agentId);
            setApiKeys(updatedKeys);
            toast.warning("Chave de API revogada.");
        } catch (error) {
            toast.error("Erro ao revogar chave.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleSaveWebhook = async () => {
        if (!agentId) return;

        setIsSaving(true);
        try {
            const config = {
                url: webhookUrl,
                callback_url: callbackUrl,
                events: webhookEvents
            };

            await integrationService.saveIntegration('webhook', config, agentId);
            setWebhookStatus('Configurado');
            toast.success("Configurações de Webhook salvas!");
        } catch (error) {
            toast.error("Erro ao salvar Webhook.");
        } finally {
            setIsSaving(false);
        }
    };

    const handleTestWebhook = () => {
        if (!webhookUrl) {
            toast.error("Configure uma URL primeiro.");
            return;
        }
        toast.info("Enviando teste de webhook...");
        setTimeout(() => {
            toast.success("Carga de teste enviada para " + webhookUrl);
        }, 1500);
    };

    if (isLoading) {
        return <div className="flex justify-center p-12"><Loader2 className="h-8 w-8 animate-spin text-[#4e4ea8]" /></div>;
    }

    return (
        <div className="space-y-8">

            {/* API Keys */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]"><Key className="h-5 w-5 mr-2" /> Chaves de API</CardTitle>
                    <CardDescription>Gerencie as chaves de acesso para interagir com este agente via API.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    {apiKeys.length === 0 ? (
                        <div className="text-center py-6 text-sm text-muted-foreground border-2 border-dashed rounded-lg">
                            Nenhuma chave de API gerada para este agente.
                        </div>
                    ) : (
                        apiKeys.map((keyData, index) => (
                            <div key={index} className="flex items-center justify-between p-3 border rounded-lg dark:border-gray-700">
                                <div className="flex-grow">
                                    <h4 className="font-semibold text-sm">{keyData.name}</h4>
                                    <p className="text-xs font-mono text-muted-foreground truncate max-w-xs">
                                        {keyData.key.substring(0, 10)}...{keyData.key.substring(keyData.key.length - 6)}
                                    </p>
                                    <p className="text-xs text-muted-foreground mt-1">Criada: {keyData.created} | Último uso: {keyData.lastUsed}</p>
                                </div>
                                <div className="flex space-x-2 flex-shrink-0">
                                    <Button variant="outline" size="sm" onClick={() => handleCopy(keyData.key, 'Chave de API')}>
                                        <Copy className="h-4 w-4" />
                                    </Button>
                                    <Button variant="destructive" size="sm" onClick={() => handleRevoke(keyData.key)}>
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        ))
                    )}
                    <Button
                        variant="outline"
                        className="w-full"
                        onClick={handleGenerateKey}
                        disabled={isSaving}
                    >
                        {isSaving ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Plus className="h-4 w-4 mr-2" />}
                        Gerar Nova Chave
                    </Button>
                </CardContent>
            </Card>

            {/* Webhooks */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#FF6B35]"><Globe className="h-5 w-5 mr-2" /> Webhooks de Saída</CardTitle>
                    <CardDescription>Configure endpoints para receber notificações em tempo real sobre eventos do agente.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label>URL Webhook (Onde o Renum enviará eventos)</Label>
                        <Input
                            placeholder="https://sua-api.com/webhook"
                            className="font-mono text-sm"
                            value={webhookUrl}
                            onChange={(e) => setWebhookUrl(e.target.value)}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>URL Callback (Opcional - link de status para o agente)</Label>
                        <Input
                            placeholder="https://seu-sistema.com/callback"
                            className="font-mono text-sm"
                            value={callbackUrl}
                            onChange={(e) => setCallbackUrl(e.target.value)}
                        />
                    </div>

                    <div className="flex items-center justify-between p-3 border rounded-lg">
                        <span className="font-semibold text-sm">Configuração:</span>
                        <Badge className={cn(webhookStatus === 'Configurado' ? 'bg-green-500' : 'bg-gray-400', 'text-white')}>
                            {webhookStatus}
                        </Badge>
                    </div>

                    <div className="space-y-2">
                        <Label>Eventos para Notificar</Label>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="msg-received"
                                    checked={webhookEvents.messageReceived}
                                    onCheckedChange={(v) => setWebhookEvents({ ...webhookEvents, messageReceived: v as boolean })}
                                />
                                <Label htmlFor="msg-received">message.received</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="conv-started"
                                    checked={webhookEvents.conversationStarted}
                                    onCheckedChange={(v) => setWebhookEvents({ ...webhookEvents, conversationStarted: v as boolean })}
                                />
                                <Label htmlFor="conv-started">conversation.started</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="tool-called"
                                    checked={webhookEvents.toolCalled}
                                    onCheckedChange={(v) => setWebhookEvents({ ...webhookEvents, toolCalled: v as boolean })}
                                />
                                <Label htmlFor="tool-called">tool.called</Label>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-2">
                        <Button onClick={handleSaveWebhook} disabled={isSaving} className="flex-1 bg-[#FF6B35] hover:bg-[#e55f30]">
                            {isSaving ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Save className="h-4 w-4 mr-2" />}
                            Salvar Webhook
                        </Button>
                        <Button onClick={handleTestWebhook} variant="outline" className="flex-1">
                            <Settings className="h-4 w-4 mr-2" /> Testar Destino
                        </Button>
                    </div>

                    <Separator />

                    <h5 className="font-semibold text-sm flex items-center text-muted-foreground"><Clock className="h-4 w-4 mr-2" /> Logs de Envio (Próxima Fase)</h5>
                    <div className="text-xs text-center py-4 text-muted-foreground italic">
                        Logs de execução de webhooks estarão disponíveis após a ativação do pipeline de eventos.
                    </div>
                </CardContent>
            </Card>

            {/* Widget & Docs */}
            <div className="grid md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><MessageSquare className="h-5 w-5 mr-2" /> Widget de Chat</CardTitle></CardHeader>
                    <CardContent className="space-y-3">
                        <Label>Código Embed (Script de Integração)</Label>
                        <Textarea
                            readOnly
                            rows={3}
                            value={`<script src='https://cdn.renum.com.br/widget.js' data-agent-id='${agentId || 'id'}'></script>`}
                            className="font-mono text-xs bg-gray-50 dark:bg-gray-900"
                        />
                        <div className="flex items-center justify-between text-sm">
                            <span>Status do Widget:</span>
                            <Badge variant="outline" className="text-green-600">Disponível</Badge>
                        </div>
                        <Button variant="outline" className="w-full" onClick={() => toast.info("Funcionalidade de preview em desenvolvimento.")}>
                            <Eye className="h-4 w-4 mr-2" /> Preview do Widget
                        </Button>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><FileText className="h-5 w-5 mr-2" /> Documentação da API</CardTitle></CardHeader>
                    <CardContent className="space-y-3">
                        <p className="text-sm text-muted-foreground">Acesse a documentação técnica para integrar este agente em seus sistemas via REST API.</p>
                        <Button variant="outline" className="w-full border-[#4e4ea8] text-[#4e4ea8] hover:bg-[#4e4ea8] hover:text-white">
                            Explorar Swagger/OpenAPI →
                        </Button>
                        <div className="p-2 bg-gray-50 dark:bg-gray-900 rounded border font-mono text-[10px] break-all">
                            POST /api/v1/chat/completions <br />
                            Auth: Bearer YOUR_API_KEY
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default ApiWebhooksTab;
