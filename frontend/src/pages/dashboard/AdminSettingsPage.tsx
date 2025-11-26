import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Settings, Building, User, Mail, Zap, Shield, Palette, DollarSign, Database, Terminal, Search, Save, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Separator } from '@/components/ui/separator';

// Import Tab Components
import CompanyProfileTab from '@/components/settings/CompanyProfileTab';
import UserPermissionsTab from '@/components/settings/UserPermissionsTab';
import NotificationsTab from '@/components/settings/NotificationsTab';
import IntegrationsTab from '@/components/settings/IntegrationsTab';
import AppearanceTab from '@/components/settings/AppearanceTab';
import BillingTab from '@/components/settings/BillingTab';
import BackupExportTab from '@/components/settings/BackupExportTab';
import AdvancedTab from '@/components/settings/AdvancedTab';
import GlobalGuardrailsTab from '@/components/settings/GlobalGuardrailsTab'; // Importando o novo componente

interface SettingCategory {
  id: string;
  title: string;
  icon: React.ElementType;
  component: React.FC;
}

const categories: SettingCategory[] = [
  { id: 'profile', title: 'Perfil da Empresa', icon: Building, component: CompanyProfileTab },
  { id: 'users', title: 'Usuários e Permissões', icon: User, component: UserPermissionsTab },
  { id: 'notifications', title: 'Notificações', icon: Mail, component: NotificationsTab },
  { id: 'guardrails-global', title: 'Guardrails (Global)', icon: Shield, component: GlobalGuardrailsTab }, // Nova Categoria
  { id: 'integrations', title: 'Integrações', icon: Zap, component: IntegrationsTab },
  { id: 'appearance', title: 'Aparência', icon: Palette, component: AppearanceTab },
  { id: 'billing', title: 'Faturamento', icon: DollarSign, component: BillingTab },
  { id: 'backup', title: 'Backup e Exportação', icon: Database, component: BackupExportTab },
  { id: 'advanced', title: 'Avançado', icon: Terminal, component: AdvancedTab },
];

const AdminSettingsPage: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState(categories[0].id);
  const [searchTerm, setSearchTerm] = useState('');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false); // Mock state

  const ActiveComponent = useMemo(() => {
    const category = categories.find(c => c.id === activeCategory);
    return category ? category.component : () => <div>Configuração não encontrada.</div>;
  }, [activeCategory]);

  const filteredCategories = useMemo(() => {
    if (!searchTerm) return categories;
    const lowerCaseSearch = searchTerm.toLowerCase();
    return categories.filter(cat => cat.title.toLowerCase().includes(lowerCaseSearch));
  }, [searchTerm]);

  const handleSaveAll = () => {
    // Mock save logic
    toast.success("Todas as configurações salvas com sucesso!");
    setHasUnsavedChanges(false);
  };

  const handleCancel = () => {
    // Mock cancel logic
    toast.info("Alterações descartadas.");
    setHasUnsavedChanges(false);
  };

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Settings className="h-7 w-7 mr-3 text-[#4e4ea8]" />
          Configurações
        </h2>
      </div>

      <div className="flex h-[calc(100vh-180px)] overflow-hidden border rounded-lg bg-card dark:bg-gray-900">
        
        {/* Sidebar de Navegação */}
        <div className="w-64 flex-shrink-0 border-r p-4 overflow-y-auto">
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Buscar configurações..." 
              className="pl-10" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <nav className="space-y-1">
            {filteredCategories.map((category) => (
              <Button
                key={category.id}
                variant="ghost"
                className={cn(
                  "w-full justify-start text-base h-12",
                  activeCategory === category.id 
                    ? "bg-accent text-primary dark:bg-gray-800 dark:text-white font-semibold" 
                    : "text-muted-foreground hover:bg-gray-100 dark:hover:bg-gray-800/50"
                )}
                onClick={() => setActiveCategory(category.id)}
              >
                <category.icon className="h-5 w-5 mr-3" />
                {category.title}
              </Button>
            ))}
          </nav>
        </div>

        {/* Conteúdo da Configuração */}
        <div className="flex-grow overflow-y-auto p-6 md:p-8 relative">
          <ActiveComponent />
        </div>
      </div>

      {/* Footer Fixo para Salvar/Cancelar */}
      {hasUnsavedChanges && (
        <div className="fixed bottom-0 left-0 right-0 bg-background border-t shadow-2xl p-4 flex justify-end space-x-4 z-50">
            <Button variant="outline" onClick={handleCancel}>
                <X className="h-4 w-4 mr-2" /> Cancelar
            </Button>
            <Button onClick={handleSaveAll} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                <Save className="h-4 w-4 mr-2" /> Salvar Todas as Alterações
            </Button>
        </div>
      )}
    </DashboardLayout>
  );
};

export default AdminSettingsPage;