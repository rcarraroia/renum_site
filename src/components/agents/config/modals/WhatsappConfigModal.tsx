import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { MessageSquare, Copy, RefreshCw, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

interface WhatsappConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialConfig: { token: string; url: string; phoneId: string; isConnected: boolean };
  onSave: (config: { token: string; url: string; phoneId: string }) => void;
  agentSlug: string;
}

import { integrationService } from '@/services/integrationService';

const WhatsappConfigModal: React.FC<WhatsappConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave, agentSlug }) => {
  const [config, setConfig] = useState(initialConfig);
  const [isTesting, setIsTesting] = useState(false);
  const webhookUrl = `https://api.renum.com.br/webhook/${agentSlug}/whatsapp`;

  const handleTestConnection = async () => {
    setIsTesting(true);
    toast.info("Testando conexão com a API Uazapi...");

    try {
      const result = await integrationService.testIntegration('uazapi', config);

      if (result.success) {
        toast.success("Conexão bem-sucedida!");
        onSave({ ...config, isConnected: true }); // Pass isConnected status to parent
      } else {
        toast.error(`Falha na conexão: ${result.message || 'Erro desconhecido'}`);
      }
    } catch (e: any) {
      toast.error(`Erro ao conectar: ${e.message}`);
    } finally {
      setIsTesting(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(webhookUrl);
    toast.info("URL do Webhook copiada!");
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center text-green-600">
            <MessageSquare className="h-5 w-5 mr-2" /> Configurar WhatsApp Business (Uazapi)
          </DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="url">API URL *</Label>
            <Input id="url" value={config.url} onChange={(e) => setConfig({ ...config, url: e.target.value })} placeholder="https://api.uazapi.com" required />
            <p className="text-xs text-muted-foreground">URL base da API Uazapi</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="token">API Token *</Label>
            <Input id="token" type="password" value={config.token} onChange={(e) => setConfig({ ...config, token: e.target.value })} placeholder="••••••••••" required />
            <p className="text-xs text-muted-foreground">Token fornecido pela Uazapi</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="phoneId">Phone Number ID *</Label>
            <Input id="phoneId" value={config.phoneId} onChange={(e) => setConfig({ ...config, phoneId: e.target.value })} placeholder="5511999999999" required />
            <p className="text-xs text-muted-foreground">ID do número WhatsApp Business</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="webhook">Webhook URL (Readonly)</Label>
            <div className="flex space-x-2">
              <Input id="webhook" readOnly value={webhookUrl} className="font-mono text-xs" />
              <Button variant="outline" size="icon" onClick={handleCopy}><Copy className="h-4 w-4" /></Button>
            </div>
            <p className="text-xs text-muted-foreground">Configure esta URL no painel Uazapi para receber mensagens.</p>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancelar</Button>
          <Button onClick={handleTestConnection} disabled={isTesting || !config.token || !config.url || !config.phoneId} className="bg-[#FF6B35] hover:bg-[#e55f30]">
            {isTesting ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : config.isConnected ? <RefreshCw className="h-4 w-4 mr-2" /> : <CheckCircle className="h-4 w-4 mr-2" />}
            {config.isConnected ? 'Testar e Salvar' : 'Testar Conexão'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default WhatsappConfigModal;