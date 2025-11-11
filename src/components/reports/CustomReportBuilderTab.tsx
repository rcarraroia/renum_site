import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Zap, Settings, Filter, Save, Clock, Eye } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

const CustomReportBuilderTab: React.FC = () => {
    const handleSave = () => {
        toast.success("Template de relatório personalizado salvo!");
    };

    const handleSchedule = () => {
        toast.info("Agendamento de relatório simulado para o seu email.");
    };

    return (
        <div className="space-y-8">
            <Card className="border-2 border-dashed border-[#0ca7d2] dark:border-[#4e4ea8]">
                <CardHeader>
                    <CardTitle className="flex items-center text-[#0ca7d2]">
                        <Settings className="h-5 w-5 mr-2" /> Construtor de Relatórios Personalizados
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">Crie relatórios específicos selecionando métricas, dimensões e filtros.</p>
                </CardHeader>
                <CardContent className="space-y-6">
                    
                    <div className="grid md:grid-cols-3 gap-4">
                        <div>
                            <Label>Métrica Principal</Label>
                            <Select>
                                <SelectTrigger><SelectValue placeholder="Ex: Taxa de Conclusão" /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="completion_rate">Taxa de Conclusão</SelectItem>
                                    <SelectItem value="budget_variance">Variação Orçamentária</SelectItem>
                                    <SelectItem value="lead_conversion">Conversão de Leads</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label>Dimensão (Agrupar por)</Label>
                            <Select>
                                <SelectTrigger><SelectValue placeholder="Ex: Tipo de Projeto" /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="project_type">Tipo de Projeto</SelectItem>
                                    <SelectItem value="client_segment">Segmento do Cliente</SelectItem>
                                    <SelectItem value="responsible_agent">Agente Responsável</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label>Visualização</Label>
                            <Select defaultValue="table">
                                <SelectTrigger><SelectValue placeholder="Tipo de Gráfico" /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="table">Tabela de Dados</SelectItem>
                                    <SelectItem value="bar">Gráfico de Barras</SelectItem>
                                    <SelectItem value="line">Gráfico de Linhas</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <Separator />

                    <h5 className="font-semibold flex items-center text-[#FF6B35]"><Filter className="h-4 w-4 mr-2" /> Filtros Adicionais</h5>
                    <div className="grid md:grid-cols-2 gap-4">
                        <div>
                            <Label>Status do Projeto</Label>
                            <Input placeholder="Ex: Em Andamento, Em Revisão" />
                        </div>
                        <div>
                            <Label>Período de Tempo</Label>
                            <Input placeholder="Ex: Últimos 90 dias" />
                        </div>
                    </div>

                    <div className="flex justify-end space-x-3 pt-4">
                        <Button variant="outline" onClick={() => toast.info("Simulando geração de preview...")}>
                            <Eye className="h-4 w-4 mr-2" /> Pré-visualizar
                        </Button>
                        <Button onClick={handleSave} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                            <Save className="h-4 w-4 mr-2" /> Salvar Template
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-[#FF6B35]">Agendamento e Exportação</CardTitle>
                    <p className="text-sm text-muted-foreground">Configure a entrega automática deste relatório.</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-3 gap-4">
                        <div>
                            <Label>Frequência</Label>
                            <Select>
                                <SelectTrigger><SelectValue placeholder="Mensal" /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="daily">Diário</SelectItem>
                                    <SelectItem value="weekly">Semanal</SelectItem>
                                    <SelectItem value="monthly">Mensal</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label>Formato de Exportação</Label>
                            <Select>
                                <SelectTrigger><SelectValue placeholder="PDF" /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="pdf">PDF</SelectItem>
                                    <SelectItem value="excel">Excel</SelectItem>
                                    <SelectItem value="csv">CSV</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label>Destinatários</Label>
                            <Input placeholder="emails separados por vírgula" />
                        </div>
                    </div>
                    <Button onClick={handleSchedule} variant="secondary">
                        <Clock className="h-4 w-4 mr-2" /> Agendar Envio
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
};

export default CustomReportBuilderTab;