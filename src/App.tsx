import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import { ThemeProvider } from "./context/ThemeContext";
import { RenusChatProvider } from "./context/RenusChatContext";
import RenusPage from "./pages/RenusPage";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/auth/LoginPage";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import AdminOverview from "./pages/dashboard/AdminOverview";
import ClientOverview from "./pages/dashboard/ClientOverview";
import RenusConfigPage from "./pages/dashboard/RenusConfigPage";
import DebugPanel from "./components/DebugPanel";
import AdminProjectsPage from "./pages/dashboard/AdminProjectsPage";
import AdminClientsPage from "./pages/dashboard/AdminClientsPage";
import AdminConversationsPage from "./pages/dashboard/AdminConversationsPage";
import AdminReportsPage from "./pages/dashboard/AdminReportsPage";
import AdminSettingsPage from "./pages/dashboard/AdminSettingsPage";
import PesquisasEntrevistasPage from './pages/dashboard/PesquisasEntrevistasPage';
import PesquisasResultadosPage from './pages/dashboard/PesquisasResultadosPage';
import PesquisasAnalisePage from './pages/dashboard/PesquisasAnalisePage';
import AdminLeadsPage from './pages/dashboard/AdminLeadsPage';
import AssistenteIsaPage from './pages/dashboard/AssistenteIsaPage';
import AgentsListPage from './pages/admin/agents/AgentsListPage'; // Import new page
import AgentCreatePage from './pages/admin/agents/AgentCreatePage'; // Import new page
import AgentDetailsPage from './pages/admin/agents/AgentDetailsPage'; // Import updated page

const queryClient = new QueryClient();

// Component to conditionally render the DebugPanel
const DebugWrapper = () => {
  const location = useLocation();
  const isDashboard = location.pathname.startsWith('/dashboard');
  const isAuthPage = location.pathname.startsWith('/auth');

  if (isDashboard || isAuthPage) {
    return <DebugPanel />;
  }
  return null;
};


const App = () => (
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
                <Route path="/" element={<Index />} />
                <Route path="/renus" element={<RenusPage />} />
                <Route path="/auth/login" element={<LoginPage />} />

                {/* Protected Admin Routes */}
                <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                  <Route path="/dashboard/admin" element={<AdminOverview />} />
                  {/* Admin Routes */}
                  <Route path="/dashboard/admin/projects" element={<AdminProjectsPage />} />
                  <Route path="/dashboard/admin/leads" element={<AdminLeadsPage />} />
                  <Route path="/dashboard/admin/clients" element={<AdminClientsPage />} />
                  
                  {/* Agent Routes */}
                  <Route path="/dashboard/admin/agents" element={<AgentsListPage />} />
                  <Route path="/dashboard/admin/agents/create" element={<AgentCreatePage />} />
                  <Route path="/dashboard/admin/agents/:id" element={<AgentDetailsPage />} />
                  <Route path="/dashboard/admin/agents/templates" element={<AdminOverview />} /> {/* Mock route for templates */}
                  
                  <Route path="/dashboard/admin/conversations" element={<AdminConversationsPage />} />
                  <Route path="/dashboard/admin/reports" element={<AdminReportsPage />} />
                  
                  {/* Global Config */}
                  <Route path="/dashboard/admin/renus-config" element={<RenusConfigPage />} />
                  
                  <Route path="/dashboard/admin/pesquisas/entrevistas" element={<PesquisasEntrevistasPage />} />
                  <Route path="/dashboard/admin/pesquisas/resultados" element={<PesquisasResultadosPage />} />
                  <Route path="/dashboard/admin/pesquisas/analise" element={<PesquisasAnalisePage />} />
                  <Route path="/dashboard/admin/assistente-isa" element={<AssistenteIsaPage />} />
                </Route>

                {/* Protected Client Routes */}
                <Route element={<ProtectedRoute allowedRoles={['client']} />}>
                  <Route path="/dashboard/client" element={<ClientOverview />} />
                  {/* Client Routes */}
                  <Route path="/dashboard/client/projects" element={<ClientOverview />} />
                  <Route path="/dashboard/client/conversations" element={<ClientOverview />} />
                  <Route path="/dashboard/client/documents" element={<ClientOverview />} />
                  <Route path="/dashboard/client/calendar" element={<ClientOverview />} />
                  <Route path="/dashboard/client/support" element={<ClientOverview />} />
                </Route>

                {/* Common Protected Routes */}
                <Route element={<ProtectedRoute allowedRoles={['admin', 'client']} />}>
                  <Route path="/dashboard/settings" element={<AdminSettingsPage />} /> {/* Rota de Configurações */}
                </Route>

                {/* Catch-all Route */}
                <Route path="*" element={<NotFound />} />
              </Routes>
              <DebugWrapper />
            </BrowserRouter>
          </TooltipProvider>
        </AuthProvider>
      </RenusChatProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;