import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Server, CheckCircle, XCircle } from 'lucide-react';

const AgentInstancesTab: React.FC = () => {
  const instances = [
    { id: 'i-prod-01', region: 'us-east-1', status: 'running', load: '20%', uptime: '99.9%' },
    { id: 'i-prod-02', region: 'eu-west-1', status: 'running', load: '15%', uptime: '99.9%' },
    { id: 'i-dev-01', region: 'us-east-1', status: 'stopped', load: '0%', uptime: '0%' },
  ];

  return (
    <Card>
      <CardHeader><CardTitle className="flex items-center"><Server className="h-5 w-5 mr-2" /> Instâncias de Execução</CardTitle></CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Região</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Carga</TableHead>
              <TableHead>Uptime</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {instances.map((instance) => (
              <TableRow key={instance.id}>
                <TableCell className="font-mono text-sm">{instance.id}</TableCell>
                <TableCell>{instance.region}</TableCell>
                <TableCell>
                  <div className="flex items-center">
                    {instance.status === 'running' ? <CheckCircle className="h-4 w-4 text-green-500 mr-2" /> : <XCircle className="h-4 w-4 text-red-500 mr-2" />}
                    {instance.status}
                  </div>
                </TableCell>
                <TableCell>{instance.load}</TableCell>
                <TableCell>{instance.uptime}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default AgentInstancesTab;