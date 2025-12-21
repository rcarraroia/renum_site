/**
 * Task 32: Cross-Component Navigation
 * Links, breadcrumbs e deep linking entre interfaces
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
    label: string;
    path: string;
}

// Mapeamento de rotas para breadcrumbs
const routeMap: Record<string, BreadcrumbItem[]> = {
    '/dashboard/agents/renus': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Agentes', path: '/dashboard/agents' },
        { label: 'RENUS', path: '/dashboard/agents/renus' }
    ],
    '/dashboard/agents/pesquisas': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Agentes', path: '/dashboard/agents' },
        { label: 'Pesquisas', path: '/dashboard/agents/pesquisas' }
    ],
    '/dashboard/agents/isa': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Agentes', path: '/dashboard/agents' },
        { label: 'ISA', path: '/dashboard/agents/isa' }
    ],
    '/dashboard/marketplace': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Marketplace', path: '/dashboard/marketplace' }
    ],
    '/dashboard/intelligence': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Intelligence', path: '/dashboard/intelligence' }
    ],
    '/dashboard/integrations/radar': [
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Integrações', path: '/dashboard/integrations' },
        { label: 'Radar', path: '/dashboard/integrations/radar' }
    ]
};

export const Breadcrumbs: React.FC = () => {
    const location = useLocation();
    const items = routeMap[location.pathname] || [];

    if (items.length === 0) return null;

    return (
        <nav className="flex items-center space-x-2 text-sm text-muted-foreground mb-4">
            <Link to="/dashboard" className="hover:text-foreground">
                <Home className="h-4 w-4" />
            </Link>
            {items.slice(1).map((item, index) => (
                <React.Fragment key={item.path}>
                    <ChevronRight className="h-4 w-4" />
                    {index === items.length - 2 ? (
                        <span className="text-foreground font-medium">{item.label}</span>
                    ) : (
                        <Link to={item.path} className="hover:text-foreground">
                            {item.label}
                        </Link>
                    )}
                </React.Fragment>
            ))}
        </nav>
    );
};

// Links rápidos entre interfaces
interface QuickLink {
    label: string;
    path: string;
    description: string;
}

export const quickLinks: Record<string, QuickLink[]> = {
    renus: [
        { label: 'Configuração Técnica', path: '/dashboard/admin/renus-config', description: 'Editar prompts e modelo' },
        { label: 'Intelligence', path: '/dashboard/intelligence', description: 'Ver evolução e memórias' },
        { label: 'Integrações', path: '/dashboard/integrations/radar', description: 'Status de integrações' }
    ],
    pesquisas: [
        { label: 'Configuração Técnica', path: '/dashboard/admin/pesquisas-config', description: 'Editar templates' },
        { label: 'Resultados', path: '/dashboard/pesquisas/resultados', description: 'Ver resultados de pesquisas' },
        { label: 'Relatórios', path: '/dashboard/pesquisas/relatorios', description: 'Relatórios de IA' }
    ],
    isa: [
        { label: 'Configuração Técnica', path: '/dashboard/admin/isa-config', description: 'Configurar SICC' },
        { label: 'Auditoria', path: '/dashboard/isa/audit', description: 'Logs de auditoria' },
        { label: 'Comandos', path: '/dashboard/isa/commands', description: 'Histórico de comandos' }
    ]
};

interface QuickLinksProps {
    context: 'renus' | 'pesquisas' | 'isa';
}

export const QuickLinks: React.FC<QuickLinksProps> = ({ context }) => {
    const links = quickLinks[context] || [];

    return (
        <div className="flex flex-wrap gap-2">
            {links.map(link => (
                <Link
                    key={link.path}
                    to={link.path}
                    className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm hover:bg-secondary/80 transition"
                    title={link.description}
                >
                    {link.label}
                </Link>
            ))}
        </div>
    );
};

// Deep linking helper
export const generateDeepLink = (
    type: 'agent' | 'config' | 'conversation',
    id: string,
    section?: string
): string => {
    switch (type) {
        case 'agent':
            return `/dashboard/agents/${id}${section ? `?tab=${section}` : ''}`;
        case 'config':
            return `/dashboard/admin/agents/${id}/config${section ? `#${section}` : ''}`;
        case 'conversation':
            return `/dashboard/conversations/${id}`;
        default:
            return '/dashboard';
    }
};

export default Breadcrumbs;
