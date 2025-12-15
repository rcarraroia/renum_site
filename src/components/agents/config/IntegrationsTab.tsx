
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, Mail, MessageSquare, Phone, Wrench, CheckCircle, XCircle, RefreshCw, Settings, Clock, Globe } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import WhatsappConfigModal from './modals/WhatsappConfigModal.tsx';
import GoogleConfigModal from './modals/GoogleConfigModal.tsx';
// ... imports

interface IntegrationConfig {
  name: string;
  icon: React.ElementType;
  status: 'connected' | 'disconnected' | 'pending';
  color: string;
  provider: string;
  displayProvider: string;
  details: string[];
  modalType: 'whatsapp' | 'chatwoot' | 'google';
  configData: any;
}
//...
// In renderModal
      case 'google':
return (
  <GoogleConfigModal
    isOpen={isModalOpen}
    onClose={() => setIsModalOpen(false)}
    initialConfig={selectedIntegration.configData}
    onSave={handleSaveConfig}
  />
);
//...

const SUPPORTED_INTEGRATIONS: IntegrationConfig[] = [
  {
    name: 'WhatsApp Business',
    icon: MessageSquare,
    status: 'disconnected',
    color: 'text-green-600',
    provider: 'uazapi',
    displayProvider: 'Uazapi',
    details: ['Permite: Envio/Recebimento de Mensagens', 'Suporta: Áudio, Imagem, Vídeo', 'Transcrição Automática de Áudio'],
    modalType: 'whatsapp',
    configData: { token: '', url: 'https://api.uazapi.com', phoneId: '', isConnected: false },
  },
  {
    name: 'Chatwoot (Human Handoff)',
    icon: MessageSquare,
    status: 'disconnected',
    color: 'text-blue-600',
    provider: 'chatwoot',
    displayProvider: 'Chatwoot',
    details: ['Permite: Transbordo para atendente humano', 'Sincroniza conversas do WhatsApp', 'Criação automática de Inbox'],
    modalType: 'chatwoot',
    configData: { url: 'https://app.chatwoot.com', api_access_token: '', account_id: '1', isConnected: false },
  },
  {
    name: 'Google Workspace',
    icon: Globe,
    status: 'disconnected',
    color: 'text-yellow-600',
    provider: 'google',
    displayProvider: 'Google',
    details: ['Inclui: Gmail, Calendar, Drive, Sheets, Meet, Forms', 'Login Único (OAuth2)'],
    modalType: 'google',
    configData: { isConnected: false },
  },
];

const FUTURE_INTEGRATIONS = [
  { name: 'Gmail / Email', icon: Mail, color: 'text-red-600' },
  { name: 'Telegram', icon: MessageSquare, color: 'text-blue-400' },
  { name: 'SMS (Twilio)', icon: MessageSquare, color: 'text-orange-400' },
  { name: 'Zapier', icon: Zap, color: 'text-red-400' },
];

const IntegrationsTab: React.FC = () => {
  const [integrations, setIntegrations] = useState<IntegrationConfig[]>(SUPPORTED_INTEGRATIONS);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIntegration, setSelectedIntegration] = useState<IntegrationConfig | null>(null);

  const agentSlug = 'slim-vendas';

  // Load Integrations from Backend
  React.useEffect(() => {
    loadIntegrations();
  }, []);

  const loadIntegrations = async () => {
    try {
      setLoading(true);
      const savedIntegrations = await integrationService.listIntegrations();

      const mergedList = SUPPORTED_INTEGRATIONS.map(def => {
        // Match provider (case insensitive)
        const saved = savedIntegrations.find(i => i.provider.toLowerCase() === def.provider.toLowerCase());

        if (saved) {
          return {
            ...def,
            status: 'connected',
            configData: { ...def.configData, ...saved.config, isConnected: true },
            details: [`Configurado em: ${new Date(saved.created_at).toLocaleDateString()}`, ...def.details.slice(1)]
          };
        }
        return { ...def, status: 'disconnected', configData: def.configData };
      });

      setIntegrations(mergedList as IntegrationConfig[]);
    } catch (error) {
      toast.error("Erro ao carregar integrações");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (integration: IntegrationConfig) => {
    setSelectedIntegration(integration);
    setIsModalOpen(true);
  };

  const handleSaveConfig = async (updatedConfig: any) => {
    if (!selectedIntegration) return;

    try {
      await integrationService.saveIntegration(selectedIntegration.provider, updatedConfig);
      toast.success("Integração salva com sucesso!");
      await loadIntegrations();
      setIsModalOpen(false);
    } catch (error) {
      toast.error("Erro ao salvar integração");
      console.error(error);
    }
  };

  const getStatusIcon = (status: IntegrationConfig['status']) => {
    switch (status) {
      case 'connected': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'disconnected': return <XCircle className="h-5 w-5 text-red-500" />;
      case 'pending': return <Clock className="h-5 w-5 text-yellow-500" />;
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
      case 'chatwoot':
        return (
          <ChatwootConfigModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            initialConfig={selectedIntegration.configData}
            onSave={handleSaveConfig}
            agentSlug={agentSlug}
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
            <RefreshCw className={cn("h-5 w-5 mr-2", loading && "animate-spin")} /> Integrações do Agente
          </CardTitle>
          <CardDescription>
            Conecte serviços externos. WhatsApp para comunicação e Chatwoot para atendimento humano.
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