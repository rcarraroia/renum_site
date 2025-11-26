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
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    let loggedInUser: User | null = null;

    if (email === MOCK_ADMIN.email && password === 'password') {
      loggedInUser = MOCK_ADMIN;
    } else if (email === MOCK_CLIENT.email && password === 'password') {
      loggedInUser = MOCK_CLIENT;
    } else {
      toast.error('Credenciais inválidas. Tente admin@renum.tech ou client@alpha.com com senha: password');
    }
    
    if (loggedInUser) {
        setUser(loggedInUser);
        toast.success(`Bem-vindo, ${loggedInUser.name}!`);
    }
    setIsLoading(false);
  };

  const logout = () => {
    console.log("[Auth] Logging out.");
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