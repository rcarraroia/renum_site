import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Terminal, Bug, Trash2, Save, Settings } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';

const AdvancedTab: React.FC = () => {
    const [settings, setSettings] = useState({
        debugMode: false,
        featureFlags: true,
    });
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = () => {
        setIsSaving(true);
        setTimeout(() => {
            setIsSaving(false);
            toast.success("Configurações avançadas salvas!");
        }, 1000);
    };

    const handleClearCache = () => {
        toast.info("Limpando cache do sistema...");
        setTimeout(() => {
            toast.success("Cache limpo com sucesso!");
        }, 1000);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Bug className="h-5 w-5 mr-2" /> Debug e Logs</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="debugMode">Modo Debug</Label>
                        <Switch id="debugMode" checked={settings.debugMode} onCheckedChange={(v) => setSettings({...settings, debugMode: v})} />
                    </div>
                    <Button variant="outline">
                        <Terminal className="h-4 w-4 mr-2" /> Visualizar Logs do Sistema (Mock)
                    </Button>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Settings className="h-5 w-5 mr-2" /> Gerenciamento de Sistema</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="featureFlags">Feature Flags Ativas</Label>
                        <Switch id="featureFlags" checked={settings.featureFlags} onCheckedChange={(v) => setSettings({...settings, featureFlags: v})} />
                    </div>
                    <Button onClick={handleClearCache} variant="destructive">
                        <Trash2 className="h-4 w-4 mr-2" /> Limpar Cache
                    </Button>
                </CardContent>
            </Card>
            
            <div className="flex justify-end">
                <Button onClick={handleSave} disabled={isSaving} className="bg-[#0ca7d2] hover:bg-[#0987a8]">
                    <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Avançado'}
                </Button>
            </div>
        </div>
    );
};

export default AdvancedTab;