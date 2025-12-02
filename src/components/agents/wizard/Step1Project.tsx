import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Briefcase, Users, Tag, DollarSign, Clock } from 'lucide-react';
import { mockProjects, mockClients, mockCategories } from '@/mocks/agents.mock';
import { AgentCategory, AgentType } from '@/types/agent';
import { Badge } from '@/components/ui/badge';

interface Step1ProjectProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step1Project: React.FC<Step1ProjectProps> = ({ formData, setFormData, onValidate }) => {
  const selectedProject = mockProjects.find(p => p.id === formData.project_id);
  const selectedClient = mockClients.find(c => c.id === formData.client_id);

  const handleSelectChange = (key: string, value: string) => {
    let updates: any = { [key]: value };
    
    if (key === 'project_id') {
        const project = mockProjects.find(p => p.id === value);
        if (project) {
            updates.client_id = project.client_id;
        }
    }
    if (key === 'client_id') {
        const client = mockClients.find(c => c.id === value);
        if (client) {
            updates.type = client.type;
        }
    }

    setFormData({ ...formData, ...updates });
  };

  return (
    <div className="space-y-6">
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
          <div className="grid md:grid-cols-2 gap-4">
            {/* Project Selection */}
            <div className="space-y-2">
              <Label htmlFor="project_id" className="flex items-center"><Briefcase className="h-4 w-4 mr-2" /> Projeto</Label>
              <Select value={formData.project_id} onValueChange={(v) => handleSelectChange('project_id', v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o Projeto" />
                </SelectTrigger>
                <SelectContent>
                  {mockProjects.map(p => (
                    <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Client Display (Derived from Project) */}
            <div className="space-y-2">
              <Label htmlFor="client_id" className="flex items-center"><Users className="h-4 w-4 mr-2" /> Cliente</Label>
              <Select value={formData.client_id} onValueChange={(v) => handleSelectChange('client_id', v)}>
                <SelectTrigger disabled>
                  <SelectValue placeholder="Cliente" />
                </SelectTrigger>
                <SelectContent>
                    {mockClients.map(c => (
                        <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
                    ))}
                </SelectContent>
              </Select>
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
            <Tag className="h-5 w-5 mr-2" /> 2. Tipo e Categoria
          </CardTitle>
          <CardDescription>
            Defina o tipo de cliente e a categoria de atuação do agente.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            {/* Agent Type (Derived from Client) */}
            <div className="space-y-2">
              <Label htmlFor="type">Tipo de Cliente</Label>
              <Input readOnly value={selectedClient?.type || 'N/A'} className="bg-gray-100 dark:bg-gray-700" />
              <p className="text-xs text-muted-foreground">
                {selectedClient?.type === 'b2b_empresa' ? 'Empresa B2B' : selectedClient?.type === 'b2c_marketplace' ? 'Marketplace B2C' : 'Individual B2C'}
              </p>
            </div>

            {/* Category Selection */}
            <div className="space-y-2">
              <Label htmlFor="category">Categoria de Atuação</Label>
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
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step1Project;