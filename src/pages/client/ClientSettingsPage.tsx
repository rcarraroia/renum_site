
import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Settings, User, Shield, Lock, Bell, Mail } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';

const ClientSettingsPage: React.FC = () => {
    const [loading, setLoading] = useState(false);

    // Mock Profile Data
    const [profile, setProfile] = useState({
        name: 'Cliente Exemplo',
        email: 'cliente@exemplo.com',
        company: 'Empresa Teste Ltda'
    });

    const handleSaveProfile = (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            setLoading(false);
            toast.success("Perfil atualizado com sucesso!");
        }, 1000);
    };

    const handlePasswordChange = (e: React.FormEvent) => {
        e.preventDefault();
        toast.info("Função de alteração de senha simulada.");
    };

    return (
        <DashboardLayout>
            <div className="mb-6">
                <h2 className="text-3xl font-bold flex items-center text-gray-900 dark:text-gray-100">
                    <Settings className="h-7 w-7 mr-3 text-gray-500" />
                    Minha Conta
                </h2>
                <p className="text-muted-foreground mt-1 ml-10">Gerencie suas informações pessoais e de segurança.</p>
            </div>

            <Tabs defaultValue="profile" className="space-y-6">
                <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
                    <TabsTrigger value="profile">Perfil</TabsTrigger>
                    <TabsTrigger value="security">Segurança</TabsTrigger>
                    <TabsTrigger value="notifications">Notificações</TabsTrigger>
                </TabsList>

                {/* PROFILE TAB */}
                <TabsContent value="profile">
                    <Card>
                        <CardHeader>
                            <CardTitle>Dados Pessoais</CardTitle>
                            <CardDescription>Atualize suas informações de contato.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSaveProfile} className="space-y-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="name">Nome Completo</Label>
                                    <Input
                                        id="name"
                                        value={profile.name}
                                        onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                                    />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="email">Email</Label>
                                    <Input
                                        id="email"
                                        value={profile.email}
                                        disabled
                                        className="bg-gray-100 dark:bg-gray-800 cursor-not-allowed"
                                    />
                                    <p className="text-xs text-muted-foreground">O email não pode ser alterado.</p>
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="company">Empresa</Label>
                                    <Input
                                        id="company"
                                        value={profile.company}
                                        onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                                    />
                                </div>
                                <Button type="submit" disabled={loading} className="mt-4">
                                    {loading ? "Salvando..." : "Salvar Alterações"}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* SECURITY TAB */}
                <TabsContent value="security">
                    <Card>
                        <CardHeader>
                            <CardTitle>Segurança</CardTitle>
                            <CardDescription>Gerencie sua senha e acesso.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="current-password">Senha Atual</Label>
                                    <Input id="current-password" type="password" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="new-password">Nova Senha</Label>
                                    <Input id="new-password" type="password" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="confirm-password">Confirmar Nova Senha</Label>
                                    <Input id="confirm-password" type="password" />
                                </div>
                                <Button onClick={handlePasswordChange} variant="outline">Alterar Senha</Button>
                            </div>

                            <div className="mt-8 pt-6 border-t">
                                <h4 className="text-sm font-medium mb-4 text-red-600">Zona de Perigo</h4>
                                <Button variant="destructive" size="sm">Excluir Conta</Button>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* NOTIFICATIONS TAB */}
                <TabsContent value="notifications">
                    <Card>
                        <CardHeader>
                            <CardTitle>Preferências de Notificação</CardTitle>
                            <CardDescription>Escolha como deseja ser notificado.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="flex items-center justify-between space-x-2">
                                <Label htmlFor="email-notif" className="flex flex-col space-y-1">
                                    <span>Notificações por Email</span>
                                    <span className="font-normal text-xs text-muted-foreground">Receba relatórios semanais e alertas importantes.</span>
                                </Label>
                                <Switch id="email-notif" defaultChecked />
                            </div>
                            <div className="flex items-center justify-between space-x-2">
                                <Label htmlFor="security-alert" className="flex flex-col space-y-1">
                                    <span>Alertas de Segurança</span>
                                    <span className="font-normal text-xs text-muted-foreground">Avisos sobre logins suspeitos.</span>
                                </Label>
                                <Switch id="security-alert" defaultChecked disabled />
                            </div>
                            <div className="flex items-center justify-between space-x-2">
                                <Label htmlFor="marketing-emails" className="flex flex-col space-y-1">
                                    <span>Novidades e Ofertas</span>
                                    <span className="font-normal text-xs text-muted-foreground">Informações sobre novos recursos e promoções.</span>
                                </Label>
                                <Switch id="marketing-emails" />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button onClick={() => toast.success("Preferências salvas.")}>Salvar Preferências</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>
            </Tabs>
        </DashboardLayout>
    );
};

export default ClientSettingsPage;
