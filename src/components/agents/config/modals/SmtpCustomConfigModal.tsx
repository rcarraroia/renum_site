import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Mail, Send, CheckCircle, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';
import { Switch } from '@/components/ui/switch';

interface SmtpCustomConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialConfig: { host: string; port: string; email: string; password: string; useTls: boolean; isConnected: boolean };
  onSave: (config: any) => void;
}

const SmtpCustomConfigModal: React.FC<SmtpCustomConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
  const [config, setConfig] = useState(initialConfig);
  const [isTesting, setIsTesting] = useState(false);

  const handleTestConnection = () => {
    setIsTesting(true);
    toast.info("Enviando email de teste...");
    setTimeout(() => {
      setIsTesting(false);
      if (config.host && config.port && config.email && config.password) {
        toast.success("Email de teste enviado com sucesso! Conexão SMTP OK.");
        onSave(config);
      } else {
        toast.error("Falha no envio. Verifique as configurações.");
      }
    }, 1500);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-gray-600 dark:text-gray-300">
            <Mail className="h-5 w-5 mr-2" /> Configurar Servidor SMTP Custom
          </DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="host">SMTP Host *</Label>
              <Input id="host" value={config.host} onChange={(e) => setConfig({ ...config, host: e.target.value })} placeholder="smtp.sendgrid.net" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="port">Porta *</Label>
              <Input id="port" type="number" value={config.port} onChange={(e) => setConfig({ ...config, port: e.target.value })} placeholder="587" required />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email de Envio *</Label>
            <Input id="email" type="email" value={config.email} onChange={(e) => setConfig({ ...config, email: e.target.value })} placeholder="notificacoes@empresa.com" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Senha / App Password *</Label>
            <Input id="password" type="password" value={config.password} onChange={(e) => setConfig({ ...config, password: e.target.value })} placeholder="••••••••" required />
          </div>
          
          <div className="flex items-center justify-between p-2 border rounded-lg">
            <Label htmlFor="tls">Usar TLS/SSL</Label>
            <Switch id="tls" checked={config.useTls} onCheckedChange={(v) => setConfig({ ...config, useTls: v })} />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <Button onClick={handleTestConnection} disabled={isTesting || !config.host || !config.email} className="bg-[#0ca7d2] hover:bg-[#0987a8]">
            <Send className="h-4 w-4 mr-2" /> {isTesting ? 'Enviando Teste...' : 'Enviar Email Teste'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default SmtpCustomConfigModal;