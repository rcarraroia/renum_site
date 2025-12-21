
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, useLocation, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import { ThemeProvider } from "./context/ThemeContext";
import { RenusChatProvider } from "./context/RenusChatContext";
import RenusPage from "./pages/RenusPage";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/auth/LoginPage";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import AdminOverview from "./pages/dashboard/AdminOverview";
import ClientOverview from "./pages/dashboard/ClientOverview";
import RenusConfigPage from "./pages/dashboard/RenusConfigPage";
import AdminProjectsPage from "./pages/dashboard/AdminProjectsPage";
import AdminClientsPage from "./pages/dashboard/AdminClientsPage";
import AdminConversationsPage from "./pages/dashboard/AdminConversationsPage";
import AdminReportsPage from "./pages/dashboard/AdminReportsPage";
import AdminSettingsPage from "./pages/dashboard/AdminSettingsPage";
import AdminIntegrationsPage from "./pages/dashboard/AdminIntegrationsPage";
import ClientIntegrationsPage from "./pages/dashboard/ClientIntegrationsPage";
import PesquisasEntrevistasPage from './pages/dashboard/PesquisasEntrevistasPage';
import PesquisasResultadosPage from './pages/dashboard/PesquisasResultadosPage';
import PesquisasAnalisePage from './pages/dashboard/PesquisasAnalisePage';
import AdminLeadsPage from './pages/dashboard/AdminLeadsPage';
import AssistenteIsaPage from './pages/dashboard/AssistenteIsaPage';
import AgentsListPage from './pages/admin/agents/AgentsListPage'; // Import new page
import AgentCreatePage from './pages/admin/agents/AgentCreatePage'; // Import new page
import AgentDetailsPage from './pages/admin/agents/AgentDetailsPage'; // Import updated page
import EvolutionPage from './pages/sicc/EvolutionPage'; // Import new SICC page
import MemoryManagerPage from './pages/sicc/MemoryManagerPage'; // Import new SICC page
import LearningQueuePage from './pages/sicc/LearningQueuePage'; // Import new SICC page
import SettingsPage from './pages/sicc/SettingsPage'; // Import new SICC page
import ErrorBoundary from './components/ErrorBoundary'; // Import ErrorBoundary
import TemplatesListPage from './pages/admin/agents/TemplatesListPage'; // Import Templates page
import MarketplacePage from './pages/client/MarketplacePage'; // Import Marketplace page
import CheckoutPage from './pages/client/CheckoutPage'; // Import Checkout page
import ClientAgentsPage from './pages/client/ClientAgentsPage';
import ClientAgentDetailsPage from './pages/client/ClientAgentDetailsPage';
import RenusInterface from './pages/agents/contextual/RenusInterface';
import PesquisasInterface from './pages/agents/contextual/PesquisasInterface';
import IsaInterface from './pages/agents/contextual/IsaInterface';
import IntelligenceDashboard from './pages/intelligence/IntelligenceDashboard';
import IntegrationsRadar from './pages/integrations/IntegrationsRadar';
import TemplateMarketplace from './pages/marketplace/TemplateMarketplace';

// Component to redirect authenticated users to dashboard
const HomeRedirect = () => {
  const { isAuthenticated, role } = useAuth();

  if (isAuthenticated) {
    const dashboardPath = role === 'admin' ? '/dashboard/admin' : '/dashboard/client';
    return <Navigate to={dashboardPath} replace />;
  }

  return <Index />;
};

const queryClient = new QueryClient();


