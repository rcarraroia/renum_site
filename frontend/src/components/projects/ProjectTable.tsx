import React, { useState, useMemo } from 'react';
import { Project, ProjectStatus, ProjectType, TeamMember } from '@/types/project';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { ArrowUpDown, MoreHorizontal, User as UserIcon, FileText, Edit, Archive, Clock } from 'lucide-react';
import { StatusBadge, TypeBadge } from './ProjectBadges';
import { Link } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface ProjectTableProps {
  projects: Project[];
  onEdit: (project: Project) => void;
  onArchive: (projectId: string) => void;
}

type SortKey = keyof Project | 'actions';
type SortDirection = 'asc' | 'desc';

const ProjectTable: React.FC<ProjectTableProps> = ({ projects, onEdit, onArchive }) => {
  const [sortConfig, setSortConfig] = useState<{ key: SortKey; direction: SortDirection }>({
    key: 'name',
    direction: 'asc',
  });

  const sortedProjects = useMemo(() => {
    let sortableItems = [...projects];
    if (sortConfig.key !== 'actions') {
      sortableItems.sort((a, b) => {
        const aValue = a[sortConfig.key as keyof Project];
        const bValue = b[sortConfig.key as keyof Project];

        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [projects, sortConfig]);

  const requestSort = (key: SortKey) => {
    let direction: SortDirection = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key: SortKey) => {
    if (sortConfig.key !== key) return null;
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  const isDueDateCritical = (dueDate: Date) => {
    const diffTime = dueDate.getTime() - new Date().getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7 && diffDays >= 0; // Approaching deadline (7 days or less)
  };

  const isDueDatePast = (dueDate: Date) => {
    return dueDate.getTime() < new Date().getTime();
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            {[
              { key: 'name', label: 'Projeto' },
              { key: 'clientName', label: 'Cliente' },
              { key: 'status', label: 'Status' },
              { key: 'type', label: 'Tipo' },
              { key: 'startDate', label: 'Início' },
              { key: 'dueDate', label: 'Prazo' },
              { key: 'progress', label: 'Progresso' },
              { key: 'responsible', label: 'Responsável' },
              { key: 'actions', label: 'Ações' },
            ].map(({ key, label }) => (
              <TableHead key={key} className={cn(key === 'actions' ? 'text-right' : 'cursor-pointer')}>
                <div className="flex items-center" onClick={() => key !== 'actions' && requestSort(key as SortKey)}>
                  {label}
                  {key !== 'actions' && <ArrowUpDown className="ml-2 h-4 w-4 opacity-50" />}
                  {getSortIcon(key as SortKey)}
                </div>
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedProjects.length > 0 ? (
            sortedProjects.map((project) => (
              <TableRow key={project.id} className="hover:bg-accent/50 transition-colors">
                <TableCell className="font-medium">
                  <Link to={`/dashboard/admin/projects/${project.id}`} className="text-[#4e4ea8] dark:text-[#0ca7d2] hover:underline">
                    {project.name}
                  </Link>
                </TableCell>
                <TableCell>
                  <Link to={`/dashboard/admin/clients/${project.clientId}`} className="text-muted-foreground hover:text-primary hover:underline">
                    {project.clientName}
                  </Link>
                </TableCell>
                <TableCell>
                  <StatusBadge status={project.status} />
                </TableCell>
                <TableCell>
                  <TypeBadge type={project.type} />
                </TableCell>
                <TableCell className="text-sm">
                  {format(project.startDate, 'dd/MM/yyyy', { locale: ptBR })}
                </TableCell>
                <TableCell className={cn(
                    "text-sm font-medium",
                    isDueDatePast(project.dueDate) && project.status !== 'Concluído' && 'text-red-500 font-bold',
                    isDueDateCritical(project.dueDate) && project.status !== 'Concluído' && 'text-yellow-500'
                )}>
                  <div className="flex items-center space-x-1">
                    {isDueDatePast(project.dueDate) && project.status !== 'Concluído' && <Clock className="h-4 w-4" />}
                    {format(project.dueDate, 'dd/MM/yyyy', { locale: ptBR })}
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center space-x-2 w-32">
                    <Progress value={project.progress} className="h-2 [&>div]:bg-[#FF6B35]" />
                    <span className="text-xs font-medium">{project.progress}%</span>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center space-x-2">
                    <Avatar className="h-6 w-6">
                      <AvatarFallback className="text-xs bg-gray-200 dark:bg-gray-700">
                        {project.responsible.avatarUrl ? <img src={project.responsible.avatarUrl} alt={project.responsible.name} /> : getInitials(project.responsible.name)}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm hidden lg:inline">{project.responsible.name}</span>
                  </div>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <span className="sr-only">Abrir menu</span>
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Ações</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => console.log('Ver detalhes', project.id)}>
                        <FileText className="mr-2 h-4 w-4" /> Ver Detalhes
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => onEdit(project)}>
                        <Edit className="mr-2 h-4 w-4" /> Editar
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem onClick={() => onArchive(project.id)} className="text-red-500">
                        <Archive className="mr-2 h-4 w-4" /> Arquivar
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={9} className="h-24 text-center text-muted-foreground">
                Nenhum projeto encontrado.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
};

export default ProjectTable;