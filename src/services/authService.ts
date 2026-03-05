// resource_id: e47e2c07-9c65-4654-832f-37235dc397de
/**
 * Authentication Service
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Frontend API client for authentication operations.
 * Connects React components to Flask backend authentication APIs.
 */

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';
const API_TIMEOUT = 10000; // 10 seconds

// Types for API requests and responses
interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
}

interface FirebaseLoginRequest {
  id_token: string;
}

interface AuthResponse {
  success: boolean;
  message?: string;
  user?: {
    id: number;
    username: string;
    email: string;
    auth_provider?: 'local' | 'google';
    created_at?: string;
    last_login?: string;
  };
  session?: {
    token: string;
    expires_at: string;
  };
  errors?: string[];
  field_errors?: Record<string, string[]>;
}

interface SessionValidationResponse {
  valid: boolean;
  user?: {
    id: number;
    username: string;
    email: string;
    auth_provider?: 'local' | 'google';
    created_at?: string;
    last_login?: string;
  };
  session?: {
    expires_at: string;
  };
  errors?: string[];
}

interface FirebaseConfigResponse {
  apiKey: string;
  authDomain: string;
  projectId: string;
  storageBucket: string;
  messagingSenderId: string;
  appId: string;
}

// HTTP client with timeout and error handling
class APIClient {
  private baseURL: string;
  private timeout: number;

  constructor(baseURL: string, timeout: number = API_TIMEOUT) {
    this.baseURL = baseURL;
    this.timeout = timeout;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        // Try to parse error response
        try {
          const errorData = await response.json();
          throw new APIError(
            errorData.message || `HTTP ${response.status}`,
            response.status,
            errorData
          );
        } catch (parseError) {
          throw new APIError(
            `HTTP ${response.status}: ${response.statusText}`,
            response.status
          );
        }
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof APIError) {
        throw error;
      }
      
      if (error.name === 'AbortError') {
        throw new APIError('Request timed out', 0);
      }
      
      if (!navigator.onLine) {
        throw new APIError('No internet connection', 0);
      }
      
      throw new APIError(
        error.message || 'Network request failed',
        0
      );
    }
  }

  async post<T>(endpoint: string, data?: any, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      headers,
    });
  }

  async get<T>(endpoint: string, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'GET',
      headers,
    });
  }
}

// Custom API Error class
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Authentication API service
class AuthenticationService {
  private client: APIClient;

  constructor() {
    this.client = new APIClient(API_BASE_URL);
  }

  /**
   * Login with email and password
   */
  async login(email: string, password: string, rememberMe?: boolean): Promise<{ success: boolean; data?: any; error?: string }> {
    try {
      const response = await this.client.post<any>('/auth/login', {
        email,
        password,
        remember_me: rememberMe || false
      });
      
      // Flask backend returns direct success/error format
      if (response.success) {
        return {
          success: true,
          data: {
            user: response.user,
            token: response.token
          }
        };
      }
      
      return {
        success: false,
        error: response.message || response.error || 'Login failed'
      };
    } catch (error) {
      console.error('Login API error:', error);
      
      if (error instanceof APIError) {
        return {
          success: false,
          error: error.data?.message || error.message
        };
      }
      
      return {
        success: false,
        error: 'Login failed. Please check your connection and try again.'
      };
    }
  }

  /**
   * Register new user account
   */
  async register(data: { username: string; email: string; password: string }): Promise<{ success: boolean; data?: any; error?: string }> {
    try {
      const response = await this.client.post<any>('/auth/register', {
        username: data.username,
        email: data.email,
        password: data.password,
        confirm_password: data.password
      });
      
      if (response.success) {
        return {
          success: true,
          data: {
            user: response.user,
            token: response.token
          }
        };
      }
      
      return {
        success: false,
        error: response.message || response.error || 'Registration failed'
      };
    } catch (error) {
      console.error('Registration API error:', error);
      
      if (error instanceof APIError) {
        return {
          success: false,
          error: error.data?.message || error.message
        };
      }
      
      return {
        success: false,
        error: 'Registration failed. Please check your connection and try again.'
      };
    }
  }

