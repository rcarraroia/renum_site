import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { User, Mail, Lock, Plus, Edit, Trash2, CheckCircle, XCircle, Settings, Shield, Key } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';

interface UserData {
    id: number;
    name: string;
    email: string;
    role: 'Admin' | 'Manager' | 'Staff' | 'Client';
    status: 'Active' | 'Inactive';
    lastLogin: string;
}

const MOCK_USERS: UserData[] = [
    { id: 1, name: 'Renato Carraro', email: 'admin@renum.tech', role: 'Admin', status: 'Active', lastLogin: 'Agora' },
    { id: 2, name: 'Ana Silva', email: 'ana.s@renum.tech', role: 'Manager', status: 'Active', lastLogin: '1h atrás' },
    { id: 3, name: 'Bruno Costa', email: 'bruno.c@renum.tech', role: 'Staff', status: 'Inactive', lastLogin: '3 dias atrás' },
];

const UserPermissionsTab: React.FC = () => {
    const [users, setUsers] = useState(MOCK_USERS);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingUser, setEditingUser] = useState<UserData | null>(null);

    const handleEdit = (user: UserData) => {
        setEditingUser(user);
        setIsModalOpen(true);
    };

    const handleDelete = (id: number) => {
        setUsers(users.filter(u => u.id !== id));
        toast.warning("Usuário excluído.");
    };

    const handleSaveUser = (e: React.FormEvent) => {
        e.preventDefault();
        // Mock save logic
        toast.success(`Usuário ${editingUser ? 'atualizado' : 'adicionado'} com sucesso!`);
        setIsModalOpen(false);
        setEditingUser(null);
    };

    const getRoleColor = (role: UserData['role']) => {
        switch (role) {
            case 'Admin': return 'bg-[#4e4ea8] hover:bg-[#4e4ea8]/80 text-white';
            case 'Manager': return 'bg-[#FF6B35] hover:bg-[#FF6B35]/80 text-white';
            case 'Staff': return 'bg-[#0ca7d2] hover:bg-[#0ca7d2]/80 text-white';
            default: return 'bg-gray-500 text-white';
        }
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="flex items-center text-[#4e4ea8]"><User className="h-5 w-5 mr-2" /> Gerenciamento de Usuários</CardTitle>
                    <Button onClick={() => { setEditingUser(null); setIsModalOpen(true); }} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                        <Plus className="h-4 w-4 mr-2" /> Adicionar Usuário
                    </Button>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Nome</TableHead>
                                <TableHead>Email</TableHead>
                                <TableHead>Função</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Último Login</TableHead>
                                <TableHead className="text-right">Ações</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {users.map(user => (
                                <TableRow key={user.id}>
                                    <TableCell className="font-medium">{user.name}</TableCell>
                                    <TableCell>{user.email}</TableCell>
                                    <TableCell><Badge className={getRoleColor(user.role)}>{user.role}</Badge></TableCell>
                                    <TableCell>
                                        {user.status === 'Active' ? <CheckCircle className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                                    </TableCell>
                                    <TableCell className="text-sm text-muted-foreground">{user.lastLogin}</TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Button variant="ghost" size="sm" onClick={() => handleEdit(user)}><Edit className="h-4 w-4" /></Button>
                                        <Button variant="destructive" size="sm" onClick={() => handleDelete(user.id)}><Trash2 className="h-4 w-4" /></Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><Shield className="h-5 w-5 mr-2" /> Segurança</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label htmlFor="2fa" className="flex flex-col space-y-1">
                            <span>Autenticação de Dois Fatores (2FA)</span>
                            <span className="font-normal leading-snug text-muted-foreground">Exigir 2FA para todos os usuários administradores.</span>
                        </Label>
                        <Switch id="2fa" defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label htmlFor="password-policy" className="flex flex-col space-y-1">
                            <span>Política de Senha Forte</span>
                            <span className="font-normal leading-snug text-muted-foreground">Exigir senhas com 8+ caracteres, maiúsculas, minúsculas e símbolos.</span>
                        </Label>
                        <Switch id="password-policy" defaultChecked />
                    </div>
                </CardContent>
            </Card>

            {/* User Modal */}
            <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                        <DialogTitle>{editingUser ? 'Editar Usuário' : 'Adicionar Novo Usuário'}</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSaveUser} className="grid gap-4 py-4">
                        <div className="space-y-2"><Label htmlFor="name">Nome</Label><Input id="name" defaultValue={editingUser?.name} required /></div>
                        <div className="space-y-2"><Label htmlFor="email">Email</Label><Input id="email" type="email" defaultValue={editingUser?.email} required /></div>
                        <div className="space-y-2"><Label htmlFor="password">Senha</Label><Input id="password" type="password" placeholder="Deixe em branco para não alterar" /></div>
                        <div className="space-y-2">
                            <Label htmlFor="role">Função</Label>
                            <Select defaultValue={editingUser?.role || 'Staff'}>
                                <SelectTrigger><SelectValue placeholder="Selecione a Função" /></SelectTrigger>
                                <SelectContent>
                                    {['Admin', 'Manager', 'Staff', 'Client'].map(r => <SelectItem key={r} value={r}>{r}</SelectItem>)}
                                </SelectContent>
                            </Select>
                        </div>
                        <DialogFooter>
                            <Button type="submit" className="bg-[#4e4ea8] hover:bg-[#3a3a80]">Salvar</Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default UserPermissionsTab;