import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Zap, Key, Copy, Trash2, Globe, MessageSquare, RefreshCw, Clock, FileText, CheckCircle, XCircle, Settings, Code, ChevronDown, ChevronUp, Plus } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { Agent } from '@/types/agent';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Textarea } from '@/components/ui/textarea';

interface ApiWebhooksTabProps {
  agent: Agent;
}

const ApiWebhooksTab: React.FC<ApiWebhooksTabProps> = ({ agent }) => {
  const [isWebhookLogsOpen, setIsWebhookLogsOpen] = useState(false);

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.info(`${label} copiado!`);
  };

  const handleRevoke = (key: string) => {
    toast.warning(`Chave ${key.substring(0, 10)}... revogada (Mock).`);
  };

  const handleTestWebhook = () => {
    toast.info("Simulando teste de webhook...");
    setTimeout(() => {
        toast.success("Webhook testado com sucesso! Resposta 200 OK.");
    }, 1000);
  };

  return (
    <div className="space-y-8">
      
      {/* API Keys */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <Key className="h-5 w-5 mr-2" /> Chaves de API
          </CardTitle>
          <CardDescription>Gerencie as chaves de acesso para interagir com a API do agente.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Chave</TableHead>
                <TableHead>Nome</TableHead>
                <TableHead>Criada</TableHead>
                <TableHead>Último Uso</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {agent.apiKeys.map((key, index) => (
                <TableRow key={index}>
                  <TableCell className="font-mono text-xs">
                    {key.key.substring(0, 10)}***{key.key.substring(key.key.length - 6)}
                  </TableCell>
                  <TableCell>{key.name}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">{key.createdAt}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">{key.lastUsed}</TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button variant="ghost" size="sm" onClick={() => handleCopy(key.key, 'Chave API')}>
                      <Copy className="h-4 w-4" />
                    </Button>
                    <Button variant="destructive" size="sm" onClick={() => handleRevoke(key.key)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Button variant="outline" className="mt-4">
            <Plus className="h-4 w-4 mr-2" /> Gerar Nova Chave
          </Button>
        </CardContent>
      </Card>

      {/* Webhooks */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Globe className="h-5 w-5 mr-2" /> Webhooks
          </CardTitle>
          <CardDescription>Configure endpoints para receber notificações de eventos do agente.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>URL Webhook</Label>
            <div className="flex space-x-2">
                <Input readOnly value={agent.webhookConfig.url} className="font-mono text-sm" />
                <Button variant="outline" size="icon" onClick={() => handleCopy(agent.webhookConfig.url, 'URL Webhook')}><Copy className="h-4 w-4" /></Button>
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
                <Label>URL Callback (Opcional)</Label>
                <Input value={agent.webhookConfig.callbackUrl} placeholder="https://seuapp.com/callback" />
            </div>
            <div>
                <Label>Status</Label>
                <div className="flex items-center space-x-2 mt-2">
                    {agent.webhookConfig.status === 'Funcionando' ? (
                        <Badge className="bg-green-500 text-white flex items-center"><CheckCircle className="h-4 w-4 mr-1" /> Funcionando</Badge>
                    ) : (
                        <Badge className="bg-red-500 text-white flex items-center"><XCircle className="h-4 w-4 mr-1" /> {agent.webhookConfig.status}</Badge>
                    )}
                    <Button variant="outline" size="sm" onClick={handleTestWebhook}><RefreshCw className="h-4 w-4 mr-2" /> Testar</Button>
                </div>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label>Eventos Ativos</Label>
            <div className="flex flex-wrap gap-2">
                {agent.webhookConfig.events.map(event => (
                    <Badge key={event} variant="secondary" className="flex items-center">
                        <MessageSquare className="h-3 w-3 mr-1" /> {event}
                    </Badge>
                ))}
            </div>
          </div>

          <Collapsible open={isWebhookLogsOpen} onOpenChange={setIsWebhookLogsOpen}>
            <CollapsibleTrigger asChild>
                <Button variant="link" className="p-0 h-auto text-[#0ca7d2] flex items-center">
                    <Clock className="h-4 w-4 mr-2" /> Logs Recentes ({agent.webhookConfig.logs.length})
                    {isWebhookLogsOpen ? <ChevronUp className="h-4 w-4 ml-1" /> : <ChevronDown className="h-4 w-4 ml-1" />}
                </Button>
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-2 border rounded-lg overflow-hidden">
                <Table>
                    <TableBody>
                        {agent.webhookConfig.logs.map((log, index) => (
                            <TableRow key={index} className={cn(log.status.includes('500') && 'bg-red-50/50 dark:bg-red-900/20')}>
                                <TableCell className="text-xs font-mono">{log.date}</TableCell>
                                <TableCell className="text-xs">{log.event}</TableCell>
                                <TableCell className={cn("text-xs font-semibold", log.status.includes('200') ? 'text-green-600' : 'text-red-600')}>{log.status}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CollapsibleContent>
          </Collapsible>
        </CardContent>
      </Card>

      {/* Widget Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#0ca7d2]">
            <Code className="h-5 w-5 mr-2" /> Widget de Chat (Web)
          </CardTitle>
          <CardDescription>Configure e obtenha o código para incorporar o agente no seu site.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
                <div>
                    <Label>Cor Primária</Label>
                    <Input type="color" value={agent.widgetConfig.primaryColor} className="w-full h-10 p-1" />
                </div>
                <div>
                    <Label>Posição</Label>
                    <Input readOnly value={agent.widgetConfig.position} />
                </div>
            </div>
            <Separator />
            <div className="space-y-2">
                <Label>Código de Incorporação (Embed Code)</Label>
                <div className="flex space-x-2">
                    <Textarea readOnly rows={2} value={agent.widgetConfig.embedCode} className="font-mono text-xs bg-gray-100 dark:bg-gray-800" />
                    <Button variant="outline" size="icon" onClick={() => handleCopy(agent.widgetConfig.embedCode, 'Código Embed')}><Copy className="h-4 w-4" /></Button>
                </div>
            </div>
        </CardContent>
      </Card>
      
      {/* Documentation Link */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-green-500">
            <FileText className="h-5 w-5 mr-2" /> Documentação
          </CardTitle>
        </CardHeader>
        <CardContent>
            <Button variant="link" className="p-0 h-auto">
                Ver Documentação da API para Agente {agent.name}
            </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default ApiWebhooksTab;