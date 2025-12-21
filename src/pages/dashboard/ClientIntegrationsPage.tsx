import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import IntegrationsTab from '@/components/agents/config/IntegrationsTab';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MessageSquarePlus, RefreshCw, Send } from 'lucide-react';
import { toast } from 'sonner';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const ClientIntegrationsPage: React.FC = () => {
    const [isSolicitacaoOpen, setIsSolicitacaoOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSendSolicitacao = () => {
        setLoading(true);
        // Simulação de envio para o backend
        setTimeout(() => {
            setLoading(false);
            setIsSolicitacaoOpen(false);
            toast.success("Solicitação enviada com sucesso! Nossa equipe analisará o seu pedido.");
        }, 1500);
    };

    return (
        <DashboardLayout>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                <div>
                    <h2 className="text-3xl font-bold flex items-center">
                        <RefreshCw className="h-7 w-7 mr-3 text-[#FF6B35]" />
                        Minhas Integrações
                    </h2>
                    <p className="text-muted-foreground mt-1">Gerencie as conexões ativas do seu projeto.</p>
                </div>

                <Dialog open={isSolicitacaoOpen} onOpenChange={setIsSolicitacaoOpen}>
                    <DialogTrigger asChild>
                        <Button className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                            <MessageSquarePlus className="h-4 w-4 mr-2" />
                            Sugerir Nova Integração
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Sugerir Integração ou Ferramenta</DialogTitle>
                            <DialogDescription>
                                Sentiu falta de alguma conexão? Conte para nós o que você precisa e nossa equipe priorizará no roadmap.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="name">Nome da Ferramenta</Label>
                                <Input id="name" placeholder="Ex: RD Station, Salesforce, Slack..." />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="reason">Como isso ajudaria seu negócio?</Label>
                                <Textarea id="reason" placeholder="Descreva brevemente como você pretende usar essa integração..." />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setIsSolicitacaoOpen(false)}>Cancelar</Button>
                            <Button onClick={handleSendSolicitacao} disabled={loading}>
                                {loading ? "Enviando..." : "Enviar Sugestão"}
                                {!loading && <Send className="ml-2 h-4 w-4" />}
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            <Card className="mb-6 bg-blue-50 border-blue-100 dark:bg-blue-900/10 dark:border-blue-900/30">
                <CardContent className="p-4 flex items-center space-x-4">
                    <div className="bg-blue-100 p-2 rounded-full dark:bg-blue-800">
                        <RefreshCw className="h-5 w-5 text-blue-600 dark:text-blue-300" />
                    </div>
                    <div>
                        <p className="text-sm font-medium text-blue-800 dark:text-blue-200">
                            <strong>Dica:</strong> As integrações ativas abaixo podem ser usadas por qualquer agente ou automação que você criar no Wizard.
                        </p>
                    </div>
                </CardContent>
            </Card>

            <IntegrationsTab globalMode={true} />
        </DashboardLayout>
    );
};

export default ClientIntegrationsPage;
