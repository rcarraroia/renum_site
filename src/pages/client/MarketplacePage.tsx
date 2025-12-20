import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingCart, Star, Check, Filter } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { marketplaceService } from '@/services/marketplaceService';
import { paymentService, Plan } from '@/services/paymentService';

interface Template {
    id: string;
    name: string;
    description: string;
    category: 'b2b' | 'b2c';
    niche: string;
    available_tools: Record<string, any>;
    available_integrations: Record<string, any>;
}

const MarketplacePage: React.FC = () => {
    const navigate = useNavigate();
    const { toast } = useToast();
    const [templates, setTemplates] = useState<Template[]>([]);
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState(true);
    const [nicheFilter, setNicheFilter] = useState<string>('all');

    useEffect(() => {
        loadMarketplace();
    }, [nicheFilter]);

    const loadMarketplace = async () => {
        try {
            const [templatesData, plansData] = await Promise.all([
                marketplaceService.listMarketplaceTemplates(
                    nicheFilter !== 'all' ? { niche: nicheFilter } : {}
                ),
                paymentService.listPlans()
            ]);

            setTemplates(templatesData);
            setPlans(plansData);
        } catch (error) {
            console.error('Error loading marketplace:', error);
            toast({
                title: "Erro",
                description: "Falha ao carregar marketplace",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    const handleSubscribe = (templateId: string, planKey: string) => {
        navigate(`/checkout?template=${templateId}&plan=${planKey}`);
    };

    const getDefaultPlan = (category: 'b2b' | 'b2c'): Plan | undefined => {
        return plans.find(p => p.category === category && p.key.includes('pro'));
    };

    return (
        <DashboardLayout>
            <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-3xl font-bold">Marketplace de Agentes</h1>
                        <p className="text-muted-foreground">
                            Escolha um template e comece a usar seu agente em minutos
                        </p>
                    </div>

                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4 text-muted-foreground" />
                        <Select value={nicheFilter} onValueChange={setNicheFilter}>
                            <SelectTrigger className="w-[200px]">
                                <SelectValue placeholder="Filtrar por nicho" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">Todos os nichos</SelectItem>
                                <SelectItem value="Vendas">Vendas</SelectItem>
                                <SelectItem value="Suporte">Suporte</SelectItem>
                                <SelectItem value="Imobiliário">Imobiliário</SelectItem>
                                <SelectItem value="Saúde">Saúde</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <p className="text-muted-foreground">Carregando templates...</p>
                    </div>
                ) : templates.length === 0 ? (
                    <Card>
                        <CardContent className="flex flex-col items-center justify-center h-64">
                            <p className="text-muted-foreground mb-4">Nenhum template disponível</p>
                        </CardContent>
                    </Card>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {templates.map((template) => {
                            const defaultPlan = getDefaultPlan(template.category);
                            const price = defaultPlan?.price_brl || 0;

                            return (
                                <Card key={template.id} className="hover:shadow-lg transition-shadow flex flex-col">
                                    <CardHeader>
                                        <div className="flex justify-between items-start">
                                            <CardTitle className="text-lg">{template.name}</CardTitle>
                                            <Badge variant={template.category === 'b2b' ? 'default' : 'secondary'}>
                                                {template.category.toUpperCase()}
                                            </Badge>
                                        </div>
                                    </CardHeader>

                                    <CardContent className="flex-1">
                                        <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                                            {template.description || 'Template profissional para seu negócio'}
                                        </p>

                                        <div className="mb-4">
                                            <Badge variant="outline" className="mb-2">{template.niche}</Badge>
                                            <div className="flex items-center gap-1 text-yellow-400">
                                                <Star className="h-4 w-4 fill-current" />
                                                <Star className="h-4 w-4 fill-current" />
                                                <Star className="h-4 w-4 fill-current" />
                                                <Star className="h-4 w-4 fill-current" />
                                                <Star className="h-4 w-4 fill-current" />
                                                <span className="text-sm text-muted-foreground ml-1">(4.9)</span>
                                            </div>
                                        </div>

                                        <div className="mb-4">
                                            <p className="text-sm font-medium mb-2">Recursos inclusos:</p>
                                            <ul className="space-y-1">
                                                {defaultPlan?.features.slice(0, 3).map((feature, idx) => (
                                                    <li key={idx} className="flex items-center text-sm">
                                                        <Check className="h-4 w-4 mr-2 text-green-500" />
                                                        {feature}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>

                                        <div className="mt-auto">
                                            <p className="text-2xl font-bold">
                                                R$ {price.toFixed(2)}
                                                <span className="text-sm font-normal text-muted-foreground">/mês</span>
                                            </p>
                                        </div>
                                    </CardContent>

                                    <CardFooter>
                                        <Button
                                            className="w-full"
                                            onClick={() => handleSubscribe(template.id, defaultPlan?.key || 'b2c_pro')}
                                        >
                                            <ShoppingCart className="h-4 w-4 mr-2" />
                                            Assinar Agora
                                        </Button>
                                    </CardFooter>
                                </Card>
                            );
                        })}
                    </div>
                )}
            </div>
        </DashboardLayout>
    );
};

export default MarketplacePage;
