import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingOverlay } from './LoadingSpinner';

interface PublicRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export const PublicRoute: React.FC<PublicRouteProps> = ({ 
  children, 
  redirectTo = '/dashboard' 
}) => {
  const { isAuthenticated, isLoading, isInitialized } = useAuth();

  // Show loading while checking authentication
  if (!isInitialized || isLoading) {
    return (
      <LoadingOverlay 
        isVisible={true} 
        text="Loading..." 
      />
    );
  }

  // Redirect to dashboard if already authenticated
  if (isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  // Render public content
  return <>{children}</>;
};