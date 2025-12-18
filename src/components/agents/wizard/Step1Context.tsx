import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Button } from '@/components/ui/button';
import { Briefcase, Tag, Plus, Loader2 } from 'lucide-react';
import { projectService } from '@/services/projectService';
import { clientService } from '@/services/clientService';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import Step1ProjectModals from './Step1ProjectModal';
import { Project } from '@/types/project';
import { Client } from '@/types/client';

interface Step1ContextProps {
    formData: any;
    setFormData: (data: any) => void;
    onValidate: () => boolean;
}

const Step1Context: React.FC<Step1ContextProps> = ({ formData, setFormData, onValidate }) => {
    const [isProjectModalOpen, setIsProjectModalOpen] = useState(false);
    const [isClientModalOpen, setIsClientModalOpen] = useState(false);

    const [projects, setProjects] = useState<Project[]>([]);
    const [clients, setClients] = useState<Client[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [projectsList, clientsList] = await Promise.all([
                projectService.getAll({ limit: 100 }),
                clientService.getAll({ limit: 100 })
            ]);
            setProjects(projectsList.items || []);
            setClients(clientsList.items || []);
        } catch (error) {
            console.error('Error loading projects/clients:', error);
        } finally {
            setLoading(false);
        }
    };

    const selectedProject = projects.find(p => p.id === formData.project_id);
    const selectedClient = clients.find(c => c.id === formData.client_id);

    const handleSelectChange = (key: string, value: string) => {
        let updates: any = { [key]: value };

        if (key === 'project_id') {
            const project = projects.find(p => p.id === value);
            if (project) {
                updates.client_id = project.client_id;
                // Automagic contract type based on client (if available)
                const client = clients.find(c => c.id === project.client_id);
                if (client) {
                    updates.contract_type = client.type === 'b2b' ? 'b2b_empresa' : 'b2c_individual';
                }
            }
        }
        if (key === 'client_id') {
            const client = clients.find(c => c.id === value);
            if (client) {
                updates.contract_type = client.type === 'b2b' ? 'b2b_empresa' : 'b2c_individual';
            }
        }

        setFormData({ ...formData, ...updates });
    };

    const handleContractTypeChange = (value: string) => {
        setFormData({ ...formData, contract_type: value });
    };

    const handleProjectCreated = (newProject: any) => {
        setProjects(prev => [...prev, newProject]);
        setFormData(prev => ({ ...prev, project_id: newProject.id, client_id: newProject.client_id }));
    };

    const handleClientCreated = (newClient: any) => {
        setClients(prev => [...prev, newClient]);
        setFormData(prev => ({ ...prev, client_id: newClient.id, contract_type: newClient.type }));
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="h-10 w-10 animate-spin text-[#4e4ea8]" />
                <p className="mt-4 text-muted-foreground">Carregando dados de contexto...</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <Step1ProjectModals
                isProjectModalOpen={isProjectModalOpen}
                isClientModalOpen={isClientModalOpen}
                onCloseProjectModal={() => setIsProjectModalOpen(false)}
                onCloseClientModal={() => setIsClientModalOpen(false)}
                onProjectCreated={handleProjectCreated}
                onClientCreated={handleClientCreated}
            />

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]">
                        <Briefcase className="h-5 w-5 mr-2" /> 1. Seleção de Projeto e Cliente
                    </CardTitle>
                    <CardDescription>
                        Defina a qual conta e projeto este novo agente pertencerá.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">

                    <div className="space-y-2">
                        <Label htmlFor="client_id">Selecionar Cliente: *</Label>
                        <div className="flex space-x-2">
                            <Select value={formData.client_id} onValueChange={(v) => handleSelectChange('client_id', v)}>
                                <SelectTrigger className="flex-grow">
                                    <SelectValue placeholder="Escolha um cliente" />
                                </SelectTrigger>
                                <SelectContent>
                                    {clients.map(c => (
                                        <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <Button variant="outline" size="icon" onClick={() => setIsClientModalOpen(true)}>
                                <Plus className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="project_id">Selecionar Projeto: *</Label>
                        <div className="flex space-x-2">
                            <Select value={formData.project_id} onValueChange={(v) => handleSelectChange('project_id', v)}>
                                <SelectTrigger className="flex-grow">
                                    <SelectValue placeholder="Escolha um projeto" />
                                </SelectTrigger>
                                <SelectContent>
                                    {projects.filter(p => !formData.client_id || p.client_id === formData.client_id).map(p => (
                                        <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <Button variant="outline" size="icon" onClick={() => setIsProjectModalOpen(true)}>
                                <Plus className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>

                    {selectedProject && (
                        <div className="p-4 bg-blue-50/50 dark:bg-gray-800/50 border border-blue-100 dark:border-gray-700 rounded-lg text-sm">
                            <p className="font-semibold mb-2">Detalhes do Projeto:</p>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Status:</span>
                                <Badge variant="outline" className="capitalize">{selectedProject.status}</Badge>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#FF6B35]">
                        <Tag className="h-5 w-5 mr-2" /> Tipo de Contrato
                    </CardTitle>
                    <CardDescription>
                        Como este agente será utilizado?
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <RadioGroup
                        value={formData.contract_type}
                        onValueChange={handleContractTypeChange}
                        className="grid grid-cols-1 md:grid-cols-2 gap-4"
                    >
                        <div className={cn(
                            "p-4 border rounded-lg cursor-pointer transition-all",
                            formData.contract_type === 'b2b_empresa' ? 'border-2 border-[#4e4ea8] bg-blue-50/30' : 'hover:bg-gray-50'
                        )}>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="b2b_empresa" id="b2b" />
                                <Label htmlFor="b2b" className="font-bold cursor-pointer">B2B - Corporativo</Label>
                            </div>
                            <p className="text-xs text-muted-foreground mt-2 ml-6">Ideal para empresas com múltiplos usuários/vendedores.</p>
                        </div>

                        <div className={cn(
                            "p-4 border rounded-lg cursor-pointer transition-all",
                            formData.contract_type === 'b2c_individual' ? 'border-2 border-[#4e4ea8] bg-blue-50/30' : 'hover:bg-gray-50'
                        )}>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="b2c_individual" id="b2c" />
                                <Label htmlFor="b2c" className="font-bold cursor-pointer">B2C - Individual</Label>
                            </div>
                            <p className="text-xs text-muted-foreground mt-2 ml-6">1 usuário final (ex: corretor avulso, consultor).</p>
                        </div>
                    </RadioGroup>
                </CardContent>
            </Card>
        </div>
    );
};

export default Step1Context;
