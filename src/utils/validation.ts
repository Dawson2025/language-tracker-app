/**
 * Frontend Validation Utilities
 * Language Tracker Authentication Feature
 * Created via GitHub Spec Kit Implementation Phase
 * 
 * Client-side validation functions for forms and user input.
 * Provides real-time validation feedback and prevents unnecessary API calls.
 */

// Validation result type
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  score?: number;
  strength?: string;
  hasUppercase?: boolean;
  hasLowercase?: boolean;
  hasNumbers?: boolean;
  hasSpecial?: boolean;
}

// Email validation
export function validateEmail(email: string): ValidationResult {
  const errors: string[] = [];
  
  if (!email) {
    return {
      isValid: false,
      errors: ['Email is required']
    };
  }
  
  if (!email.trim()) {
    return {
      isValid: false,
      errors: ['Email cannot be empty']
    };
  }
  
  // Check email length
  if (email.length > 255) {
    errors.push('Email address is too long (maximum 255 characters)');
  }
  
  // Basic email format validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    errors.push('Please enter a valid email address');
  }
  
  // Check for multiple @ symbols
  if ((email.match(/@/g) || []).length !== 1) {
    errors.push('Email address must contain exactly one @ symbol');
  }
  
  // Check for suspicious patterns
  if (email.includes('..') || email.startsWith('.') || email.endsWith('.')) {
    errors.push('Email address format is invalid');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

// Username validation
export function validateUsername(username: string): ValidationResult {
  const errors: string[] = [];
  
  if (!username) {
    return {
      isValid: false,
      errors: ['Username is required']
    };
  }
  
  const trimmedUsername = username.trim();
  
  if (!trimmedUsername) {
    return {
      isValid: false,
      errors: ['Username cannot be empty']
    };
  }
  
  // Length validation
  if (trimmedUsername.length < 3) {
    errors.push('Username must be at least 3 characters long');
  } else if (trimmedUsername.length > 50) {
    errors.push('Username cannot exceed 50 characters');
  }
  
  // Character validation (alphanumeric, underscore, hyphen only)
  const usernameRegex = /^[a-zA-Z0-9_-]+$/;
  if (!usernameRegex.test(trimmedUsername)) {
    errors.push('Username can only contain letters, numbers, underscores, and hyphens');
  }
  
  // Forbidden usernames
  const forbiddenUsernames = [
    'admin', 'administrator', 'root', 'system', 'api', 'www', 'mail',
    'ftp', 'web', 'support', 'help', 'info', 'contact', 'service',
    'user', 'guest', 'anonymous', 'null', 'undefined', 'test'
  ];
  
  if (forbiddenUsernames.includes(trimmedUsername.toLowerCase())) {
    errors.push('This username is not available');
  }
  
  // Additional security checks
  if (trimmedUsername.toLowerCase().startsWith('admin') || 
      trimmedUsername.toLowerCase().startsWith('root') || 
      trimmedUsername.toLowerCase().startsWith('system')) {
    errors.push('Username cannot start with reserved words');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

// Password validation with strength scoring
export function validatePassword(password: string): ValidationResult {
  const errors: string[] = [];
  let score = 0;
  
  if (!password) {
    return {
      isValid: false,
      errors: ['Password is required'],
      score: 0,
      strength: 'Very Weak'
    };
  }
  
  // Length validation
  if (password.length < 6) {
    errors.push('Password must be at least 6 characters long');
  } else {
    score += 1;
  }
  
  // Maximum length for security (prevent DoS)
  if (password.length > 128) {
    errors.push('Password cannot exceed 128 characters');
  }
  
  // Character type checks
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  // Score bonus for character diversity
  if (hasUppercase) score += 1;
  if (hasLowercase) score += 1;
  if (hasNumbers) score += 1;
  if (hasSpecial) score += 1;
  
  // Length bonus
  if (password.length >= 8) score += 1;
  if (password.length >= 12) score += 1;
  
  // Common password check
  const commonPasswords = [
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password123', '123123', 'admin', 'letmein', 'welcome',
    '1234567890', 'dragon', 'sunshine', 'master', 'login',
    'football', 'shadow', 'monkey', 'princess', 'superman'
  ];
  
  if (commonPasswords.includes(password.toLowerCase())) {
    errors.push('Password is too common. Please choose a stronger password.');
    score = Math.max(0, score - 2);
  }
  
  // Security checks
  if (password.trim() !== password) {
    errors.push('Password cannot start or end with spaces');
  }
  
  // Check for null bytes or control characters
  if (password.includes('\0') || /[\x00-\x1f\x7f-\x9f]/.test(password)) {
    errors.push('Password contains invalid characters');
  }
  
  // Sequential character check
  if (/123|abc|qwe|asd|zxc/i.test(password)) {
    score = Math.max(0, score - 1);
  }
  
  // Repeated character check
  if (/(.)\1{2,}/.test(password)) {
    score = Math.max(0, score - 1);
  }
  
  // Determine strength label
  const strength = getPasswordStrengthLabel(score);
  
  return {
    isValid: errors.length === 0,
    errors,
    score: Math.min(score, 6), // Max score of 6
    strength,
    hasUppercase,
    hasLowercase,
    hasNumbers,
    hasSpecial
  };
}

// Convert numeric password strength score to descriptive label
function getPasswordStrengthLabel(score: number): string {
  if (score <= 1) return 'Very Weak';
  if (score <= 2) return 'Weak';
  if (score <= 3) return 'Fair';
  if (score <= 4) return 'Good';
  if (score <= 5) return 'Strong';
  return 'Very Strong';
}

// Validate password confirmation
export function validatePasswordConfirmation(password: string, confirmPassword: string): ValidationResult {
  const errors: string[] = [];
  
  if (!confirmPassword) {
    errors.push('Please confirm your password');
  } else if (password !== confirmPassword) {
    errors.push('Passwords do not match');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

// General form field validation
export function validateRequired(value: string, fieldName: string): ValidationResult {
  if (!value || !value.trim()) {
    return {
      isValid: false,
      errors: [`${fieldName} is required`]
    };
  }
  
  return {
    isValid: true,
    errors: []
  };
}

// Validate text length
export function validateLength(
  value: string,
  fieldName: string,
  minLength?: number,
  maxLength?: number
): ValidationResult {
  const errors: string[] = [];
  
  if (minLength && value.length < minLength) {
    errors.push(`${fieldName} must be at least ${minLength} characters long`);
  }
  
  if (maxLength && value.length > maxLength) {
    errors.push(`${fieldName} cannot exceed ${maxLength} characters`);
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

// Sanitize user input
export function sanitizeInput(input: string, maxLength?: number): string {
  if (!input) return '';
  
  // Remove null bytes and control characters (except tab, newline, carriage return)
  let sanitized = input.replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]/g, '');
  
  // Trim whitespace
  sanitized = sanitized.trim();
  
  // Limit length if specified
  if (maxLength && sanitized.length > maxLength) {
    sanitized = sanitized.substring(0, maxLength);
  }
  
  return sanitized;
}

// Validate multiple fields at once
export function validateForm(fields: Record<string, any>): { isValid: boolean; fieldErrors: Record<string, string[]> } {
  const fieldErrors: Record<string, string[]> = {};
  let hasErrors = false;
  
  for (const [fieldName, fieldValue] of Object.entries(fields)) {
    let validation: ValidationResult;
    
    switch (fieldName) {
      case 'email':
        validation = validateEmail(fieldValue as string);
        break;
      case 'username':
        validation = validateUsername(fieldValue as string);
        break;
      case 'password':
        validation = validatePassword(fieldValue as string);
        break;
      case 'confirmPassword':
        validation = validatePasswordConfirmation(
          fields.password as string,
          fieldValue as string
        );
        break;
      default:
        validation = validateRequired(fieldValue as string, fieldName);
        break;
    }
    
    if (!validation.isValid) {
      fieldErrors[fieldName] = validation.errors;
      hasErrors = true;
    }
  }
  
  return {
    isValid: !hasErrors,
    fieldErrors
  };
}

// Email format check (simple version for real-time validation)
export function isValidEmailFormat(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

// Password strength color for UI
export function getPasswordStrengthColor(score: number): string {
  if (score <= 1) return '#dc3545'; // red
  if (score <= 2) return '#fd7e14'; // orange
  if (score <= 3) return '#ffc107'; // yellow
  if (score <= 4) return '#0d6efd'; // blue
  return '#198754'; // green
}

// Password strength progress percentage
export function getPasswordStrengthPercentage(score: number): number {
  return Math.max(10, (score / 6) * 100);
}

// Export all validation functions
export default {
  validateEmail,
  validateUsername,
  validatePassword,
  validatePasswordConfirmation,
  validateRequired,
  validateLength,
  validateForm,
  sanitizeInput,
  isValidEmailFormat,
  getPasswordStrengthColor,
  getPasswordStrengthPercentage
};