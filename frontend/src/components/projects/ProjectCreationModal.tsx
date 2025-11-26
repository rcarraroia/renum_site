import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Project, ProjectType, TeamMember } from '@/types/project';
import { getMockClients, getMockTeam } from '@/data/mockProjects';
import { Zap, Save, Settings, DollarSign, Calendar, User } from 'lucide-react';
import { toast } from 'sonner';

interface ProjectCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (project: Omit<Project, 'id' | 'status' | 'progress'>) => void;
}

const ProjectCreationModal: React.FC<ProjectCreationModalProps> = ({ isOpen, onClose, onCreate }) => {
  const mockClients = getMockClients();
  const mockTeam = getMockTeam();
  
  const [formData, setFormData] = useState({
    name: '',
    clientId: mockClients[0].id,
    description: '',
    type: 'AI Native' as ProjectType,
    startDate: new Date().toISOString().split('T')[0],
    dueDate: new Date(new Date().setMonth(new Date().getMonth() + 3)).toISOString().split('T')[0],
    responsibleId: mockTeam[0].id,
    scope: '',
    budget: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: id === 'budget' ? parseFloat(value) || 0 : value }));
  };

  const handleSelectChange = (id: string, value: string) => {
    setFormData(prev => ({ ...prev, [id]: value as any }));
  };

  const handleSubmit = (redirect: boolean) => {
    if (!formData.name || !formData.description) {
      toast.error("Preencha todos os campos obrigatórios.");
      return;
    }

    const responsible = mockTeam.find(t => t.id === formData.responsibleId)!;
    const clientName = mockClients.find(c => c.id === formData.clientId)?.name || 'Desconhecido';

    const newProjectData = {
        ...formData,
        clientName,
        responsible,
        startDate: new Date(formData.startDate),
        dueDate: new Date(formData.dueDate),
    };

    onCreate(newProjectData);
    onClose();
    toast.success(`Projeto '${formData.name}' criado com sucesso!`);
    
    if (redirect) {
        // Mock redirect to detail page
        console.log("Redirecting to project detail page...");
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-[#4e4ea8]">
            <Zap className="h-6 w-6 mr-2" /> Novo Projeto
          </DialogTitle>
          <p className="text-sm text-muted-foreground">Preencha os detalhes para iniciar um novo projeto de IA/Automação.</p>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          
          {/* Nome e Cliente */}
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">Nome</Label>
            <Input id="name" value={formData.name} onChange={handleChange} className="col-span-3" placeholder="Ex: Agente de Suporte 24/7" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="clientId" className="text-right">Cliente</Label>
            <Select value={formData.clientId} onValueChange={(v) => handleSelectChange('clientId', v)}>
              <SelectTrigger className="col-span-3">
                <SelectValue placeholder="Selecione o Cliente" />
              </SelectTrigger>
              <SelectContent>
                {mockClients.map(client => (
                  <SelectItem key={client.id} value={client.id}>{client.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Tipo e Responsável */}
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="type" className="text-right">Tipo</Label>
            <Select value={formData.type} onValueChange={(v) => handleSelectChange('type', v)}>
              <SelectTrigger className="col-span-3">
                <SelectValue placeholder="Selecione o Tipo" />
              </SelectTrigger>
              <SelectContent>
                {['AI Native', 'Workflow', 'Agente Solo'].map(type => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="responsibleId" className="text-right">Responsável</Label>
            <Select value={formData.responsibleId} onValueChange={(v) => handleSelectChange('responsibleId', v)}>
              <SelectTrigger className="col-span-3">
                <SelectValue placeholder="Selecione o Responsável" />
              </SelectTrigger>
              <SelectContent>
                {mockTeam.map(member => (
                  <SelectItem key={member.id} value={member.id}>
                    <div className="flex items-center">
                        <User className="h-4 w-4 mr-2" /> {member.name}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Datas e Orçamento */}
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="startDate" className="text-right">Início</Label>
            <Input id="startDate" type="date" value={formData.startDate} onChange={handleChange} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="dueDate" className="text-right">Prazo</Label>
            <Input id="dueDate" type="date" value={formData.dueDate} onChange={handleChange} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="budget" className="text-right">Orçamento (R$)</Label>
            <div className="col-span-3 flex items-center">
                <DollarSign className="h-4 w-4 text-muted-foreground mr-2" />
                <Input id="budget" type="number" value={formData.budget} onChange={handleChange} placeholder="15000" />
            </div>
          </div>

          {/* Descrição */}
          <div className="space-y-2 mt-4">
            <Label htmlFor="description">Descrição</Label>
            <Textarea id="description" rows={3} value={formData.description} onChange={handleChange} placeholder="Breve resumo do objetivo do projeto." />
          </div>

          {/* Escopo Inicial */}
          <div className="space-y-2">
            <Label htmlFor="scope">Escopo Inicial (Markdown)</Label>
            <Textarea id="scope" rows={5} value={formData.scope} onChange={handleChange} placeholder="## Módulos&#10;- Módulo A&#10;- Módulo B" className="font-mono text-sm" />
          </div>

        </div>
        
        <DialogFooter className="sm:justify-between">
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <div className="flex space-x-2">
            <Button type="button" onClick={() => handleSubmit(false)} className="bg-[#FF6B35] hover:bg-[#e55f30]">
              <Save className="h-4 w-4 mr-2" /> Salvar Rascunho
            </Button>
            <Button type="button" onClick={() => handleSubmit(true)} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
              <Settings className="h-4 w-4 mr-2" /> Criar e Configurar
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ProjectCreationModal;