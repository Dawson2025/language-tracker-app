import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { validateEmail, validateUsername, validatePassword } from '../utils/validation';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Alert } from '../components/ui/Alert';

interface ProfileFormData {
  username: string;
  email: string;
}

interface PasswordFormData {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

export const ProfilePage: React.FC = () => {
  const [profileData, setProfileData] = useState<ProfileFormData>({
    username: '',
    email: ''
  });
  const [passwordData, setPasswordData] = useState<PasswordFormData>({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      setProfileData({
        username: user.username || '',
        email: user.email || ''
      });
    }
  }, [user]);

  const validateProfileForm = () => {
    const errors: Record<string, string> = {};
    
    const usernameValidation = validateUsername(profileData.username);
    if (!usernameValidation.isValid) {
      errors.username = usernameValidation.errors[0];
    }

    const emailValidation = validateEmail(profileData.email);
    if (!emailValidation.isValid) {
      errors.email = emailValidation.errors[0];
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const validatePasswordForm = () => {
    const errors: Record<string, string> = {};
    
    if (!passwordData.currentPassword) {
      errors.currentPassword = 'Current password is required';
    }

    const passwordValidation = validatePassword(passwordData.newPassword);
    if (!passwordValidation.isValid) {
      errors.newPassword = passwordValidation.errors[0];
    }

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!validateProfileForm()) {
      return;
    }

    setIsUpdatingProfile(true);
    try {
      // For now, show that profile updates are not implemented
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      setError('Profile updates will be implemented in the next phase.');
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsUpdatingProfile(false);
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!validatePasswordForm()) {
      return;
    }

    setIsChangingPassword(true);
    try {
      // For now, show that password changes are not implemented
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      setError('Password changes will be implemented in the next phase.');
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
    
    // Clear validation error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
    
    // Clear validation error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      setIsLoading(true);
      try {
        // For now, show that account deletion is not implemented
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
        setError('Account deletion will be implemented in the next phase.');
      } catch (err) {
        setError('An unexpected error occurred. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Link to="/dashboard" className="text-2xl font-bold text-gray-900">
                🗣️ Language Tracker
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/dashboard"
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Profile Settings</h1>
          <p className="text-gray-600">
            Manage your account settings and preferences
          </p>
        </div>

        {/* Alerts */}
        {error && (
          <div className="mb-6">
            <Alert variant="error" message={error} />
          </div>
        )}

        {success && (
          <div className="mb-6">
            <Alert variant="success" message={success} />
          </div>
        )}

        {/* Profile Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Profile Information</h2>
            <p className="text-sm text-gray-600 mt-1">
              Update your account details
            </p>
          </div>
          
          <form onSubmit={handleProfileSubmit} className="px-6 py-4 space-y-6">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Username
              </label>
              <div className="mt-1">
                <input
                  id="username"
                  name="username"
                  type="text"
                  autoComplete="username"
                  required
                  value={profileData.username}
                  onChange={handleProfileChange}
                  className={`input-field ${validationErrors.username ? 'border-red-500 focus:ring-red-500' : ''}`}
                  placeholder="Enter your username"
                />
                {validationErrors.username && (
                  <p className="mt-1 text-sm text-red-600">{validationErrors.username}</p>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={profileData.email}
                  onChange={handleProfileChange}
                  className={`input-field ${validationErrors.email ? 'border-red-500 focus:ring-red-500' : ''}`}
                  placeholder="Enter your email"
                />
                {validationErrors.email && (
                  <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
                )}
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isUpdatingProfile}
                className="btn-primary flex items-center"
              >
                {isUpdatingProfile ? (
                  <>
                    <LoadingSpinner size="sm" className="mr-2" />
                    Updating...
                  </>
                ) : (
                  'Update Profile'
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Security Settings */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Security</h2>
            <p className="text-sm text-gray-600 mt-1">
              Manage your password and security settings
            </p>
          </div>
          
          <div className="px-6 py-4">
            {!showPasswordForm ? (
              <button
                onClick={() => setShowPasswordForm(true)}
                className="btn-secondary"
              >
                Change Password
              </button>
            ) : (
              <form onSubmit={handlePasswordSubmit} className="space-y-6">
                <div>
                  <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700">
                    Current Password
                  </label>
                  <div className="mt-1">
                    <input
                      id="currentPassword"
                      name="currentPassword"
                      type="password"
                      autoComplete="current-password"
                      required
                      value={passwordData.currentPassword}
                      onChange={handlePasswordChange}
                      className={`input-field ${validationErrors.currentPassword ? 'border-red-500 focus:ring-red-500' : ''}`}
                      placeholder="Enter current password"
                    />
                    {validationErrors.currentPassword && (
                      <p className="mt-1 text-sm text-red-600">{validationErrors.currentPassword}</p>
                    )}
                  </div>
                </div>

                <div>
                  <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700">
                    New Password
                  </label>
                  <div className="mt-1">
                    <input
                      id="newPassword"
                      name="newPassword"
                      type="password"
                      autoComplete="new-password"
                      required
                      value={passwordData.newPassword}
                      onChange={handlePasswordChange}
                      className={`input-field ${validationErrors.newPassword ? 'border-red-500 focus:ring-red-500' : ''}`}
                      placeholder="Enter new password"
                    />
                    {validationErrors.newPassword && (
                      <p className="mt-1 text-sm text-red-600">{validationErrors.newPassword}</p>
                    )}
                  </div>
                </div>

                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                    Confirm New Password
                  </label>
                  <div className="mt-1">
                    <input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      autoComplete="new-password"
                      required
                      value={passwordData.confirmPassword}
                      onChange={handlePasswordChange}
                      className={`input-field ${validationErrors.confirmPassword ? 'border-red-500 focus:ring-red-500' : ''}`}
                      placeholder="Confirm new password"
                    />
                    {validationErrors.confirmPassword && (
                      <p className="mt-1 text-sm text-red-600">{validationErrors.confirmPassword}</p>
                    )}
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowPasswordForm(false);
                      setPasswordData({
                        currentPassword: '',
                        newPassword: '',
                        confirmPassword: ''
                      });
                      setValidationErrors({});
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isChangingPassword}
                    className="btn-primary flex items-center"
                  >
                    {isChangingPassword ? (
                      <>
                        <LoadingSpinner size="sm" className="mr-2" />
                        Changing...
                      </>
                    ) : (
                      'Change Password'
                    )}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-white rounded-lg shadow-sm border border-red-200">
          <div className="px-6 py-4 border-b border-red-200">
            <h2 className="text-lg font-semibold text-red-900">Danger Zone</h2>
            <p className="text-sm text-red-600 mt-1">
              Irreversible and destructive actions
            </p>
          </div>
          
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-medium text-gray-900">Delete Account</h3>
                <p className="text-sm text-gray-600">
                  Permanently delete your account and all associated data
                </p>
              </div>
              <button
                onClick={handleDeleteAccount}
                disabled={isLoading}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 flex items-center"
              >
                {isLoading ? (
                  <>
                    <LoadingSpinner size="sm" className="mr-2" />
                    Deleting...
                  </>
                ) : (
                  'Delete Account'
                )}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};