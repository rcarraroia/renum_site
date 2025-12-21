import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useWizard } from '../WizardContext';

export const WizardStep3Personality: React.FC = () => {
    const { data, setData } = useWizard();

    const personalities = [
        { value: 'professional', label: 'Profissional e Respeitoso' },
        { value: 'friendly', label: 'Amigável e Descontraído' },
        { value: 'technical', label: 'Técnico e Especialista' },
        { value: 'bold', label: 'Persuasivo e Enérgico' },
    ];

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Comportamento e Tom</CardTitle>
                    <CardDescription>
                        Como o seu agente deve se comunicar com os usuários?
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-8">
                    <div className="space-y-4">
                        <Label htmlFor="personality">Perfil de Personalidade</Label>
                        <Select
                            value={data.personality}
                            onValueChange={(val) => setData({ personality: val })}
                        >
                            <SelectTrigger id="personality">
                                <SelectValue placeholder="Selecione um perfil..." />
                            </SelectTrigger>
                            <SelectContent>
                                {personalities.map((p) => (
                                    <SelectItem key={p.value} value={p.value}>
                                        {p.label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="space-y-4">
                        <div className="flex justify-between">
                            <Label>Nível de Formalidade</Label>
                            <span className="text-sm font-medium text-muted-foreground">{data.tone_formal}%</span>
                        </div>
                        <Slider
                            value={[data.tone_formal]}
                            onValueChange={(val) => setData({ tone_formal: val[0] })}
                            max={100}
                            step={1}
                        />
                        <div className="flex justify-between text-xs text-muted-foreground">
                            <span>Informal</span>
                            <span>Muito Formal</span>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="flex justify-between">
                            <Label>Objetividade</Label>
                            <span className="text-sm font-medium text-muted-foreground">{data.tone_direct}%</span>
                        </div>
                        <Slider
                            value={[data.tone_direct]}
                            onValueChange={(val) => setData({ tone_direct: val[0] })}
                            max={100}
                            step={1}
                        />
                        <div className="flex justify-between text-xs text-muted-foreground">
                            <span>Explicativo</span>
                            <span>Direto ao ponto</span>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
