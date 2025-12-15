import React, { createContext, useContext, useState, useMemo, useEffect } from 'react';
import { User, UserRole, AuthContextType } from '@/types/auth';
import { toast } from 'sonner';
import { apiClient } from '@/services/api';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Function to get initial user from localStorage if valid
const getInitialUser = (): User | null => {
  if (typeof window !== 'undefined') {
    const storedUser = localStorage.getItem('renum_user');
    const storedToken = localStorage.getItem('renum_token');

    if (storedUser && storedToken) {
      try {
        const parsedUser = JSON.parse(storedUser);
        console.log('[Auth] Usuário restaurado do localStorage:', parsedUser.email);
        return parsedUser;
      } catch (e) {
        console.error('[Auth] Erro ao parsear usuário do storage', e);
        localStorage.removeItem('renum_user');
        localStorage.removeItem('renum_token');
      }
    }
  }
  return null;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(getInitialUser);
  const [isLoading, setIsLoading] = useState(false);

  const isAuthenticated = !!user;
  const role: UserRole = user?.role || 'guest';

  // Sincronizar localStorage quando user mudar
  useEffect(() => {
    if (user) {
      localStorage.setItem('renum_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('renum_user');
      // Nota: renum_token é gerido no login/logout explicitamente
    }
    console.log(`[Auth] State updated. Authenticated: ${isAuthenticated}, Role: ${role}`);
  }, [user, isAuthenticated, role]);


  const login = async (email: string, password: string) => {
    setIsLoading(true);
    console.log(`[Auth] Attempting login for: ${email}`);

    try {
      // Login real via API
      const response = await apiClient.post<any>('/auth/login', { email, password });
      const data = response.data;

      const { access_token, user: userData } = data;

      if (!access_token || !userData) {
        throw new Error('Resposta de login inválida');
      }

      // Mapear resposta do backend para tipo User do frontend
      const loggedInUser: User = {
        id: userData.id,
        name: `${userData.first_name || ''} ${userData.last_name || ''}`.trim() || userData.email,
        email: userData.email,
        role: (userData.role as UserRole) || 'client',
        avatar: userData.avatar_url
      };

      // Salvar token e usuário
      localStorage.setItem('renum_token', access_token);
      setUser(loggedInUser);

      toast.success(`Bem-vindo, ${loggedInUser.name}!`);
      console.log('[Auth] Login successful');

      // Redirecionar para dashboard se estiver na pagina de login
      // Redirecionar para dashboard se estiver na pagina de login
      if (window.location.pathname.includes('/login')) {
        const dashboardPath = loggedInUser.role === 'admin' ? '/dashboard/admin' : '/dashboard/client';
        window.location.href = dashboardPath;
      }

    } catch (error: any) {
      console.error('[Auth] Login error:', error);
      const msg = error.response?.data?.detail || 'Erro ao realizar login. Verifique suas credenciais.';
      toast.error(msg);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    console.log("[Auth] Logging out.");
    localStorage.removeItem('renum_token');
    localStorage.removeItem('renum_user');
    setUser(null);
    toast.info('Sessão encerrada.');
    window.location.href = '/auth/login';
  };

  const value = useMemo(() => ({
    user,
    isAuthenticated,
    role,
    login,
    logout,
    isLoading,
  }), [user, isLoading, isAuthenticated, role]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};