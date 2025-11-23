import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Zap, LayoutDashboard, Users, Settings, FileText, MessageSquare, Briefcase, Calendar, BarChart, Wrench, ChevronLeft, ChevronRight, ClipboardList, UserPlus } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/context/AuthContext';
import RenumLogo from '@/components/RenumLogo';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';

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
  { title: 'Conversas', href: '/dashboard/admin/conversations', icon: MessageSquare, roles: ['admin'] },
  { title: 'Pesquisas', href: '/dashboard/admin/pesquisas/entrevistas', icon: ClipboardList, roles: ['admin'] },
  { title: 'Relatórios', href: '/dashboard/admin/reports', icon: BarChart, roles: ['admin'] },
  { title: 'Config. Renus', href: '/dashboard/admin/renus-config', icon: Wrench, roles: ['admin'] },
];

const clientNavItems: NavItem[] = [
  { title: 'Overview', href: '/dashboard/client', icon: LayoutDashboard, roles: ['client'] },
  { title: 'Meus Projetos', href: '/dashboard/client/projects', icon: Briefcase, roles: ['client'] },
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

  const navItems = [
    ...(role === 'admin' ? adminNavItems : []),
    ...(role === 'client' ? clientNavItems : []),
    ...commonNavItems,
  ];

  const toggleCollapse = () => setIsCollapsed(!isCollapsed);

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

      <nav className="flex-grow p-4 space-y-2 overflow-y-auto">
        {navItems.map((item) => (
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