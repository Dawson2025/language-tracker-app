// resource_id: 740964ed-7148-4615-8638-448c96cb371e
/**
 * Playwright Global Setup
 * Prepares test environment for E2E and user story testing
 * 
 * Hard Testing Rule Implementation:
 * - Sets up test databases
 * - Configures Firebase test environment
 * - Prepares test data fixtures
 * - Validates system prerequisites
 */

const { chromium } = require('@playwright/test');
const fs = require('fs').promises;
const path = require('path');

async function globalSetup(config) {
  console.log('🚀 Setting up Playwright test environment...');
  
  try {
    // Ensure test results directory exists
    await fs.mkdir('test-results', { recursive: true });
    await fs.mkdir('playwright-report', { recursive: true });
    
    // Set up test environment variables
    process.env.NODE_ENV = 'test';
    process.env.FIREBASE_PROJECT_ID = 'lang-trak-test';
    
    // Create test data fixtures directory
    await fs.mkdir('tests/fixtures', { recursive: true });
    
    // Create test database schema if needed
    await setupTestDatabase();
    
    // Validate Firebase test environment
    await validateFirebaseTestEnv();
    
    // Create basic test fixtures
    await createTestFixtures();
    
    console.log('✅ Playwright test environment ready');
    
    // Launch a browser instance for debugging if needed
    if (process.env.DEBUG_MODE === 'true') {
      const browser = await chromium.launch({ headless: false });
      const context = await browser.newContext();
      const page = await context.newPage();
      
      // Store browser instance for cleanup
      global.__BROWSER_GLOBAL__ = browser;
      
      console.log('🐛 Debug browser launched');
    }
    
  } catch (error) {
    console.error('❌ Failed to setup Playwright environment:', error);
    throw error;
  }
}

async function setupTestDatabase() {
  console.log('📊 Setting up test database...');
  
  // Check if authentication schema exists
  const schemaPath = 'features/authentication/schema.sql';
  try {
    await fs.access(schemaPath);
    console.log('✅ Database schema found');
  } catch (error) {
    console.log('⚠️  Database schema not found, creating basic structure');
    
    // Create basic schema for testing
    const basicSchema = `
-- Basic test database schema
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
  id VARCHAR(64) PRIMARY KEY,
  user_id INTEGER NOT NULL,
  expires_at DATETIME NOT NULL,
  user_agent TEXT,
  ip_address VARCHAR(45),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
`;
    
    await fs.writeFile('tests/fixtures/test-schema.sql', basicSchema);
    console.log('✅ Basic test schema created');
  }
}

async function validateFirebaseTestEnv() {
  console.log('🔥 Validating Firebase test environment...');
  
  // Check for Firebase test credentials
  const testCredentialsPath = 'firebase-service-account-test.json';
  try {
    await fs.access(testCredentialsPath);
    console.log('✅ Firebase test credentials found');
  } catch (error) {
    console.log('⚠️  Firebase test credentials not found');
    console.log('   Create firebase-service-account-test.json for full Firebase testing');
  }
  
  // Validate Firebase project configuration
  if (process.env.FIREBASE_PROJECT_ID) {
    console.log(`✅ Firebase project: ${process.env.FIREBASE_PROJECT_ID}`);
  } else {
    console.log('⚠️  FIREBASE_PROJECT_ID not set, using default test project');
    process.env.FIREBASE_PROJECT_ID = 'lang-trak-test';
  }
}

async function createTestFixtures() {
  console.log('📝 Creating test fixtures...');
  
  // User test data
  const testUsers = [
    {
      id: 'test-user-1',
      username: 'testuser1',
      email: 'test1@example.com',
      password: 'ValidPassword123!',
      isActive: true
    },
    {
      id: 'test-user-2', 
      username: 'testuser2',
      email: 'test2@example.com',
      password: 'AnotherValid456!',
      isActive: true
    }
  ];
  
  await fs.writeFile(
    'tests/fixtures/test-users.json', 
    JSON.stringify(testUsers, null, 2)
  );
  
  // Authentication test scenarios
  const authScenarios = [
    {
      name: 'Valid Registration',
      data: {
        username: 'newuser',
        email: 'newuser@example.com',
        password: 'StrongPassword789!',
        confirmPassword: 'StrongPassword789!'
      },
      expectedResult: 'success'
    },
    {
      name: 'Invalid Email Format',
      data: {
        username: 'testuser',
        email: 'invalid-email',
        password: 'ValidPassword123!',
        confirmPassword: 'ValidPassword123!'
      },
      expectedResult: 'validation_error'
    },
    {
      name: 'Weak Password',
      data: {
        username: 'testuser',
        email: 'test@example.com',
        password: '123',
        confirmPassword: '123'
      },
      expectedResult: 'validation_error'
    }
  ];
  
  await fs.writeFile(
    'tests/fixtures/auth-scenarios.json',
    JSON.stringify(authScenarios, null, 2)
  );
  
  console.log('✅ Test fixtures created');
}

module.exports = globalSetup;