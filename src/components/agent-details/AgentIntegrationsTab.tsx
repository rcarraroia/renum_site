import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Zap, Mail, Calendar, MessageSquare, Database, CheckCircle, XCircle, RefreshCw, Settings, Edit, Plug, Info, Phone } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Agent, AgentIntegration } from '@/types/agent';
import { Badge } from '@/components/ui/badge';

interface AgentIntegrationsTabProps {
  agent: Agent;
}

const getIntegrationIcon = (name: string) => {
    switch (name) {
        case 'WhatsApp Business': return MessageSquare;
        case 'Gmail': return Mail;
        case 'Google Workspace': return Calendar;
        case 'Composio': return Database;
        case 'SMTP Custom': return Settings;
        default: return Plug;
    }
};

const getStatusColor = (status: AgentIntegration['status']) => {
    switch (status) {
        case 'Configurado': return 'text-green-500';
        case 'Não configurado': return 'text-red-500';
        case 'Parcialmente configurado': return 'text-yellow-500';
    }
};

const AgentIntegrationsTab: React.FC<AgentIntegrationsTabProps> = ({ agent }) => {
  const [isTesting, setIsTesting] = useState(false);

  const handleTestConnection = (name: string) => {
    setIsTesting(true);
    toast.info(`Testando conexão com ${name}...`);
    setTimeout(() => {
      setIsTesting(false);
      toast.success(`Conexão com ${name} verificada com sucesso!`);
    }, 1500);
  };

  return (
    <div className="space-y-8">
        <Card className="border-l-4 border-[#0ca7d2]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#0ca7d2]">
                    <Zap className="h-5 w-5 mr-2" /> Integrações do Agente
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Gerencie as conexões externas para o agente: <strong>{agent.name}</strong>.
                </p>
            </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
            {agent.integrations.map((integration, index) => {
                const Icon = getIntegrationIcon(integration.name);
                const statusColor = getStatusColor(integration.status);
                const isConfigured = integration.status === 'Configurado' || integration.status === 'Parcialmente configurado';

                return (
                    <Card key={index} className={cn(
                        "border-l-4",
                        integration.status === 'Configurado' && 'border-green-500',
                        integration.status === 'Não configurado' && 'border-red-500',
                        integration.status === 'Parcialmente configurado' && 'border-yellow-500',
                    )}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-lg flex items-center">
                                <Icon className={cn("h-5 w-5 mr-2", statusColor)} />
                                {integration.name}
                            </CardTitle>
                            <Badge className={cn(
                                "capitalize",
                                integration.status === 'Configurado' && 'bg-green-500 text-white',
                                integration.status === 'Não configurado' && 'bg-red-500 text-white',
                                integration.status === 'Parcialmente configurado' && 'bg-yellow-500 text-gray-900',
                            )}>
                                {integration.status}
                            </Badge>
                        </CardHeader>
                        <CardContent className="space-y-3 pt-4">
                            {integration.provider && (
                                <div className="text-sm">
                                    <span className="font-semibold">Provider:</span> {integration.provider}
                                </div>
                            )}
                            {integration.details.phone && (
                                <div className="text-sm flex items-center">
                                    <Phone className="h-4 w-4 mr-2 text-muted-foreground" />
                                    <span className="font-semibold">Telefone:</span> {integration.details.phone}
                                </div>
                            )}
                            {integration.details.email && (
                                <div className="text-sm flex items-center">
                                    <Mail className="h-4 w-4 mr-2 text-muted-foreground" />
                                    <span className="font-semibold">Email:</span> {integration.details.email}
                                </div>
                            )}
                            {integration.details.apps && (
                                <div className="text-sm flex items-center">
                                    <Info className="h-4 w-4 mr-2 text-muted-foreground" />
                                    <span className="font-semibold">Apps Conectados:</span> {integration.details.apps}
                                </div>
                            )}
                            {integration.configuredAt && (
                                <div className="text-xs text-muted-foreground">
                                    Configurado em: {integration.configuredAt}
                                </div>
                            )}
                            
                            <Separator />

                            <div className="flex space-x-2">
                                {isConfigured ? (
                                    <>
                                        <Button variant="outline" size="sm" onClick={() => toast.info(`Abrindo edição para ${integration.name}`)}>
                                            <Edit className="h-4 w-4 mr-2" /> Editar
                                        </Button>
                                        <Button variant="outline" size="sm" onClick={() => handleTestConnection(integration.name)} disabled={isTesting}>
                                            <RefreshCw className="h-4 w-4 mr-2" /> Testar
                                        </Button>
                                        <Button variant="destructive" size="sm" onClick={() => toast.warning(`Desconectando ${integration.name}`)}>
                                            <XCircle className="h-4 w-4 mr-2" /> Desconectar
                                        </Button>
                                    </>
                                ) : (
                                    <Button className="bg-[#FF6B35] hover:bg-[#e55f30] w-full">
                                        <Settings className="h-4 w-4 mr-2" /> Configurar
                                    </Button>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                );
            })}
        </div>
    </div>
  );
};

export default AgentIntegrationsTab;