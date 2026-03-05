// resource_id: b3b1dc0d-d7da-4a53-8373-943d16c645fc
/**
 * Google Sign-In Button Component
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Implements US-003: Firebase Authentication (Google Sign-In)
 * Provides Firebase OAuth integration with graceful fallback handling.
 */

import React, { useState, useCallback, useEffect } from 'react';
import { authAPI } from '../../services/authService';
import { LoadingSpinner } from '../common/LoadingSpinner';

// Firebase imports with error handling
let firebaseAuth: any = null;
let GoogleAuthProvider: any = null;
let signInWithPopup: any = null;

try {
  const firebase = require('firebase/auth');
  firebaseAuth = firebase.getAuth;
  GoogleAuthProvider = firebase.GoogleAuthProvider;
  signInWithPopup = firebase.signInWithPopup;
} catch (error) {
  console.warn('Firebase Auth not available:', error);
}

interface GoogleSignInButtonProps {
  onSuccess?: (user: any) => void;
  onError?: (error: string) => void;
  redirectTo?: string;
  disabled?: boolean;
  className?: string;
}

export const GoogleSignInButton: React.FC<GoogleSignInButtonProps> = ({
  onSuccess,
  onError,
  redirectTo = '/dashboard',
  disabled = false,
  className = ''
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isFirebaseAvailable, setIsFirebaseAvailable] = useState(false);

  useEffect(() => {
    // Check if Firebase is properly configured
    const checkFirebaseConfig = async () => {
      try {
        if (firebaseAuth && GoogleAuthProvider && signInWithPopup) {
          // Check if Firebase config is available from backend
          const config = await authAPI.getFirebaseConfig();
          setIsFirebaseAvailable(!!config);
        }
      } catch (error) {
        console.warn('Firebase configuration check failed:', error);
        setIsFirebaseAvailable(false);
      }
    };

    checkFirebaseConfig();
  }, []);

  const handleGoogleSignIn = useCallback(async () => {
    if (!isFirebaseAvailable) {
      onError?.('Google Sign-In is temporarily unavailable. Please use email/password login.');
      return;
    }

    setIsLoading(true);

    try {
      // Initialize Firebase Auth
      const auth = firebaseAuth();
      const provider = new GoogleAuthProvider();

      // Configure OAuth scopes
      provider.addScope('email');
      provider.addScope('profile');

      // Sign in with popup
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      if (user) {
        // Get Firebase ID token
        const idToken = await user.getIdToken();

        // Send token to backend for verification and account linking
        const response = await authAPI.loginWithFirebase({
          id_token: idToken
        });

        if (response.success) {
          // Store auth token
          if (response.session?.token) {
            localStorage.setItem('auth_token', response.session.token);
          }

          onSuccess?.(response.user);

          // Redirect to dashboard
          window.location.href = redirectTo;
        } else {
          // Handle authentication errors
          const errorMessage = response.errors?.[0] || 'Google Sign-In failed';
          onError?.(errorMessage);
        }
      } else {
        onError?.('Google Sign-In was cancelled');
      }
    } catch (error: any) {
      console.error('Google Sign-In error:', error);

      // Handle specific Firebase Auth errors
      let errorMessage = 'Google Sign-In failed. Please try again.';

      if (error.code === 'auth/popup-closed-by-user') {
        errorMessage = 'Sign-in was cancelled';
      } else if (error.code === 'auth/popup-blocked') {
        errorMessage = 'Sign-in popup was blocked by your browser. Please allow popups and try again.';
      } else if (error.code === 'auth/cancelled-popup-request') {
        errorMessage = 'Sign-in was cancelled';
      } else if (error.code === 'auth/network-request-failed') {
        errorMessage = 'Network error. Please check your connection and try again.';
      } else if (error.code === 'auth/too-many-requests') {
        errorMessage = 'Too many sign-in attempts. Please try again later.';
      }

      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [isFirebaseAvailable, onSuccess, onError, redirectTo]);

  // Don't render if Firebase is not available
  if (!isFirebaseAvailable) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={handleGoogleSignIn}
      disabled={disabled || isLoading}
      className={`w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition ease-in-out duration-150 ${className}`}
    >
      {isLoading ? (
        <>
          <LoadingSpinner size="sm" className="mr-2" />
          Signing in with Google...
        </>
      ) : (
        <>
          <GoogleIcon className="mr-2" />
          Continue with Google
        </>
      )}
    </button>
  );
};

/**
 * Google Logo Icon Component
 */
const GoogleIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg
    className={`w-5 h-5 ${className}`}
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      fill="#4285F4"
      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
    />
    <path
      fill="#34A853"
      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
    />
    <path
      fill="#FBBC05"
      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
    />
    <path
      fill="#EA4335"
      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
    />
  </svg>
);

export default GoogleSignInButton;