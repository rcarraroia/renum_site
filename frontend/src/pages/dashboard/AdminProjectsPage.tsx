import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Zap, Briefcase, Clock, CheckCircle, Plus, Filter, Download, List, LayoutGrid, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MOCK_PROJECTS } from '@/data/mockProjects';
import { Project } from '@/types/project';
import ProjectTable from '@/components/projects/ProjectTable';
import ProjectCreationModal from '@/components/projects/ProjectCreationModal';
import { toast } from 'sonner';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { StatusBadge } from '@/components/projects/ProjectBadges';
import { Progress } from '@/components/ui/progress';

const AdminProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [viewMode, setViewMode] = useState<'table' | 'grid'>('table');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredProjects = useMemo(() => {
    if (!searchTerm) return projects;
    const lowerCaseSearch = searchTerm.toLowerCase();
    return projects.filter(project => 
        project.name.toLowerCase().includes(lowerCaseSearch) ||
        project.clientName.toLowerCase().includes(lowerCaseSearch) ||
        project.responsible.name.toLowerCase().includes(lowerCaseSearch)
    );
  }, [projects, searchTerm]);

  const metrics = useMemo(() => ({
    total: projects.length,
    inProgress: projects.filter(p => p.status === 'Em Andamento').length,
    completed: projects.filter(p => p.status === 'Concluído').length,
  }), [projects]);

  const handleCreateProject = (newProjectData: Omit<Project, 'id' | 'status' | 'progress'>) => {
    const newProject: Project = {
      ...newProjectData,
      id: `p${Date.now()}`,
      status: 'Em Andamento', // Default status upon creation
      progress: 0,
    };
    setProjects(prev => [newProject, ...prev]);
  };

  const handleEditProject = (project: Project) => {
    // In a real app, this would open an edit modal
    toast.info(`Abrindo edição para: ${project.name}`);
  };

  const handleArchiveProject = (projectId: string) => {
    setProjects(prev => prev.filter(p => p.id !== projectId));
    toast.warning(`Projeto arquivado (ID: ${projectId})`);
  };

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Briefcase className="h-7 w-7 mr-3 text-[#4e4ea8]" />
          Projetos
        </h2>
        <div className="flex space-x-2">
          <Button onClick={() => setIsModalOpen(true)} className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <Plus className="h-4 w-4 mr-2" /> Novo Projeto
          </Button>
        </div>
      </div>
      
      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Projetos</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Em Andamento</CardTitle>
            <Clock className="h-4 w-4 text-[#4e4ea8]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#4e4ea8]">{metrics.inProgress}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Concluídos</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">{metrics.completed}</div>
          </CardContent>
        </Card>
      </div>

      {/* Toolbar and View Toggle */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 space-y-4 md:space-y-0">
        <div className="flex w-full md:w-auto space-x-2">
            <div className="relative w-full md:w-64">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input 
                    placeholder="Buscar projeto ou cliente..." 
                    className="pl-10" 
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <Button variant="outline"><Filter className="h-4 w-4 mr-2" /> Filtros</Button>
            <Button variant="outline"><Download className="h-4 w-4 mr-2" /> Exportar</Button>
        </div>
        
        <ToggleGroup type="single" value={viewMode} onValueChange={(value: 'table' | 'grid') => value && setViewMode(value)} className="flex-shrink-0">
            <ToggleGroupItem value="table" aria-label="Visualização em Tabela">
                <List className="h-4 w-4" />
            </ToggleGroupItem>
            <ToggleGroupItem value="grid" aria-label="Visualização em Grid">
                <LayoutGrid className="h-4 w-4" />
            </ToggleGroupItem>
        </ToggleGroup>
      </div>

      {/* Main Content Area */}
      {viewMode === 'table' ? (
        <ProjectTable projects={filteredProjects} onEdit={handleEditProject} onArchive={handleArchiveProject} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Placeholder for Grid View */}
            {filteredProjects.map(project => (
                <Card key={project.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader className="flex flex-row items-center justify-between">
                        <CardTitle className="text-lg">{project.name}</CardTitle>
                        <StatusBadge status={project.status} />
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground mb-2">Cliente: {project.clientName}</p>
                        <div className="flex items-center space-x-2">
                            <Progress value={project.progress} className="h-2 flex-grow [&>div]:bg-[#FF6B35]" />
                            <span className="text-xs font-medium">{project.progress}%</span>
                        </div>
                        <Button variant="link" className="p-0 mt-3 h-auto text-[#0ca7d2]">Ver Detalhes</Button>
                    </CardContent>
                </Card>
            ))}
            {filteredProjects.length === 0 && (
                <div className="col-span-full text-center py-12 border-2 border-dashed rounded-lg">
                    <Briefcase className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
                    <p className="text-lg text-muted-foreground">Nenhum projeto corresponde à sua busca.</p>
                </div>
            )}
        </div>
      )}

      {/* Pagination (Mock) */}
      <div className="mt-6 flex justify-end text-sm text-muted-foreground">
        Mostrando 1 a {filteredProjects.length} de {projects.length} projetos.
      </div>

      <ProjectCreationModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onCreate={handleCreateProject} 
      />
    </DashboardLayout>
  );
};

export default AdminProjectsPage;