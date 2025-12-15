
import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Globe, CheckCircle, AlertTriangle, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';

interface GoogleConfigModalProps {
    isOpen: boolean;
    onClose: () => void;
    initialConfig: { isConnected: boolean };
    onSave: (config: any) => void;
}

const GoogleConfigModal: React.FC<GoogleConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
    const [config, setConfig] = useState(initialConfig);
    const [isLoading, setIsLoading] = useState(false);


    // In the future, this will be the URL to the backend endpoint that starts the OAuth flow
    const AUTH_URL = `http://localhost:8000/api/auth/google/login`; // Assuming local dev for now, typically env var

    const handleConnect = () => {
        setIsLoading(true);

        // Open Popup
        const width = 500;
        const height = 600;
        const left = window.screen.width / 2 - width / 2;
        const top = window.screen.height / 2 - height / 2;

        const popup = window.open(
            AUTH_URL,
            'Google Auth',
            `width=${width},height=${height},top=${top},left=${left}`
        );

        // Listen for message from popup
        const handleMessage = (event: MessageEvent) => {
            // Validation origin could be added here
            if (event.data?.type === 'GOOGLE_AUTH_SUCCESS') {
                const credentials = event.data.payload;

                toast.success("Autenticado com sucesso! Salvando...");

                // Pass credentials to parent to save via integrationService
                onSave({
                    isConnected: true,
                    ...credentials
                });

                popup?.close();
                window.removeEventListener('message', handleMessage);
                setIsLoading(false);
            }
        };

        window.addEventListener('message', handleMessage);

        // Initial timeout check in case popup is closed manually
        const checkPopup = setInterval(() => {
            if (!popup || popup.closed) {
                clearInterval(checkPopup);
                window.removeEventListener('message', handleMessage);
                setIsLoading(false);
            }
        }, 1000);
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center text-yellow-600">
                        <Globe className="h-5 w-5 mr-2" /> Conectar Google Workspace
                    </DialogTitle>
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    <div className="p-4 bg-yellow-50 text-yellow-800 rounded-md text-sm border border-yellow-100">
                        <div className="flex items-center mb-2 font-semibold">
                            <AlertTriangle className="h-4 w-4 mr-2" /> Permissões Necessárias
                        </div>
                        <p className="mb-2">O Agente solicitará acesso a:</p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li>Gmail (Ler/Enviar)</li>
                            <li>Calendar (Agenda)</li>
                            <li>Drive & Sheets (Arquivos)</li>
                            <li>Google Meet (Reuniões)</li>
                            <li>Google Forms (Respostas)</li>
                        </ul>
                    </div>

                    <div className="text-sm text-muted-foreground text-center">
                        Você será redirecionado para a página de login segura do Google.
                        O Renum não terá acesso à sua senha.
                    </div>
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>Cancelar</Button>
                    <Button onClick={handleConnect} disabled={isLoading || config.isConnected} className="bg-blue-600 hover:bg-blue-700">
                        {isLoading ? <span className="animate-spin mr-2">⏳</span> : config.isConnected ? <CheckCircle className="h-4 w-4 mr-2" /> : <Globe className="h-4 w-4 mr-2" />}
                        {config.isConnected ? 'Conectado' : 'Entrar com Google'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default GoogleConfigModal;
