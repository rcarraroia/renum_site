import React, { createContext, useContext, useState, useMemo, useEffect } from 'react';
import { User, UserRole, AuthContextType } from '@/types/auth';
import { toast } from 'sonner';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const MOCK_ADMIN: User = {
  id: 'admin-123',
  name: 'Admin Renum',
  email: 'admin@renum.tech',
  role: 'admin',
};

const MOCK_CLIENT: User = {
  id: 'client-456',
  name: 'Client Alpha',
  email: 'client@alpha.com',
  role: 'client',
};

// Function to simulate checking local storage for a session
const getInitialUser = (): User | null => {
    if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('renum_user');
        if (storedUser) {
            try {
                return JSON.parse(storedUser) as User;
            } catch (e) {
                console.error("Failed to parse stored user:", e);
                return null;
            }
        }
    }
    return null;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(getInitialUser());
  const [isLoading, setIsLoading] = useState(false); // Set to false initially since we check local storage synchronously

  const isAuthenticated = !!user;
  const role: UserRole = user?.role || 'guest';

  useEffect(() => {
    // Persist user state to local storage whenever it changes
    if (user) {
        localStorage.setItem('renum_user', JSON.stringify(user));
    } else {
        localStorage.removeItem('renum_user');
    }
    console.log(`[Auth] State updated. Authenticated: ${isAuthenticated}, Role: ${role}`);
  }, [user, isAuthenticated, role]);


  const login = async (email: string, password: string) => {
    setIsLoading(true);
    console.log(`[Auth] Attempting login for: ${email}`);
    
    try {
      // Chamar API real do backend
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        toast.error(error.detail || 'Credenciais inválidas');
        setIsLoading(false);
        return;
      }

      const data = await response.json();
      
      // Mapear resposta do backend para formato do frontend
      const loggedInUser: User = {
        id: data.user.id,
        name: data.user.name || `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim() || data.user.email,
        email: data.user.email,
        role: data.user.role as UserRole,
      };

      // Salvar token
      localStorage.setItem('renum_token', data.access_token);
      
      setUser(loggedInUser);
      toast.success(`Bem-vindo, ${loggedInUser.name}!`);
    } catch (error) {
      console.error('[Auth] Login error:', error);
      toast.error('Erro ao conectar com o servidor');
    }
    
    setIsLoading(false);
  };

  const logout = () => {
    console.log("[Auth] Logging out.");
    localStorage.removeItem('renum_token');
    setUser(null);
    toast.info('Sessão encerrada.');
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