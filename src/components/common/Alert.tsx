// resource_id: 0158c18a-14b1-415e-a4ea-9766723c08da
/**
 * Alert Component
 * Language Tracker Common Components
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Reusable alert component for success, error, warning, and info messages.
 */

import React, { useState, useEffect } from 'react';

interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info';
  children: React.ReactNode;
  className?: string;
  dismissible?: boolean;
  autoClose?: number; // milliseconds
  onClose?: () => void;
  title?: string;
  icon?: boolean;
}

export const Alert: React.FC<AlertProps> = ({
  type,
  children,
  className = '',
  dismissible = false,
  autoClose,
  onClose,
  title,
  icon = true
}) => {
  const [isVisible, setIsVisible] = useState(true);

  // Auto-close functionality
  useEffect(() => {
    if (autoClose && autoClose > 0) {
      const timer = setTimeout(() => {
        handleClose();
      }, autoClose);

      return () => clearTimeout(timer);
    }
  }, [autoClose]);

  const handleClose = () => {
    setIsVisible(false);
    onClose?.();
  };

  if (!isVisible) return null;

  // Style mappings for different alert types
  const typeStyles = {
    success: {
      container: 'bg-green-50 border-green-200 text-green-700',
      icon: 'text-green-400',
      iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    error: {
      container: 'bg-red-50 border-red-200 text-red-700',
      icon: 'text-red-400',
      iconPath: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    warning: {
      container: 'bg-yellow-50 border-yellow-200 text-yellow-700',
      icon: 'text-yellow-400',
      iconPath: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z'
    },
    info: {
      container: 'bg-blue-50 border-blue-200 text-blue-700',
      icon: 'text-blue-400',
      iconPath: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
    }
  };

  const styles = typeStyles[type];

  return (
    <div
      className={`
        border rounded-md p-4 
        ${styles.container}
        ${className}
      `.trim()}
      role="alert"
      data-testid={`alert-${type}`}
    >
      <div className="flex">
        {icon && (
          <div className="flex-shrink-0">
            <svg
              className={`h-5 w-5 ${styles.icon}`}
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d={styles.iconPath}
                clipRule="evenodd"
              />
            </svg>
          </div>
        )}
        
        <div className={`${icon ? 'ml-3' : ''} flex-1`}>
          {title && (
            <h3 className="text-sm font-medium mb-1">
              {title}
            </h3>
          )}
          
          <div className="text-sm">
            {children}
          </div>
        </div>

        {dismissible && (
          <div className="ml-auto pl-3">
            <div className="-mx-1.5 -my-1.5">
              <button
                type="button"
                onClick={handleClose}
                className={`
                  inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2
                  ${type === 'success' ? 'text-green-500 hover:bg-green-100 focus:ring-offset-green-50 focus:ring-green-600' : ''}
                  ${type === 'error' ? 'text-red-500 hover:bg-red-100 focus:ring-offset-red-50 focus:ring-red-600' : ''}
                  ${type === 'warning' ? 'text-yellow-500 hover:bg-yellow-100 focus:ring-offset-yellow-50 focus:ring-yellow-600' : ''}
                  ${type === 'info' ? 'text-blue-500 hover:bg-blue-100 focus:ring-offset-blue-50 focus:ring-blue-600' : ''}
                `.trim()}
                aria-label="Close alert"
                data-testid="alert-close-button"
              >
                <span className="sr-only">Dismiss</span>
                <svg
                  className="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Specialized alert components
export const SuccessAlert: React.FC<Omit<AlertProps, 'type'>> = (props) => (
  <Alert {...props} type="success" />
);

export const ErrorAlert: React.FC<Omit<AlertProps, 'type'>> = (props) => (
  <Alert {...props} type="error" />
);

export const WarningAlert: React.FC<Omit<AlertProps, 'type'>> = (props) => (
  <Alert {...props} type="warning" />
);

export const InfoAlert: React.FC<Omit<AlertProps, 'type'>> = (props) => (
  <Alert {...props} type="info" />
);

// Toast notification component
interface ToastProps extends Omit<AlertProps, 'dismissible'> {
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
}

export const Toast: React.FC<ToastProps> = ({
  position = 'top-right',
  autoClose = 5000,
  ...alertProps
}) => {
  const positionClasses = {
    'top-right': 'fixed top-4 right-4 z-50',
    'top-left': 'fixed top-4 left-4 z-50',
    'bottom-right': 'fixed bottom-4 right-4 z-50',
    'bottom-left': 'fixed bottom-4 left-4 z-50',
    'top-center': 'fixed top-4 left-1/2 transform -translate-x-1/2 z-50',
    'bottom-center': 'fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50'
  };

  return (
    <div className={positionClasses[position]}>
      <Alert
        {...alertProps}
        dismissible
        autoClose={autoClose}
        className={`max-w-sm shadow-lg ${alertProps.className || ''}`}
      />
    </div>
  );
};

// Alert list for displaying multiple alerts
interface AlertListProps {
  alerts: Array<{
    id: string;
    type: AlertProps['type'];
    message: React.ReactNode;
    title?: string;
    dismissible?: boolean;
  }>;
  onDismiss?: (id: string) => void;
  className?: string;
}

export const AlertList: React.FC<AlertListProps> = ({
  alerts,
  onDismiss,
  className = ''
}) => {
  if (alerts.length === 0) return null;

  return (
    <div className={`space-y-3 ${className}`}>
      {alerts.map((alert) => (
        <Alert
          key={alert.id}
          type={alert.type}
          title={alert.title}
          dismissible={alert.dismissible}
          onClose={() => onDismiss?.(alert.id)}
        >
          {alert.message}
        </Alert>
      ))}
    </div>
  );
};

// Banner alert for full-width notifications
interface BannerAlertProps extends Omit<AlertProps, 'className'> {
  fixed?: boolean;
}

export const BannerAlert: React.FC<BannerAlertProps> = ({
  fixed = false,
  ...alertProps
}) => {
  const containerClass = fixed 
    ? 'fixed top-0 left-0 right-0 z-40'
    : 'w-full';

  return (
    <div className={containerClass}>
      <Alert
        {...alertProps}
        className={`rounded-none border-x-0 ${fixed ? 'border-t-0' : ''}`}
      />
    </div>
  );
};

export default Alert;