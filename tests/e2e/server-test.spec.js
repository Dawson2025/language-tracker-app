// resource_id: e9475569-ec55-4270-9b16-5cb1c1c4ffaf
const { test, expect } = require('@playwright/test');

test.describe('Flask Server Connectivity', () => {
  test('should connect to Flask server and see development page', async ({ page }) => {
    // Navigate to the Flask server
    await page.goto('/');
    
    // Verify the development page loads
    await expect(page).toHaveTitle('Language Tracker - Development');
    
    // Verify the main heading
    await expect(page.locator('h1')).toHaveText('Language Tracker API Server');
    
    // Verify API endpoints are listed
    await expect(page.locator('text=POST /api/auth/register')).toBeVisible();
    await expect(page.locator('text=POST /api/auth/login')).toBeVisible();
    await expect(page.locator('text=GET /api/health')).toBeVisible();
    
    // Wait a moment to see the page (for headed mode visibility)
    await page.waitForTimeout(2000);
  });

  test('should access health check endpoint', async ({ page, request }) => {
    // Test API endpoint directly
    const response = await request.get('/api/health');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data.status).toBe('healthy');
    expect(data.version).toBe('1.0.0');
  });

  test('should handle API not found correctly', async ({ request }) => {
    const response = await request.get('/api/nonexistent');
    expect(response.status()).toBe(404);
    
    const data = await response.json();
    expect(data.error).toBe('API endpoint not found');
  });
});