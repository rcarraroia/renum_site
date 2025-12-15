import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { MessageSquare, Mail, Database, CheckCircle, XCircle, RefreshCw, Zap, Plus, Trash2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { integrationService, type Integration } from '@/services/integrationService';
import type { IntegrationType } from '@/types/integration';

const INTEGRATION_ICONS: Record<IntegrationType, React.ElementType> = {
    whatsapp: MessageSquare,
    email_smtp: Mail,
    email_sendgrid: Mail,
    database: Database,
};

const INTEGRATION_COLORS: Record<IntegrationType, string> = {
    whatsapp: 'text-green-500',
    email_smtp: 'text-blue-500',
    email_sendgrid: 'text-purple-500',
    database: 'text-orange-500',
};

const IntegrationsTab: React.FC = () => {
    const [integrations, setIntegrations] = useState<Integration[]>([]);
    const [loading, setLoading] = useState(true);
    const [testing, setTesting] = useState<string | null>(null);

    useEffect(() => {
        loadIntegrations();
    }, []);

    const loadIntegrations = async () => {
        try {
            setLoading(true);
            const data = await integrationService.getIntegrations();
            setIntegrations(data);
        } catch (error) {
            console.error('Error loading integrations:', error);
            toast.error('Erro ao carregar integrações');
        } finally {
            setLoading(false);
        }
    };

    const handleTestConnection = async (integration: Integration) => {
        try {
            setTesting(integration.id);
            toast.info(`Testando conexão com ${integration.name}...`);
            
            const result = await integrationService.testIntegration(integration.id);
            
            if (result.success) {
                toast.success(`Conexão com ${integration.name} bem-sucedida! (${result.latency_ms}ms)`);
            } else {
                toast.error(`Falha na conexão: ${result.message}`);
            }
            
            // Reload to get updated status
            await loadIntegrations();
        } catch (error: any) {
            console.error('Error testing integration:', error);
            toast.error(error.message || 'Erro ao testar conexão');
        } finally {
            setTesting(null);
        }
    };

    const handleDelete = async (id: string, name: string) => {
        if (!confirm(`Tem certeza que deseja excluir a integração "${name}"?`)) {
            return;
        }

        try {
            await integrationService.deleteIntegration(id);
            toast.success('Integração excluída com sucesso');
            await loadIntegrations();
        } catch (error: any) {
            console.error('Error deleting integration:', error);
            toast.error(error.message || 'Erro ao excluir integração');
        }
    };

    const getStatusIcon = (status: Integration['status']) => {
        if (status === 'connected') {
            return <CheckCircle className="h-4 w-4 text-green-500" />;
        } else if (status === 'error') {
            return <XCircle className="h-4 w-4 text-red-500" />;
        } else {
            return <XCircle className="h-4 w-4 text-gray-400" />;
        }
    };

    const getStatusText = (status: Integration['status']) => {
        const statusMap = {
            connected: 'Conectado',
            disconnected: 'Desconectado',
            error: 'Erro'
        };
        return statusMap[status] || status;
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-8">
                <RefreshCw className="h-6 w-6 animate-spin text-[#4e4ea8]" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center text-[#4e4ea8]">
                            <Zap className="h-5 w-5 mr-2" /> Gerenciamento de Integrações
                        </CardTitle>
                        <Button size="sm" onClick={() => toast.info('Funcionalidade de adicionar integração em desenvolvimento')}>
                            <Plus className="h-4 w-4 mr-2" /> Nova Integração
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    {integrations.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            <Database className="h-12 w-12 mx-auto mb-4 opacity-50" />
                            <p>Nenhuma integração configurada</p>
                            <p className="text-sm mt-2">Clique em "Nova Integração" para começar</p>
                        </div>
                    ) : (
                        <div className="grid md:grid-cols-2 gap-6">
                            {integrations.map((integration) => {
                                const Icon = INTEGRATION_ICONS[integration.type];
                                const color = INTEGRATION_COLORS[integration.type];
                                
                                return (
                                    <div key={integration.id} className="p-4 border rounded-lg space-y-3 dark:border-gray-700">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-2">
                                                <Icon className={cn("h-5 w-5", color)} />
                                                <div>
                                                    <h4 className="font-semibold">{integration.name}</h4>
                                                    <p className="text-xs text-gray-500">{integration.type}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                {getStatusIcon(integration.status)}
                                                <span className="text-sm">{getStatusText(integration.status)}</span>
                                            </div>
                                        </div>
                                        
                                        {integration.last_error && (
                                            <div className="text-xs text-red-500 bg-red-50 dark:bg-red-900/20 p-2 rounded">
                                                {integration.last_error}
                                            </div>
                                        )}
                                        
                                        {integration.last_tested_at && (
                                            <div className="text-xs text-gray-500">
                                                Último teste: {new Date(integration.last_tested_at).toLocaleString('pt-BR')}
                                            </div>
                                        )}
                                        
                                        <div className="flex gap-2">
                                            <Button 
                                                variant="outline" 
                                                className="flex-1" 
                                                onClick={() => handleTestConnection(integration)}
                                                disabled={testing === integration.id}
                                            >
                                                <RefreshCw className={cn("h-4 w-4 mr-2", testing === integration.id && "animate-spin")} />
                                                Testar Conexão
                                            </Button>
                                            <Button 
                                                variant="outline" 
                                                size="icon"
                                                onClick={() => handleDelete(integration.id, integration.name)}
                                                disabled={testing === integration.id}
                                            >
                                                <Trash2 className="h-4 w-4 text-red-500" />
                                            </Button>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default IntegrationsTab;