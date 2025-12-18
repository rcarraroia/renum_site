import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Cpu, Globe, MessageSquare, Zap } from 'lucide-react';

interface Step3TechnicalProps {
    formData: any;
    setFormData: (data: any) => void;
}

const Step3Technical: React.FC<Step3TechnicalProps> = ({ formData, setFormData }) => {
    const channels = [
        { id: 'web', label: 'Web Widget', icon: Globe },
        { id: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
        { id: 'telegram', label: 'Telegram', icon: Zap },
    ];

    const models = [
        { id: 'gpt-4o-mini', label: 'GPT-4o Mini (Recomendado)', description: 'Rápido e econômico' },
        { id: 'gpt-4o', label: 'GPT-4o', description: 'Máxima inteligência' },
        { id: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet', description: 'Excelente em raciocínio' },
    ];

    const toggleChannel = (channelId: string) => {
        const currentChannels = formData.channels || ['web'];
        const newChannels = currentChannels.includes(channelId)
            ? currentChannels.filter((c: string) => c !== channelId)
            : [...currentChannels, channelId];

        // Web deve ser o padrão se nenhum outro estiver selecionado
        if (newChannels.length === 0) newChannels.push('web');

        setFormData({ ...formData, channels: newChannels });
    };

    const handleModelChange = (value: string) => {
        setFormData({ ...formData, model: value });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]">
                        <Globe className="h-5 w-5 mr-2" /> Canais de Atendimento
                    </CardTitle>
                    <CardDescription>
                        Onde seu agente estará disponível para conversar?
                    </CardDescription>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {channels.map((channel) => (
                        <div
                            key={channel.id}
                            onClick={() => toggleChannel(channel.id)}
                            className={`p-4 border rounded-lg cursor-pointer transition-all flex flex-col items-center text-center space-y-2 ${(formData.channels || ['web']).includes(channel.id)
                                    ? 'border-2 border-[#4e4ea8] bg-blue-50/30'
                                    : 'hover:bg-gray-50'
                                }`}
                        >
                            <channel.icon className={`h-8 w-8 ${(formData.channels || ['web']).includes(channel.id) ? 'text-[#4e4ea8]' : 'text-gray-400'
                                }`} />
                            <span className="font-medium">{channel.label}</span>
                            <Checkbox
                                checked={(formData.channels || ['web']).includes(channel.id)}
                                className="pointer-events-none"
                            />
                        </div>
                    ))}
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#FF6B35]">
                        <Cpu className="h-5 w-5 mr-2" /> Modelo de Inteligência
                    </CardTitle>
                    <CardDescription>
                        Selecione o "cérebro" do seu agente.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="model">Modelo de IA:</Label>
                        <Select value={formData.model || 'gpt-4o-mini'} onValueChange={handleModelChange}>
                            <SelectTrigger>
                                <SelectValue placeholder="Selecione o modelo" />
                            </SelectTrigger>
                            <SelectContent>
                                {models.map(m => (
                                    <SelectItem key={m.id} value={m.id}>
                                        <div className="flex flex-col items-start py-1">
                                            <span className="font-medium">{m.label}</span>
                                            <span className="text-xs text-muted-foreground">{m.description}</span>
                                        </div>
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="p-4 bg-orange-50/50 border border-orange-100 rounded-lg">
                        <p className="text-sm text-orange-800">
                            <strong>Nota:</strong> Modelos mais avançados podem ter um custo de processamento (tokens) maior por mensagem.
                        </p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default Step3Technical;
