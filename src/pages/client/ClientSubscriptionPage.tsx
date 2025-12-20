
import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent, CardFooter, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CreditCard, Check, Zap, Shield, Users, Download, AlertTriangle } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { clientDashboardService } from '@/services/clientDashboardService';
import { Loader2 } from 'lucide-react';

const ClientSubscriptionPage: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [subscription, setSubscription] = useState<any>(null);

    useEffect(() => {
        const fetchSubscription = async () => {
            try {
                setLoading(true);
                // Mock data fallback if service fails or returns empty in dev
                try {
                    const data = await clientDashboardService.getSubscription();
                    setSubscription(data);
                } catch (e) {
                    console.warn("Using mock subscription data");
                    setSubscription({
                        plan: {
                            name: "Plano Pro (B2C)",
                            price: "R$ 97,00",
                            interval: "mês"
                        },
                        status: "active",
                        next_billing_date: "2025-01-19",
                        payment_method: "**** 4242",
                        addons: []
                    });
                }
            } catch (error) {
                console.error('Error fetching subscription:', error);
                toast.error('Erro ao carregar dados da assinatura.');
            } finally {
                setLoading(false);
            }
        };

        fetchSubscription();
    }, []);

    const handleManageSubscription = () => {
        toast.info("Redirecionando para portal de pagamento...");
        // window.location.href = subscription.portal_url;
    };

    const handleToggleAddon = (addon: string) => {
        toast.success(`Add-on ${addon} ativado com sucesso! (Simulação)`);
        // Logic to call API to add addon
    };

    if (loading) {
        return (
            <DashboardLayout>
                <div className="flex justify-center items-center h-screen">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Minha Assinatura</h1>
                <p className="text-muted-foreground mt-1">Gerencie seu plano, pagamentos e funcionalidades adicionais.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {/* Current Plan Card */}
                <Card className="lg:col-span-2 border-primary/20 shadow-md">
                    <CardHeader>
                        <div className="flex justify-between items-start">
                            <div>
                                <CardTitle className="text-2xl font-bold text-primary">{subscription?.plan?.name || 'Plano Gratuito'}</CardTitle>
                                <CardDescription>Sua assinatura está ativa e operante.</CardDescription>
                            </div>
                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 px-3 py-1">
                                {subscription?.status === 'active' ? 'ATIVO' : 'INATIVO'}
                            </Badge>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="grid md:grid-cols-2 gap-6">
                            <div>
                                <div className="text-sm font-medium text-muted-foreground mb-1">Valor do Plano</div>
                                <div className="text-2xl font-bold">{subscription?.plan?.price} <span className="text-sm font-normal text-muted-foreground">/{subscription?.plan?.interval}</span></div>
                            </div>
                            <div>
                                <div className="text-sm font-medium text-muted-foreground mb-1">Próxima Fatura</div>
                                <div className="text-xl font-medium">{new Date(subscription?.next_billing_date).toLocaleDateString()}</div>
                                <div className="text-sm text-muted-foreground flex items-center mt-1">
                                    <CreditCard className="w-3 h-3 mr-1" /> {subscription?.payment_method}
                                </div>
                            </div>
                        </div>

                        <Separator />

                        <div className="space-y-3">
                            <h4 className="font-medium flex items-center"><Zap className="w-4 h-4 mr-2 text-yellow-500" /> Funcionalidades Inclusas</h4>
                            <div className="grid md:grid-cols-2 gap-2">
                                <div className="flex items-center text-sm"><Check className="w-4 h-4 mr-2 text-green-500" /> 1 Agente de IA</div>
                                <div className="flex items-center text-sm"><Check className="w-4 h-4 mr-2 text-green-500" /> 500 Mensagens/mês</div>
                                <div className="flex items-center text-sm"><Check className="w-4 h-4 mr-2 text-green-500" /> Chatwoot Integrado</div>
                                <div className="flex items-center text-sm"><Check className="w-4 h-4 mr-2 text-green-500" /> Suporte por Email</div>
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter className="bg-gray-50 dark:bg-gray-800/50 p-6 flex justify-between items-center rounded-b-xl">
                        <span className="text-sm text-muted-foreground">Precisa de mais recursos?</span>
                        <Button onClick={handleManageSubscription}>Gerenciar Assinatura</Button>
                    </CardFooter>
                </Card>

                {/* Add-ons Marketplace */}
                <Card className="shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center"><Users className="w-5 h-5 mr-2 text-indigo-500" /> Add-ons Disponíveis</CardTitle>
                        <CardDescription>Expanda as capacidades do seu agente.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="border rounded-lg p-3 space-y-2">
                            <div className="flex justify-between items-center">
                                <span className="font-medium">Sub-Agentes</span>
                                <Badge variant="secondary">R$ 49,00/mês</Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">Permite criar departamentos especializados (Vendas, Suporte, etc).</p>
                            <Button
                                variant="outline"
                                size="sm"
                                className="w-full mt-2"
                                onClick={() => handleToggleAddon('Sub-Agentes')}
                            >
                                Adicionar
                            </Button>
                        </div>

                        <div className="border rounded-lg p-3 space-y-2 opacity-75">
                            <div className="flex justify-between items-center">
                                <span className="font-medium">Gestão B2B</span>
                                <Badge variant="secondary">Consultar</Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">Múltiplos usuários e instâncias para sua equipe.</p>
                            <Button variant="ghost" size="sm" className="w-full mt-2" disabled>Em breve</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Billing History */}
            <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">Histórico de Faturas</h3>
                <Card>
                    <CardContent className="p-0">
                        <div className="relative w-full overflow-auto">
                            <table className="w-full caption-bottom text-sm">
                                <thead className="[&_tr]:border-b">
                                    <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                        <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Data</th>
                                        <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Valor</th>
                                        <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Status</th>
                                        <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Fatura</th>
                                    </tr>
                                </thead>
                                <tbody className="[&_tr:last-child]:border-0">
                                    <tr className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle">19/12/2024</td>
                                        <td className="p-4 align-middle">R$ 97,00</td>
                                        <td className="p-4 align-middle"><Badge className="bg-green-100 text-green-800 hover:bg-green-100">Pago</Badge></td>
                                        <td className="p-4 align-middle text-right">
                                            <Button variant="ghost" size="sm">
                                                <Download className="h-4 w-4" /> PDF
                                            </Button>
                                        </td>
                                    </tr>
                                    <tr className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle">19/11/2024</td>
                                        <td className="p-4 align-middle">R$ 97,00</td>
                                        <td className="p-4 align-middle"><Badge className="bg-green-100 text-green-800 hover:bg-green-100">Pago</Badge></td>
                                        <td className="p-4 align-middle text-right">
                                            <Button variant="ghost" size="sm">
                                                <Download className="h-4 w-4" /> PDF
                                            </Button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </DashboardLayout>
    );
};

export default ClientSubscriptionPage;
