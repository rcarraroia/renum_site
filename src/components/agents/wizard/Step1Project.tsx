import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Button } from '@/components/ui/button';
import { Zap, Briefcase, Users, Tag, DollarSign, Clock, Plus } from 'lucide-react';
import { mockProjects, mockClients, mockCategories } from '@/mocks/agents.mock';
import { AgentCategory, AgentType } from '@/types/agent';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import Step1ProjectModals from './Step1ProjectModal'; // Importando o novo componente de modais

interface Step1ProjectProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step1Project: React.FC<Step1ProjectProps> = ({ formData, setFormData, onValidate }) => {
  const [isProjectModalOpen, setIsProjectModalOpen] = useState(false);
  const [isClientModalOpen, setIsClientModalOpen] = useState(false);
  
  // Mock state for dynamic lists (in a real app, these would come from global state/API)
  const [dynamicProjects, setDynamicProjects] = useState(mockProjects);
  const [dynamicClients, setDynamicClients] = useState(mockClients);

  const selectedProject = dynamicProjects.find(p => p.id === formData.project_id);
  const selectedClient = dynamicClients.find(c => c.id === formData.client_id);

  const handleSelectChange = (key: string, value: string) => {
    let updates: any = { [key]: value };
    
    if (key === 'project_id') {
        const project = dynamicProjects.find(p => p.id === value);
        if (project) {
            updates.client_id = project.client_id;
            // Automatically set contract type based on client type (mock logic)
            const client = dynamicClients.find(c => c.id === project.client_id);
            if (client) {
                updates.contract_type = client.type === 'b2b_empresa' ? 'b2b_empresa' : 'b2c_individual';
            }
        }
    }
    if (key === 'client_id') {
        const client = dynamicClients.find(c => c.id === value);
        if (client) {
            updates.contract_type = client.type === 'b2b_empresa' ? 'b2b_empresa' : 'b2c_individual';
        }
    }

    setFormData({ ...formData, ...updates });
  };
  
  const handleContractTypeChange = (value: string) => {
    setFormData({ ...formData, contract_type: value as AgentType });
  };

  const handleProjectCreated = (newProject: any) => {
    setDynamicProjects(prev => [...prev, newProject]);
    setFormData(prev => ({ ...prev, project_id: newProject.id, client_id: newProject.client_id }));
  };

  const handleClientCreated = (newClient: any) => {
    setDynamicClients(prev => [...prev, newClient]);
    setFormData(prev => ({ ...prev, client_id: newClient.id, contract_type: newClient.type }));
  };

  return (
    <div className="space-y-6">
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
            <Briefcase className="h-5 w-5 mr-2" /> 1. Seleção de Projeto
          </CardTitle>
          <CardDescription>
            Vincule o novo agente a um projeto e cliente existentes.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          
          {/* Project Selection */}
          <div className="space-y-2">
            <Label htmlFor="project_id" className="flex items-center">Selecionar Projeto: *</Label>
            <div className="flex space-x-2">
                <Select value={formData.project_id} onValueChange={(v) => handleSelectChange('project_id', v)}>
                    <SelectTrigger className="flex-grow">
                        <SelectValue placeholder="Escolha um projeto existente" />
                    </SelectTrigger>
                    <SelectContent>
                        {dynamicProjects.map(p => (
                            <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
                <Button variant="outline" size="icon" onClick={() => setIsProjectModalOpen(true)}>
                    <Plus className="h-4 w-4" />
                </Button>
            </div>
          </div>

          {/* Client Selection */}
          <div className="space-y-2">
            <Label htmlFor="client_id" className="flex items-center">Selecionar Cliente: *</Label>
            <div className="flex space-x-2">
                <Select value={formData.client_id} onValueChange={(v) => handleSelectChange('client_id', v)}>
                    <SelectTrigger className="flex-grow">
                        <SelectValue placeholder="Escolha um cliente existente" />
                    </SelectTrigger>
                    <SelectContent>
                        {dynamicClients.map(c => (
                            <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
                <Button variant="outline" size="icon" onClick={() => setIsClientModalOpen(true)}>
                    <Plus className="h-4 w-4" />
                </Button>
            </div>
          </div>

          {selectedProject && (
            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm">
              <p className="font-semibold mb-2">Detalhes do Projeto:</p>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Limite de Agentes:</span>
                <Badge variant="outline">{selectedProject.agents_limit} Agentes</Badge>
              </div>
              <div className="flex justify-between mt-1">
                <span className="text-muted-foreground">Agentes Atuais (Mock):</span>
                <span className="font-medium text-[#FF6B35]">2</span>
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
            Defina o tipo de contrato e a categoria de atuação do agente.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
            {/* Contract Type Radio Buttons */}
            <div className="space-y-2">
                <Label>Tipo de Contrato: *</Label>
                <RadioGroup 
                    value={formData.contract_type} 
                    onValueChange={handleContractTypeChange}
                    className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                    <div className={cn(
                        "p-4 border rounded-lg cursor-pointer transition-colors",
                        formData.contract_type === 'b2b_empresa' ? 'border-2 border-[#4e4ea8] bg-blue-50/50 dark:bg-gray-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    )}>
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem value="b2b_empresa" id="b2b" />
                            <Label htmlFor="b2b" className="font-medium cursor-pointer">B2B - Corporativo</Label>
                        </div>
                        <p className="text-xs text-muted-foreground mt-2 ml-6">Múltiplos usuários (vendedores, equipe)</p>
                    </div>
                    
                    <div className={cn(
                        "p-4 border rounded-lg cursor-pointer transition-colors",
                        formData.contract_type === 'b2c_individual' ? 'border-2 border-[#4e4ea8] bg-blue-50/50 dark:bg-gray-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    )}>
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem value="b2c_individual" id="b2c" />
                            <Label htmlFor="b2c" className="font-medium cursor-pointer">B2C - Individual/Avulso</Label>
                        </div>
                        <p className="text-xs text-muted-foreground mt-2 ml-6">1 usuário final por instância</p>
                    </div>
                </RadioGroup>
            </div>

            {/* Category Selection */}
            <div className="space-y-2 pt-4 border-t dark:border-gray-700">
              <Label htmlFor="category">Categoria de Atuação *</Label>
              <Select value={formData.category} onValueChange={(v) => setFormData({ ...formData, category: v as AgentCategory })}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione a Categoria" />
                </SelectTrigger>
                <SelectContent>
                  {mockCategories.map(c => (
                    <SelectItem key={c.id} value={c.id}>
                        <div className="flex items-center">
                            <span className="mr-2">{c.icon}</span> {c.name}
                        </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step1Project;