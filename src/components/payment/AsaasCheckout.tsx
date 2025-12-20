import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, CreditCard, QrCode } from 'lucide-react';
import { paymentService } from '@/services/paymentService';

interface AsaasCheckoutProps {
    templateId: string;
    planKey: string;
    onSuccess: (data: any) => void;
    onError: (error: string) => void;
}

const AsaasCheckout: React.FC<AsaasCheckoutProps> = ({ templateId, planKey, onSuccess, onError }) => {
    const [paymentMethod, setPaymentMethod] = useState<'credit_card' | 'pix'>('credit_card');
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [pixQrCode, setPixQrCode] = useState<string | null>(null);

    // Dados do cartão
    const [cardData, setCardData] = useState({
        holderName: '',
        number: '',
        expiryMonth: '',
        expiryYear: '',
        ccv: ''
    });

    const handleCreditCardPayment = async (e: React.FormEvent) => {
        e.preventDefault();
        setProcessing(true);
        setError(null);

        try {
            // Criar assinatura com cartão de crédito
            const result = await paymentService.createSubscription({
                plan_key: planKey,
                template_id: templateId,
                payment_method: 'credit_card'
            });

            if (result.gateway === 'asaas') {
                // Asaas retorna URL de pagamento
                if (result.payment_url) {
                    window.location.href = result.payment_url;
                } else {
                    onSuccess(result);
                }
            }
        } catch (err: any) {
            setError(err.message || 'Erro ao processar pagamento');
            onError(err.message || 'Erro ao processar pagamento');
        } finally {
            setProcessing(false);
        }
    };

    const handlePixPayment = async () => {
        setProcessing(true);
        setError(null);

        try {
            const result = await paymentService.createSubscription({
                plan_key: planKey,
                template_id: templateId,
                payment_method: 'pix'
            });

            if (result.payment_url) {
                // Asaas retorna QR Code para PIX
                setPixQrCode(result.payment_url);
            } else {
                onSuccess(result);
            }
        } catch (err: any) {
            setError(err.message || 'Erro ao gerar PIX');
            onError(err.message || 'Erro ao gerar PIX');
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="space-y-4">
            <Tabs value={paymentMethod} onValueChange={(value) => setPaymentMethod(value as 'credit_card' | 'pix')}>
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="credit_card">
                        <CreditCard className="h-4 w-4 mr-2" />
                        Cartão de Crédito
                    </TabsTrigger>
                    <TabsTrigger value="pix">
                        <QrCode className="h-4 w-4 mr-2" />
                        PIX
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="credit_card">
                    <form onSubmit={handleCreditCardPayment} className="space-y-4">
                        <div>
                            <Label htmlFor="holderName">Nome no Cartão</Label>
                            <Input
                                id="holderName"
                                placeholder="João Silva"
                                value={cardData.holderName}
                                onChange={(e) => setCardData({ ...cardData, holderName: e.target.value })}
                                required
                            />
                        </div>

                        <div>
                            <Label htmlFor="cardNumber">Número do Cartão</Label>
                            <Input
                                id="cardNumber"
                                placeholder="1234 5678 9012 3456"
                                value={cardData.number}
                                onChange={(e) => setCardData({ ...cardData, number: e.target.value.replace(/\s/g, '') })}
                                maxLength={16}
                                required
                            />
                        </div>

                        <div className="grid grid-cols-3 gap-4">
                            <div>
                                <Label htmlFor="expiryMonth">Mês</Label>
                                <Input
                                    id="expiryMonth"
                                    placeholder="MM"
                                    value={cardData.expiryMonth}
                                    onChange={(e) => setCardData({ ...cardData, expiryMonth: e.target.value })}
                                    maxLength={2}
                                    required
                                />
                            </div>
                            <div>
                                <Label htmlFor="expiryYear">Ano</Label>
                                <Input
                                    id="expiryYear"
                                    placeholder="AAAA"
                                    value={cardData.expiryYear}
                                    onChange={(e) => setCardData({ ...cardData, expiryYear: e.target.value })}
                                    maxLength={4}
                                    required
                                />
                            </div>
                            <div>
                                <Label htmlFor="ccv">CVV</Label>
                                <Input
                                    id="ccv"
                                    placeholder="123"
                                    value={cardData.ccv}
                                    onChange={(e) => setCardData({ ...cardData, ccv: e.target.value })}
                                    maxLength={4}
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <Alert variant="destructive">
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}

                        <Button type="submit" disabled={processing} className="w-full">
                            {processing ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Processando...
                                </>
                            ) : (
                                'Confirmar Pagamento'
                            )}
                        </Button>
                    </form>
                </TabsContent>

                <TabsContent value="pix">
                    <div className="space-y-4">
                        {!pixQrCode ? (
                            <div className="text-center py-8">
                                <QrCode className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                                <p className="text-sm text-muted-foreground mb-4">
                                    Clique no botão abaixo para gerar o código PIX
                                </p>
                                <Button onClick={handlePixPayment} disabled={processing}>
                                    {processing ? (
                                        <>
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                            Gerando PIX...
                                        </>
                                    ) : (
                                        'Gerar Código PIX'
                                    )}
                                </Button>
                            </div>
                        ) : (
                            <div className="text-center py-4">
                                <div className="bg-white p-4 rounded-lg inline-block mb-4">
                                    <img src={pixQrCode} alt="QR Code PIX" className="w-64 h-64" />
                                </div>
                                <p className="text-sm text-muted-foreground">
                                    Escaneie o QR Code com o app do seu banco
                                </p>
                                <p className="text-xs text-muted-foreground mt-2">
                                    O pagamento será confirmado automaticamente
                                </p>
                            </div>
                        )}

                        {error && (
                            <Alert variant="destructive">
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default AsaasCheckout;
