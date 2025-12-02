import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, LineChart, Zap } from 'lucide-react';

const AgentMetricsTab: React.FC = () => {
  return (
    <Card>
      <CardHeader><CardTitle className="flex items-center"><BarChart className="h-5 w-5 mr-2" /> Métricas de Uso</CardTitle></CardHeader>
      <CardContent>
        <div className="h-64 flex items-center justify-center text-muted-foreground">
          Gráfico de Latência e Uso de Tokens (Mock)
        </div>
      </CardContent>
    </Card>
  );
};

export default AgentMetricsTab;