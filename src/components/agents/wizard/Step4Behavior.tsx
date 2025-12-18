import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Slider } from '@/components/ui/slider';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Headphones, ShoppingCart, Briefcase, Users, Sparkles, MessageSquare, Brain } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Step4BehaviorProps {
    formData: any;
    setFormData: (data: any) => void;
}

const templates = [
    { type: 'customer_service', name: 'Atendimento', icon: Headphones, color: 'bg-blue-500' },
    { type: 'sales', name: 'Vendas', icon: ShoppingCart, color: 'bg-green-500' },
    { type: 'support', name: 'Suporte', icon: Briefcase, color: 'bg-purple-500' },
    { type: 'recruitment', name: 'Recrutamento', icon: Users, color: 'bg-orange-500' },
    { type: 'custom', name: 'Personalizado', icon: Sparkles, color: 'bg-pink-500' },
];

const personalities = [
    { id: 'professional', label: 'Profissional', description: 'Sério e direto ao ponto.' },
    { id: 'friendly', label: 'Amigável', description: 'Acolhedor e empático.' },
    { id: 'technical', label: 'Técnico', description: 'Focado em detalhes e precisão.' },
    { id: 'casual', label: 'Casual', description: 'Descontraído e informal.' },
];

const Step4Behavior: React.FC<Step4BehaviorProps> = ({ formData, setFormData }) => {
    const handleTemplateSelect = (templateType: string) => {
        setFormData({ ...formData, template_type: templateType });
    };

    const updateField = (id: string, value: any) => {
        setFormData({ ...formData, [id]: value });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]">
                        <Brain className="h-5 w-5 mr-2" /> Template de Base
                    </CardTitle>
                    <CardDescription>Escolha o comportamento base para o agente.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                        {templates.map((t) => {
                            const isSelected = formData.template_type === t.type;
                            return (
                                <div
                                    key={t.type}
                                    onClick={() => handleTemplateSelect(t.type)}
                                    className={cn(
                                        "p-3 border rounded-xl cursor-pointer transition-all flex flex-col items-center space-y-2 text-center",
                                        isSelected ? "border-2 border-[#4e4ea8] bg-blue-50" : "hover:bg-gray-50"
                                    )}
                                >
                                    <div className={cn("p-2 rounded-lg text-white", t.color)}>
                                        <t.icon className="h-5 w-5" />
                                    </div>
                                    <span className="text-xs font-semibold">{t.name}</span>
                                </div>
                            );
                        })}
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#FF6B35]">
                        <MessageSquare className="h-5 w-5 mr-2" /> Instruções do Agente (System Prompt)
                    </CardTitle>
                    <CardDescription>Defina como o agente deve agir, o que ele sabe e quais as regras.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="system_prompt">Personalidade Predominante</Label>
                        <RadioGroup
                            value={formData.personality || 'professional'}
                            onValueChange={(v) => updateField('personality', v)}
                            className="grid grid-cols-2 gap-3"
                        >
                            {personalities.map(p => (
                                <div key={p.id} className="flex items-center space-x-2 border p-2 rounded-md">
                                    <RadioGroupItem value={p.id} id={p.id} />
                                    <div className="leading-tight">
                                        <Label htmlFor={p.id} className="text-sm font-medium">{p.label}</Label>
                                        <p className="text-[10px] text-muted-foreground">{p.description}</p>
                                    </div>
                                </div>
                            ))}
                        </RadioGroup>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="system_prompt">Prompt Principal *</Label>
                        <Textarea
                            id="system_prompt"
                            placeholder="Ex: Você é um assistente de vendas da Renum. Seu objetivo é captar o nome e zap do cliente..."
                            value={formData.system_prompt || ''}
                            onChange={(e) => updateField('system_prompt', e.target.value)}
                            rows={6}
                            className="font-mono text-sm leading-relaxed"
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <Label>Nível de Formalidade</Label>
                                <span className="text-xs font-mono">{formData.tone_formal || 50}%</span>
                            </div>
                            <Slider
                                value={[formData.tone_formal || 50]}
                                max={100} step={1}
                                onValueChange={([v]) => updateField('tone_formal', v)}
                            />
                        </div>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <Label>Nível de Objetividade</Label>
                                <span className="text-xs font-mono">{formData.tone_direct || 50}%</span>
                            </div>
                            <Slider
                                value={[formData.tone_direct || 50]}
                                max={100} step={1}
                                onValueChange={([v]) => updateField('tone_direct', v)}
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default Step4Behavior;
