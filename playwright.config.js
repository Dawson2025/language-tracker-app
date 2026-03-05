// resource_id: a62fba2b-1778-411b-a07b-b092a8116f8b
// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright Configuration for Language Tracker E2E Testing
 * Implements Hard Testing Rule with Playwright MCP Server + Headed Chromium
 * 
 * Features:
 * - Headed Chromium testing (visible browser windows)
 * - Both fast and realistic test variants
 * - User story automation coverage
 * - Parallel execution support
 * - Comprehensive reporting
 */

module.exports = defineConfig({
  // Test directory structure
  testDir: './tests',
  
  // Test matching patterns
  testMatch: [
    '**/e2e/**/*.spec.js',
    '**/user_stories/**/*.spec.js',
    '**/e2e/**/*.test.js',
    '**/user_stories/**/*.test.js'
  ],

  // Global timeout settings
  timeout: 60000, // 1 minute per test
  expect: {
    timeout: 10000 // 10 seconds for assertions
  },

  // Run tests in parallel
  fullyParallel: true,
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Parallel workers
  workers: process.env.CI ? 2 : undefined,
  
  // Reporter configuration
  reporter: [
    ['html', { 
      outputFolder: 'playwright-report',
      open: process.env.CI ? 'never' : 'on-failure'
    }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['list'],
    ['line'] // Detailed line-by-line output
  ],

  // Global test settings
  use: {
    // Base URL for the application - Flask development server
    baseURL: process.env.BASE_URL || 'http://localhost:5001',
    
    // Browser context options
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    
    // Screenshots and videos
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    
    // Action timeouts
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  // Output directories
  outputDir: 'test-results/',

  // Project configurations for different test types
  projects: [
    {
      name: 'chromium-headed',
      use: { 
        ...devices['Desktop Chrome'],
        // CRITICAL: Use headed mode (visible browser)
        headless: false,
        // Slow down for better visibility in headed mode
        slowMo: process.env.CI ? 0 : 500,
        // Additional Chrome args for stability
        launchOptions: {
          args: [
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-dev-shm-usage',
            '--no-sandbox'
          ],
        }
      },
      testMatch: '**/e2e/**/*'
    },

    {
      name: 'user-stories-fast',
      use: { 
        ...devices['Desktop Chrome'],
        headless: false,
        // Fast tests - minimal delay
        slowMo: 100,
        // Fast test specific settings
        actionTimeout: 5000,
        navigationTimeout: 15000,
      },
      testMatch: '**/user_stories/fast/**/*'
    },

    {
      name: 'user-stories-realistic',
      use: { 
        ...devices['Desktop Chrome'],
        headless: false,
        // Realistic tests - human-like timing
        slowMo: 1000,
        // Realistic test specific settings
        actionTimeout: 15000,
        navigationTimeout: 45000,
      },
      testMatch: '**/user_stories/realistic/**/*'
    }
  ],

  // Web Server configuration - start Flask server for testing
  webServer: process.env.CI ? undefined : {
    command: 'python app.py',
    port: 5001,
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
    env: {
      FLASK_ENV: 'testing',
      DATABASE_PATH: 'test_langtrak.db'
    }
  },

  // Global setup and teardown
  globalSetup: require.resolve('./tests/global-setup.js'),
  globalTeardown: require.resolve('./tests/global-teardown.js'),
});