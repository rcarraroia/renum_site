import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Filter, Users, Zap, Clock, CheckCircle, XCircle } from 'lucide-react';
import { mockClients, mockCategories } from '@/mocks/agents.mock';
import { AgentStatus, AgentCategory } from '@/types/agent';

interface AgentFiltersProps {
  onFilterChange: (filters: { search: string; status: string; client: string; category: string }) => void;
}

const AgentFilters: React.FC<AgentFiltersProps> = ({ onFilterChange }) => {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('all');
  const [client, setClient] = useState('all');
  const [category, setCategory] = useState('all');

  const handleFilter = () => {
    onFilterChange({ search, status, client, category });
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="grid gap-4 md:grid-cols-5">
          {/* Search */}
          <div className="relative md:col-span-2">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar agente, cliente ou slug..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8"
            />
          </div>

          {/* Status Filter */}
          <Select value={status} onValueChange={setStatus}>
            <SelectTrigger>
              <Filter className="h-4 w-4 mr-2 text-[#4e4ea8]" />
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Status</SelectItem>
              <SelectItem value="ativo">Ativo</SelectItem>
              <SelectItem value="pausado">Pausado</SelectItem>
              <SelectItem value="inativo">Inativo</SelectItem>
              <SelectItem value="erro">Erro</SelectItem>
            </SelectContent>
          </Select>

          {/* Client Filter */}
          <Select value={client} onValueChange={setClient}>
            <SelectTrigger>
              <Users className="h-4 w-4 mr-2 text-[#FF6B35]" />
              <SelectValue placeholder="Cliente" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Clientes</SelectItem>
              {mockClients.map(c => (
                <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Category Filter */}
          <Select value={category} onValueChange={setCategory}>
            <SelectTrigger>
              <Zap className="h-4 w-4 mr-2 text-[#0ca7d2]" />
              <SelectValue placeholder="Categoria" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas as Categorias</SelectItem>
              {mockCategories.map(c => (
                <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex justify-end mt-4">
            <Button onClick={handleFilter} className="bg-[#4e4ea8] hover:bg-[#3a3a80]">
                <Filter className="h-4 w-4 mr-2" /> Aplicar Filtros
            </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default AgentFilters;