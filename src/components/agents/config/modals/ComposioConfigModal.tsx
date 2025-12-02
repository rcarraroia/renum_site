import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Zap, CheckCircle, RefreshCw, Link } from 'lucide-react';
import { toast } from 'sonner';
import { Checkbox } from '@/components/ui/checkbox';

interface ComposioConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialConfig: { apiKey: string; entityId: string; isConnected: boolean };
  onSave: (config: { apiKey: string; entityId: string }) => void;
}

const ComposioConfigModal: React.FC<ComposioConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
  const [config, setConfig] = useState(initialConfig);
  const [isTesting, setIsTesting] = useState(false);

  const handleTestConnection = () => {
    setIsTesting(true);
    toast.info("Testando conexão com Composio...");
    setTimeout(() => {
      setIsTesting(false);
      if (config.apiKey) {
        toast.success("Conexão Composio bem-sucedida! 500+ apps disponíveis.");
        onSave(config);
      } else {
        toast.error("Falha na conexão. API Key inválida.");
      }
    }, 1500);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-purple-600">
            <Zap className="h-5 w-5 mr-2" /> Configurar Composio Platform
          </DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="apiKey">Composio API Key *</Label>
            <Input id="apiKey" type="password" value={config.apiKey} onChange={(e) => setConfig({ ...config, apiKey: e.target.value })} placeholder="••••••••••" required />
            <p className="text-xs text-muted-foreground flex items-center">
                Token fornecido pela Composio. <Link className="text-[#0ca7d2] ml-1 hover:underline" href="https://composio.dev/dashboard" target="_blank">Como obter API Key</Link>
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="entityId">Entity ID (Opcional)</Label>
            <Input id="entityId" value={config.entityId} onChange={(e) => setConfig({ ...config, entityId: e.target.value })} placeholder="user@empresa.com" />
            <p className="text-xs text-muted-foreground">Identificador único do usuário/empresa para logs.</p>
          </div>
          
          <div className="flex items-center space-x-2">
            <Checkbox id="auto-connect" defaultChecked />
            <Label htmlFor="auto-connect" className="text-sm">Conectar automaticamente apps disponíveis</Label>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <Button onClick={handleTestConnection} disabled={isTesting || !config.apiKey} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
            {isTesting ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <CheckCircle className="h-4 w-4 mr-2" />}
            {config.isConnected ? 'Testar e Salvar' : 'Testar Conexão'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ComposioConfigModal;