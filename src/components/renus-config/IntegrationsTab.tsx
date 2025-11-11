import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea'; // Adicionando Textarea
import { Zap, Mail, Calendar, MessageSquare, Database, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

interface Integration {
  name: string;
  icon: React.ElementType;
  status: 'connected' | 'disconnected' | 'pending';
  color: string;
  configFields: { label: string; key: string; type: string; placeholder: string }[];
}

const MOCK_INTEGRATIONS: Integration[] = [
  {
    name: 'WhatsApp Business API',
    icon: MessageSquare,
    status: 'connected',
    color: 'text-green-500',
    configFields: [
      { label: 'Token de Acesso', key: 'wa_token', type: 'password', placeholder: 'WA-XXXXX' },
      { label: 'ID do Número', key: 'wa_id', type: 'text', placeholder: '123456789' },
    ],
  },
  {
    name: 'Email SMTP',
    icon: Mail,
    status: 'disconnected',
    color: 'text-red-500',
    configFields: [
      { label: 'Servidor SMTP', key: 'smtp_server', type: 'text', placeholder: 'smtp.renum.tech' },
      { label: 'Porta', key: 'smtp_port', type: 'number', placeholder: '587' },
      { label: 'Senha', key: 'smtp_password', type: 'password', placeholder: '••••••••' },
    ],
  },
  {
    name: 'Google Calendar',
    icon: Calendar,
    status: 'pending',
    color: 'text-yellow-500',
    configFields: [
      { label: 'Chave API', key: 'cal_api', type: 'password', placeholder: 'G-XXXXX' },
      { label: 'ID do Calendário', key: 'cal_id', type: 'text', placeholder: 'consultoria@renum.tech' },
    ],
  },
  {
    name: 'CRM (Mock DB)',
    icon: Database,
    status: 'connected',
    color: 'text-green-500',
    configFields: [
      { label: 'Endpoint', key: 'crm_endpoint', type: 'text', placeholder: 'https://api.crm.com/v1' },
      { label: 'Chave Secreta', key: 'crm_secret', type: 'password', placeholder: 'S-XXXXX' },
    ],
  },
];

const IntegrationsTab: React.FC = () => {
  const [integrations, setIntegrations] = useState(MOCK_INTEGRATIONS);
  const [configData, setConfigData] = useState<Record<string, string>>({});
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

  return (
    <div className="space-y-8">
      <div className="grid md:grid-cols-2 gap-6">
        {integrations.map((integration, index) => (
          <Card key={index} className={cn(
            "border-l-4",
            integration.status === 'connected' && 'border-green-500',
            integration.status === 'disconnected' && 'border-red-500',
            integration.status === 'pending' && 'border-yellow-500',
          )}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-lg flex items-center">
                <integration.icon className={cn("h-5 w-5 mr-2", integration.color)} />
                {integration.name}
              </CardTitle>
              <div className="flex items-center space-x-2">
                {getStatusIcon(integration.status)}
                <span className="text-sm font-medium capitalize">
                  {integration.status === 'connected' ? 'Conectado' : integration.status === 'disconnected' ? 'Desconectado' : 'Pendente'}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4 pt-4">
              {integration.configFields.map(field => (
                <div key={field.key}>
                  <Label htmlFor={field.key}>{field.label}</Label>
                  <Input
                    id={field.key}
                    type={field.type}
                    placeholder={field.placeholder}
                    value={configData[field.key] || ''}
                    onChange={(e) => setConfigData({ ...configData, [field.key]: e.target.value })}
                  />
                </div>
              ))}
              <Button 
                className="w-full bg-[#FF6B35] hover:bg-[#e55f30]"
                onClick={() => handleTestConnection(integration.name, integration.status)}
                disabled={isTesting}
              >
                {isTesting ? 'Testando...' : 'Salvar e Testar Conexão'}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-[#0ca7d2]">Configuração de Templates (Mock)</CardTitle>
          <CardDescription>Gerencie os templates de mensagens para WhatsApp e Email.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
                <div>
                    <Label>Template de Boas-Vindas (WhatsApp)</Label>
                    <Textarea rows={3} defaultValue="Olá {{client_name}}, sou Renus. Seu projeto {{project_name}} está na fase {{status}}." />
                </div>
                <div>
                    <Label>Template de Follow-up (Email)</Label>
                    <Textarea rows={3} defaultValue="Prezado(a) {{client_name}}, gostaríamos de agendar uma call para discutir o próximo marco." />
                </div>
            </div>
            <Button variant="outline">Salvar Templates</Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default IntegrationsTab;