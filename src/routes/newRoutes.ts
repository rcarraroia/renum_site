/**
 * Novas Rotas - Contextual Interfaces, Marketplace, Intelligence
 * Adicionar ao arquivo de rotas principal
 */

import { lazy } from 'react';

// Contextual Interfaces (Tasks 22-24)
export const RenusInterface = lazy(() => import('@/pages/agents/contextual/RenusInterface'));
export const PesquisasInterface = lazy(() => import('@/pages/agents/contextual/PesquisasInterface'));
export const IsaInterface = lazy(() => import('@/pages/agents/contextual/IsaInterface'));

// Marketplace (Tasks 25-26)
export const TemplateMarketplace = lazy(() => import('@/pages/marketplace/TemplateMarketplace'));
export const TemplatePreview = lazy(() => import('@/pages/marketplace/TemplatePreview'));

// Intelligence (Task 30)
export const IntelligenceDashboard = lazy(() => import('@/pages/intelligence/IntelligenceDashboard'));

// Integrations Radar (Task 31)
export const IntegrationsRadar = lazy(() => import('@/pages/integrations/IntegrationsRadar'));

/**
 * Rotas para adicionar ao router:
 * 
 * // Contextual Interfaces
 * { path: '/dashboard/agents/renus', element: <RenusInterface /> }
 * { path: '/dashboard/agents/pesquisas', element: <PesquisasInterface /> }
 * { path: '/dashboard/agents/isa', element: <IsaInterface /> }
 * 
 * // Marketplace
 * { path: '/dashboard/marketplace', element: <TemplateMarketplace /> }
 * { path: '/dashboard/marketplace/template/:templateId/preview', element: <TemplatePreview /> }
 * 
 * // Intelligence
 * { path: '/dashboard/intelligence', element: <IntelligenceDashboard /> }
 * 
 * // Integrations
 * { path: '/dashboard/integrations/radar', element: <IntegrationsRadar /> }
 */

export const newRoutes = [
    // Contextual Interfaces
    { path: 'agents/renus', component: 'RenusInterface' },
    { path: 'agents/pesquisas', component: 'PesquisasInterface' },
    { path: 'agents/isa', component: 'IsaInterface' },

    // Marketplace
    { path: 'marketplace', component: 'TemplateMarketplace' },
    { path: 'marketplace/template/:templateId/preview', component: 'TemplatePreview' },

    // Intelligence & Integrations
    { path: 'intelligence', component: 'IntelligenceDashboard' },
    { path: 'integrations/radar', component: 'IntegrationsRadar' }
];
