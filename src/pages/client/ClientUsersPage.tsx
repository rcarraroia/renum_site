
import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Users, UserPlus, Trash2, Shield, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

// Mock Data
const MOCK_USERS = [
    { id: 1, name: 'Admin Cliente', email: 'admin@cliente.com', role: 'Dono', status: 'active', avatar: '' },
    { id: 2, name: 'Gerente Vendas', email: 'vendas@cliente.com', role: 'Membro', status: 'active', avatar: '' },
];

const ClientUsersPage: React.FC = () => {
    // Check permission logic (Mocked - TODO: check subscription Addon)
    const hasAccess = true; // Set to false to test "Upgrade required" state
    const [users, setUsers] = useState(MOCK_USERS);
    const [inviteEmail, setInviteEmail] = useState('');
    const [isInviteOpen, setIsInviteOpen] = useState(false);

    const handleInvite = () => {
        if (!inviteEmail) return;
        toast.success(`Convite enviado para ${inviteEmail}`);
        setIsInviteOpen(false);
        setInviteEmail('');
        // Logic to call API
    };

    const handleRemoveUser = (id: number) => {
        toast.success("Usuário removido da organização.");
        setUsers(users.filter(u => u.id !== id));
    };

    if (!hasAccess) {
        return (
            <DashboardLayout>
                <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
                    <div className="bg-yellow-100 p-4 rounded-full">
                        <Users className="h-12 w-12 text-yellow-600" />
                    </div>
                    <h2 className="text-2xl font-bold">Gestão de Equipe (B2B)</h2>
                    <p className="max-w-md text-muted-foreground">
                        A funcionalidade de múltiplos usuários está disponível apenas para planos Empresariais ou com o Add-on de Equipe ativo.
                    </p>
                    <Button variant="default" className="bg-[#4e4ea8]">Fazer Upgrade Agora</Button>
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-3xl font-bold flex items-center text-gray-900 dark:text-gray-100">
                        <Users className="h-7 w-7 mr-3 text-indigo-600" />
                        Minha Equipe
                    </h2>
                    <p className="text-muted-foreground mt-1">Gerencie quem tem acesso à sua conta Renum.</p>
                </div>

                <Dialog open={isInviteOpen} onOpenChange={setIsInviteOpen}>
                    <DialogTrigger asChild>
                        <Button className="bg-indigo-600 hover:bg-indigo-700">
                            <UserPlus className="h-4 w-4 mr-2" /> Convidar Membro
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Convidar Novo Usuário</DialogTitle>
                            <DialogDescription>
                                Envie um convite por email para adicionar um membro à sua equipe.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="email">Email do Usuário</Label>
                                <Input
                                    id="email"
                                    placeholder="exemplo@empresa.com"
                                    value={inviteEmail}
                                    onChange={(e) => setInviteEmail(e.target.value)}
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setIsInviteOpen(false)}>Cancelar</Button>
                            <Button onClick={handleInvite}>Enviar Convite</Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Membros da Organização</CardTitle>
                    <CardDescription>
                        Você tem {users.length} usuários ativos em seu plano.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Usuário</TableHead>
                                    <TableHead>Função</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Ações</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {users.map((user) => (
                                    <TableRow key={user.id}>
                                        <TableCell className="font-medium">
                                            <div className="flex items-center space-x-3">
                                                <Avatar className="h-8 w-8">
                                                    <AvatarImage src={user.avatar} />
                                                    <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                                                </Avatar>
                                                <div>
                                                    <div className="font-bold">{user.name}</div>
                                                    <div className="text-xs text-muted-foreground">{user.email}</div>
                                                </div>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={user.role === 'Dono' ? 'default' : 'secondary'}>
                                                {user.role}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <span className="flex items-center text-sm text-green-600">
                                                <div className="h-2 w-2 rounded-full bg-green-600 mr-2" />
                                                Ativo
                                            </span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            {user.role !== 'Dono' && (
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                                    onClick={() => handleRemoveUser(user.id)}
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>

            <Alert className="mt-6 bg-blue-50 border-blue-200">
                <AlertCircle className="h-4 w-4 text-blue-600" />
                <AlertTitle className="text-blue-800">Sobre Permissões</AlertTitle>
                <AlertDescription className="text-blue-700">
                    Membros da equipe têm acesso a todos os agentes e conversas, mas não podem alterar configurações de faturamento ou excluir a conta da organização.
                </AlertDescription>
            </Alert>
        </DashboardLayout>
    );
};

export default ClientUsersPage;
