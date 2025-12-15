import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { MessageSquare, Mail, Database, CheckCircle, AlertCircle } from 'lucide-react';

interface Step4IntegrationsProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const integrations = [
  {
    id: 'whatsapp',
    name: 'WhatsApp Business',
    description: 'Enviar e receber mensagens via WhatsApp',
    icon: MessageSquare,
    color: 'bg-green-500',
  },
  {
    id: 'email',
    name: 'Email',
    description: 'Enviar emails automáticos',
    icon: Mail,
    color: 'bg-blue-500',
  },
  {
    id: 'database',
    name: 'Database Cliente',
    description: 'Consultar dados do cliente',
    icon: Database,
    color: 'bg-purple-500',
  },
];

const Step4Integrations: React.FC<Step4IntegrationsProps> = ({ formData, setFormData }) => {
  const [integrationsStatus, setIntegrationsStatus] = useState<Record<string, boolean>>({});
  const selectedIntegrations = formData.integrations || {};

  useEffect(() => {
    // TODO: Fetch real integration status from API
    // For now, mock status
    setIntegrationsStatus({
      whatsapp: true,  // Configured
      email: true,     // Configured
      database: false, // Not configured
    });
  }, []);

  const handleIntegrationToggle = (integrationId: string, checked: boolean) => {
    setFormData({
      ...formData,
      integrations: {
        ...selectedIntegrations,
        [integrationId]: checked,
      },
    });
  };

  const handleConfigureIntegration = (integrationId: string) => {
    // TODO: Open integration configuration modal from Sprint 07A
    alert(`Abrir configuração de ${integrationId}`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Integrações Disponíveis</h3>
        <p className="text-sm text-muted-foreground mb-4">
          Selecione quais integrações este agente poderá usar
        </p>

        <div className="space-y-4">
          {integrations.map((integration) => {
            const Icon = integration.icon;
            const isConfigured = integrationsStatus[integration.id];
            const isEnabled = selectedIntegrations[integration.id] || false;

            return (
              <Card key={integration.id}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      <div className={`${integration.color} p-2 rounded-lg`}>
                        <Icon className="h-5 w-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-semibold text-sm">{integration.name}</h4>
                          {isConfigured ? (
                            <div className="flex items-center space-x-1 text-green-600">
                              <CheckCircle className="h-4 w-4" />
                              <span className="text-xs">Configurado</span>
                            </div>
                          ) : (
                            <div className="flex items-center space-x-1 text-orange-600">
                              <AlertCircle className="h-4 w-4" />
                              <span className="text-xs">Não Configurado</span>
                            </div>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          {integration.description}
                        </p>
                      </div>
                    </div>

                    <div className="flex flex-col items-end space-y-2">
                      {isConfigured ? (
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            checked={isEnabled}
                            onCheckedChange={(checked) =>
                              handleIntegrationToggle(integration.id, checked as boolean)
                            }
                          />
                          <span className="text-sm">Permitir uso</span>
                        </div>
                      ) : (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleConfigureIntegration(integration.id)}
                        >
                          Configurar Agora
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      <Card className="bg-muted/50">
        <CardContent className="p-4">
          <p className="text-sm text-muted-foreground">
            <strong>Dica:</strong> As integrações permitem que seu agente execute ações automáticas
            como enviar mensagens no WhatsApp, emails ou consultar dados. Configure-as antes de
            publicar o agente para aproveitar todos os recursos.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step4Integrations;
