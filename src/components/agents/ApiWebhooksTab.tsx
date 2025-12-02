import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Key, Copy, Trash2, Globe, MessageSquare, FileText, CheckCircle, XCircle, Clock, Settings, Plus, Eye } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Checkbox } from '@/components/ui/checkbox';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

interface ApiKey {
    key: string;
    name: string;
    created: string;
    lastUsed: string;
}

interface WebhookLog {
    date: string;
    event: string;
    status: string;
}

const MOCK_API_KEYS: ApiKey[] = [
    { key: 'sk-slim-abc123', name: 'Site Slim Quality', created: '15/11/2025', lastUsed: '2 min atrás' },
    { key: 'sk-slim-xyz789', name: 'WhatsApp Bot', created: '10/11/2025', lastUsed: '1 hora atrás' },
];

const MOCK_WEBHOOK_LOGS: WebhookLog[] = [
    { date: '01/12 10:23', event: 'message.received', status: '200 OK' },
    { date: '01/12 10:15', event: 'conversation.started', status: '200 OK' },
    { date: '01/12 09:47', event: 'message.received', status: '500 Error' },
];

const ApiWebhooksTab: React.FC = () => {
    const [apiKeys, setApiKeys] = useState(MOCK_API_KEYS);
    const [webhookStatus, setWebhookStatus] = useState('Funcionando');
    const [webhookEvents, setWebhookEvents] = useState({
        messageReceived: true,
        conversationStarted: true,
        toolCalled: false,
    });

    const handleCopy = (text: string, label: string) => {
        navigator.clipboard.writeText(text);
        toast.info(`${label} copiada!`);
    };

    const handleRevoke = (key: string) => {
        setApiKeys(apiKeys.filter(k => k.key !== key));
        toast.warning("Chave de API revogada.");
    };

    const handleTestWebhook = () => {
        toast.info("Enviando teste de webhook...");
        setTimeout(() => {
            setWebhookStatus('Funcionando');
            toast.success("Webhook testado com sucesso! Status: 200 OK.");
        }, 1500);
    };

    return (
        <div className="space-y-8">
            
            {/* API Keys */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]"><Key className="h-5 w-5 mr-2" /> Chaves de API</CardTitle>
                    <CardDescription>Gerencie as chaves de acesso para interagir com este agente via API.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    {apiKeys.map((keyData, index) => (
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
                    ))}
                    <Button variant="outline" className="w-full"><Plus className="h-4 w-4 mr-2" /> Gerar Nova Chave</Button>
                </CardContent>
            </Card>

            {/* Webhooks */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#FF6B35]"><Globe className="h-5 w-5 mr-2" /> Webhooks</CardTitle>
                    <CardDescription>Configure endpoints para receber notificações em tempo real sobre eventos do agente.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label>URL Webhook</Label>
                        <Input readOnly defaultValue="https://api.renum.com.br/webhook/slim/abc123" className="font-mono text-sm" />
                    </div>
                    <div className="space-y-2">
                        <Label>URL Callback (Opcional)</Label>
                        <Input readOnly defaultValue="https://slim.com.br/webhook/renum" className="font-mono text-sm" />
                    </div>
                    
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                        <span className="font-semibold text-sm">Status:</span>
                        <Badge className={cn(webhookStatus === 'Funcionando' ? 'bg-green-500' : 'bg-red-500', 'text-white')}>
                            {webhookStatus}
                        </Badge>
                    </div>

                    <div className="space-y-2">
                        <Label>Eventos Ativos</Label>
                        <div className="grid grid-cols-3 gap-4">
                            <div className="flex items-center space-x-2"><Checkbox id="msg-received" checked={webhookEvents.messageReceived} onCheckedChange={(v) => setWebhookEvents({...webhookEvents, messageReceived: v as boolean})} /><Label htmlFor="msg-received">message.received</Label></div>
                            <div className="flex items-center space-x-2"><Checkbox id="conv-started" checked={webhookEvents.conversationStarted} onCheckedChange={(v) => setWebhookEvents({...webhookEvents, conversationStarted: v as boolean})} /><Label htmlFor="conv-started">conversation.started</Label></div>
                            <div className="flex items-center space-x-2"><Checkbox id="tool-called" checked={webhookEvents.toolCalled} onCheckedChange={(v) => setWebhookEvents({...webhookEvents, toolCalled: v as boolean})} /><Label htmlFor="tool-called">tool.called</Label></div>
                        </div>
                    </div>

                    <Button onClick={handleTestWebhook} variant="outline" className="w-full"><Settings className="h-4 w-4 mr-2" /> Testar Webhook</Button>
                    
                    <Separator />

                    <h5 className="font-semibold text-sm flex items-center text-muted-foreground"><Clock className="h-4 w-4 mr-2" /> Logs Recentes</h5>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Data</TableHead>
                                <TableHead>Evento</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {MOCK_WEBHOOK_LOGS.map((log, index) => (
                                <TableRow key={index}>
                                    <TableCell className="text-xs">{log.date}</TableCell>
                                    <TableCell className="text-xs font-mono">{log.event}</TableCell>
                                    <TableCell className={cn("text-xs font-medium", log.status.startsWith('200') ? 'text-green-500' : 'text-red-500')}>
                                        {log.status}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            {/* Widget & Docs */}
            <div className="grid md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><MessageSquare className="h-5 w-5 mr-2" /> Widget de Chat</CardTitle></CardHeader>
                    <CardContent className="space-y-3">
                        <Label>Código Embed</Label>
                        <Textarea readOnly rows={3} defaultValue="<script src='renum.js' data-agent='slim-vendas'></script>" className="font-mono text-xs" />
                        <p className="text-sm">Cor Primária: <Badge style={{ backgroundColor: '#6366F1' }} className="text-white">#6366F1</Badge></p>
                        <p className="text-sm">Posição: bottom-right</p>
                        <Button variant="outline" className="w-full"><Eye className="h-4 w-4 mr-2" /> Preview do Widget</Button>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><FileText className="h-5 w-5 mr-2" /> Documentação</CardTitle></CardHeader>
                    <CardContent className="space-y-3">
                        <p className="text-sm text-muted-foreground">Acesse a documentação completa da API para este agente.</p>
                        <Button variant="link" className="p-0 h-auto text-[#4e4ea8]">
                            Ver Docs da API →
                        </Button>
                        <p className="text-xs font-mono mt-2">Endpoint: /api/v1/agents/slim-vendas</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default ApiWebhooksTab;