/**
 * Task 31: Integrations Radar Dashboard
 * Monitoramento de saúde e status das integrações
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle, XCircle, AlertCircle, RefreshCw, Wifi } from 'lucide-react';

interface IntegrationStatus {
    id: string;
    type: string;
    name: string;
    status: 'active' | 'inactive' | 'error' | 'testing';
    last_test: string | null;
    error_message?: string;
    agent_count: number;
}
import { apiClient } from '@/services/api';

export const IntegrationsRadar: React.FC = () => {
    const [integrations, setIntegrations] = useState<IntegrationStatus[]>([]);
    const [testing, setTesting] = useState<string | null>(null);

    useEffect(() => {
        loadIntegrations();
    }, []);

    const loadIntegrations = async () => {
        try {
            const { data } = await apiClient.get<IntegrationStatus[]>('/api/integrations/status');
            setIntegrations(data || []);
        } catch (error) {
            console.error('Erro ao carregar integrações:', error);
            // Mock data para desenvolvimento
            setIntegrations([
                { id: '1', type: 'whatsapp', name: 'WhatsApp Business', status: 'active', last_test: new Date().toISOString(), agent_count: 2 },
                { id: '2', type: 'email', name: 'Email SMTP', status: 'active', last_test: new Date().toISOString(), agent_count: 1 },
                { id: '3', type: 'sms', name: 'SMS Gateway', status: 'inactive', last_test: null, agent_count: 0 },
                { id: '4', type: 'crm', name: 'CRM Integration', status: 'error', last_test: new Date().toISOString(), error_message: 'Token expirado', agent_count: 1 }
            ]);
        }
    };

    const testIntegration = async (integrationId: string) => {
        setTesting(integrationId);
        try {
            await apiClient.post(`/api/integrations/${integrationId}/test`);
            loadIntegrations();
        } catch (error) {
            console.error('Erro ao testar integração:', error);
        } finally {
            setTesting(null);
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'active':
                return <CheckCircle className="h-5 w-5 text-green-600" />;
            case 'error':
                return <XCircle className="h-5 w-5 text-red-600" />;
            case 'inactive':
                return <AlertCircle className="h-5 w-5 text-gray-400" />;
            case 'testing':
                return <RefreshCw className="h-5 w-5 text-blue-600 animate-spin" />;
            default:
                return <AlertCircle className="h-5 w-5 text-yellow-600" />;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'active': return 'bg-green-100 text-green-800';
            case 'error': return 'bg-red-100 text-red-800';
            case 'inactive': return 'bg-gray-100 text-gray-800';
            case 'testing': return 'bg-blue-100 text-blue-800';
            default: return 'bg-yellow-100 text-yellow-800';
        }
    };

    const activeCount = integrations.filter(i => i.status === 'active').length;
    const errorCount = integrations.filter(i => i.status === 'error').length;

    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold flex items-center gap-2">
                    <Wifi className="h-8 w-8" />
                    Radar de Integrações
                </h1>
                <p className="text-muted-foreground">
                    Monitore a saúde e conectividade das suas integrações
                </p>
            </div>

            {/* Status Geral */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardContent className="p-4 flex items-center gap-4">
                        <div className="p-3 bg-blue-100 rounded-full">
                            <Wifi className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold">{integrations.length}</p>
                            <p className="text-sm text-muted-foreground">Total</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4 flex items-center gap-4">
                        <div className="p-3 bg-green-100 rounded-full">
                            <CheckCircle className="h-6 w-6 text-green-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold">{activeCount}</p>
                            <p className="text-sm text-muted-foreground">Ativas</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4 flex items-center gap-4">
                        <div className="p-3 bg-red-100 rounded-full">
                            <XCircle className="h-6 w-6 text-red-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold">{errorCount}</p>
                            <p className="text-sm text-muted-foreground">Com Erro</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4 flex items-center justify-center">
                        <Button onClick={loadIntegrations} variant="outline">
                            <RefreshCw className="h-4 w-4 mr-2" />
                            Atualizar
                        </Button>
                    </CardContent>
                </Card>
            </div>

            {/* Lista de Integrações */}
            <div className="grid gap-4">
                {integrations.map(integration => (
                    <Card key={integration.id} className={integration.status === 'error' ? 'border-red-200' : ''}>
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    {getStatusIcon(integration.status)}
                                    <div>
                                        <h3 className="font-medium">{integration.name}</h3>
                                        <p className="text-sm text-muted-foreground">
                                            {integration.agent_count} agente(s) usando
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    <span className={`px-3 py-1 rounded-full text-sm ${getStatusColor(integration.status)}`}>
                                        {integration.status === 'active' ? 'Ativo' :
                                            integration.status === 'error' ? 'Erro' :
                                                integration.status === 'inactive' ? 'Inativo' : 'Testando'}
                                    </span>

                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => testIntegration(integration.id)}
                                        disabled={testing === integration.id}
                                    >
                                        {testing === integration.id ? (
                                            <RefreshCw className="h-4 w-4 animate-spin" />
                                        ) : (
                                            'Testar'
                                        )}
                                    </Button>
                                </div>
                            </div>

                            {integration.error_message && (
                                <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-800">
                                    <strong>Erro:</strong> {integration.error_message}
                                </div>
                            )}

                            {integration.last_test && (
                                <p className="mt-2 text-xs text-muted-foreground">
                                    Último teste: {new Date(integration.last_test).toLocaleString()}
                                </p>
                            )}
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};

export default IntegrationsRadar;
