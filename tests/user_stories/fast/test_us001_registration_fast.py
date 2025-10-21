"""
US-001: User Registration - Fast Test
Fast validation of core registration functionality with minimal UI interactions and mocked dependencies.
Target: <30 seconds execution time

This test focuses on:
- Core form validation logic
- Firebase Auth integration (mocked)
- Error handling paths
- Success flow confirmation
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from playwright.async_api import async_playwright


class TestUS001RegistrationFast:
    """Fast tests for user registration functionality"""
    
    @pytest.fixture
    async def browser_context(self):
        """Set up headed Chromium browser for testing"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)  # Headed for MCP
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        yield context
        await context.close()
        await browser.close()
        await playwright.stop()
    
    @pytest.fixture
    async def page(self, browser_context):
        """Create a new page for testing"""
        page = await browser_context.new_page()
        # Navigate to registration page
        await page.goto("http://localhost:5000/register")
        return page
    
    @patch('firebase_admin.auth.create_user')
    async def test_valid_registration_form_submission(self, mock_create_user, page):
        """Test successful registration with valid data"""
        # Arrange
        mock_create_user.return_value = Mock(uid='test-uid-123')
        
        # Act - Fill registration form
        await page.fill('[data-testid="email-input"]', 'test@example.com')
        await page.fill('[data-testid="password-input"]', 'SecurePass123!')
        await page.fill('[data-testid="confirm-password-input"]', 'SecurePass123!')
        await page.check('[data-testid="terms-checkbox"]')
        
        # Submit form
        await page.click('[data-testid="register-button"]')
        
        # Assert
        # Wait for success message or redirect
        await page.wait_for_selector('[data-testid="success-message"]', timeout=5000)
        
        # Verify Firebase auth was called
        mock_create_user.assert_called_once()
        
        # Verify form is submitted correctly
        success_message = await page.text_content('[data-testid="success-message"]')
        assert "registration successful" in success_message.lower()
    
    async def test_email_validation_errors(self, page):
        """Test email validation error display"""
        # Test invalid email formats
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "test@",
            "test..test@domain.com"
        ]
        
        for invalid_email in invalid_emails:
            # Fill form with invalid email
            await page.fill('[data-testid="email-input"]', invalid_email)
            await page.fill('[data-testid="password-input"]', 'ValidPass123!')
            
            # Try to submit
            await page.click('[data-testid="register-button"]')
            
            # Check for validation error
            await page.wait_for_selector('[data-testid="email-error"]', timeout=2000)
            error_text = await page.text_content('[data-testid="email-error"]')
            assert "valid email" in error_text.lower()
            
            # Clear for next test
            await page.fill('[data-testid="email-input"]', '')
    
    async def test_password_strength_validation(self, page):
        """Test password strength requirements"""
        weak_passwords = [
            "weak",           # Too short
            "weakpassword",   # No numbers or special chars
            "12345678",       # Only numbers
            "WEAKPASS"        # No lowercase or numbers
        ]
        
        for weak_password in weak_passwords:
            await page.fill('[data-testid="email-input"]', 'test@example.com')
            await page.fill('[data-testid="password-input"]', weak_password)
            
            # Check if password strength indicator appears
            await page.wait_for_selector('[data-testid="password-strength"]', timeout=1000)
            strength_indicator = await page.get_attribute('[data-testid="password-strength"]', 'class')
            
            # Should show weak/invalid strength
            assert 'weak' in strength_indicator.lower() or 'invalid' in strength_indicator.lower()
    
    async def test_password_confirmation_mismatch(self, page):
        """Test password confirmation validation"""
        await page.fill('[data-testid="email-input"]', 'test@example.com')
        await page.fill('[data-testid="password-input"]', 'ValidPass123!')
        await page.fill('[data-testid="confirm-password-input"]', 'DifferentPass456!')
        
        await page.click('[data-testid="register-button"]')
        
        # Check for mismatch error
        await page.wait_for_selector('[data-testid="confirm-password-error"]', timeout=2000)
        error_text = await page.text_content('[data-testid="confirm-password-error"]')
        assert "passwords do not match" in error_text.lower()
    
    async def test_terms_acceptance_required(self, page):
        """Test that terms of service must be accepted"""
        await page.fill('[data-testid="email-input"]', 'test@example.com')
        await page.fill('[data-testid="password-input"]', 'ValidPass123!')
        await page.fill('[data-testid="confirm-password-input"]', 'ValidPass123!')
        
        # Don't check terms checkbox
        await page.click('[data-testid="register-button"]')
        
        # Should show terms error
        await page.wait_for_selector('[data-testid="terms-error"]', timeout=2000)
        error_text = await page.text_content('[data-testid="terms-error"]')
        assert "terms" in error_text.lower() and "accept" in error_text.lower()
    
    @patch('firebase_admin.auth.create_user')
    async def test_registration_network_error(self, mock_create_user, page):
        """Test registration handling when Firebase is unavailable"""
        # Simulate network error
        mock_create_user.side_effect = Exception("Network error")
        
        await page.fill('[data-testid="email-input"]', 'test@example.com')
        await page.fill('[data-testid="password-input"]', 'ValidPass123!')
        await page.fill('[data-testid="confirm-password-input"]', 'ValidPass123!')
        await page.check('[data-testid="terms-checkbox"]')
        
        await page.click('[data-testid="register-button"]')
        
        # Should show error message
        await page.wait_for_selector('[data-testid="error-message"]', timeout=5000)
        error_text = await page.text_content('[data-testid="error-message"]')
        assert "error" in error_text.lower() or "failed" in error_text.lower()
    
    async def test_form_field_persistence(self, page):
        """Test that form fields retain values on validation errors"""
        test_email = 'test@example.com'
        await page.fill('[data-testid="email-input"]', test_email)
        await page.fill('[data-testid="password-input"]', 'weak')  # Trigger validation error
        
        await page.click('[data-testid="register-button"]')
        
        # Wait for error to appear
        await page.wait_for_selector('[data-testid="password-error"]', timeout=2000)
        
        # Email field should still contain the value
        email_value = await page.input_value('[data-testid="email-input"]')
        assert email_value == test_email


@pytest.mark.asyncio
async def test_registration_accessibility():
    """Test basic accessibility features of registration form"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        await page.goto("http://localhost:5000/register")
        
        # Check for proper labels
        email_label = await page.locator('label[for*="email"]').count()
        password_label = await page.locator('label[for*="password"]').count()
        
        assert email_label > 0, "Email input should have associated label"
        assert password_label > 0, "Password input should have associated label"
        
        # Check tab navigation
        await page.press('body', 'Tab')  # Should focus first input
        focused_element = await page.evaluate('document.activeElement.getAttribute("data-testid")')
        assert focused_element == 'email-input'
        
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    # Run fast tests
    pytest.main([__file__, "-v", "--tb=short"])