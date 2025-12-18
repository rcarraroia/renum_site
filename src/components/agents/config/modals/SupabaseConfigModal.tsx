import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Database, ShieldCheck } from 'lucide-react';

interface SupabaseConfigModalProps {
    isOpen: boolean;
    onClose: () => void;
    initialConfig: any;
    onSave: (config: any) => void;
}

const SupabaseConfigModal: React.FC<SupabaseConfigModalProps> = ({ isOpen, onClose, initialConfig, onSave }) => {
    const [config, setConfig] = useState(initialConfig);

    const handleSave = () => {
        onSave({ ...config, isConnected: true });
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center">
                        <Database className="h-5 w-5 mr-2 text-emerald-500" />
                        Configurar Supabase Externo
                    </DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                        <Label htmlFor="url">Supabase Project URL</Label>
                        <Input
                            id="url"
                            value={config.url}
                            onChange={(e) => setConfig({ ...config, url: e.target.value })}
                            placeholder="https://xyz.supabase.co"
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="anon_key">Anon Key</Label>
                        <Input
                            id="anon_key"
                            type="password"
                            value={config.anon_key}
                            onChange={(e) => setConfig({ ...config, anon_key: e.target.value })}
                            placeholder="public-anon-key"
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="service_role">Service Role Key (Opcional)</Label>
                        <Input
                            id="service_role"
                            type="password"
                            value={config.service_role_key}
                            onChange={(e) => setConfig({ ...config, service_role_key: e.target.value })}
                            placeholder="service-role-key (para operações administrativas)"
                        />
                    </div>
                    <div className="bg-emerald-50 p-3 rounded-lg flex items-start space-x-3 text-emerald-800 text-xs">
                        <ShieldCheck className="h-4 w-4 mt-0.5 mt-0.5 flex-shrink-0" />
                        <p>Seus dados de conexão são criptografados. O Renum utilizará essas chaves apenas para executar as ações que você definir nas ferramentas do seu agente.</p>
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>Cancelar</Button>
                    <Button onClick={handleSave} className="bg-emerald-600 hover:bg-emerald-700">Salvar Conexão</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default SupabaseConfigModal;
