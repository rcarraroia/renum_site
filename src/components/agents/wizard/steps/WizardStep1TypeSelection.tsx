/**
 * Task 10: Create wizard step components
 * WizardStep1TypeSelection - Type selection with dynamic fields
 * Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
 */

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';

interface Step1Data {
    agent_type: 'template' | 'client' | 'system';
    category?: 'b2b' | 'b2c';
    client_id?: string;
    project_id?: string;
}

interface WizardStep1Props {
    data: Step1Data;
    onChange: (data: Step1Data) => void;
}

import { clientService } from '@/services/clientService';

export const WizardStep1TypeSelection: React.FC<WizardStep1Props> = ({ data, onChange }) => {
    const [clients, setClients] = useState<any[]>([]);

    React.useEffect(() => {
        const loadClients = async () => {
            try {
                // Using getAll which returns { data: [...], ... }
                const response = await clientService.getAll({ limit: 100 });
                // clientService.getAll returns ClientList which has data property
                const clientList = response.clients || response.data || [];
                setClients(clientList);
            } catch (error) {
                console.error("Failed to load clients", error);
            }
        };
        loadClients();
    }, []);

    const handleTypeChange = (type: Step1Data['agent_type']) => {
        onChange({ ...data, agent_type: type });
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Tipo de Agente</CardTitle>
                    <CardDescription>
                        Selecione o tipo de agente que deseja criar
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <RadioGroup value={data.agent_type || ''} onValueChange={handleTypeChange}>
                        {/* Radio options code remains same */}
                        <div className="flex items-center space-x-2 p-4 border rounded-lg hover:bg-accent">
                            <RadioGroupItem value="template" id="template" />
                            <Label htmlFor="template" className="flex-1 cursor-pointer">
                                <div className="font-semibold">Template (Marketplace)</div>
                                <div className="text-sm text-muted-foreground">
                                    Agente reutilizável disponível no marketplace
                                </div>
                            </Label>
                        </div>

                        <div className="flex items-center space-x-2 p-4 border rounded-lg hover:bg-accent">
                            <RadioGroupItem value="client" id="client" />
                            <Label htmlFor="client" className="flex-1 cursor-pointer">
                                <div className="font-semibold">Agente de Cliente</div>
                                <div className="text-sm text-muted-foreground">
                                    Agente específico para um cliente/projeto
                                </div>
                            </Label>
                        </div>

                        <div className="flex items-center space-x-2 p-4 border rounded-lg hover:bg-accent">
                            <RadioGroupItem value="system" id="system" />
                            <Label htmlFor="system" className="flex-1 cursor-pointer">
                                <div className="font-semibold">Agente de Sistema</div>
                                <div className="text-sm text-muted-foreground">
                                    Agente interno (RENUS, ISA, etc) - Apenas Admin
                                </div>
                            </Label>
                        </div>
                    </RadioGroup>
                </CardContent>
            </Card>

            {/* Conditional Fields Based on Type */}
            {data.agent_type === 'template' && (
                <Card>
                    <CardHeader>
                        <CardTitle>Categoria do Template</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <RadioGroup
                            value={data.category || ''}
                            onValueChange={(cat: 'b2b' | 'b2c') => onChange({ ...data, category: cat })}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="b2b" id="b2b" />
                                <Label htmlFor="b2b">B2B (Business to Business)</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="b2c" id="b2c" />
                                <Label htmlFor="b2c">B2C (Business to Consumer)</Label>
                            </div>
                        </RadioGroup>
                    </CardContent>
                </Card>
            )}

            {data.agent_type === 'client' && (
                <Card>
                    <CardHeader>
                        <CardTitle>Cliente e Projeto</CardTitle>
                        <CardDescription>Selecione o cliente e projeto para este agente</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <Label htmlFor="client">Cliente <span className="text-destructive">*</span></Label>
                            <select
                                id="client"
                                className="w-full border rounded p-2"
                                value={data.client_id || ''}
                                onChange={(e) => onChange({ ...data, client_id: e.target.value })}
                            >
                                <option value="">Selecione um cliente...</option>
                                {clients.map(client => (
                                    <option key={client.id} value={client.id}>
                                        {client.name || 'Sem nome'} ({client.type || client.segment || 'N/A'})
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <Label htmlFor="project">Projeto</Label>
                            <select
                                id="project"
                                className="w-full border rounded p-2"
                                value={data.project_id || ''}
                                onChange={(e) => onChange({ ...data, project_id: e.target.value })}
                            >
                                <option value="">Selecione um projeto (opcional)...</option>
                                {/* Projects could load based on client, keeping simple for now */}
                            </select>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
};
