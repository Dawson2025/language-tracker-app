// resource_id: dd7cfebb-f350-488f-b03e-c4373f2abded
const { test, expect } = require('@playwright/test');

test.describe('Headed Browser Test', () => {
  test('should open the test app and display the title', async ({ page }) => {
    // Navigate to the test app
    await page.goto('/');
    
    // Verify the page loads and displays the correct title
    await expect(page).toHaveTitle('Language Tracker - Test App');
    
    // Verify the header is visible
    await expect(page.locator('h1')).toHaveText('Language Tracker');
    
    // Verify navigation buttons are present
    await expect(page.locator('button:has-text("Home")')).toBeVisible();
    await expect(page.locator('button:has-text("Sign Up")')).toBeVisible();
    await expect(page.locator('button:has-text("Login")')).toBeVisible();
    
    // Wait a moment to see the browser (for headed mode visibility)
    await page.waitForTimeout(3000);
  });

  test('should navigate between sections', async ({ page }) => {
    await page.goto('/');
    
    // Click Sign Up button
    await page.click('button:has-text("Sign Up")');
    
    // Verify Sign Up form is visible
    await expect(page.locator('h2:has-text("Sign Up")')).toBeVisible();
    await expect(page.locator('[data-testid="registration-form"]')).toBeVisible();
    
    // Click Login button
    await page.click('button:has-text("Login")');
    
    // Verify Login form is visible
    await expect(page.locator('h2:has-text("Login")')).toBeVisible();
    
    // Click Home button
    await page.click('button:has-text("Home")');
    
    // Verify Home content is visible
    await expect(page.locator('h2:has-text("Welcome to Language Tracker")')).toBeVisible();
    
    // Wait to see the navigation in action
    await page.waitForTimeout(2000);
  });
});