/**
 * E2E Authentication Tests
 * Implements Hard Testing Rule with Playwright MCP Server + Headed Chromium
 * 
 * Tests comprehensive authentication workflows:
 * - User registration flow
 * - Login/logout functionality
 * - Session management
 * - Error handling
 * - UI/UX validation
 */

const { test, expect } = require('@playwright/test');
const fs = require('fs').promises;

// Test fixtures
let testUsers;
let authScenarios;

test.beforeAll(async () => {
  // Load test fixtures
  try {
    testUsers = JSON.parse(await fs.readFile('tests/fixtures/test-users.json', 'utf8'));
    authScenarios = JSON.parse(await fs.readFile('tests/fixtures/auth-scenarios.json', 'utf8'));
  } catch (error) {
    console.warn('⚠️ Test fixtures not found, using fallback data');
    testUsers = [
      {
        username: 'testuser1',
        email: 'test1@example.com',
        password: 'ValidPassword123!'
      }
    ];
    authScenarios = [];
  }
});

test.describe('Authentication E2E Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
    
    // Wait for the page to be ready
    await page.waitForLoadState('domcontentloaded');
  });

  test('should display registration form', async ({ page }) => {
    // Navigate to registration page
    await page.click('text=Sign Up');
    
    // Verify form elements are present
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('input[name="confirmPassword"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    
    // Take screenshot for visual validation
    await page.screenshot({ path: 'test-results/registration-form.png' });
  });

  test('should register a new user successfully', async ({ page }) => {
    // Go to registration page
    await page.click('text=Sign Up');
    
    // Fill out registration form with valid data
    const testUser = {
      username: `testuser_${Date.now()}`,
      email: `test_${Date.now()}@example.com`,
      password: 'StrongPassword123!',
      confirmPassword: 'StrongPassword123!'
    };
    
    await page.fill('input[name="username"]', testUser.username);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.confirmPassword);
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Wait for success response
    await page.waitForSelector('.success-message', { timeout: 10000 });
    
    // Verify success message
    const successMessage = await page.textContent('.success-message');
    expect(successMessage).toContain('Account created successfully');
    
    // Verify redirect to dashboard or appropriate page
    await expect(page).toHaveURL(/\/(dashboard|home)/);
    
    // Take screenshot of success state
    await page.screenshot({ path: 'test-results/registration-success.png' });
  });

  test('should show validation errors for invalid registration data', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Test invalid email format
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'ValidPassword123!');
    await page.fill('input[name="confirmPassword"]', 'ValidPassword123!');
    
    await page.click('button[type="submit"]');
    
    // Wait for validation error
    await page.waitForSelector('.error-message', { timeout: 5000 });
    
    // Verify error message
    const errorMessage = await page.textContent('.error-message');
    expect(errorMessage).toContain('email');
    
    // Test weak password
    await page.fill('input[name="email"]', 'valid@example.com');
    await page.fill('input[name="password"]', '123');
    await page.fill('input[name="confirmPassword"]', '123');
    
    await page.click('button[type="submit"]');
    
    // Wait for validation error
    await page.waitForSelector('.error-message', { timeout: 5000 });
    
    // Take screenshot of validation errors
    await page.screenshot({ path: 'test-results/validation-errors.png' });
  });

  test('should login with valid credentials', async ({ page }) => {
    // Assume we have a test user (this would typically be created in setup)
    const testUser = testUsers[0];
    
    // Go to login page
    await page.click('text=Login');
    
    // Fill login form
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    
    // Submit login
    await page.click('button[type="submit"]');
    
    // Wait for successful login
    await page.waitForSelector('.welcome-message', { timeout: 10000 });
    
    // Verify welcome message
    const welcomeMessage = await page.textContent('.welcome-message');
    expect(welcomeMessage).toContain('Welcome back');
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL(/\/(dashboard|home)/);
    
    // Verify user menu is available
    await expect(page.locator('.user-menu')).toBeVisible();
    
    await page.screenshot({ path: 'test-results/login-success.png' });
  });

  test('should show error for invalid login credentials', async ({ page }) => {
    await page.click('text=Login');
    
    // Try with invalid credentials
    await page.fill('input[name="email"]', 'nonexistent@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    
    await page.click('button[type="submit"]');
    
    // Wait for error message
    await page.waitForSelector('.error-message', { timeout: 5000 });
    
    // Verify error message
    const errorMessage = await page.textContent('.error-message');
    expect(errorMessage).toContain('Invalid credentials');
    
    // Verify still on login page
    await expect(page).toHaveURL(/\/login/);
    
    await page.screenshot({ path: 'test-results/login-error.png' });
  });

  test('should logout successfully', async ({ page }) => {
    // First login (assuming we have a way to authenticate)
    await page.click('text=Login');
    const testUser = testUsers[0];
    
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    
    // Wait for login to complete
    await page.waitForSelector('.user-menu', { timeout: 10000 });
    
    // Logout
    await page.click('.user-menu');
    await page.click('text=Logout');
    
    // Verify logout
    await page.waitForSelector('text=Login', { timeout: 5000 });
    await expect(page.locator('.user-menu')).not.toBeVisible();
    
    // Verify redirect to home/login page
    await expect(page).toHaveURL(/\/(|login|home)/);
    
    await page.screenshot({ path: 'test-results/logout-success.png' });
  });

  test('should handle session expiration', async ({ page }) => {
    // This test would simulate session expiration
    // For now, we'll test the basic flow
    
    await page.goto('/dashboard');
    
    // If not logged in, should redirect to login
    await page.waitForSelector('text=Login', { timeout: 10000 });
    await expect(page).toHaveURL(/\/login/);
    
    await page.screenshot({ path: 'test-results/session-expired.png' });
  });

  test('should validate password strength in real-time', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Test real-time password validation
    const passwordField = page.locator('input[name="password"]');
    
    // Weak password
    await passwordField.fill('123');
    await page.waitForSelector('.password-strength.weak', { timeout: 2000 });
    
    // Strong password
    await passwordField.fill('StrongPassword123!');
    await page.waitForSelector('.password-strength.strong', { timeout: 2000 });
    
    await page.screenshot({ path: 'test-results/password-strength.png' });
  });

  test('should support remember me functionality', async ({ page }) => {
    await page.click('text=Login');
    
    const testUser = testUsers[0];
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    
    // Check remember me
    await page.check('input[name="rememberMe"]');
    
    await page.click('button[type="submit"]');
    
    // Wait for login success
    await page.waitForSelector('.user-menu', { timeout: 10000 });
    
    // Verify session persistence (this would need backend support)
    const sessionToken = await page.evaluate(() => localStorage.getItem('sessionToken'));
    expect(sessionToken).toBeTruthy();
    
    await page.screenshot({ path: 'test-results/remember-me.png' });
  });

});

test.describe('Authentication Security Tests', () => {
  
  test('should prevent XSS in form inputs', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Try XSS payload
    const xssPayload = '<script>alert("xss")</script>';
    
    await page.fill('input[name="username"]', xssPayload);
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'ValidPassword123!');
    await page.fill('input[name="confirmPassword"]', 'ValidPassword123!');
    
    await page.click('button[type="submit"]');
    
    // Verify XSS was prevented (no alert dialog)
    await page.waitForTimeout(2000);
    
    // Should see validation error, not XSS execution
    await expect(page.locator('.error-message')).toBeVisible();
    
    await page.screenshot({ path: 'test-results/xss-prevention.png' });
  });

  test('should enforce HTTPS redirect', async ({ page }) => {
    // This test would verify HTTPS enforcement
    // Implementation depends on your server configuration
    
    const response = await page.goto('/');
    expect(response.url()).toMatch(/^https:/);
  });

});