  /**
   * Login with Firebase/Google OAuth
   */
  async loginWithFirebase(): Promise<{ success: boolean; data?: any; error?: string }> {
    try {
      // For now, return mock Firebase login - this would be implemented with actual Firebase SDK
      return {
        success: false,
        error: 'Firebase authentication not yet implemented'
      };
    } catch (error) {
      console.error('Firebase login error:', error);
      return {
        success: false,
        error: 'Google Sign-In failed. Please check your connection and try again.'
      };
    }
  }

  /**
   * Validate current session token
   */
  async validateSession(token: string): Promise<{ valid: boolean; user?: any; error?: string }> {
    try {
      const response = await this.client.get<any>('/auth/validate', {
        'Authorization': `Bearer ${token}`
      });
      
      if (response.success) {
        return {
          valid: true,
          user: response.user
        };
      }
      
      return {
        valid: false,
        error: response.message || 'Session invalid'
      };
    } catch (error) {
      console.error('Session validation API error:', error);
      
      return {
        valid: false,
        error: 'Session validation failed'
      };
    }
  }

  /**
   * Logout and invalidate session
   */
  async logout(token?: string): Promise<{ success: boolean; message?: string }> {
    try {
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await this.client.post<any>('/auth/logout', {}, headers);
      
      return {
        success: response.success || true,
        message: response.message || 'Logged out successfully'
      };
    } catch (error) {
      console.error('Logout API error:', error);
      
      // Logout should succeed even if server request fails
      return {
        success: true,
        message: 'Logged out locally (server logout may have failed)'
      };
    }
  }

  /**
   * Get Firebase configuration for client-side OAuth
   */
  async getFirebaseConfig(): Promise<FirebaseConfigResponse | null> {
    try {
      return await this.client.get<FirebaseConfigResponse>('/auth/firebase-config');
    } catch (error) {
      console.warn('Firebase config unavailable:', error);
      return null;
    }
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<{ success: boolean; message?: string; errors?: string[] }> {
    try {
      return await this.client.post('/auth/password-reset', { email });
    } catch (error) {
      console.error('Password reset API error:', error);
      
      if (error instanceof APIError) {
        return {
          success: false,
          errors: [error.message]
        };
      }
      
      return {
        success: false,
        errors: ['Password reset request failed. Please try again.']
      };
    }
  }

  /**
   * Change password
   */
  async changePassword(data: { currentPassword: string; newPassword: string }): Promise<{ success: boolean; error?: string }> {
    try {
      // For now, return mock response - this would be implemented with actual API call
      return {
        success: false,
        error: 'Password change not yet implemented'
      };
    } catch (error) {
      console.error('Change password API error:', error);
      return {
        success: false,
        error: 'Password change failed. Please try again.'
      };
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(data: { username: string; email: string }): Promise<{ success: boolean; data?: any; error?: string }> {
    try {
      // For now, return mock response - this would be implemented with actual API call
      return {
        success: false,
        error: 'Profile update not yet implemented'
      };
    } catch (error) {
      console.error('Profile update API error:', error);
      return {
        success: false,
        error: 'Profile update failed. Please try again.'
      };
    }
  }

  /**
   * Delete user account
   */
  async deleteAccount(): Promise<{ success: boolean; error?: string }> {
    try {
      // For now, return mock response - this would be implemented with actual API call
      return {
        success: false,
        error: 'Account deletion not yet implemented'
      };
    } catch (error) {
      console.error('Account deletion API error:', error);
      return {
        success: false,
        error: 'Account deletion failed. Please try again.'
      };
    }
  }
}

// Export singleton instance
export const authAPI = new AuthenticationService();
export const authService = authAPI; // Alias for compatibility

// Export types for use in components
export type {
  AuthResponse,
  SessionValidationResponse,
  FirebaseConfigResponse,
  LoginRequest,
  RegisterRequest,
  FirebaseLoginRequest
};

// Export error class for custom error handling
export { APIError };

export default authAPI;
