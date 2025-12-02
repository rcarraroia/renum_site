import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Server, CheckCircle, XCircle, Clock, Zap } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface Instance {
  id: string;
  region: string;
  status: 'running' | 'stopped' | 'error';
  load: string;
  uptime: string;
}

const MOCK_INSTANCES: Instance[] = [
  { id: 'i-prod-01', region: 'us-east-1', status: 'running', load: '20%', uptime: '99.9%' },
  { id: 'i-prod-02', region: 'eu-west-1', status: 'running', load: '15%', uptime: '99.9%' },
  { id: 'i-dev-01', region: 'us-east-1', status: 'stopped', load: '0%', uptime: '0%' },
  { id: 'i-prod-03', region: 'sa-east-1', status: 'error', load: '100%', uptime: '50%' },
];

const InstanceList: React.FC = () => {
  return (
    <Card>
      <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Server className="h-5 w-5 mr-2" /> Instâncias de Execução</CardTitle></CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Região</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Carga</TableHead>
              <TableHead>Uptime</TableHead>
              <TableHead>Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {MOCK_INSTANCES.map((instance) => (
              <TableRow key={instance.id}>
                <TableCell className="font-mono text-sm">{instance.id}</TableCell>
                <TableCell>{instance.region}</TableCell>
                <TableCell>
                  <div className="flex items-center">
                    {instance.status === 'running' ? <CheckCircle className="h-4 w-4 text-green-500 mr-2" /> : instance.status === 'stopped' ? <Clock className="h-4 w-4 text-yellow-500 mr-2" /> : <XCircle className="h-4 w-4 text-red-500 mr-2" />}
                    <Badge className={cn(
                        instance.status === 'running' && 'bg-green-500',
                        instance.status === 'stopped' && 'bg-yellow-500',
                        instance.status === 'error' && 'bg-red-500',
                        'text-white capitalize'
                    )}>
                        {instance.status}
                    </Badge>
                  </div>
                </TableCell>
                <TableCell>{instance.load}</TableCell>
                <TableCell>{instance.uptime}</TableCell>
                <TableCell>
                    <Button variant="outline" size="sm" disabled={instance.status === 'running'}>
                        <Zap className="h-4 w-4" />
                    </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default InstanceList;