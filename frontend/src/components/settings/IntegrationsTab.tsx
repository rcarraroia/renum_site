import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { MessageSquare, Mail, Database, Calendar, Cloud, CheckCircle, XCircle, RefreshCw, Zap, Save } from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

interface Integration {
    name: string;
    icon: React.ElementType;
    status: 'connected' | 'disconnected';
    color: string;
    configKey: string;
}

const MOCK_INTEGRATIONS: Integration[] = [
    { name: 'WhatsApp Business', icon: MessageSquare, status: 'connected', color: 'text-green-500', configKey: 'wa_token' },
    { name: 'CRM Hub (Mock)', icon: Database, status: 'disconnected', color: 'text-red-500', configKey: 'crm_api' },
    { name: 'Google Calendar', icon: Calendar, status: 'connected', color: 'text-blue-500', configKey: 'cal_key' },
    { name: 'Email SMTP', icon: Mail, status: 'disconnected', color: 'text-yellow-500', configKey: 'smtp_pass' },
    { name: 'AWS S3 Storage', icon: Cloud, status: 'connected', color: 'text-orange-500', configKey: 's3_bucket' },
];

const IntegrationsTab: React.FC = () => {
    const [integrations, setIntegrations] = useState(MOCK_INTEGRATIONS);
    const [config, setConfig] = useState<Record<string, string>>({
        wa_token: 'WA-XXXXX',
        crm_api: '',
        cal_key: 'G-YYYYY',
        smtp_pass: '',
        s3_bucket: 'renum-files-prod',
    });
    const [isTesting, setIsTesting] = useState(false);

    const handleTestConnection = (name: string, key: string) => {
        setIsTesting(true);
        toast.info(`Testando conexão com ${name}...`);
        setTimeout(() => {
            setIsTesting(false);
            const newStatus = config[key] ? 'connected' : 'disconnected';
            setIntegrations(integrations.map(i => (i.name === name ? { ...i, status: newStatus } : i)));
            toast[newStatus === 'connected' ? 'success' : 'error'](`Conexão com ${name} ${newStatus === 'connected' ? 'bem-sucedida!' : 'falhou. Verifique as credenciais.'}`);
        }, 1500);
    };

    const getStatusIcon = (status: Integration['status']) => {
        return status === 'connected' ? <CheckCircle className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />;
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Zap className="h-5 w-5 mr-2" /> Gerenciamento de Integrações</CardTitle></CardHeader>
                <CardContent className="grid md:grid-cols-2 gap-6">
                    {integrations.map((integration, index) => (
                        <div key={index} className="p-4 border rounded-lg space-y-3 dark:border-gray-700">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-2">
                                    <integration.icon className={cn("h-5 w-5", integration.color)} />
                                    <h4 className="font-semibold">{integration.name}</h4>
                                </div>
                                <div className="flex items-center space-x-2">
                                    {getStatusIcon(integration.status)}
                                    <span className="text-sm capitalize">{integration.status}</span>
                                </div>
                            </div>
                            
                            <div>
                                <Label htmlFor={integration.configKey}>Chave de Configuração</Label>
                                <Input 
                                    id={integration.configKey}
                                    type={integration.configKey.includes('pass') || integration.configKey.includes('token') ? 'password' : 'text'}
                                    value={config[integration.configKey] || ''}
                                    onChange={(e) => setConfig({...config, [integration.configKey]: e.target.value})}
                                    placeholder={`Insira a chave para ${integration.name}`}
                                />
                            </div>
                            
                            <Button 
                                variant="outline" 
                                className="w-full" 
                                onClick={() => handleTestConnection(integration.name, integration.configKey)}
                                disabled={isTesting}
                            >
                                <RefreshCw className="h-4 w-4 mr-2" /> Testar e Salvar
                            </Button>
                        </div>
                    ))}
                </CardContent>
            </Card>
        </div>
    );
};

export default IntegrationsTab;