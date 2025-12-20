import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';
import StripeCheckout from '@/components/payment/StripeCheckout';
import AsaasCheckout from '@/components/payment/AsaasCheckout';
import { paymentService, Plan } from '@/services/paymentService';
import { marketplaceService } from '@/services/marketplaceService';

// Inicializar Stripe (substitua pela sua chave pública)
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_...');

const CheckoutPage: React.FC = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const { toast } = useToast();

    const templateId = searchParams.get('template');
    const planKey = searchParams.get('plan');

    const [template, setTemplate] = useState<any>(null);
    const [plan, setPlan] = useState<Plan | null>(null);
    const [gateway, setGateway] = useState<'asaas' | 'stripe'>('asaas');
    const [clientSecret, setClientSecret] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        if (!templateId || !planKey) {
            toast({
                title: "Erro",
                description: "Template ou plano não especificado",
                variant: "destructive"
            });
            navigate('/marketplace');
            return;
        }

        loadCheckoutData();
    }, [templateId, planKey]);

    const loadCheckoutData = async () => {
        try {
            const [templateData, plansData] = await Promise.all([
                marketplaceService.getTemplate(templateId!),
                paymentService.listPlans()
            ]);

            setTemplate(templateData);
            const selectedPlan = plansData.find(p => p.key === planKey);
            setPlan(selectedPlan || null);

            // Detectar gateway baseado no país (simplificado)
            // Em produção, isso viria do backend
            const userCountry = 'Brasil'; // TODO: Detectar país do usuário
            setGateway(userCountry === 'Brasil' ? 'asaas' : 'stripe');

        } catch (error) {
            console.error('Error loading checkout data:', error);
            toast({
                title: "Erro",
                description: "Falha ao carregar dados do checkout",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    const handlePaymentSuccess = async (data?: any) => {
        setSuccess(true);

        toast({
            title: "Pagamento confirmado!",
            description: "Seu agente está sendo configurado...",
        });

        // Aguardar 2 segundos e redirecionar
        setTimeout(() => {
            navigate('/dashboard/agents');
        }, 2000);
    };

    const handlePaymentError = (error: string) => {
        toast({
            title: "Erro no pagamento",
            description: error,
            variant: "destructive"
        });
    };

    if (loading) {
        return (
            <DashboardLayout>
                <div className="flex justify-center items-center h-screen">
                    <p className="text-muted-foreground">Carregando checkout...</p>
                </div>
            </DashboardLayout>
        );
    }

    if (success) {
        return (
            <DashboardLayout>
                <div className="flex flex-col items-center justify-center h-screen">
                    <CheckCircle className="h-16 w-16 text-green-500 mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Pagamento Confirmado!</h2>
                    <p className="text-muted-foreground">Redirecionando...</p>
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="max-w-4xl mx-auto p-6">
                <Button
                    variant="ghost"
                    onClick={() => navigate('/marketplace')}
                    className="mb-6"
                >
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Voltar ao Marketplace
                </Button>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Resumo do Pedido */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Resumo do Pedido</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <p className="text-sm text-muted-foreground">Template</p>
                                <p className="font-semibold">{template?.name}</p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">Plano</p>
                                <p className="font-semibold">{plan?.name}</p>
                            </div>

                            <Separator />

                            <div>
                                <p className="text-sm text-muted-foreground mb-2">Recursos inclusos:</p>
                                <ul className="space-y-1">
                                    {plan?.features.map((feature, idx) => (
                                        <li key={idx} className="text-sm flex items-start">
                                            <CheckCircle className="h-4 w-4 mr-2 text-green-500 flex-shrink-0 mt-0.5" />
                                            {feature}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <Separator />

                            <div className="flex justify-between items-center">
                                <span className="font-semibold">Total</span>
                                <span className="text-2xl font-bold">
                                    R$ {(plan?.price_brl || 0).toFixed(2)}
                                    <span className="text-sm font-normal text-muted-foreground">/mês</span>
                                </span>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Formulário de Pagamento */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Pagamento</CardTitle>
                        </CardHeader>
                        <CardContent>
                            {gateway === 'stripe' && clientSecret ? (
                                <Elements stripe={stripePromise}>
                                    <StripeCheckout
                                        clientSecret={clientSecret}
                                        onSuccess={handlePaymentSuccess}
                                        onError={handlePaymentError}
                                    />
                                </Elements>
                            ) : (
                                <AsaasCheckout
                                    templateId={templateId!}
                                    planKey={planKey!}
                                    onSuccess={handlePaymentSuccess}
                                    onError={handlePaymentError}
                                />
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </DashboardLayout>
    );
};

export default CheckoutPage;
