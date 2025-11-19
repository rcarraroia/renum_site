import React from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Briefcase, Clock, CheckCircle, FileText, MessageSquare } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';

const ClientOverview: React.FC = () => {
  const projectStatus = {
    name: 'Projeto Automação Vendas',
    progress: 65,
    stage: 'Desenvolvimento Backend',
    nextMilestone: 'Revisão da API (2 semanas)',
  };

  return (
    <DashboardLayout>
      <h2 className="text-3xl font-bold mb-6">Bem-vindo(a) ao seu Portal</h2>
      
      <div className="grid gap-6 lg:grid-cols-3 mb-8">
        <Card className="lg:col-span-2 border-l-4 border-[#4e4ea8]">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Briefcase className="h-5 w-5 text-[#4e4ea8]" />
              <span>Status do Projeto Atual</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <h3 className="text-xl font-semibold mb-2">{projectStatus.name}</h3>
            <p className="text-sm text-muted-foreground mb-4">Fase: {projectStatus.stage}</p>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm font-medium">
                <span>Progresso Geral</span>
                <span>{projectStatus.progress}%</span>
              </div>
              <Progress value={projectStatus.progress} className="h-3 bg-gray-200 dark:bg-gray-700 [&>div]:bg-[#FF6B35]" />
            </div>
            
            <div className="mt-4 flex items-center space-x-2 text-sm text-muted-foreground">
              <Clock className="h-4 w-4" />
              <span>Próximo Marco: {projectStatus.nextMilestone}</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Ações Rápidas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full bg-[#FF6B35] hover:bg-[#e55f30]">
              <FileText className="h-4 w-4 mr-2" /> Ver Último Relatório
            </Button>
            <Button variant="outline" className="w-full">
              <MessageSquare className="h-4 w-4 mr-2" /> Contatar Equipe
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Entregáveis Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3 text-sm">
            <li className="flex items-center justify-between p-2 border rounded">
              <span><CheckCircle className="h-4 w-4 mr-2 inline text-green-500" /> Mockup Frontend V1.0</span>
              <span className="text-xs text-muted-foreground">2 dias atrás</span>
            </li>
            <li className="flex items-center justify-between p-2 border rounded">
              <span><FileText className="h-4 w-4 mr-2 inline text-[#0ca7d2]" /> Documento de Escopo Final</span>
              <span className="text-xs text-muted-foreground">1 semana atrás</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
};

export default ClientOverview;