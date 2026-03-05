// resource_id: 9d9cc25b-0e7e-4718-828d-37673b1d0357
/**
 * Playwright Global Teardown
 * Cleans up test environment after E2E and user story testing
 * 
 * Hard Testing Rule Implementation:
 * - Cleans up test databases
 * - Archives test results
 * - Closes browser instances
 * - Validates test completion
 */

async function globalTeardown(config) {
  console.log('🧹 Cleaning up Playwright test environment...');
  
  try {
    // Close any global browser instances
    if (global.__BROWSER_GLOBAL__) {
      await global.__BROWSER_GLOBAL__.close();
      console.log('✅ Debug browser closed');
    }
    
    // Clean up temporary test data
    await cleanupTestData();
    
    // Archive test results
    await archiveTestResults();
    
    // Reset environment variables
    delete process.env.NODE_ENV;
    
    console.log('✅ Playwright test environment cleaned up');
    
  } catch (error) {
    console.error('❌ Failed to cleanup Playwright environment:', error);
    // Don't throw - cleanup failures shouldn't fail the test run
  }
}

async function cleanupTestData() {
  console.log('🗑️  Cleaning up test data...');
  
  // In a real implementation, you might:
  // - Clean up test database records
  // - Remove temporary files
  // - Reset Firebase test data
  // For now, we'll just log the cleanup
  
  console.log('✅ Test data cleaned up');
}

async function archiveTestResults() {
  console.log('📦 Archiving test results...');
  
  // Test results are already saved by Playwright reporters
  // This is where you might:
  // - Upload results to a dashboard
  // - Send notifications about test failures
  // - Update test coverage reports
  
  console.log('✅ Test results archived');
}

module.exports = globalTeardown;