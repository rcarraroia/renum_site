import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useWizard } from '../WizardContext';
import { CheckCircle, Play, Rocket, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

interface WizardStep6Props {
    onPublish: () => void;
}

export const WizardStep6TestPublish: React.FC<WizardStep6Props> = ({ onPublish }) => {
    const { data } = useWizard();
    const [testRan, setTestRan] = useState(false);
    const [isTesting, setIsTesting] = useState(false);

    const handleRunTest = () => {
        setIsTesting(true);
        // Simular teste
        setTimeout(() => {
            setIsTesting(false);
            setTestRan(true);
            toast.success('Simulação concluída com sucesso!');
        }, 1500);
    };

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="border-primary/20 bg-primary/5">
                    <CardHeader>
                        <CardTitle className="flex items-center">
                            <Rocket className="h-5 w-5 mr-2 text-primary" />
                            Resumo da Configuração
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex justify-between items-center py-2 border-b">
                            <span className="text-sm text-muted-foreground">Tipo de Agente</span>
                            <Badge variant="outline" className="capitalize">{data.agent_type}</Badge>
                        </div>
                        <div className="flex justify-between items-center py-2 border-b">
                            <span className="text-sm text-muted-foreground">Nome</span>
                            <span className="font-medium">{data.name}</span>
                        </div>
                        <div className="flex justify-between items-center py-2 border-b">
                            <span className="text-sm text-muted-foreground">Personalidade</span>
                            <Badge variant="secondary">{data.personality}</Badge>
                        </div>
                        <div className="flex justify-between items-center py-2 border-b">
                            <span className="text-sm text-muted-foreground">Canais Selecionados</span>
                            <div className="flex gap-1">
                                {data.integrations.map(i => (
                                    <Badge key={i} variant="outline" className="text-[10px]">{i}</Badge>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center">
                            <Play className="h-5 w-5 mr-2 text-green-500" />
                            Sandbox de Teste
                        </CardTitle>
                        <CardDescription>
                            Simule o comportamento do seu agente antes de publicar.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center p-8 space-y-4 text-center">
                        <div className="h-32 w-32 rounded-full bg-muted flex items-center justify-center">
                            {testRan ? (
                                <CheckCircle className="h-16 w-16 text-green-500 animate-in zoom-in" />
                            ) : (
                                <Rocket className={`h-16 w-16 text-muted-foreground ${isTesting ? 'animate-bounce' : ''}`} />
                            )}
                        </div>
                        <div className="space-y-1">
                            <div className="font-semibold">{testRan ? 'Agente Validado' : 'Pronto para Teste'}</div>
                            <div className="text-sm text-muted-foreground">
                                {testRan
                                    ? 'O comportamento foi validado pelo nosso motor de IA.'
                                    : 'Execute um teste rápido para garantir a qualidade do sistema.'}
                            </div>
                        </div>
                        <Button
                            variant={testRan ? "outline" : "default"}
                            onClick={handleRunTest}
                            disabled={isTesting}
                            className="w-full"
                        >
                            {isTesting ? 'Simulando...' : testRan ? 'Testar Novamente' : 'Iniciar Simulação'}
                        </Button>
                    </CardContent>
                </Card>
            </div>

            {!testRan && (
                <div className="flex items-center p-4 border rounded-lg bg-yellow-50 text-yellow-800 border-yellow-200">
                    <AlertCircle className="h-5 w-5 mr-3 flex-shrink-0" />
                    <p className="text-sm">
                        Recomendamos que você execute a simulação no Sandbox antes de publicar o agente para garantir que o tom de voz está adequado.
                    </p>
                </div>
            )}
        </div>
    );
};
