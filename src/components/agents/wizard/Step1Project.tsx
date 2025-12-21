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
  
  const [dynamicProjects, setDynamicProjects] = useState<any[]>([]);
  const [dynamicClients, setDynamicClients] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Carregar dados reais da API
  React.useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const [clientsData, projectsData] = await Promise.all([
          clientService.getAll({ limit: 100 }),
          projectService.getAll({ limit: 100 })
        ]);
        
        setDynamicClients(clientsData.items || []);
        setDynamicProjects(projectsData.items || []);
      } catch (error) {
        console.error("Erro ao carregar dados para o Wizard:", error);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  const selectedProject = dynamicProjects.find(p => p.id === formData.project_id);
  const selectedClient = dynamicClients.find(c => c.id === formData.client_id);

  const handleSelectChange = (key: string, value: string) => {
    let updates: any = { [key]: value };
    
    // Se selecionou "Nenhum/Template"
    if (value === 'template') {
        setFormData({ 
            ...formData, 
            client_id: null, 
            project_id: null,
            marketplace_visible: true 
        });
        return;
    }

    if (key === 'project_id') {
        const project = dynamicProjects.find(p => p.id === value);
        if (project) {
            updates.client_id = project.client_id;
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

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4e4ea8]"></div>
        <span className="ml-3 text-muted-foreground">Carregando dados...</span>
      </div>
    );
  }

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
            <Briefcase className="h-5 w-5 mr-2" /> 1. Seleção de Escopo
          </CardTitle>
          <CardDescription>
            Defina se este agente pertence a um cliente real ou se será um Template de Marketplace.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          
          {/* Opção de Template (Marketplace) */}
          <div className="p-4 border-2 border-dashed rounded-lg bg-orange-50/30 border-orange-200 dark:bg-orange-900/10 dark:border-orange-900/30 mb-4 transition-all hover:bg-orange-50/50">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                    <Zap className="h-5 w-5 text-orange-500" />
                    <div>
                        <p className="font-semibold text-orange-700 dark:text-orange-400">Criar como Template de Marketplace</p>
                        <p className="text-xs text-orange-600/80">Agnóstico a clientes e projetos. Disponível para todos.</p>
                    </div>
                </div>
                <Button 
                    variant={!formData.client_id && formData.marketplace_visible ? "default" : "outline"}
                    className={cn(!formData.client_id && formData.marketplace_visible ? "bg-orange-500 hover:bg-orange-600" : "")}
                    onClick={() => handleSelectChange('client_id', 'template')}
                >
                    {!formData.client_id && formData.marketplace_visible ? "Selecionado" : "Selecionar"}
                </Button>
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">Ou vincular a cliente</span>
            </div>
          </div>

          {/* Project Selection */}
          <div className="space-y-2">
            <Label htmlFor="project_id" className="flex items-center">Vincular a Projeto:</Label>
            <div className="flex space-x-2">
                <Select value={formData.project_id || ""} onValueChange={(v) => handleSelectChange('project_id', v)}>
                    <SelectTrigger className="flex-grow">
                        <SelectValue placeholder="Escolha um projeto (Opcional)" />
                    </SelectTrigger>
                    <SelectContent>
                        {dynamicProjects.length > 0 ? dynamicProjects.map(p => (
                            <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                        )) : (
                            <SelectItem value="none" disabled>Nenhum projeto encontrado</SelectItem>
                        )}
                    </SelectContent>
                </Select>
                <Button variant="outline" size="icon" onClick={() => setIsProjectModalOpen(true)}>
                    <Plus className="h-4 w-4" />
                </Button>
            </div>
          </div>

          {/* Client Selection */}
          <div className="space-y-2">
            <Label htmlFor="client_id" className="flex items-center">Vincular a Cliente:</Label>
            <div className="flex space-x-2">
                <Select value={formData.client_id || ""} onValueChange={(v) => handleSelectChange('client_id', v)}>
                    <SelectTrigger className="flex-grow">
                        <SelectValue placeholder="Escolha um cliente (Opcional)" />
                    </SelectTrigger>
                    <SelectContent>
                        {dynamicClients.length > 0 ? dynamicClients.map(c => (
                            <SelectItem key={c.id} value={c.id}>{c.company_name || c.name}</SelectItem>
                        )) : (
                            <SelectItem value="none" disabled>Nenhum cliente encontrado</SelectItem>
                        )}
                    </SelectContent>
                </Select>
                <Button variant="outline" size="icon" onClick={() => setIsClientModalOpen(true)}>
                    <Plus className="h-4 w-4" />
                </Button>
            </div>
          </div>

          {(selectedProject || selectedClient) && (
            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm transition-all border border-blue-100 dark:border-blue-900/30">
              <p className="font-semibold mb-2 flex items-center text-[#4e4ea8]">
                <Users className="h-4 w-4 mr-2" /> Vinculação Ativa:
              </p>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Cliente:</span>
                <span className="font-medium text-blue-700 dark:text-blue-400">{selectedClient?.company_name || selectedClient?.name || 'Não selecionado'}</span>
              </div>
              {selectedProject && (
                <div className="flex justify-between mt-1">
                  <span className="text-muted-foreground">Projeto:</span>
                  <Badge variant="secondary" className="bg-[#4e4ea8]/10 text-[#4e4ea8] border-[#4e4ea8]/20">{selectedProject.name}</Badge>
                </div>
              )}
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