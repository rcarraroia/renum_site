import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { User, CheckCircle, XCircle, MessageSquare, Clock, Edit, Trash2, Plus, Phone, Mail } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface AgentUser {
    id: string;
    name: string;
    email: string;
    whatsappConfigured: boolean;
    status: 'ativo' | 'inativo';
    conversationsToday: number;
    lastAccess: string;
}

const MOCK_USERS: AgentUser[] = [
    { id: 'u1', name: 'João Vendedor', email: 'joao@slim.com', whatsappConfigured: true, status: 'ativo', conversationsToday: 15, lastAccess: '10 min atrás' },
    { id: 'u2', name: 'Maria Gerente', email: 'maria@slim.com', whatsappConfigured: true, status: 'ativo', conversationsToday: 5, lastAccess: '1h atrás' },
    { id: 'u3', name: 'Pedro Teste', email: 'pedro@slim.com', whatsappConfigured: false, status: 'inativo', conversationsToday: 0, lastAccess: '3 dias atrás' },
];

const AgentUsersTab: React.FC<{ agentType: string }> = ({ agentType }) => {
    const [users, setUsers] = useState(MOCK_USERS);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingUser, setEditingUser] = useState<AgentUser | null>(null);

    if (agentType !== 'b2b_empresa') {
        return (
            <Card className="border-l-4 border-[#FF6B35]">
                <CardHeader>
                    <CardTitle className="text-[#FF6B35] flex items-center"><User className="h-5 w-5 mr-2" /> Gerenciamento de Usuários</CardTitle>
                    <CardDescription>Esta funcionalidade é exclusiva para agentes do tipo B2B Corporativo.</CardDescription>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground">O agente atual é do tipo {agentType.toUpperCase()}. Não há necessidade de gerenciar usuários individuais.</p>
                </CardContent>
            </Card>
        );
    }

    const handleToggleStatus = (id: string) => {
        setUsers(prev => prev.map(u => 
            u.id === id ? { ...u, status: u.status === 'ativo' ? 'inativo' : 'ativo' } : u
        ));
        toast.info("Status do usuário atualizado.");
    };

    const handleOpenModal = (user: AgentUser | null = null) => {
        setEditingUser(user);
        setIsModalOpen(true);
    };

    const handleSaveUser = (e: React.FormEvent) => {
        e.preventDefault();
        // Mock save logic
        toast.success(`Usuário ${editingUser ? 'atualizado' : 'adicionado'} com sucesso!`);
        setIsModalOpen(false);
        setEditingUser(null);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="flex items-center text-[#4e4ea8]"><User className="h-5 w-5 mr-2" /> Usuários Cadastrados ({users.length})</CardTitle>
                    <Button onClick={() => handleOpenModal()} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                        <Plus className="h-4 w-4 mr-2" /> Adicionar Usuário
                    </Button>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Nome</TableHead>
                                <TableHead>Email</TableHead>
                                <TableHead>WhatsApp</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Conversas (Hoje)</TableHead>
                                <TableHead>Último Acesso</TableHead>
                                <TableHead className="text-right">Ações</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {users.map(user => (
                                <TableRow key={user.id}>
                                    <TableCell className="font-medium">{user.name}</TableCell>
                                    <TableCell className="text-sm text-muted-foreground">{user.email}</TableCell>
                                    <TableCell>
                                        {user.whatsappConfigured ? <CheckCircle className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                                    </TableCell>
                                    <TableCell>
                                        <Badge className={cn(user.status === 'ativo' ? 'bg-green-500' : 'bg-red-500', 'text-white capitalize')}>
                                            {user.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="font-semibold text-[#0ca7d2]">{user.conversationsToday}</TableCell>
                                    <TableCell className="text-sm text-muted-foreground">{user.lastAccess}</TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Button variant="ghost" size="sm" onClick={() => handleOpenModal(user)}><Edit className="h-4 w-4" /></Button>
                                        <Button 
                                            variant="outline" 
                                            size="sm" 
                                            onClick={() => handleToggleStatus(user.id)}
                                            className={cn(user.status === 'ativo' ? 'text-red-500' : 'text-green-500')}
                                        >
                                            {user.status === 'ativo' ? <Trash2 className="h-4 w-4" /> : <CheckCircle className="h-4 w-4" />}
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            {/* Modal de Adição/Edição */}
            <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                        <DialogTitle>{editingUser ? 'Editar Usuário' : 'Adicionar Novo Usuário'}</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSaveUser} className="grid gap-4 py-4">
                        <div className="space-y-2"><Label htmlFor="name">Nome</Label><Input id="name" defaultValue={editingUser?.name} required /></div>
                        <div className="space-y-2"><Label htmlFor="email">Email</Label><Input id="email" type="email" defaultValue={editingUser?.email} required /></div>
                        <div className="space-y-2"><Label htmlFor="phone">Telefone (WhatsApp)</Label><Input id="phone" defaultValue={'+55 11 9XXXX-XXXX'} /></div>
                        <DialogFooter>
                            <Button type="submit" className="bg-[#4e4ea8] hover:bg-[#3a3a80]">Salvar</Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default AgentUsersTab;