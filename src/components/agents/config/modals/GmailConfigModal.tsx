import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Mail, Globe, CheckCircle, RefreshCw, Send } from 'lucide-react';
import { toast } from 'sonner';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Separator } from '@/components/ui/separator';

interface GmailConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialConfig: { method: 'oauth' | 'smtp'; email: string; host: string; port: string; password: string; isConnected: boolean };
  onSave: (config: any) => void;
}

const GmailConfigModal: React.FC<GmailConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
  const [config, setConfig] = useState(initialConfig);
  const [isTesting, setIsTesting] = useState(false);

  const handleOAuthConnect = () => {
    toast.info("Iniciando fluxo OAuth com Google (Simulação)...");
    setTimeout(() => {
      const mockEmail = "vendas@slim.com";
      setConfig(prev => ({ ...prev, method: 'oauth', email: mockEmail }));
      onSave({ ...config, method: 'oauth', email: mockEmail });
      toast.success(`Conta conectada: ${mockEmail}`);
      onClose();
    }, 1500);
  };

  const handleTestSmtp = () => {
    setIsTesting(true);
    toast.info("Testando conexão SMTP...");
    setTimeout(() => {
      setIsTesting(false);
      if (config.host && config.port && config.email && config.password) {
        toast.success("Conexão SMTP bem-sucedida!");
        onSave(config);
      } else {
        toast.error("Falha na conexão SMTP. Verifique as credenciais.");
      }
    }, 1500);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-red-600">
            <Mail className="h-5 w-5 mr-2" /> Conectar Conta Gmail / Email
          </DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <RadioGroup value={config.method} onValueChange={(v) => setConfig(prev => ({ ...prev, method: v as 'oauth' | 'smtp' }))}>
            
            {/* Opção 1: OAuth */}
            <div className="p-4 border rounded-lg space-y-3">
                <div className="flex items-center space-x-2">
                    <RadioGroupItem value="oauth" id="oauth" />
                    <Label htmlFor="oauth" className="font-medium">Opção 1: OAuth (Gmail via Composio)</Label>
                </div>
                <p className="text-sm text-muted-foreground ml-6">Conecte sua conta Gmail de forma segura.</p>
                <Button 
                    onClick={handleOAuthConnect} 
                    disabled={config.method !== 'oauth'}
                    variant="outline" 
                    className="w-full bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-800"
                >
                    <Globe className="h-4 w-4 mr-2 text-blue-500" /> Conectar com Google
                </Button>
            </div>

            {/* Opção 2: SMTP Manual */}
            <div className="p-4 border rounded-lg space-y-3">
                <div className="flex items-center space-x-2">
                    <RadioGroupItem value="smtp" id="smtp" />
                    <Label htmlFor="smtp" className="font-medium">Opção 2: SMTP Manual</Label>
                </div>
                
                <div className="grid grid-cols-2 gap-4 ml-6" hidden={config.method !== 'smtp'}>
                    <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" type="email" value={config.email} onChange={(e) => setConfig({ ...config, email: e.target.value })} placeholder="seu@email.com" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="password">Senha/App Password</Label>
                        <Input id="password" type="password" value={config.password} onChange={(e) => setConfig({ ...config, password: e.target.value })} placeholder="••••••••" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="host">SMTP Host</Label>
                        <Input id="host" value={config.host} onChange={(e) => setConfig({ ...config, host: e.target.value })} placeholder="smtp.gmail.com" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="port">SMTP Port</Label>
                        <Input id="port" type="number" value={config.port} onChange={(e) => setConfig({ ...config, port: e.target.value })} placeholder="587" />
                    </div>
                    <Button onClick={handleTestSmtp} disabled={config.method !== 'smtp' || isTesting} variant="secondary" className="col-span-2">
                        <Send className="h-4 w-4 mr-2" /> {isTesting ? 'Testando...' : 'Testar Conexão'}
                    </Button>
                </div>
            </div>
          </RadioGroup>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <Button onClick={() => onSave(config)} disabled={isTesting} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
            <CheckCircle className="h-4 w-4 mr-2" /> Salvar Configuração
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default GmailConfigModal;