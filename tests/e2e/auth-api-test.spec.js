const { test, expect } = require('@playwright/test');

test.describe('Authentication API Integration', () => {
  test('should register a new user via API', async ({ request }) => {
    const registrationData = {
      username: 'testuser',
      email: 'test@example.com',
      password: 'TestPass123!',
      confirm_password: 'TestPass123!'
    };

    const response = await request.post('/api/auth/register', {
      data: registrationData
    });

    expect(response.status()).toBe(201);
    
    const data = await response.json();
    expect(data.success).toBe(true);
    expect(data.user).toBeDefined();
    expect(data.user.username).toBe('testuser');
    expect(data.user.email).toBe('test@example.com');
    expect(data.session).toBeDefined();
    expect(data.session.token).toBeDefined();
  });

  test('should login with registered credentials', async ({ request }) => {
    // First register a user
    await request.post('/api/auth/register', {
      data: {
        username: 'logintest',
        email: 'login@example.com',
        password: 'LoginPass123!',
        confirm_password: 'LoginPass123!'
      }
    });

    // Then login
    const loginResponse = await request.post('/api/auth/login', {
      data: {
        email: 'login@example.com',
        password: 'LoginPass123!',
        remember_me: false
      }
    });

    expect(loginResponse.status()).toBe(200);
    
    const loginData = await loginResponse.json();
    expect(loginData.success).toBe(true);
    expect(loginData.user).toBeDefined();
    expect(loginData.session).toBeDefined();
    expect(loginData.session.token).toBeDefined();

    // Test session validation
    const validateResponse = await request.get('/api/auth/validate', {
      headers: {
        'Authorization': `Bearer ${loginData.session.token}`
      }
    });

    expect(validateResponse.status()).toBe(200);
    const validateData = await validateResponse.json();
    expect(validateData.valid).toBe(true);
    expect(validateData.user.email).toBe('login@example.com');
  });

  test('should handle invalid login credentials', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'nonexistent@example.com',
        password: 'wrongpassword'
      }
    });

    expect(response.status()).toBe(401);
    
    const data = await response.json();
    expect(data.success).toBe(false);
    expect(data.errors).toBeDefined();
    expect(Array.isArray(data.errors)).toBe(true);
  });

  test('should validate session token correctly', async ({ request }) => {
    // Test with invalid token
    const invalidResponse = await request.get('/api/auth/validate', {
      headers: {
        'Authorization': 'Bearer invalid-token'
      }
    });

    expect(invalidResponse.status()).toBe(401);
    
    const invalidData = await invalidResponse.json();
    expect(invalidData.error).toBe('Invalid or expired session');
  });

  test('should get app info correctly', async ({ request }) => {
    const response = await request.get('/api/info');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data.name).toBe('Language Tracker');
    expect(data.version).toBe('1.0.0');
    expect(data.features).toBeDefined();
    expect(data.features.authentication).toBe(true);
    expect(data.features.session_management).toBe(true);
  });

  test('should handle logout endpoint', async ({ request }) => {
    // Register and login first
    const regResponse = await request.post('/api/auth/register', {
      data: {
        username: 'logouttest',
        email: 'logout@example.com',
        password: 'LogoutPass123!',
        confirm_password: 'LogoutPass123!'
      }
    });

    const regData = await regResponse.json();
    const token = regData.session.token;

    // Test logout
    const logoutResponse = await request.post('/api/auth/logout', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    expect(logoutResponse.status()).toBe(200);
    
    const logoutData = await logoutResponse.json();
    expect(logoutData.success).toBe(true);

    // Verify token is now invalid
    const validateResponse = await request.get('/api/auth/validate', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    expect(validateResponse.status()).toBe(401);
  });
});