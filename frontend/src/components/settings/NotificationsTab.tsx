import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Mail, Bell, Clock, Save } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

const NotificationsTab: React.FC = () => {
    const [settings, setSettings] = useState({
        emailNewClient: true,
        emailNewProject: true,
        emailConversationAlert: false,
        inAppNewLead: true,
        inAppProjectUpdate: true,
        scheduleDigest: 'daily',
    });

    const handleSave = () => {
        toast.success("Configurações de notificação salvas!");
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Mail className="h-5 w-5 mr-2" /> Notificações por Email</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="emailNewClient">Alerta de Novo Cliente/Prospecto</Label>
                        <Switch id="emailNewClient" checked={settings.emailNewClient} onCheckedChange={(v) => setSettings({...settings, emailNewClient: v})} />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label htmlFor="emailNewProject">Novo Projeto Iniciado</Label>
                        <Switch id="emailNewProject" checked={settings.emailNewProject} onCheckedChange={(v) => setSettings({...settings, emailNewProject: v})} />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label htmlFor="emailConversationAlert">Alerta de Conversa Crítica (Prioridade Alta)</Label>
                        <Switch id="emailConversationAlert" checked={settings.emailConversationAlert} onCheckedChange={(v) => setSettings({...settings, emailConversationAlert: v})} />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Bell className="h-5 w-5 mr-2" /> Notificações In-App</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="inAppNewLead">Novo Lead (Renus)</Label>
                        <Switch id="inAppNewLead" checked={settings.inAppNewLead} onCheckedChange={(v) => setSettings({...settings, inAppNewLead: v})} />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label htmlFor="inAppProjectUpdate">Atualização de Status de Projeto</Label>
                        <Switch id="inAppProjectUpdate" checked={settings.inAppProjectUpdate} onCheckedChange={(v) => setSettings({...settings, inAppProjectUpdate: v})} />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><Clock className="h-5 w-5 mr-2" /> Agendamento</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <Label htmlFor="scheduleDigest" className="flex flex-col space-y-1">
                        <span>Frequência do Resumo Diário/Semanal (Digest)</span>
                        <span className="font-normal leading-snug text-muted-foreground">Receba um resumo consolidado das atividades.</span>
                    </Label>
                    {/* Mock Select for scheduling */}
                    <div className="w-1/2">
                        <select id="scheduleDigest" value={settings.scheduleDigest} onChange={(e) => setSettings({...settings, scheduleDigest: e.target.value})} className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
                            <option value="immediate">Imediato</option>
                            <option value="daily">Diário (8h)</option>
                            <option value="weekly">Semanal (Segunda)</option>
                        </select>
                    </div>
                </CardContent>
            </Card>
            
            <div className="flex justify-end">
                <Button onClick={handleSave} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                    <Save className="h-4 w-4 mr-2" /> Salvar Notificações
                </Button>
            </div>
        </div>
    );
};

export default NotificationsTab;