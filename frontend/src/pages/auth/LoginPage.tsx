import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Navigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import RenumLogo from '@/components/RenumLogo';
import { Zap } from 'lucide-react';

const LoginPage: React.FC = () => {
  const { isAuthenticated, role, login, isLoading } = useAuth();
  const [email, setEmail] = useState('admin@renum.tech');
  const [password, setPassword] = useState('password');

  if (isAuthenticated) {
    const redirectPath = role === 'admin' ? '/dashboard/admin' : '/dashboard/client';
    return <Navigate to={redirectPath} replace />;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <RenumLogo />
          <CardTitle className="text-2xl mt-4">Acesso ao Dashboard</CardTitle>
          <CardDescription>
            Entre com suas credenciais para acessar o portal.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <Button type="submit" className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80]" disabled={isLoading}>
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>
          <div className="mt-6 text-center text-sm text-muted-foreground">
            <p>Use: admin@renum.tech ou client@alpha.com</p>
            <p>Senha: password</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;