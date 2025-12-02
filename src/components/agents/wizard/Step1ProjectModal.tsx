import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Briefcase, Users, Building, Mail, Hash, DollarSign } from 'lucide-react';
import { toast } from 'sonner';
import { mockClients } from '@/mocks/agents.mock';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (data: any) => void;
}

// --- Modal de Criação de Projeto ---
interface ProjectModalProps extends ModalProps {}

const ProjectCreationModal: React.FC<ProjectModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [name, setName] = useState('');
  const [clientId, setClientId] = useState(mockClients[0].id);
  const [agentLimit, setAgentLimit] = useState(5);
  const [instanceLimit, setInstanceLimit] = useState(10);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name) {
      toast.error("O nome do projeto é obrigatório.");
      return;
    }
    
    const newProject = {
      id: `p${Date.now()}`,
      name,
      client_id: clientId,
      agents_limit: agentLimit,
      instances_limit: instanceLimit,
    };
    onSuccess(newProject);
    onClose();
    toast.success(`Projeto '${name}' criado com sucesso!`);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-[#4e4ea8]"><Briefcase className="h-5 w-5 mr-2" /> Criar Novo Projeto</DialogTitle>
          <DialogDescription>Defina os limites e o cliente para o novo projeto.</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nome do Projeto *</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required placeholder="Ex: Pacote Enterprise Slim" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="client">Cliente</Label>
            <Select value={clientId} onValueChange={setClientId}>
              <SelectTrigger id="client">
                <SelectValue placeholder="Selecione o Cliente" />
              </SelectTrigger>
              <SelectContent>
                {mockClients.map(client => (
                  <SelectItem key={client.id} value={client.id}>{client.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="agentLimit">Limite de Agentes</Label>
              <Input id="agentLimit" type="number" value={agentLimit} onChange={(e) => setAgentLimit(parseInt(e.target.value) || 0)} min={1} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="instanceLimit">Limite de Instâncias</Label>
              <Input id="instanceLimit" type="number" value={instanceLimit} onChange={(e) => setInstanceLimit(parseInt(e.target.value) || 0)} min={1} />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={onClose}>Cancelar</Button>
            <Button type="submit" className="bg-[#4e4ea8] hover:bg-[#3a3a80]">Criar Projeto</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

// --- Modal de Criação de Cliente ---
interface ClientModalProps extends ModalProps {}

const ClientCreationModal: React.FC<ClientModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [companyName, setCompanyName] = useState('');
  const [type, setType] = useState('b2b_empresa');
  const [email, setEmail] = useState('');
  
  const slug = companyName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!companyName || !email) {
      toast.error("Nome e Email são obrigatórios.");
      return;
    }
    
    const newClient = {
      id: `c${Date.now()}`,
      name: companyName,
      type: type,
      slug: slug,
      email,
    };
    onSuccess(newClient);
    onClose();
    toast.success(`Cliente '${companyName}' criado com sucesso!`);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-[#FF6B35]"><Users className="h-5 w-5 mr-2" /> Criar Novo Cliente</DialogTitle>
          <DialogDescription>Adicione um novo cliente para vincular ao seu agente.</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="companyName">Nome/Razão Social *</Label>
            <Input id="companyName" value={companyName} onChange={(e) => setCompanyName(e.target.value)} required placeholder="Ex: Alpha Solutions" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="type">Tipo</Label>
            <Select value={type} onValueChange={setType}>
              <SelectTrigger id="type">
                <SelectValue placeholder="Selecione o Tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="b2b_empresa">B2B - Corporativo</SelectItem>
                <SelectItem value="b2c_individual">B2C - Individual/Avulso</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email de Contato *</Label>
            <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="contato@empresa.com" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="slug">Slug (Identificador)</Label>
            <Input id="slug" readOnly value={slug} className="font-mono bg-gray-100 dark:bg-gray-800" />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={onClose}>Cancelar</Button>
            <Button type="submit" className="bg-[#FF6B35] hover:bg-[#e55f30]">Criar Cliente</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

interface Step1ProjectModalProps {
    isProjectModalOpen: boolean;
    isClientModalOpen: boolean;
    onCloseProjectModal: () => void;
    onCloseClientModal: () => void;
    onProjectCreated: (project: any) => void;
    onClientCreated: (client: any) => void;
}

const Step1ProjectModals: React.FC<Step1ProjectModalProps> = ({
    isProjectModalOpen,
    isClientModalOpen,
    onCloseProjectModal,
    onCloseClientModal,
    onProjectCreated,
    onClientCreated,
}) => {
    return (
        <>
            <ProjectCreationModal 
                isOpen={isProjectModalOpen} 
                onClose={onCloseProjectModal} 
                onSuccess={onProjectCreated} 
            />
            <ClientCreationModal 
                isOpen={isClientModalOpen} 
                onClose={onCloseClientModal} 
                onSuccess={onClientCreated} 
            />
        </>
    );
};

export default Step1ProjectModals;