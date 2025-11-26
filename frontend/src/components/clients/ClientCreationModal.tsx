import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Client, ClientSegment, Contact, Address } from '@/types/client';
import { Zap, Save, User, Mail, Phone, Globe, MapPin, Building, Tag } from 'lucide-react';
import { toast } from 'sonner';
import { Separator } from '@/components/ui/separator';

interface ClientCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (client: Omit<Client, 'id' | 'projectsCount' | 'lastInteraction'>) => void;
  initialData?: Client;
}

const initialContact: Contact = { name: '', position: '', email: '', phone: '' };
const initialAddress: Address = { zipCode: '', street: '', number: '', complement: '', city: '', state: '' };

const ClientCreationModal: React.FC<ClientCreationModalProps> = ({ isOpen, onClose, onCreate, initialData }) => {
  const isEdit = !!initialData;
  
  const [formData, setFormData] = useState<Omit<Client, 'id' | 'projectsCount' | 'lastInteraction'>>({
    companyName: initialData?.companyName || '',
    document: initialData?.document || '',
    website: initialData?.website || '',
    segment: initialData?.segment || 'Serviços',
    status: initialData?.status || 'Prospecto',
    contact: initialData?.contact || initialContact,
    address: initialData?.address || initialAddress,
    tags: initialData?.tags || [],
    notes: initialData?.notes || '',
  });

  const handleBasicChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleContactChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, contact: { ...prev.contact, [id]: value } }));
  };

  const handleAddressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, address: { ...prev.address, [id]: value } }));
  };

  const handleSelectChange = (id: 'segment' | 'status', value: string) => {
    setFormData(prev => ({ ...prev, [id]: value as any }));
  };

  const handleSubmit = (e: React.FormEvent, createAndAddProject: boolean) => {
    e.preventDefault();
    if (!formData.companyName || !formData.contact.email) {
      toast.error("Nome da Empresa e Email de Contato são obrigatórios.");
      return;
    }

    onCreate(formData);
    onClose();
    toast.success(`Cliente '${formData.companyName}' ${isEdit ? 'atualizado' : 'criado'} com sucesso!`);
    
    if (createAndAddProject) {
        // Mock redirect/action to open project creation modal
        console.log("Action: Open Project Creation Modal for this client.");
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-[#4e4ea8]">
            <Building className="h-6 w-6 mr-2" /> {isEdit ? 'Editar Cliente' : 'Novo Cliente'}
          </DialogTitle>
          <p className="text-sm text-muted-foreground">Gerencie as informações detalhadas do cliente.</p>
        </DialogHeader>
        
        <form onSubmit={(e) => handleSubmit(e, false)} className="grid gap-6 py-4">
          
          {/* Informações Básicas */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold flex items-center text-[#FF6B35]"><Building className="h-4 w-4 mr-2" /> Informações Básicas</h4>
            <div className="grid grid-cols-2 gap-4">
              <div><Label htmlFor="companyName">Nome/Empresa*</Label><Input id="companyName" value={formData.companyName} onChange={handleBasicChange} required /></div>
              <div><Label htmlFor="document">CNPJ/CPF</Label><Input id="document" value={formData.document} onChange={handleBasicChange} placeholder="00.000.000/0001-00" /></div>
              <div><Label htmlFor="website">Website</Label><Input id="website" value={formData.website} onChange={handleBasicChange} placeholder="https://empresa.com" /></div>
              <div>
                <Label htmlFor="segment">Segmento</Label>
                <Select value={formData.segment} onValueChange={(v) => handleSelectChange('segment', v)}>
                  <SelectTrigger><SelectValue placeholder="Segmento" /></SelectTrigger>
                  <SelectContent>
                    {['MMN', 'Saúde', 'Governo', 'Serviços', 'Tecnologia'].map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="status">Status</Label>
                <Select value={formData.status} onValueChange={(v) => handleSelectChange('status', v)}>
                  <SelectTrigger><SelectValue placeholder="Status" /></SelectTrigger>
                  <SelectContent>
                    {['Ativo', 'Inativo', 'Prospecto'].map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          <Separator />

          {/* Contato Principal */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold flex items-center text-[#0ca7d2]"><User className="h-4 w-4 mr-2" /> Contato Principal</h4>
            <div className="grid grid-cols-2 gap-4">
              <div><Label htmlFor="name">Nome</Label><Input id="name" value={formData.contact.name} onChange={handleContactChange} /></div>
              <div><Label htmlFor="position">Cargo</Label><Input id="position" value={formData.contact.position} onChange={handleContactChange} /></div>
              <div><Label htmlFor="email">Email*</Label><Input id="email" type="email" value={formData.contact.email} onChange={handleContactChange} required /></div>
              <div><Label htmlFor="phone">Telefone</Label><Input id="phone" value={formData.contact.phone} onChange={handleContactChange} placeholder="(XX) XXXXX-XXXX" /></div>
            </div>
          </div>

          <Separator />

          {/* Endereço */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold flex items-center text-[#4e4ea8]"><MapPin className="h-4 w-4 mr-2" /> Endereço</h4>
            <div className="grid grid-cols-4 gap-4">
              <div className="col-span-2"><Label htmlFor="zipCode">CEP</Label><Input id="zipCode" value={formData.address.zipCode} onChange={handleAddressChange} placeholder="00000-000" /></div>
              <div className="col-span-2"><Label htmlFor="city">Cidade</Label><Input id="city" value={formData.address.city} onChange={handleAddressChange} /></div>
              <div className="col-span-3"><Label htmlFor="street">Logradouro</Label><Input id="street" value={formData.address.street} onChange={handleAddressChange} /></div>
              <div className="col-span-1"><Label htmlFor="number">Número</Label><Input id="number" value={formData.address.number} onChange={handleAddressChange} /></div>
              <div className="col-span-2"><Label htmlFor="complement">Complemento</Label><Input id="complement" value={formData.address.complement} onChange={handleAddressChange} /></div>
              <div className="col-span-2"><Label htmlFor="state">Estado</Label><Input id="state" value={formData.address.state} onChange={handleAddressChange} /></div>
            </div>
          </div>

          <Separator />

          {/* Observações */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold flex items-center text-muted-foreground"><Tag className="h-4 w-4 mr-2" /> Observações</h4>
            <div><Label htmlFor="notes">Observações Internas</Label><Textarea id="notes" rows={3} value={formData.notes} onChange={handleBasicChange} placeholder="Detalhes sobre o histórico ou necessidades do cliente." /></div>
          </div>

          <DialogFooter className="sm:justify-between mt-4">
            <Button variant="outline" onClick={onClose}>Cancelar</Button>
            <div className="flex space-x-2">
              <Button type="submit" className="bg-[#FF6B35] hover:bg-[#e55f30]">
                <Save className="h-4 w-4 mr-2" /> {isEdit ? 'Salvar Alterações' : 'Criar Cliente'}
              </Button>
              {!isEdit && (
                <Button type="button" onClick={(e) => handleSubmit(e, true)} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                  <Zap className="h-4 w-4 mr-2" /> Criar e Adicionar Projeto
                </Button>
              )}
            </div>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default ClientCreationModal;