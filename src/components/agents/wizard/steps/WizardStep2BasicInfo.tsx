import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useWizard } from '../WizardContext';

export const WizardStep2BasicInfo: React.FC = () => {
    const { data, setData } = useWizard();

    const niches = [
        { value: 'generico', label: 'Genérico/Multiuso' },
        { value: 'imobiliario', label: 'Imobiliário' },
        { value: 'juridico', label: 'Jurídico/Advocacia' },
        { value: 'saude', label: 'Saúde/Clínicas' },
        { value: 'e-commerce', label: 'E-commerce/Vendas' },
        { value: 'educacao', label: 'Educação/Cursos' },
        { value: 'rh', label: 'RH/Recrutamento' },
    ];

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Identidade do Agente</CardTitle>
                    <CardDescription>
                        Dê um nome e uma descrição clara para o seu agente de IA.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="name">Nome do Agente <span className="text-destructive">*</span></Label>
                        <Input
                            id="name"
                            placeholder="Ex: Assistente de Vendas Solar"
                            value={data.name}
                            onChange={(e) => setData({ name: e.target.value })}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="description">Descrição</Label>
                        <Textarea
                            id="description"
                            placeholder="Descreva brevemente o que este agente faz..."
                            value={data.description}
                            onChange={(e) => setData({ description: e.target.value })}
                            className="min-h-[100px]"
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="niche">Nicho de Atuação</Label>
                        <Select
                            value={data.niche}
                            onValueChange={(val) => setData({ niche: val })}
                        >
                            <SelectTrigger id="niche">
                                <SelectValue placeholder="Selecione um nicho..." />
                            </SelectTrigger>
                            <SelectContent>
                                {niches.map((niche) => (
                                    <SelectItem key={niche.value} value={niche.value}>
                                        {niche.label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
