import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Zap, Clock, MessageSquare, TrendingUp, Briefcase, Users, Globe, Copy, CheckCircle, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Agent } from '@/types/agent';
import { mockClients, mockProjects } from '@/mocks/agents.mock';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

interface AgentOverviewTabProps {
    agent: Agent;
}

const AgentOverviewTab: React.FC<AgentOverviewTabProps> = ({ agent }) => {
    const client = mockClients.find(c => c.id === agent.client_id);
    const project = mockProjects.find(p => p.id === agent.project_id);

    const mockMetrics = {
        conversationsTotal: 1200,
        uptime: '99.8%',
        avgResponseTime: '1.2s',
        resolutionRate: '85%',
    };

    const getAgentTypeLabel = (type: string) => {
        switch (type) {
            case 'b2b_empresa': return 'B2B Corporativo';
            case 'b2c_marketplace': return 'B2C Marketplace';
            case 'b2c_individual': return 'B2C Individual';
            default: return 'Custom';
        }
    };

    const handleCopy = (text: string, label: string) => {
        navigator.clipboard.writeText(text);
        toast.info(`${label} copiado!`);
    };
    
    const clientDashboardLink = `https://${agent.slug}.renum.com.br`;
    const registrationLink = `https://${agent.slug}.renum.com.br/cadastro?token=abc123xyz`;

    return (
        <div className="space-y-6">
            <div className="grid gap-6 lg:grid-cols-3">
                
                {/* Card 1: Estatísticas Rápidas */}
                <Card className="border-l-4 border-[#4e4ea8]">
                    <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Zap className="h-5 w-5 mr-2" /> Estatísticas Rápidas</CardTitle></CardHeader>
                    <CardContent className="space-y-2 text-sm">
                        <div className="flex justify-between"><span>Instâncias Ativas:</span><span className="font-semibold text-green-500">{agent.instances_count}</span></div>
                        <div className="flex justify-between"><span>Conversas Hoje:</span><span className="font-semibold text-[#FF6B35]">{agent.conversations_today}</span></div>
                        <div className="flex justify-between"><span>Conversas Total:</span><span className="font-semibold">{mockMetrics.conversationsTotal.toLocaleString()}</span></div>
                        <div className="flex justify-between"><span>Uptime (30d):</span><span className="font-semibold text-green-500">{mockMetrics.uptime}</span></div>
                    </CardContent>
                </Card>

                {/* Card 2: Informações */}
                <Card className="border-l-4 border-[#0ca7d2]">
                    <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><FileText className="h-5 w-5 mr-2" /> Informações</CardTitle></CardHeader>
                    <CardContent className="space-y-2 text-sm">
                        <div className="flex justify-between"><span>Cliente:</span><span className="font-semibold">{client?.name}</span></div>
                        <div className="flex justify-between"><span>Projeto:</span><span className="font-semibold">{project?.name}</span></div>
                        <div className="flex justify-between"><span>Tipo:</span><Badge variant="secondary">{getAgentTypeLabel(agent.type)}</Badge></div>
                        <div className="flex justify-between"><span>Categoria:</span><Badge className="bg-[#FF6B35] text-white">{agent.category.toUpperCase()}</Badge></div>
                        <div className="flex justify-between"><span>Criado em:</span><span className="font-semibold">{agent.created_at}</span></div>
                    </CardContent>
                </Card>

                {/* Card 3: Links de Acesso */}
                <Card className="border-l-4 border-[#FF6B35]">
                    <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Globe className="h-5 w-5 mr-2" /> Links de Acesso</CardTitle></CardHeader>
                    <CardContent className="space-y-4 text-sm">
                        <div className="space-y-1">
                            <Label className="font-semibold">Dashboard Cliente:</Label>
                            <div className="flex space-x-2">
                                <Input readOnly value={clientDashboardLink} className="font-mono text-xs flex-grow" />
                                <Button variant="outline" size="icon" onClick={() => handleCopy(clientDashboardLink, 'Link Dashboard')}>
                                    <Copy className="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                        <div className="space-y-1">
                            <Label className="font-semibold">Link de Cadastro:</Label>
                            <div className="flex space-x-2">
                                <Input readOnly value={registrationLink} className="font-mono text-xs flex-grow" />
                                <Button variant="outline" size="icon" onClick={() => handleCopy(registrationLink, 'Link Cadastro')}>
                                    <Copy className="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
            
            {/* Performance Chart Mock */}
            <Card>
                <CardHeader><CardTitle>Performance Recente (Mock)</CardTitle></CardHeader>
                <CardContent>
                    <div className="h-64 flex items-center justify-center text-muted-foreground">
                        Gráfico de Conversas e Latência (Últimas 24h)
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default AgentOverviewTab;