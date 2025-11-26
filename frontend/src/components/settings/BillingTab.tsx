import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { DollarSign, CreditCard, FileText, Zap, ArrowUpCircle, Download } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';

const MOCK_PLAN = {
    name: 'Plano Enterprise AI',
    price: 'R$ 999/mês',
    features: ['Agente Renus Ilimitado', '5 Usuários Admin', 'Relatórios Customizados'],
    usage: {
        conversations: 1500,
        limit: 5000,
    }
};

const MOCK_INVOICES = [
    { id: 101, date: '2024-10-01', amount: 999.00, status: 'Pago' },
    { id: 100, date: '2024-09-01', amount: 999.00, status: 'Pago' },
    { id: 99, date: '2024-08-01', amount: 999.00, status: 'Pago' },
];

const BillingTab: React.FC = () => {
    return (
        <div className="space-y-6">
            <Card className="border-l-4 border-[#4e4ea8]">
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Zap className="h-5 w-5 mr-2" /> Plano Atual</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <h3 className="text-2xl font-bold">{MOCK_PLAN.name}</h3>
                    <p className="text-xl font-semibold text-[#FF6B35]">{MOCK_PLAN.price}</p>
                    
                    <div className="space-y-2">
                        <h4 className="font-semibold">Uso Mensal (Conversas)</h4>
                        <div className="flex justify-between text-sm">
                            <span>{MOCK_PLAN.usage.conversations} de {MOCK_PLAN.usage.limit}</span>
                            <span className="text-muted-foreground">{(MOCK_PLAN.usage.conversations / MOCK_PLAN.usage.limit * 100).toFixed(0)}% Usado</span>
                        </div>
                        <div className="h-2 w-full bg-gray-200 rounded-full">
                            <div 
                                className="h-2 bg-[#0ca7d2] rounded-full" 
                                style={{ width: `${(MOCK_PLAN.usage.conversations / MOCK_PLAN.usage.limit * 100)}%` }}
                            ></div>
                        </div>
                    </div>

                    <Button className="bg-[#FF6B35] hover:bg-[#e55f30]"><ArrowUpCircle className="h-4 w-4 mr-2" /> Gerenciar Assinatura</Button>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><CreditCard className="h-5 w-5 mr-2" /> Método de Pagamento</CardTitle></CardHeader>
                <CardContent className="space-y-2">
                    <p className="text-lg font-medium">Visa **** 4242 (Exp 12/26)</p>
                    <Button variant="outline">Atualizar Cartão</Button>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><FileText className="h-5 w-5 mr-2" /> Histórico de Faturas</CardTitle></CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>ID</TableHead>
                                <TableHead>Data</TableHead>
                                <TableHead>Valor</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Ações</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {MOCK_INVOICES.map(invoice => (
                                <TableRow key={invoice.id}>
                                    <TableCell>{invoice.id}</TableCell>
                                    <TableCell>{invoice.date}</TableCell>
                                    <TableCell>{invoice.amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</TableCell>
                                    <TableCell><Badge className="bg-green-500 text-white">{invoice.status}</Badge></TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm" onClick={() => toast.info(`Baixando fatura ${invoice.id}`)}><Download className="h-4 w-4" /></Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
};

export default BillingTab;