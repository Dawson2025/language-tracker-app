/**
 * Loading Spinner Component
 * Language Tracker Common Components
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Reusable loading spinner with different sizes and styles.
 */

import React from 'react';

interface LoadingSpinnerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  color?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark' | 'white';
  text?: string;
  inline?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  className = '',
  color = 'primary',
  text,
  inline = false
}) => {
  // Size mappings
  const sizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4', 
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  // Color mappings
  const colorClasses = {
    primary: 'text-indigo-600',
    secondary: 'text-gray-600',
    success: 'text-green-600',
    danger: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
    light: 'text-gray-300',
    dark: 'text-gray-900',
    white: 'text-white'
  };

  const spinnerClasses = `
    animate-spin 
    ${sizeClasses[size]} 
    ${colorClasses[color]} 
    ${className}
  `.trim();

  const containerClasses = inline 
    ? 'inline-flex items-center'
    : 'flex items-center justify-center';

  return (
    <div className={containerClasses}>
      <svg
        className={spinnerClasses}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        aria-hidden="true"
        data-testid="loading-spinner"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="m4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      {text && (
        <span className={`ml-2 ${inline ? 'text-sm' : 'text-base'} ${colorClasses[color]}`}>
          {text}
        </span>
      )}
    </div>
  );
};

// Full-screen loading overlay
interface LoadingOverlayProps {
  isVisible: boolean;
  text?: string;
  backgroundColor?: string;
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  isVisible,
  text = 'Loading...',
  backgroundColor = 'rgba(255, 255, 255, 0.9)'
}) => {
  if (!isVisible) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ backgroundColor }}
      data-testid="loading-overlay"
    >
      <div className="text-center">
        <LoadingSpinner size="lg" color="primary" />
        <p className="mt-4 text-gray-600 font-medium">{text}</p>
      </div>
    </div>
  );
};

// Button with integrated loading state
interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading: boolean;
  loadingText?: string;
  spinnerSize?: 'xs' | 'sm' | 'md';
  children: React.ReactNode;
}

export const LoadingButton: React.FC<LoadingButtonProps> = ({
  isLoading,
  loadingText,
  spinnerSize = 'sm',
  children,
  disabled,
  className = '',
  ...props
}) => {
  return (
    <button
      {...props}
      disabled={disabled || isLoading}
      className={`
        ${className}
        ${isLoading ? 'cursor-not-allowed opacity-75' : ''}
      `.trim()}
    >
      {isLoading ? (
        <div className="flex items-center justify-center">
          <LoadingSpinner size={spinnerSize} color="white" inline />
          {loadingText && (
            <span className="ml-2">{loadingText}</span>
          )}
        </div>
      ) : (
        children
      )}
    </button>
  );
};

// Skeleton loader for content placeholders
interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  className?: string;
  circle?: boolean;
  lines?: number;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = '1rem',
  className = '',
  circle = false,
  lines = 1
}) => {
  const baseClasses = 'animate-pulse bg-gray-300 rounded';
  const shapeClasses = circle ? 'rounded-full' : 'rounded';
  
  if (lines === 1) {
    return (
      <div
        className={`${baseClasses} ${shapeClasses} ${className}`}
        style={{ width, height }}
        data-testid="skeleton"
      />
    );
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: lines }).map((_, index) => (
        <div
          key={index}
          className={`${baseClasses} ${shapeClasses}`}
          style={{ 
            width: index === lines - 1 ? '75%' : width, 
            height 
          }}
        />
      ))}
    </div>
  );
};

export default LoadingSpinner;