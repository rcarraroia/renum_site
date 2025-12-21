import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { useWizard } from '../WizardContext';

export const WizardStep4DataCollection: React.FC = () => {
    const { data, setData } = useWizard();

    const standardFields = [
        { id: 'name', label: 'Nome Completo' },
        { id: 'email', label: 'E-mail' },
        { id: 'phone', label: 'Telefone/WhatsApp' },
        { id: 'company', label: 'Empresa' },
        { id: 'role', label: 'Cargo/Função' },
    ];

    const toggleField = (fieldId: string) => {
        const currentFields = data.data_fields || [];
        if (currentFields.includes(fieldId)) {
            setData({ data_fields: currentFields.filter(f => f !== fieldId) });
        } else {
            setData({ data_fields: [...currentFields, fieldId] });
        }
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Coleta de Dados e Leads</CardTitle>
                    <CardDescription>
                        Defina quais informações o agente deve coletar durante a conversa.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="flex items-center justify-between p-4 border rounded-lg bg-muted/50">
                        <div className="space-y-0.5">
                            <Label className="text-base">Habilitar Coleta Automática</Label>
                            <div className="text-sm text-muted-foreground">
                                O agente tentará extrair dados naturalmente da conversa.
                            </div>
                        </div>
                        <Switch
                            checked={data.collect_data}
                            onCheckedChange={(checked) => setData({ collect_data: checked })}
                        />
                    </div>

                    {data.collect_data && (
                        <div className="space-y-4 animate-in fade-in slide-in-from-top-2">
                            <Label>Campos Padrão para Extração</Label>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {standardFields.map((field) => (
                                    <div key={field.id} className="flex items-center space-x-2 p-3 border rounded hover:bg-accent cursor-pointer">
                                        <Checkbox
                                            id={field.id}
                                            checked={data.data_fields.includes(field.id)}
                                            onCheckedChange={() => toggleField(field.id)}
                                        />
                                        <Label htmlFor={field.id} className="flex-1 cursor-pointer">
                                            {field.label}
                                        </Label>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};
