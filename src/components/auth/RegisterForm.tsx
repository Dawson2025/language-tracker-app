/**
 * Registration Form Component
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Implements US-001: User Registration with Local Credentials
 * Provides responsive, accessible registration form with real-time validation.
 */

import React, { useState, useCallback, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  validateEmail, 
  validateUsername, 
  validatePassword,
  type ValidationResult 
} from '../../utils/validation';
import { authAPI } from '../../services/authService';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { Alert } from '../common/Alert';

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface FieldErrors {
  username?: string[];
  email?: string[];
  password?: string[];
  confirmPassword?: string[];
}

interface RegisterFormProps {
  onSuccess?: (user: any) => void;
  onError?: (error: string) => void;
  redirectTo?: string;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({
  onSuccess,
  onError,
  redirectTo = '/dashboard'
}) => {
  const [formData, setFormData] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [generalErrors, setGeneralErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<ValidationResult | null>(null);

  // Real-time validation for password strength
  useEffect(() => {
    if (formData.password) {
      const strength = validatePassword(formData.password);
      setPasswordStrength(strength);
    } else {
      setPasswordStrength(null);
    }
  }, [formData.password]);

  const handleInputChange = useCallback((field: keyof RegisterFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear field-specific errors when user starts typing
    if (fieldErrors[field]) {
      setFieldErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
    
    // Clear general errors
    if (generalErrors.length > 0) {
      setGeneralErrors([]);
    }
  }, [fieldErrors, generalErrors]);

  const validateForm = useCallback((): boolean => {
    const errors: FieldErrors = {};
    let isValid = true;

    // Validate username
    if (!formData.username.trim()) {
      errors.username = ['Username is required'];
      isValid = false;
    } else {
      const usernameValidation = validateUsername(formData.username);
      if (!usernameValidation.isValid) {
        errors.username = usernameValidation.errors;
        isValid = false;
      }
    }

    // Validate email
    if (!formData.email.trim()) {
      errors.email = ['Email is required'];
      isValid = false;
    } else {
      const emailValidation = validateEmail(formData.email);
      if (!emailValidation.isValid) {
        errors.email = emailValidation.errors;
        isValid = false;
      }
    }

    // Validate password
    if (!formData.password) {
      errors.password = ['Password is required'];
      isValid = false;
    } else {
      const passwordValidation = validatePassword(formData.password);
      if (!passwordValidation.isValid) {
        errors.password = passwordValidation.errors;
        isValid = false;
      }
    }

    // Validate password confirmation
    if (!formData.confirmPassword) {
      errors.confirmPassword = ['Please confirm your password'];
      isValid = false;
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = ['Passwords do not match'];
      isValid = false;
    }

    setFieldErrors(errors);
    return isValid;
  }, [formData]);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true);
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setGeneralErrors([]);

    try {
      const response = await authAPI.register({
        username: formData.username.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password,
        confirm_password: formData.confirmPassword
      });

      if (response.success) {
        // Registration successful
        onSuccess?.(response.user);
        
        // Redirect or show success message
        if (response.session?.token) {
          // Auto-login successful
          localStorage.setItem('auth_token', response.session.token);
          window.location.href = redirectTo;
        } else {
          // Manual login required
          window.location.href = '/login?message=registration-success';
        }
      } else {
        // Handle registration errors
        if (response.field_errors) {
          setFieldErrors(response.field_errors);
        }
        if (response.errors) {
          setGeneralErrors(response.errors);
        }
        onError?.(response.errors?.[0] || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      const errorMessage = 'Registration failed. Please try again.';
      setGeneralErrors([errorMessage]);
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [formData, validateForm, onSuccess, onError, redirectTo]);

  const getPasswordStrengthColor = (score: number): string => {
    if (score <= 1) return 'text-red-600';
    if (score <= 2) return 'text-orange-600';
    if (score <= 3) return 'text-yellow-600';
    if (score <= 4) return 'text-blue-600';
    return 'text-green-600';
  };

  const getPasswordStrengthWidth = (score: number): string => {
    return `${Math.max(10, (score / 6) * 100)}%`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:underline transition ease-in-out duration-150"
            >
              sign in to your existing account
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit} noValidate>
          {/* General errors */}
          {generalErrors.length > 0 && (
            <Alert type="error" className="mb-4">
              <ul className="list-disc list-inside space-y-1">
                {generalErrors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </Alert>
          )}

          <div className="space-y-4">
            {/* Username field */}
            <div>
              <label htmlFor="username" className="sr-only">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                className={`appearance-none rounded-md relative block w-full px-3 py-2 border ${
                  fieldErrors.username ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Username"
                value={formData.username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                disabled={isLoading}
                aria-invalid={fieldErrors.username ? 'true' : 'false'}
                aria-describedby={fieldErrors.username ? 'username-error' : undefined}
              />
              {fieldErrors.username && (
                <div id="username-error" className="mt-1 text-sm text-red-600" role="alert">
                  {fieldErrors.username.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>

            {/* Email field */}
            <div>
              <label htmlFor="email" className="sr-only">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className={`appearance-none rounded-md relative block w-full px-3 py-2 border ${
                  fieldErrors.email ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Email address"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                disabled={isLoading}
                aria-invalid={fieldErrors.email ? 'true' : 'false'}
                aria-describedby={fieldErrors.email ? 'email-error' : undefined}
              />
              {fieldErrors.email && (
                <div id="email-error" className="mt-1 text-sm text-red-600" role="alert">
                  {fieldErrors.email.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>

            {/* Password field */}
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className={`appearance-none rounded-md relative block w-full px-3 py-2 border ${
                  fieldErrors.password ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                disabled={isLoading}
                aria-invalid={fieldErrors.password ? 'true' : 'false'}
                aria-describedby={fieldErrors.password ? 'password-error password-strength' : 'password-strength'}
              />
              
              {/* Password strength indicator */}
              {passwordStrength && formData.password && (
                <div id="password-strength" className="mt-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className={`font-medium ${getPasswordStrengthColor(passwordStrength.score)}`}>
                      {passwordStrength.strength}
                    </span>
                    <span className="text-gray-500">
                      {passwordStrength.score}/6
                    </span>
                  </div>
                  <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${
                        passwordStrength.score <= 1 ? 'bg-red-500' :
                        passwordStrength.score <= 2 ? 'bg-orange-500' :
                        passwordStrength.score <= 3 ? 'bg-yellow-500' :
                        passwordStrength.score <= 4 ? 'bg-blue-500' : 'bg-green-500'
                      }`}
                      style={{ width: getPasswordStrengthWidth(passwordStrength.score) }}
                    />
                  </div>
                </div>
              )}
              
              {fieldErrors.password && (
                <div id="password-error" className="mt-1 text-sm text-red-600" role="alert">
                  {fieldErrors.password.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>

            {/* Confirm password field */}
            <div>
              <label htmlFor="confirmPassword" className="sr-only">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                className={`appearance-none rounded-md relative block w-full px-3 py-2 border ${
                  fieldErrors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Confirm password"
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                disabled={isLoading}
                aria-invalid={fieldErrors.confirmPassword ? 'true' : 'false'}
                aria-describedby={fieldErrors.confirmPassword ? 'confirm-password-error' : undefined}
              />
              {fieldErrors.confirmPassword && (
                <div id="confirm-password-error" className="mt-1 text-sm text-red-600" role="alert">
                  {fieldErrors.confirmPassword.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition ease-in-out duration-150"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Creating Account...
                </>
              ) : (
                'Create Account'
              )}
            </button>
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              By creating an account, you agree to our{' '}
              <Link to="/terms" className="text-indigo-600 hover:text-indigo-500">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link to="/privacy" className="text-indigo-600 hover:text-indigo-500">
                Privacy Policy
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};