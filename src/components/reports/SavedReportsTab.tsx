import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Zap, Clock, FileText, Edit, Trash2, Play } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface SavedReport {
    id: number;
    name: string;
    metric: string;
    lastRun: Date;
    frequency: string;
}

const MOCK_SAVED_REPORTS: SavedReport[] = [
    { id: 1, name: 'Relatório Mensal de ROI', metric: 'Variação Orçamentária', lastRun: new Date(new Date().setDate(new Date().getDate() - 7)), frequency: 'Mensal' },
    { id: 2, name: 'Performance Semanal do Renus', metric: 'Taxa de Resolução', lastRun: new Date(new Date().setDate(new Date().getDate() - 1)), frequency: 'Semanal' },
    { id: 3, name: 'Clientes Ativos por Segmento', metric: 'Contagem de Clientes', lastRun: new Date(new Date().setDate(new Date().getDate() - 30)), frequency: 'Manual' },
];

const SavedReportsTab: React.FC = () => {
    const [reports, setReports] = useState(MOCK_SAVED_REPORTS);

    const handleRun = (reportName: string) => {
        toast.info(`Executando relatório: ${reportName}...`);
        // Simulate run time
        setTimeout(() => {
            setReports(prev => prev.map(r => r.name === reportName ? { ...r, lastRun: new Date() } : r));
            toast.success(`Relatório '${reportName}' concluído e atualizado.`);
        }, 1500);
    };

    const handleDelete = (id: number) => {
        setReports(prev => prev.filter(r => r.id !== id));
        toast.warning("Relatório excluído.");
    };

    return (
        <div className="space-y-8">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]">
                        <FileText className="h-5 w-5 mr-2" /> Templates Salvos
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">Acesse e gerencie seus relatórios personalizados salvos.</p>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Nome do Relatório</TableHead>
                                <TableHead>Métrica Principal</TableHead>
                                <TableHead>Frequência</TableHead>
                                <TableHead>Última Execução</TableHead>
                                <TableHead className="text-right">Ações</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {reports.map(report => (
                                <TableRow key={report.id}>
                                    <TableCell className="font-medium">{report.name}</TableCell>
                                    <TableCell>{report.metric}</TableCell>
                                    <TableCell>{report.frequency}</TableCell>
                                    <TableCell className="text-sm text-muted-foreground">
                                        {format(report.lastRun, 'dd/MM/yyyy HH:mm', { locale: ptBR })}
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Button variant="outline" size="sm" onClick={() => handleRun(report.name)}>
                                            <Play className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="sm">
                                            <Edit className="h-4 w-4" />
                                        </Button>
                                        <Button variant="destructive" size="sm" onClick={() => handleDelete(report.id)}>
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
};

export default SavedReportsTab;