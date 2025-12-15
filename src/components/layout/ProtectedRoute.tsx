import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types/auth';
import LoadingScreen from './LoadingScreen';

interface ProtectedRouteProps {
  allowedRoles?: UserRole[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedRoles }) => {
  const { isAuthenticated, role, isLoading } = useAuth();

  if (isLoading) {
    // Show loading screen while checking auth
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  // Se usuário admin acessar raiz, redirecionar para dashboard admin
  if (role === 'admin' && window.location.pathname === '/') {
    return <Navigate to="/dashboard/admin" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    // Redirect unauthorized users (e.g., client trying to access admin)
    // Redirect to their respective overview page if they are authenticated but unauthorized for this specific route
    const unauthorizedRedirect = role === 'client' ? '/dashboard/client' : '/dashboard/admin';
    return <Navigate to={unauthorizedRedirect} replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;