import React from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import DashboardHeader from '@/components/dashboard/DashboardHeader';
import { useAuth } from '@/context/AuthContext';
import { Navigate } from 'react-router-dom';
import { AssistenteIsaWidget } from '@/components/AssistenteIsaWidget';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    // Should be handled by ProtectedRoute, but good fallback
    return <Navigate to="/auth/login" replace />;
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <div className="hidden md:flex flex-shrink-0">
        <Sidebar />
      </div>
      <div className="flex flex-col flex-grow overflow-hidden">
        <DashboardHeader />
        <main className="flex-grow overflow-y-auto p-4 md:p-8">
          {children}
        </main>
      </div>
      {user?.role === 'admin' && <AssistenteIsaWidget />}
    </div>
  );
};

export default DashboardLayout;