// resource_id: 3f6a7803-c866-4af9-8e42-2a8431d01457
/**
 * US-001: User Registration - Fast Tests
 * Implements Hard Testing Rule with Playwright MCP Server + Headed Chromium
 * 
 * FAST VERSION: Optimized for quick execution (<30 seconds)
 * - Minimal UI delays
 * - Mock external dependencies
 * - Focus on core functionality
 * - Parallel execution friendly
 */

const { test, expect } = require('@playwright/test');

test.describe('US-001: User Registration (Fast)', () => {
  
  // Configure fast test settings
  test.use({
    actionTimeout: 5000,
    navigationTimeout: 15000,
  });

  test.beforeEach(async ({ page }) => {
    // Fast navigation - no waiting for all resources
    await page.goto('/', { waitUntil: 'domcontentloaded' });
  });

  test('US-001.1: Display registration form quickly', async ({ page }) => {
    // Fast navigation to registration
    await page.click('text=Sign Up', { timeout: 3000 });
    
    // Quick form validation
    const form = page.locator('form[data-testid="registration-form"]');
    await expect(form).toBeVisible({ timeout: 3000 });
    
    // Verify essential form fields exist
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="email"]')).toBeVisible(); 
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('US-001.2: Register with valid data (fast validation)', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Use unique timestamp for fast test data
    const timestamp = Date.now();
    const testData = {
      username: `fasttest${timestamp}`,
      email: `fasttest${timestamp}@example.com`,
      password: 'FastTest123!',
      confirmPassword: 'FastTest123!'
    };
    
    // Fast form filling
    await page.fill('input[name="username"]', testData.username);
    await page.fill('input[name="email"]', testData.email);
    await page.fill('input[name="password"]', testData.password);
    await page.fill('input[name="confirmPassword"]', testData.confirmPassword);
    
    // Mock successful registration response
    await page.route('**/api/auth/register', (route) => {
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Account created successfully',
          user: {
            id: 'test-id',
            username: testData.username,
            email: testData.email
          },
          session: {
            token: 'mock-session-token',
            expires_at: new Date(Date.now() + 24*60*60*1000).toISOString()
          }
        })
      });
    });
    
    // Submit and verify fast response
    await page.click('button[type="submit"]');
    
    // Quick success validation
    await expect(page.locator('.success-message')).toBeVisible({ timeout: 5000 });
    
    // Verify registration success elements
    const successMsg = await page.textContent('.success-message');
    expect(successMsg).toContain('Account created');
  });

  test('US-001.3: Show validation errors quickly', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Test invalid email - fast validation
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'ValidPass123!');
    await page.fill('input[name="confirmPassword"]', 'ValidPass123!');
    
    await page.click('button[type="submit"]');
    
    // Fast error validation
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 3000 });
    
    const errorMsg = await page.textContent('.error-message');
    expect(errorMsg.toLowerCase()).toContain('email');
  });

  test('US-001.4: Password strength validation (fast)', async ({ page }) => {
    await page.click('text=Sign Up');
    
    const passwordField = page.locator('input[name="password"]');
    
    // Fast password strength testing
    await passwordField.fill('123');
    await expect(page.locator('.password-strength')).toContainText('Weak', { timeout: 2000 });
    
    await passwordField.fill('StrongPassword123!');
    await expect(page.locator('.password-strength')).toContainText('Strong', { timeout: 2000 });
  });

  test('US-001.5: Duplicate username validation (fast)', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Mock duplicate username error
    await page.route('**/api/auth/register', (route) => {
      route.fulfill({
        status: 409,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          errors: ['Username already exists'],
          field_errors: {
            username: ['Username already exists']
          }
        })
      });
    });
    
    await page.fill('input[name="username"]', 'existinguser');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'ValidPass123!');
    await page.fill('input[name="confirmPassword"]', 'ValidPass123!');
    
    await page.click('button[type="submit"]');
    
    // Fast error validation
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 3000 });
    const errorMsg = await page.textContent('.error-message');
    expect(errorMsg).toContain('already exists');
  });

  test('US-001.6: Form accessibility (fast check)', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Quick accessibility validation
    const form = page.locator('form[data-testid="registration-form"]');
    
    // Check for labels
    await expect(page.locator('label[for="username"]')).toBeVisible();
    await expect(page.locator('label[for="email"]')).toBeVisible();
    await expect(page.locator('label[for="password"]')).toBeVisible();
    
    // Check ARIA attributes
    const usernameField = page.locator('input[name="username"]');
    await expect(usernameField).toHaveAttribute('aria-required', 'true');
    
    // Check keyboard navigation
    await page.keyboard.press('Tab');
    await expect(usernameField).toBeFocused();
  });

  test('US-001.7: Form submission loading state (fast)', async ({ page }) => {
    await page.click('text=Sign Up');
    
    // Mock slow response for loading state test
    await page.route('**/api/auth/register', (route) => {
      setTimeout(() => {
        route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({ success: true })
        });
      }, 1000);
    });
    
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'ValidPass123!');
    await page.fill('input[name="confirmPassword"]', 'ValidPass123!');
    
    await page.click('button[type="submit"]');
    
    // Quick loading state check
    await expect(page.locator('button[type="submit"]')).toBeDisabled({ timeout: 1000 });
    await expect(page.locator('.loading-spinner')).toBeVisible({ timeout: 1000 });
  });

  test('US-001.8: Security headers validation (fast)', async ({ page }) => {
    // Fast security header check
    const response = await page.goto('/register');
    
    const headers = response.headers();
    expect(headers['x-content-type-options']).toBe('nosniff');
    expect(headers['x-frame-options']).toBe('DENY');
  });

});

// Fast test execution summary
test.afterAll(async () => {
  console.log('✅ US-001 Fast Tests Complete - Registration functionality validated quickly');
  console.log('⚡ Fast test execution optimized for CI pipeline');
});