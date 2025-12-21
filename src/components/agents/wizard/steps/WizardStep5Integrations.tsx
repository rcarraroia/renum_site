import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { useWizard } from '../WizardContext';
import { MessageSquare, Globe, Mail, Phone, Calendar } from 'lucide-react';

export const WizardStep5Integrations: React.FC = () => {
    const { data, setData } = useWizard();

    const integrationTypes = [
        { id: 'web', label: 'Chat Web / Widget', icon: Globe, color: 'text-blue-500' },
        { id: 'whatsapp', label: 'WhatsApp Business', icon: MessageSquare, color: 'text-green-500' },
        { id: 'email', label: 'E-mail Automation', icon: Mail, color: 'text-purple-500' },
        { id: 'phone', label: 'Voz / Telefonia', icon: Phone, color: 'text-orange-500' },
        { id: 'calendar', label: 'Agendamento / Calendário', icon: Calendar, color: 'text-red-500' },
    ];

    const toggleIntegration = (id: string) => {
        const current = data.integrations || [];
        if (current.includes(id)) {
            setData({ integrations: current.filter(i => i !== id) });
        } else {
            setData({ integrations: [...current, id] });
        }
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Canais e Integrações</CardTitle>
                    <CardDescription>
                        Selecione onde o seu agente estará presente. Você poderá configurar os detalhes técnicos depois.
                    </CardDescription>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {integrationTypes.map((it) => (
                        <div
                            key={it.id}
                            onClick={() => toggleIntegration(it.id)}
                            className={`flex items-center p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md ${data.integrations.includes(it.id)
                                    ? 'border-primary bg-primary/5 ring-1 ring-primary'
                                    : 'border-border grayscale opacity-70 hover:grayscale-0 hover:opacity-100'
                                }`}
                        >
                            <div className={`p-3 rounded-full bg-background mr-4 ${it.color}`}>
                                <it.icon className="h-6 w-6" />
                            </div>
                            <div className="flex-1">
                                <div className="font-semibold">{it.label}</div>
                                <div className="text-xs text-muted-foreground">
                                    {data.integrations.includes(it.id) ? 'Selecionado' : 'Clique para adicionar'}
                                </div>
                            </div>
                            {data.integrations.includes(it.id) && (
                                <Badge variant="default" className="ml-2">Ativo</Badge>
                            )}
                        </div>
                    ))}
                </CardContent>
            </Card>
        </div>
    );
};
