import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Zap, Mail, Calendar, MessageSquare, Database, CheckCircle, XCircle, RefreshCw, Settings, Edit, Globe } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

interface Integration {
  name: string;
  icon: React.ElementType;
  status: 'connected' | 'disconnected' | 'pending';
  color: string;
  details: string[];
}

const MOCK_INTEGRATIONS: Integration[] = [
  {
    name: 'WhatsApp Business',
    icon: MessageSquare,
    status: 'connected',
    color: 'text-green-500',
    details: ['Provider: Uazapi', 'Configurado em: 14/11/2025', 'Phone: +55 11 99999-9999'],
  },
  {
    name: 'Gmail',
    icon: Mail,
    status: 'connected',
    color: 'text-red-500',
    details: ['Email: vendas@slim.com'],
  },
  {
    name: 'Google Workspace',
    icon: Globe,
    status: 'pending',
    color: 'text-yellow-500',
    details: ['Apps conectados: Docs, Sheets, Calendar'],
  },
  {
    name: 'Composio',
    icon: Zap,
    status: 'disconnected',
    color: 'text-purple-500',
    details: ['Plataforma de automação de workflows.'],
  },
  {
    name: 'SMTP Custom',
    icon: Mail,
    status: 'disconnected',
    color: 'text-gray-500',
    details: ['Configuração manual de servidor de email.'],
  },
];

const AgentIntegrationsTab: React.FC = () => {
  const [integrations, setIntegrations] = useState(MOCK_INTEGRATIONS);
  const [isTesting, setIsTesting] = useState(false);

  const handleTestConnection = (name: string, status: Integration['status']) => {
    setIsTesting(true);
    toast.info(`Testando conexão com ${name}...`);
    setTimeout(() => {
      setIsTesting(false);
      const newStatus = status === 'connected' ? 'disconnected' : 'connected';
      setIntegrations(integrations.map(i => (i.name === name ? { ...i, status: newStatus } : i)));
      toast.success(`Conexão com ${name} ${newStatus === 'connected' ? 'restabelecida!' : 'falhou.'}`);
    }, 1500);
  };

  const getStatusIcon = (status: Integration['status']) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'disconnected':
        return <XCircle className="h-5 w-5 text-red-500" />;
      case 'pending':
        return <RefreshCw className="h-5 w-5 text-yellow-500 animate-spin" />;
    }
  };

  const getStatusLabel = (status: Integration['status']) => {
    switch (status) {
      case 'connected': return 'Configurado';
      case 'disconnected': return 'Não Configurado';
      case 'pending': return 'Parcialmente Configurado';
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <RefreshCw className="h-5 w-5 mr-2" /> Integrações do Agente
          </CardTitle>
          <CardDescription>
            Conecte serviços externos para permitir que o agente execute ações e acesse dados.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-6">
          {integrations.map((integration, index) => (
            <div key={index} className={cn(
              "p-4 border rounded-lg space-y-3",
              integration.status === 'connected' && 'border-l-4 border-green-500',
              integration.status === 'disconnected' && 'border-l-4 border-red-500',
              integration.status === 'pending' && 'border-l-4 border-yellow-500',
            )}>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <integration.icon className={cn("h-5 w-5", integration.color)} />
                  <h4 className="font-semibold">{integration.name}</h4>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(integration.status)}
                  <span className="text-sm font-medium capitalize">
                    {getStatusLabel(integration.status)}
                  </span>
                </div>
              </div>
              
              <Separator />

              <div className="space-y-1 text-sm text-muted-foreground">
                {integration.details.map((detail, i) => (
                    <p key={i}>{detail}</p>
                ))}
              </div>
              
              <div className="flex space-x-2 pt-2">
                <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => toast.info(`Abrindo edição para ${integration.name}`)}
                >
                    <Edit className="h-4 w-4 mr-2" /> Editar
                </Button>
                <Button 
                    variant={integration.status === 'connected' ? 'destructive' : 'default'} 
                    size="sm"
                    onClick={() => handleTestConnection(integration.name, integration.status)}
                    disabled={isTesting}
                >
                    {integration.status === 'connected' ? 'Desconectar' : 'Configurar'}
                </Button>
                {integration.status === 'connected' && (
                    <Button 
                        variant="secondary" 
                        size="sm"
                        onClick={() => handleTestConnection(integration.name, integration.status)}
                        disabled={isTesting}
                    >
                        Testar
                    </Button>
                )}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};

export default AgentIntegrationsTab;