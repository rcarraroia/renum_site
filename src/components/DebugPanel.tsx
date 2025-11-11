import React from 'react';
import { useAuth } from '@/context/AuthContext';
import { useLocation, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, CheckCircle, XCircle, Settings, Wrench } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';

const DebugPanel: React.FC = () => {
  const { isAuthenticated, role, user, login, logout } = useAuth();
  const location = useLocation();

  const handleBypassLogin = (targetRole: 'admin' | 'client') => {
    // Mock login function for quick access
    if (targetRole === 'admin') {
        login('admin@renum.tech', 'password');
    } else {
        login('client@alpha.com', 'password');
    }
  };

  return (
    <div className="fixed bottom-4 left-4 z-[100] w-72">
      <Card className="shadow-2xl border-2 border-[#FF6B35] dark:border-[#0ca7d2]">
        <CardHeader className="p-3 pb-1">
          <CardTitle className="text-sm flex items-center text-[#FF6B35]">
            <Wrench className="h-4 w-4 mr-2" /> Painel de Debug
          </CardTitle>
        </CardHeader>
        <CardContent className="p-3 text-xs space-y-2">
          
          {/* Auth Status */}
          <div className="flex items-center space-x-2">
            {isAuthenticated ? (
              <CheckCircle className="h-4 w-4 text-green-500" />
            ) : (
              <XCircle className="h-4 w-4 text-red-500" />
            )}
            <span className="font-semibold">Auth: {isAuthenticated ? 'Autenticado' : 'Não Autenticado'}</span>
          </div>
          <p>Função: <span className="font-mono text-[#4e4ea8] dark:text-[#0ca7d2]">{role.toUpperCase()}</span></p>
          <p>Rota: <span className="font-mono text-muted-foreground">{location.pathname}</span></p>
          
          <Separator className="my-2" />

          {/* Quick Access */}
          <h4 className="font-semibold text-xs mb-2">Acesso Rápido (Dev)</h4>
          <div className="space-y-2">
            {!isAuthenticated && (
                <div className="flex space-x-2">
                    <Button size="sm" className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80]" onClick={() => handleBypassLogin('admin')}>
                        Login Admin
                    </Button>
                    <Button size="sm" variant="secondary" onClick={() => handleBypassLogin('client')}>
                        Login Client
                    </Button>
                </div>
            )}
            {isAuthenticated && (
                <div className="space-y-1">
                    <Link to="/dashboard/admin/renus-config">
                        <Button size="sm" variant="outline" className="w-full justify-start">
                            <Settings className="h-4 w-4 mr-2" /> Config Renus
                        </Button>
                    </Link>
                    <Button size="sm" variant="destructive" className="w-full" onClick={logout}>
                        <XCircle className="h-4 w-4 mr-2" /> Logout
                    </Button>
                </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DebugPanel;