
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Eye, Edit, Trash2, Globe, GlobeLock } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { apiClient } from '@/services/api'; // Corrigido

interface Template {
  id: string;
  name: string;
  description: string;
  category: 'b2b' | 'b2c';
  niche: string;
  marketplace_visible: boolean;
  created_at: string;
}

const TemplatesListPage: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const { data } = await apiClient.get('/api/agents', {
        params: { is_template: true }
      });
      setTemplates(data);
    } catch (error) {
      console.error('Error loading templates:', error);
      toast({
        title: "Erro",
        description: "Falha ao carregar templates",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = () => {
    navigate('/dashboard/admin/agents/create');
  };

  const handleToggleVisibility = async (templateId: string, currentVisibility: boolean) => {
    try {
      await apiClient.patch(`/api/agents/${templateId}`, {
        marketplace_visible: !currentVisibility
      });

      toast({
        title: "Sucesso",
        description: `Template ${!currentVisibility ? 'publicado' : 'despublicado'} no marketplace`
      });

      loadTemplates();
    } catch (error) {
      console.error('Error toggling visibility:', error);
      toast({
        title: "Erro",
        description: "Falha ao atualizar visibilidade",
        variant: "destructive"
      });
    }
  };

  const handleViewTemplate = (templateId: string) => {
    navigate(`/dashboard/admin/agents/${templateId}`);
  };

  const handleEditTemplate = (templateId: string) => {
    navigate(`/dashboard/admin/agents/${templateId}/edit`);
  };

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold">Templates de Agentes</h1>
            <p className="text-muted-foreground">
              Gerencie templates disponíveis no marketplace
            </p>
          </div>
          <Button onClick={handleCreateTemplate}>
            <Plus className="h-4 w-4 mr-2" />
            Criar Novo Template
          </Button>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <p className="text-muted-foreground">Carregando templates...</p>
          </div>
        ) : templates.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center h-64">
              <p className="text-muted-foreground mb-4">Nenhum template criado ainda</p>
              <Button onClick={handleCreateTemplate}>
                <Plus className="h-4 w-4 mr-2" />
                Criar Primeiro Template
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((template) => (
              <Card key={template.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{template.name}</CardTitle>
                    <Badge variant={template.category === 'b2b' ? 'default' : 'secondary'}>
                      {template.category.toUpperCase()}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
                    {template.description || 'Sem descrição'}
                  </p>
                  <div className="flex items-center gap-2 mb-4">
                    <Badge variant="outline">{template.niche}</Badge>
                    {template.marketplace_visible ? (
                      <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                        <Globe className="h-3 w-3 mr-1" />
                        Público
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="bg-gray-50 text-gray-700 border-gray-200">
                        <GlobeLock className="h-3 w-3 mr-1" />
                        Privado
                      </Badge>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleViewTemplate(template.id)}
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      Ver
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEditTemplate(template.id)}
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Editar
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleToggleVisibility(template.id, template.marketplace_visible)}
                      className={template.marketplace_visible ? 'text-orange-600' : 'text-green-600'}
                    >
                      {template.marketplace_visible ? <GlobeLock className="h-4 w-4" /> : <Globe className="h-4 w-4" />}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default TemplatesListPage;
