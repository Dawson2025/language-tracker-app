/**
 * Authentication Context
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Provides global authentication state management for the application.
 * Implements session persistence, automatic token validation, and logout functionality.
 */

import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { authAPI } from '../services/authService';

// Types
interface User {
  id: number;
  username: string;
  email: string;
  auth_provider?: 'local' | 'google';
  created_at?: string;
  last_login?: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isInitialized: boolean;
  error: string | null;
  sessionExpiry: Date | null;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string, rememberMe?: boolean) => Promise<boolean>;
  loginWithGoogle: (idToken: string) => Promise<boolean>;
  register: (username: string, email: string, password: string, confirmPassword: string) => Promise<boolean>;
  logout: () => Promise<void>;
  validateSession: () => Promise<boolean>;
  clearError: () => void;
  refreshUser: () => Promise<void>;
}

// Action types
type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: { user: User; sessionExpiry?: Date } }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' }
  | { type: 'SET_INITIALIZED' }
  | { type: 'UPDATE_USER'; payload: User };

// Initial state
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  isInitialized: false,
  error: null,
  sessionExpiry: null,
};

// Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };

    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
        sessionExpiry: action.payload.sessionExpiry || null,
      };

    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
        sessionExpiry: null,
      };

    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        sessionExpiry: null,
      };

    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };

    case 'SET_INITIALIZED':
      return {
        ...state,
        isInitialized: true,
        isLoading: false,
      };

    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };

    default:
      return state;
  }
}

// Context
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// Provider props
interface AuthProviderProps {
  children: React.ReactNode;
}

// Provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Token management
  const getStoredToken = useCallback((): string | null => {
    return localStorage.getItem('auth_token');
  }, []);

  const setStoredToken = useCallback((token: string): void => {
    localStorage.setItem('auth_token', token);
  }, []);

  const removeStoredToken = useCallback((): void => {
    localStorage.removeItem('auth_token');
  }, []);

  // Session validation
  const validateSession = useCallback(async (): Promise<boolean> => {
    const token = getStoredToken();
    
    if (!token) {
      return false;
    }

    try {
      const response = await authAPI.validateSession(token);
      
      if (response.valid && response.user) {
        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: response.user,
            sessionExpiry: null // We'll implement session expiry later
          }
        });
        
        return true;
      } else {
        // Invalid session - remove token
        removeStoredToken();
        dispatch({ type: 'AUTH_FAILURE', payload: response.error || 'Session expired' });
        return false;
      }
    } catch (error) {
      console.error('Session validation error:', error);
      removeStoredToken();
      dispatch({ type: 'AUTH_FAILURE', payload: 'Session validation failed' });
      return false;
    }
  }, [getStoredToken, removeStoredToken]);

  // Login function
  const login = useCallback(async (
    email: string, 
    password: string, 
    rememberMe: boolean = false
  ): Promise<boolean> => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await authAPI.login(email, password, rememberMe);

      if (response.success && response.data?.token) {
        setStoredToken(response.data.token);

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: response.data.user,
            sessionExpiry: null // We'll implement session expiry later
          }
        });

        return true;
      } else {
        const errorMessage = response.error || 'Login failed';
        dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      dispatch({ type: 'AUTH_FAILURE', payload: 'Login failed. Please try again.' });
      return false;
    }
  }, [setStoredToken]);

  // Google login function
  const loginWithGoogle = useCallback(async (idToken: string): Promise<boolean> => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await authAPI.loginWithFirebase({ id_token: idToken });

      if (response.success && response.session?.token) {
        setStoredToken(response.session.token);
        
        const sessionExpiry = response.session.expires_at 
          ? new Date(response.session.expires_at) 
          : null;

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: { ...response.user, auth_provider: 'google' },
            sessionExpiry
          }
        });

        return true;
      } else {
        const errorMessage = response.errors?.[0] || 'Google Sign-In failed';
        dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
        return false;
      }
    } catch (error) {
      console.error('Google login error:', error);
      dispatch({ type: 'AUTH_FAILURE', payload: 'Google Sign-In failed. Please try again.' });
      return false;
    }
  }, [setStoredToken]);

  // Register function
  const register = useCallback(async (
    username: string,
    email: string,
    password: string,
    confirmPassword: string
  ): Promise<boolean> => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await authAPI.register({
        username,
        email,
        password
      });

      if (response.success) {
        // If auto-login successful
        if (response.data?.token) {
          setStoredToken(response.data.token);

          dispatch({
            type: 'AUTH_SUCCESS',
            payload: {
              user: response.data.user,
              sessionExpiry: null
            }
          });
        } else {
          // Registration successful but no auto-login
          dispatch({ type: 'SET_INITIALIZED' });
        }

        return true;
      } else {
        const errorMessage = response.error || 'Registration failed';
        dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
        return false;
      }
    } catch (error) {
      console.error('Registration error:', error);
      dispatch({ type: 'AUTH_FAILURE', payload: 'Registration failed. Please try again.' });
      return false;
    }
  }, [setStoredToken]);

  // Logout function
  const logout = useCallback(async (): Promise<void> => {
    const token = getStoredToken();
    
    // Remove token immediately for responsive UI
    removeStoredToken();
    dispatch({ type: 'LOGOUT' });

    // Attempt to invalidate session on server
    if (token) {
      try {
        await authAPI.logout(token);
      } catch (error) {
        console.error('Server logout error:', error);
        // Don't throw error - local logout already successful
      }
    }
  }, [getStoredToken, removeStoredToken]);

  // Clear error function
  const clearError = useCallback((): void => {
    dispatch({ type: 'CLEAR_ERROR' });
  }, []);

  // Refresh user data
  const refreshUser = useCallback(async (): Promise<void> => {
    if (state.isAuthenticated && state.user) {
      await validateSession();
    }
  }, [state.isAuthenticated, state.user, validateSession]);

  // Initialize authentication state on app load
  useEffect(() => {
    const initializeAuth = async () => {
      const token = getStoredToken();
      
      if (token) {
        await validateSession();
      }
      
      dispatch({ type: 'SET_INITIALIZED' });
    };

    initializeAuth();
  }, [getStoredToken, validateSession]);

  // Session expiry monitoring
  useEffect(() => {
    if (state.sessionExpiry && state.isAuthenticated) {
      const checkExpiry = () => {
        const now = new Date();
        const expiry = state.sessionExpiry!;
        
        // Check if session expires within 5 minutes
        const fiveMinutes = 5 * 60 * 1000;
        const timeUntilExpiry = expiry.getTime() - now.getTime();
        
        if (timeUntilExpiry <= 0) {
          // Session expired
          logout();
        } else if (timeUntilExpiry <= fiveMinutes) {
          // Session expiring soon - could show warning or auto-refresh
          console.warn('Session expiring soon');
        }
      };

      // Check expiry every minute
      const intervalId = setInterval(checkExpiry, 60000);
      
      // Initial check
      checkExpiry();

      return () => clearInterval(intervalId);
    }
  }, [state.sessionExpiry, state.isAuthenticated, logout]);

  // Context value
  const contextValue: AuthContextValue = {
    ...state,
    login,
    loginWithGoogle,
    register,
    logout,
    validateSession,
    clearError,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use auth context
export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

// Higher-order component for route protection
export interface WithAuthProps {
  requireAuth?: boolean;
  redirectTo?: string;
  fallbackComponent?: React.ComponentType;
}

export function withAuth<P extends object>(
  Component: React.ComponentType<P>,
  options: WithAuthProps = {}
): React.ComponentType<P> {
  const { requireAuth = true, redirectTo = '/login', fallbackComponent: FallbackComponent } = options;
  
  return function AuthenticatedComponent(props: P) {
    const { isAuthenticated, isLoading, isInitialized } = useAuth();
    
    // Show loading while initializing
    if (!isInitialized || isLoading) {
      if (FallbackComponent) {
        return <FallbackComponent />;
      }
      return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
    }
    
    // Check authentication requirement
    if (requireAuth && !isAuthenticated) {
      window.location.href = redirectTo;
      return null;
    }
    
    // Render component if authenticated or auth not required
    return <Component {...props} />;
  };
}

export default AuthContext;