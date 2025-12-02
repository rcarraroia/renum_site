import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, Mail, Calendar, MessageSquare, Database, CheckCircle, XCircle, RefreshCw, Settings, Edit, Globe, ArrowUpCircle, Clock, Link, Phone, Wrench } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import WhatsappConfigModal from './modals/WhatsappConfigModal.tsx';
import GmailConfigModal from './modals/GmailConfigModal.tsx';
import WorkspaceConfigModal from './modals/WorkspaceConfigModal.tsx';
import ComposioConfigModal from './modals/ComposioConfigModal.tsx';
import SmtpCustomConfigModal from './modals/SmtpCustomConfigModal.tsx';

interface IntegrationConfig {
  name: string;
  icon: React.ElementType;
  status: 'connected' | 'disconnected' | 'pending';
  color: string;
  provider: string;
  details: string[];
  modalType: 'whatsapp' | 'gmail' | 'workspace' | 'composio' | 'smtp' | 'none';
  configData: any;
}

const MOCK_INTEGRATIONS: IntegrationConfig[] = [
  {
    name: 'WhatsApp Business',
    icon: MessageSquare,
    status: 'connected',
    color: 'text-green-600',
    provider: 'Uazapi',
    details: ['Configurado em: 14/11/2025', 'Phone: +55 11 99999-9999', 'Permite: Envio/Recebimento'],
    modalType: 'whatsapp',
    configData: { token: 'WA-XXXXX', url: 'https://api.uazapi.com', phoneId: '5511999999999', isConnected: true },
  },
  {
    name: 'Gmail / Email',
    icon: Mail,
    status: 'connected',
    color: 'text-red-600',
    provider: 'Composio / Gmail API',
    details: ['Email conectado: vendas@slim.com', 'Permite: Enviar emails automáticos'],
    modalType: 'gmail',
    configData: { method: 'oauth', email: 'vendas@slim.com', host: '', port: '', password: '', isConnected: true },
  },
  {
    name: 'Google Workspace',
    icon: Globe,
    status: 'pending',
    color: 'text-yellow-600',
    provider: 'Composio',
    details: ['Apps conectados: Docs, Sheets, Calendar'],
    modalType: 'workspace',
    configData: { apps: ['docs', 'sheets', 'calendar'], isConnected: false },
  },
  {
    name: 'Composio Platform',
    icon: Zap,
    status: 'disconnected',
    color: 'text-purple-600',
    provider: '500+ apps disponíveis',
    details: ['Slack, GitHub, Notion, Airtable, Salesforce, HubSpot, Linear e +'],
    modalType: 'composio',
    configData: { apiKey: '', entityId: '', isConnected: false },
  },
  {
    name: 'Servidor SMTP Custom',
    icon: Mail,
    status: 'disconnected',
    color: 'text-gray-600',
    provider: 'SendGrid, Mailgun, custom',
    details: ['Envio de emails transacionais e notificações do sistema'],
    modalType: 'smtp',
    configData: { host: '', port: '', email: '', password: '', useTls: true, isConnected: false },
  },
];

const FUTURE_INTEGRATIONS = [
    { name: 'Telegram', icon: MessageSquare, color: 'text-blue-400' },
    { name: 'SMS (Twilio)', icon: MessageSquare, color: 'text-orange-400' },
    { name: 'Voice (Chamadas)', icon: Phone, color: 'text-green-400' },
    { name: 'Zapier', icon: Zap, color: 'text-red-400' },
    { name: 'Make.com', icon: Wrench, color: 'text-yellow-400' },
];

const IntegrationsTab: React.FC = () => {
  const [integrations, setIntegrations] = useState(MOCK_INTEGRATIONS);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIntegration, setSelectedIntegration] = useState<IntegrationConfig | null>(null);
  
  // Mock agent slug for webhook URL generation
  const agentSlug = 'slim-vendas'; 

  const handleOpenModal = (integration: IntegrationConfig) => {
    setSelectedIntegration(integration);
    setIsModalOpen(true);
  };

  const handleSaveConfig = (updatedConfig: any) => {
    if (!selectedIntegration) return;

    const newStatus = updatedConfig.isConnected || updatedConfig.email || updatedConfig.apiKey ? 'connected' : 'disconnected';
    
    setIntegrations(prev => prev.map(i => 
      i.name === selectedIntegration.name 
        ? { 
            ...i, 
            status: newStatus, 
            configData: updatedConfig,
            details: i.modalType === 'gmail' && updatedConfig.email ? [`Email conectado: ${updatedConfig.email}`, ...i.details.slice(1)] : i.details,
        } 
        : i
    ));
    setIsModalOpen(false);
  };

  const getStatusIcon = (status: IntegrationConfig['status']) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'disconnected':
        return <XCircle className="h-5 w-5 text-red-500" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusLabel = (status: IntegrationConfig['status']) => {
    switch (status) {
      case 'connected': return 'Configurado';
      case 'disconnected': return 'Não Configurado';
      case 'pending': return 'Parcialmente Configurado';
    }
  };
  
  const renderModal = () => {
    if (!selectedIntegration) return null;

    switch (selectedIntegration.modalType) {
      case 'whatsapp':
        return (
          <WhatsappConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialConfig={selectedIntegration.configData}
            onSave={handleSaveConfig}
            agentSlug={agentSlug}
          />
        );
      case 'gmail':
        return (
          <GmailConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialConfig={selectedIntegration.configData}
            onSave={handleSaveConfig}
          />
        );
      case 'workspace':
        return (
          <WorkspaceConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialApps={selectedIntegration.configData.apps}
            onSave={(apps) => handleSaveConfig({ ...selectedIntegration.configData, apps, isConnected: apps.length > 0 })}
          />
        );
      case 'composio':
        return (
          <ComposioConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialConfig={selectedIntegration.configData}
            onSave={handleSaveConfig}
          />
        );
      case 'smtp':
        return (
          <SmtpCustomConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialConfig={selectedIntegration.configData}
            onSave={handleSaveConfig}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-8">
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
                    variant={integration.status === 'connected' ? 'outline' : 'default'} 
                    size="sm"
                    onClick={() => handleOpenModal(integration)}
                    className={cn(integration.status === 'connected' ? '' : 'bg-[#FF6B35] hover:bg-[#e55f30]')}
                >
                    <Settings className="h-4 w-4 mr-2" /> 
                    {integration.status === 'connected' ? 'Editar Configuração' : 'Configurar'}
                </Button>
                {integration.status === 'connected' && (
                    <Button 
                        variant="destructive" 
                        size="sm"
                        onClick={() => toast.warning(`Desconectando ${integration.name}...`)}
                    >
                        <XCircle className="h-4 w-4 mr-2" /> Desconectar
                    </Button>
                )}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      
      {/* Seção Em Breve */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Clock className="h-5 w-5 mr-2" /> 🔜 Em Breve
          </CardTitle>
          <CardDescription>
            Integrações que estão no nosso roadmap e serão lançadas em breve.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid md:grid-cols-3 gap-4">
            {FUTURE_INTEGRATIONS.map((integration, index) => (
                <Card key={index} className="p-4 opacity-50 border-dashed">
                    <div className="flex items-center space-x-2 mb-2">
                        <integration.icon className={cn("h-5 w-5", integration.color)} />
                        <h4 className="font-semibold">{integration.name}</h4>
                    </div>
                    <Badge className="bg-gray-200 text-gray-700">Em Breve</Badge>
                </Card>
            ))}
        </CardContent>
      </Card>

      {/* Render Modal */}
      {renderModal()}
    </div>
  );
};

export default IntegrationsTab;