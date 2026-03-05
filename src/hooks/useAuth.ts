// resource_id: 7692e6e0-dc61-4c7e-a95b-bc63fce90c3a
/**
 * Authentication Hook
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Provides authentication utilities and helper functions.
 * Extends the basic useAuth hook from AuthContext with additional features.
 */

import { useCallback, useEffect, useState } from 'react';
import { useAuth as useAuthContext } from '../contexts/AuthContext';

// Additional hook for authentication utilities
export function useAuthHelpers() {
  const auth = useAuthContext();
  const [sessionTimeRemaining, setSessionTimeRemaining] = useState<number | null>(null);

  // Calculate remaining session time
  const updateSessionTime = useCallback(() => {
    if (auth.sessionExpiry) {
      const now = new Date().getTime();
      const expiry = auth.sessionExpiry.getTime();
      const remaining = expiry - now;
      setSessionTimeRemaining(Math.max(0, remaining));
    } else {
      setSessionTimeRemaining(null);
    }
  }, [auth.sessionExpiry]);

  // Update session time every minute
  useEffect(() => {
    updateSessionTime();
    
    const interval = setInterval(updateSessionTime, 60000); // Every minute
    return () => clearInterval(interval);
  }, [updateSessionTime]);

  // Format remaining time
  const formatSessionTime = useCallback((milliseconds: number): string => {
    const hours = Math.floor(milliseconds / (1000 * 60 * 60));
    const minutes = Math.floor((milliseconds % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
      return `${minutes}m`;
    } else {
      return 'Expiring soon';
    }
  }, []);

  // Check if session is expiring soon (within 5 minutes)
  const isSessionExpiringSoon = useCallback((): boolean => {
    if (!sessionTimeRemaining) return false;
    return sessionTimeRemaining <= 5 * 60 * 1000; // 5 minutes in milliseconds
  }, [sessionTimeRemaining]);

  // Get user initials for avatar
  const getUserInitials = useCallback((): string => {
    if (!auth.user) return '';
    
    const { username, email } = auth.user;
    
    if (username) {
      return username.slice(0, 2).toUpperCase();
    } else if (email) {
      return email.slice(0, 2).toUpperCase();
    }
    
    return 'U';
  }, [auth.user]);

  // Get user display name
  const getUserDisplayName = useCallback((): string => {
    if (!auth.user) return '';
    
    return auth.user.username || auth.user.email || 'User';
  }, [auth.user]);

  // Check if user is using Google auth
  const isGoogleUser = useCallback((): boolean => {
    return auth.user?.auth_provider === 'google';
  }, [auth.user]);

  // Format last login time
  const getLastLoginFormatted = useCallback((): string | null => {
    if (!auth.user?.last_login) return null;
    
    try {
      const lastLogin = new Date(auth.user.last_login);
      const now = new Date();
      const diffMs = now.getTime() - lastLogin.getTime();
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      
      if (diffDays > 0) {
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
      } else if (diffHours > 0) {
        return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
      } else if (diffMinutes > 0) {
        return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
      } else {
        return 'Just now';
      }
    } catch (error) {
      return null;
    }
  }, [auth.user?.last_login]);

  return {
    ...auth,
    sessionTimeRemaining,
    formatSessionTime,
    isSessionExpiringSoon,
    getUserInitials,
    getUserDisplayName,
    isGoogleUser,
    getLastLoginFormatted,
  };
}

// Hook for route protection
export function useRequireAuth(redirectTo: string = '/login') {
  const { isAuthenticated, isInitialized, isLoading } = useAuthContext();

  useEffect(() => {
    if (isInitialized && !isLoading && !isAuthenticated) {
      window.location.href = redirectTo;
    }
  }, [isAuthenticated, isInitialized, isLoading, redirectTo]);

  return { isAuthenticated, isInitialized, isLoading };
}

// Hook for guest-only pages (login, register)
export function useRequireGuest(redirectTo: string = '/dashboard') {
  const { isAuthenticated, isInitialized, isLoading } = useAuthContext();

  useEffect(() => {
    if (isInitialized && !isLoading && isAuthenticated) {
      window.location.href = redirectTo;
    }
  }, [isAuthenticated, isInitialized, isLoading, redirectTo]);

  return { isAuthenticated, isInitialized, isLoading };
}

// Hook for handling authentication actions
export function useAuthActions() {
  const auth = useAuthContext();
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  // Enhanced login with loading state
  const handleLogin = useCallback(async (
    email: string,
    password: string,
    rememberMe: boolean = false
  ): Promise<boolean> => {
    setIsActionLoading(true);
    setActionError(null);

    try {
      const success = await auth.login(email, password, rememberMe);
      if (!success && auth.error) {
        setActionError(auth.error);
      }
      return success;
    } catch (error) {
      setActionError('Login failed. Please try again.');
      return false;
    } finally {
      setIsActionLoading(false);
    }
  }, [auth]);

  // Enhanced registration with loading state
  const handleRegister = useCallback(async (
    username: string,
    email: string,
    password: string,
    confirmPassword: string
  ): Promise<boolean> => {
    setIsActionLoading(true);
    setActionError(null);

    try {
      const success = await auth.register(username, email, password, confirmPassword);
      if (!success && auth.error) {
        setActionError(auth.error);
      }
      return success;
    } catch (error) {
      setActionError('Registration failed. Please try again.');
      return false;
    } finally {
      setIsActionLoading(false);
    }
  }, [auth]);

  // Enhanced Google login with loading state
  const handleGoogleLogin = useCallback(async (idToken: string): Promise<boolean> => {
    setIsActionLoading(true);
    setActionError(null);

    try {
      const success = await auth.loginWithGoogle(idToken);
      if (!success && auth.error) {
        setActionError(auth.error);
      }
      return success;
    } catch (error) {
      setActionError('Google Sign-In failed. Please try again.');
      return false;
    } finally {
      setIsActionLoading(false);
    }
  }, [auth]);

  // Enhanced logout with loading state
  const handleLogout = useCallback(async (): Promise<void> => {
    setIsActionLoading(true);
    setActionError(null);

    try {
      await auth.logout();
    } catch (error) {
      setActionError('Logout failed. Please try again.');
    } finally {
      setIsActionLoading(false);
    }
  }, [auth]);

  // Clear action error
  const clearActionError = useCallback(() => {
    setActionError(null);
  }, []);

  return {
    handleLogin,
    handleRegister,
    handleGoogleLogin,
    handleLogout,
    isActionLoading,
    actionError,
    clearActionError,
  };
}

// Re-export the basic useAuth hook
export { useAuth } from '../contexts/AuthContext';

export default useAuthHelpers;