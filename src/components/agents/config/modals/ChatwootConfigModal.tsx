
import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { MessageSquare, RefreshCw, CheckCircle, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';
import { integrationService } from '@/services/integrationService';

interface ChatwootConfigModalProps {
    isOpen: boolean;
    onClose: () => void;
    initialConfig: { url: string; api_access_token: string; account_id: string; isConnected: boolean };
    onSave: (config: any) => void;
    agentSlug?: string;
}

const ChatwootConfigModal: React.FC<ChatwootConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
    const [config, setConfig] = useState(initialConfig);
    const [isTesting, setIsTesting] = useState(false);

    const handleTestConnection = async () => {
        setIsTesting(true);
        toast.info("Testando conexão com Chatwoot...");

        try {
            const result = await integrationService.testIntegration('chatwoot', config);

            if (result.success) {
                toast.success("Conectado! Caixas de entrada encontradas.");
                onSave({ ...config, isConnected: true });
            } else {
                toast.error(`Falha na conexão: ${result.message || 'Verifique Token/URL'}`);
            }
        } catch (e: any) {
            toast.error(`Erro ao conectar: ${e.message}`);
        } finally {
            setIsTesting(false);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center text-blue-600">
                        <MessageSquare className="h-5 w-5 mr-2" /> Configurar Chatwoot
                    </DialogTitle>
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    <div className="space-y-2">
                        <Label htmlFor="cw-url">Chatwoot URL</Label>
                        <Input
                            id="cw-url"
                            value={config.url}
                            onChange={(e) => setConfig({ ...config, url: e.target.value })}
                            placeholder="https://app.chatwoot.com"
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="cw-token">API Access Token</Label>
                        <Input
                            id="cw-token"
                            type="password"
                            value={config.api_access_token}
                            onChange={(e) => setConfig({ ...config, api_access_token: e.target.value })}
                            placeholder="Token"
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="cw-account">Account ID</Label>
                        <Input
                            id="cw-account"
                            value={config.account_id}
                            onChange={(e) => setConfig({ ...config, account_id: e.target.value })}
                            placeholder="1"
                        />
                    </div>

                    <div className="p-3 bg-blue-50 text-blue-800 rounded-md text-sm border border-blue-100 flex items-start">
                        <ExternalLink className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                        <div>
                            <p className="font-semibold">Info</p>
                            <p>Sincroniza conversas do WhatsApp com Chatwoot.</p>
                        </div>
                    </div>
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>Cancelar</Button>
                    <Button onClick={handleTestConnection} disabled={isTesting || !config.url || !config.api_access_token} className="bg-blue-600 hover:bg-blue-700">
                        {isTesting ? "Testando..." : config.isConnected ? "Salvar" : "Conectar"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default ChatwootConfigModal;
