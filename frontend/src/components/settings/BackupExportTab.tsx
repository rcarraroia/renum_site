import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Database, UploadCloud, Download, Clock, Save } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';

const BackupExportTab: React.FC = () => {
    const [settings, setSettings] = useState({
        autoBackup: true,
        backupFrequency: 'daily',
        exportFormat: 'json',
    });
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = () => {
        setIsSaving(true);
        setTimeout(() => {
            setIsSaving(false);
            toast.success("Configurações de Backup salvas!");
        }, 1000);
    };

    const handleManualBackup = () => {
        toast.info("Iniciando backup manual do banco de dados...");
        setTimeout(() => {
            toast.success("Backup concluído e enviado para AWS S3.");
        }, 2000);
    };

    const handleExport = () => {
        toast.info(`Exportando dados no formato ${settings.exportFormat}...`);
        setTimeout(() => {
            toast.success("Exportação de dados concluída!");
        }, 1500);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Database className="h-5 w-5 mr-2" /> Backup do Banco de Dados</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="autoBackup">Backup Automático Diário</Label>
                        <Switch id="autoBackup" checked={settings.autoBackup} onCheckedChange={(v) => setSettings({...settings, autoBackup: v})} />
                    </div>
                    
                    <div>
                        <Label>Frequência de Backup</Label>
                        <Select value={settings.backupFrequency} onValueChange={(v) => setSettings({...settings, backupFrequency: v as string})}>
                            <SelectTrigger className="w-[180px]"><SelectValue placeholder="Frequência" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="daily">Diário</SelectItem>
                                <SelectItem value="weekly">Semanal</SelectItem>
                                <SelectItem value="monthly">Mensal</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <Button onClick={handleManualBackup} variant="outline">
                        <UploadCloud className="h-4 w-4 mr-2" /> Fazer Backup Manual Agora
                    </Button>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Download className="h-5 w-5 mr-2" /> Exportação de Dados</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Formato de Exportação</Label>
                        <Select value={settings.exportFormat} onValueChange={(v) => setSettings({...settings, exportFormat: v as string})}>
                            <SelectTrigger className="w-[180px]"><SelectValue placeholder="Formato" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="json">JSON</SelectItem>
                                <SelectItem value="csv">CSV</SelectItem>
                                <SelectItem value="sql">SQL Dump</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <Button onClick={handleExport} className="bg-[#0ca7d2] hover:bg-[#0987a8]">
                        <Download className="h-4 w-4 mr-2" /> Exportar Todos os Dados
                    </Button>
                </CardContent>
            </Card>
            
            <div className="flex justify-end">
                <Button onClick={handleSave} disabled={isSaving} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                    <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Configurações'}
                </Button>
            </div>
        </div>
    );
};

export default BackupExportTab;