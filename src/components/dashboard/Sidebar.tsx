import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Zap, LayoutDashboard, Users, Settings, FileText, MessageSquare, Briefcase, Calendar, BarChart, Wrench, ChevronLeft, ChevronRight, ClipboardList, UserPlus, Sparkles, Plus, Bot, Brain, TrendingUp, Database, Clock, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/context/AuthContext';
import RenumLogo from '@/components/RenumLogo';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge'; // Importando Badge
import { agentService } from '@/services/agentService';

interface NavItem {
  title: string;
  href: string;
  icon: React.ElementType;
  roles: ('admin' | 'client')[];
}

const adminNavItems: NavItem[] = [
  { title: 'Overview', href: '/dashboard/admin', icon: LayoutDashboard, roles: ['admin'] },
  { title: 'Projetos', href: '/dashboard/admin/projects', icon: Briefcase, roles: ['admin'] },
  { title: 'Leads', href: '/dashboard/admin/leads', icon: UserPlus, roles: ['admin'] },
  { title: 'Clientes', href: '/dashboard/admin/clients', icon: Users, roles: ['admin'] },
];

const adminAgentItems: NavItem[] = [
  { title: 'Gestão de Agentes', href: '/dashboard/admin/agents', icon: Zap, roles: ['admin'] },
  { title: 'Marketplace', href: '/dashboard/marketplace', icon: Bot, roles: ['admin'] },
];

const adminOperationsItems: NavItem[] = [
  { title: 'Conversas', href: '/dashboard/admin/conversations', icon: MessageSquare, roles: ['admin'] },
  { title: 'Relatórios & KPIs', href: '/dashboard/admin/reports', icon: BarChart, roles: ['admin'] },
  { title: 'Hub de Integrações', href: '/dashboard/integrations/radar', icon: RefreshCw, roles: ['admin'] },
];

// SICC Intelligence items removidos - agora são contextuais por agente
// Acesso via: /dashboard/admin/agents/:slug/intelligence/*

const clientNavItems: NavItem[] = [
  { title: 'Overview', href: '/dashboard/client', icon: LayoutDashboard, roles: ['client'] },
  { title: 'Meus Projetos', href: '/dashboard/client/projects', icon: Briefcase, roles: ['client'] },
  { title: 'Integrações', href: '/dashboard/client/integrations', icon: RefreshCw, roles: ['client'] },
  { title: 'Conversas Renus', href: '/dashboard/client/conversations', icon: MessageSquare, roles: ['client'] },
  { title: 'Documentos', href: '/dashboard/client/documents', icon: FileText, roles: ['client'] },
  { title: 'Calendário', href: '/dashboard/client/calendar', icon: Calendar, roles: ['client'] },
  { title: 'Suporte', href: '/dashboard/client/support', icon: Wrench, roles: ['client'] },
];

const commonNavItems: NavItem[] = [
  { title: 'Configurações', href: '/dashboard/settings', icon: Settings, roles: ['admin', 'client'] },
];

const Sidebar: React.FC = () => {
  const { role } = useAuth();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeAgentsCount, setActiveAgentsCount] = useState(0);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const agents = await agentService.listAgents();
        setActiveAgentsCount(agents.length);
      } catch (error) {
        console.error('Error fetching agents count:', error);
      }
    };

    if (role === 'admin') {
      fetchAgents();
    }
  }, [role]);

  const toggleCollapse = () => setIsCollapsed(!isCollapsed);

  const renderNavGroup = (items: NavItem[], title: string) => (
    <div className="space-y-1">
      {!isCollapsed && <h3 className="text-xs font-semibold uppercase text-sidebar-foreground/70 px-3 pt-2 pb-1">{title}</h3>}
      {items.map((item) => (
        <Link
          key={item.title}
          to={item.href}
          className={cn(
            "flex items-center rounded-md p-3 text-sm font-medium transition-colors",
            "text-sidebar-foreground hover:bg-sidebar-accent dark:hover:bg-gray-800",
            isCollapsed ? "justify-center" : "justify-start"
          )}
        >
          <item.icon className={cn("h-5 w-5", !isCollapsed && "mr-3")} />
          {!isCollapsed && item.title}
        </Link>
      ))}
    </div>
  );

  const renderAgentGroup = () => (
    <div className="space-y-1">
      {!isCollapsed && (
        <h3 className="text-xs font-semibold uppercase text-sidebar-foreground/70 px-3 pt-2 pb-1 flex items-center justify-between">
          Agentes
          <Badge variant="secondary" className="bg-[#FF6B35] text-white text-xs h-4">
            {activeAgentsCount}
          </Badge>
        </h3>
      )}
      {adminAgentItems.map((item) => (
        <Link
          key={item.title}
          to={item.href}
          className={cn(
            "flex items-center rounded-md p-3 text-sm font-medium transition-colors",
            "text-sidebar-foreground hover:bg-sidebar-accent dark:hover:bg-gray-800",
            isCollapsed ? "justify-center" : "justify-start"
          )}
        >
          <item.icon className={cn("h-5 w-5", !isCollapsed && "mr-3")} />
          {!isCollapsed && item.title}
        </Link>
      ))}
    </div>
  );

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-sidebar dark:bg-gray-950 border-r border-sidebar-border dark:border-gray-800 transition-all duration-300",
        isCollapsed ? "w-20" : "w-64"
      )}
    >
      <div className="flex items-center justify-between p-4 h-16">
        {!isCollapsed && <RenumLogo />}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleCollapse}
          className="text-sidebar-foreground hover:bg-sidebar-accent"
        >
          {isCollapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
        </Button>
      </div>

      <Separator className="bg-sidebar-border dark:bg-gray-800" />

      <nav className="flex-grow p-4 space-y-4 overflow-y-auto">
        {role === 'admin' ? (
          <>
            {renderNavGroup(adminNavItems, 'Administração')}

            {renderAgentGroup()}

            {renderNavGroup(adminOperationsItems, 'Operações')}
          </>
        ) : (
          renderNavGroup(clientNavItems, 'Geral')
        )}

        <Separator className="bg-sidebar-border dark:bg-gray-800" />

        {renderNavGroup(commonNavItems, 'Conta')}
      </nav>

      <div className="p-4 mt-auto">
        <Link to="/" className="flex items-center text-xs text-muted-foreground hover:text-primary transition-colors">
          <Zap className={cn("h-4 w-4", !isCollapsed && "mr-2")} />
          {!isCollapsed && "Voltar ao Site"}
        </Link>
      </div>
    </div>
  );
};

export default Sidebar;