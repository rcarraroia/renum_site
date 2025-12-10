import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { FileText, Table, Calendar, Users, Globe, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

interface WorkspaceConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialApps: string[];
  onSave: (apps: string[]) => void;
}

const appOptions = [
  { id: 'docs', label: 'Google Docs', icon: FileText, description: 'Criar/editar documentos' },
  { id: 'sheets', label: 'Google Sheets', icon: Table, description: 'Criar/editar planilhas' },
  { id: 'drive', label: 'Google Drive', icon: Users, description: 'Upload/download arquivos' },
  { id: 'calendar', label: 'Google Calendar', icon: Calendar, description: 'Agendar eventos' },
];

const WorkspaceConfigModal: React.FC<WorkspaceConfigModalProps> = ({ isOpen, onClose, initialApps, onSave }) => {
  const [selectedApps, setSelectedApps] = useState<string[]>(initialApps);

  const handleToggleApp = (appId: string, checked: boolean) => {
    setSelectedApps(prev => 
      checked ? [...prev, appId] : prev.filter(id => id !== appId)
    );
  };

  const handleConnect = () => {
    toast.info("Iniciando fluxo OAuth para Google Workspace (Simulação)...");
    setTimeout(() => {
      onSave(selectedApps);
      toast.success(`Google Workspace conectado. ${selectedApps.length} apps autorizados.`);
      onClose();
    }, 1500);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-blue-600">
            <Globe className="h-5 w-5 mr-2" /> Conectar Google Workspace
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
          <p className="text-sm text-muted-foreground">Selecione os aplicativos que o agente Renus terá permissão para interagir:</p>
          
          <div className="space-y-3">
            {appOptions.map(app => (
              <div key={app.id} className="flex items-start space-x-3 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
                <Checkbox 
                  id={app.id} 
                  checked={selectedApps.includes(app.id)}
                  onCheckedChange={(checked) => handleToggleApp(app.id, checked as boolean)}
                  className="mt-1"
                />
                <div className="flex items-start space-x-3">
                    <app.icon className="h-5 w-5 text-[#4e4ea8] flex-shrink-0" />
                    <div>
                        <Label htmlFor={app.id} className="font-medium">{app.label}</Label>
                        <p className="text-xs text-muted-foreground">{app.description}</p>
                    </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <Button onClick={handleConnect} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
            <CheckCircle className="h-4 w-4 mr-2" /> Conectar com Google ({selectedApps.length} Apps)
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default WorkspaceConfigModal;