const App = () => (
  <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <RenusChatProvider>
          <AuthProvider>
            <TooltipProvider>
              <Toaster />
              <Sonner />
              <BrowserRouter>
                <Routes>
                  {/* Public Routes */}
                  <Route path="/" element={<HomeRedirect />} />
                  <Route path="/renus" element={<RenusPage />} />
                  <Route path="/auth/login" element={<LoginPage />} />

                  {/* Protected Admin Routes */}
                  <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                    <Route path="/dashboard/admin" element={<AdminOverview />} />
                    {/* Admin Routes */}
                    <Route path="/dashboard/admin/projects" element={<AdminProjectsPage />} />
                    <Route path="/dashboard/admin/leads" element={<AdminLeadsPage />} />
                    <Route path="/dashboard/admin/clients" element={<AdminClientsPage />} />
                    <Route path="/dashboard/admin/clients/:id" element={<AdminClientsPage />} />

                    {/* Agent Routes */}
                    <Route path="/dashboard/admin/agents" element={<AgentsListPage />} />
                    <Route path="/dashboard/admin/agents/create" element={<AgentCreatePage />} />
                    <Route path="/dashboard/admin/agents/:slug" element={<AgentDetailsPage />} />
                    <Route path="/dashboard/admin/agents/templates" element={<TemplatesListPage />} />

                    <Route path="/dashboard/admin/conversations" element={<AdminConversationsPage />} />
                    <Route path="/dashboard/admin/reports" element={<AdminReportsPage />} />
                    <Route path="/dashboard/admin/integrations" element={<AdminIntegrationsPage />} />

                    {/* Global Config */}
                    <Route path="/dashboard/admin/renus-config" element={<RenusConfigPage />} />

                    <Route path="/dashboard/admin/pesquisas/entrevistas" element={<PesquisasEntrevistasPage />} />
                    <Route path="/dashboard/admin/pesquisas/resultados" element={<PesquisasResultadosPage />} />
                    <Route path="/dashboard/admin/pesquisas/analise" element={<PesquisasAnalisePage />} />
                    <Route path="/dashboard/admin/assistente-isa" element={<AssistenteIsaPage />} />

                    {/* Contextual Interfaces */}
                    <Route path="/dashboard/agents/renus" element={<RenusInterface />} />
                    <Route path="/dashboard/agents/pesquisas" element={<PesquisasInterface />} />
                    <Route path="/dashboard/agents/isa" element={<IsaInterface />} />

                    {/* Intelligence & Integrations */}
                    <Route path="/dashboard/intelligence" element={<IntelligenceDashboard />} />
                    <Route path="/dashboard/integrations/radar" element={<IntegrationsRadar />} />

                    {/* Marketplace */}
                    <Route path="/dashboard/marketplace" element={<TemplateMarketplace />} />

                    {/* SICC Routes */}
                    <Route path="/intelligence/evolution" element={<EvolutionPage />} />
                    <Route path="/intelligence/memories" element={<MemoryManagerPage />} />
                    <Route path="/intelligence/queue" element={<LearningQueuePage />} />
                    <Route path="/intelligence/settings" element={<SettingsPage />} />
                  </Route>

                  {/* Protected Client Routes */}
                  <Route element={<ProtectedRoute allowedRoles={['client']} />}>
                    <Route path="/dashboard/client" element={<ClientOverview />} />
                    {/* Client Routes */}
                    <Route path="/dashboard/client/projects" element={<ClientOverview />} />
                    <Route path="/dashboard/client/agents" element={<ClientAgentsPage />} />
                    <Route path="/dashboard/client/agents/:slug" element={<ClientAgentDetailsPage />} />
                    <Route path="/dashboard/client/conversations" element={<ClientOverview />} />
                    <Route path="/dashboard/client/documents" element={<ClientOverview />} />
                    <Route path="/dashboard/client/calendar" element={<ClientOverview />} />
                    <Route path="/dashboard/client/support" element={<ClientOverview />} />
                    <Route path="/dashboard/client/integrations" element={<ClientIntegrationsPage />} />

                    {/* Marketplace Routes */}
                    <Route path="/marketplace" element={<MarketplacePage />} />
                    <Route path="/checkout" element={<CheckoutPage />} />
                  </Route>

                  {/* Common Protected Routes */}
                  <Route element={<ProtectedRoute allowedRoles={['admin', 'client']} />}>
                    <Route path="/dashboard/settings" element={<AdminSettingsPage />} /> {/* Rota de Configurações */}
                  </Route>

                  {/* Catch-all Route */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </BrowserRouter>
            </TooltipProvider>
          </AuthProvider>
        </RenusChatProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </ErrorBoundary>
);

export default App;