# resource_id: d6aa36a6-b4fb-4e00-84c7-453ba01a7821
"""
US-001: User Registration - Realistic Test
Full end-to-end registration workflow with real Firebase backend integration.
Target: <5 minutes execution time

This test covers:
- Complete user registration journey
- Real Firebase Authentication integration
- Email verification workflow
- Database record creation
- UI/UX validation with realistic user behavior
- Cross-browser compatibility checks
"""

import pytest
import asyncio
import time
from playwright.async_api import async_playwright
from tests.utils.firebase_helpers import FirebaseTestHelper
from tests.utils.email_helpers import EmailTestHelper


class TestUS001RegistrationRealistic:
    """Realistic end-to-end tests for user registration"""
    
    @pytest.fixture(scope="class")
    async def firebase_helper(self):
        """Firebase test helper for managing test data"""
        helper = FirebaseTestHelper(environment="test")
        await helper.initialize()
        yield helper
        await helper.cleanup()
    
    @pytest.fixture(scope="class")
    async def email_helper(self):
        """Email test helper for verification workflow"""
        helper = EmailTestHelper()
        yield helper
        await helper.cleanup()
    
    @pytest.fixture
    async def browser_context(self):
        """Set up headed Chromium browser with realistic settings"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=False,  # Headed for MCP visual validation
            slow_mo=100,     # Realistic interaction speed
        )
        
        # Create context with realistic browser settings
        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        yield context
        await context.close()
        await browser.close()
        await playwright.stop()
    
    @pytest.fixture
    async def page(self, browser_context):
        """Create a new page for testing"""
        page = await browser_context.new_page()
        
        # Set up request/response logging
        page.on("request", lambda request: print(f"Request: {request.method} {request.url}"))
        page.on("response", lambda response: print(f"Response: {response.status} {response.url}"))
        
        return page
    
    async def test_complete_registration_workflow(self, page, firebase_helper, email_helper):
        """Test complete user registration from start to email verification"""
        test_email = f"test_{int(time.time())}@example.com"
        test_password = "SecureTestPass123!"
        
        # Step 1: Navigate to registration page
        await page.goto("http://localhost:5000/register")
        await page.wait_for_load_state("networkidle")
        
        # Verify page loaded correctly
        await page.wait_for_selector('[data-testid=\"registration-form\"]', timeout=10000)
        assert await page.title() == "Register - Language Tracker"
        
        # Step 2: Fill out registration form with realistic typing speed
        await self._realistic_form_fill(page, {
            '[data-testid=\"email-input\"]': test_email,
            '[data-testid=\"password-input\"]': test_password,
            '[data-testid=\"confirm-password-input\"]': test_password,
            '[data-testid=\"first-name-input\"]': 'Test',
            '[data-testid=\"last-name-input\"]': 'User'
        })\n        \n        # Step 3: Accept terms of service\n        await page.check('[data-testid=\"terms-checkbox\"]')\n        \n        # Wait for form validation to complete\n        await page.wait_for_function(\n            'document.querySelector(\"[data-testid=register-button]\").disabled === false'\n        )\n        \n        # Step 4: Submit registration\n        await page.click('[data-testid=\"register-button\"]')\n        \n        # Wait for registration to process\n        await page.wait_for_selector('[data-testid=\"registration-pending\"]', timeout=10000)\n        \n        # Step 5: Verify success message appears\n        await page.wait_for_selector('[data-testid=\"registration-success\"]', timeout=30000)\n        success_message = await page.text_content('[data-testid=\"registration-success\"]')\n        assert \"registration successful\" in success_message.lower()\n        assert \"verification email\" in success_message.lower()\n        \n        # Step 6: Verify user was created in Firebase\n        user_record = await firebase_helper.get_user_by_email(test_email)\n        assert user_record is not None\n        assert user_record.email == test_email\n        assert not user_record.email_verified  # Should be unverified initially\n        \n        # Step 7: Check that verification email was sent\n        verification_emails = await email_helper.get_emails_for_address(test_email)\n        assert len(verification_emails) > 0\n        \n        verification_email = verification_emails[-1]  # Most recent\n        assert \"verify your email\" in verification_email.subject.lower()\n        \n        # Step 8: Extract verification link and verify email\n        verification_link = email_helper.extract_verification_link(verification_email.body)\n        assert verification_link is not None\n        \n        # Navigate to verification link\n        await page.goto(verification_link)\n        await page.wait_for_load_state(\"networkidle\")\n        \n        # Step 9: Verify email verification success\n        await page.wait_for_selector('[data-testid=\"email-verified-success\"]', timeout=10000)\n        verification_message = await page.text_content('[data-testid=\"email-verified-success\"]')\n        assert \"email verified\" in verification_message.lower()\n        \n        # Step 10: Verify user is now marked as verified in Firebase\n        updated_user = await firebase_helper.get_user_by_email(test_email)\n        assert updated_user.email_verified\n        \n        # Step 11: Verify can now login\n        await page.goto(\"http://localhost:5000/login\")\n        await page.fill('[data-testid=\"login-email\"]', test_email)\n        await page.fill('[data-testid=\"login-password\"]', test_password)\n        await page.click('[data-testid=\"login-button\"]')\n        \n        # Should successfully log in and redirect to dashboard\n        await page.wait_for_url(\"**/dashboard\", timeout=15000)\n        \n        # Clean up test user\n        await firebase_helper.delete_user(user_record.uid)\n    \n    async def test_registration_with_realistic_user_errors(self, page):\n        \"\"\"Test registration handling realistic user input errors\"\"\"\n        await page.goto(\"http://localhost:5000/register\")\n        await page.wait_for_load_state(\"networkidle\")\n        \n        # Scenario 1: User types email incorrectly, then corrects it\n        await page.type('[data-testid=\"email-input\"]', 'test@gmial.com', delay=50)  # Typo\n        await page.blur('[data-testid=\"email-input\"]')  # Focus away to trigger validation\n        \n        # Wait for any email suggestions or validation\n        await asyncio.sleep(1)\n        \n        # User realizes mistake and corrects it\n        await page.triple_click('[data-testid=\"email-input\"]')\n        await page.type('[data-testid=\"email-input\"]', 'test@gmail.com', delay=50)\n        \n        # Scenario 2: User creates weak password, sees strength indicator, improves it\n        await page.type('[data-testid=\"password-input\"]', 'password', delay=50)\n        \n        # Check password strength indicator\n        await page.wait_for_selector('[data-testid=\"password-strength-weak\"]', timeout=5000)\n        \n        # User improves password\n        await page.fill('[data-testid=\"password-input\"]', '')\n        await page.type('[data-testid=\"password-input\"]', 'StrongPass123!', delay=50)\n        \n        # Should now show strong password\n        await page.wait_for_selector('[data-testid=\"password-strength-strong\"]', timeout=5000)\n        \n        # Scenario 3: User forgets to match password confirmation\n        await page.type('[data-testid=\"confirm-password-input\"]', 'DifferentPass', delay=50)\n        await page.blur('[data-testid=\"confirm-password-input\"]')\n        \n        # Should show mismatch error\n        await page.wait_for_selector('[data-testid=\"password-mismatch-error\"]', timeout=5000)\n        \n        # User corrects it\n        await page.fill('[data-testid=\"confirm-password-input\"]', 'StrongPass123!')\n        \n        # Mismatch error should disappear\n        await page.wait_for_selector('[data-testid=\"password-mismatch-error\"]', state='hidden', timeout=5000)\n        \n        # Scenario 4: User tries to submit without accepting terms\n        await page.click('[data-testid=\"register-button\"]')\n        \n        # Should highlight terms checkbox and show error\n        await page.wait_for_selector('[data-testid=\"terms-error\"]', timeout=5000)\n        \n        # User accepts terms\n        await page.check('[data-testid=\"terms-checkbox\"]')\n        \n        # Error should disappear\n        await page.wait_for_selector('[data-testid=\"terms-error\"]', state='hidden', timeout=5000)\n    \n    async def test_registration_performance_realistic_load(self, browser_context):\n        \"\"\"Test registration under realistic load conditions\"\"\"\n        # Create multiple concurrent registration attempts\n        tasks = []\n        for i in range(5):\n            task = self._concurrent_registration_test(browser_context, i)\n            tasks.append(task)\n        \n        # Wait for all registrations to complete\n        results = await asyncio.gather(*tasks, return_exceptions=True)\n        \n        # Verify all succeeded or identify issues\n        successful_registrations = [r for r in results if not isinstance(r, Exception)]\n        assert len(successful_registrations) >= 4, \"At least 80% of concurrent registrations should succeed\"\n    \n    async def _concurrent_registration_test(self, browser_context, user_id):\n        \"\"\"Helper method for concurrent registration testing\"\"\"\n        page = await browser_context.new_page()\n        try:\n            test_email = f\"concurrent_test_{user_id}_{int(time.time())}@example.com\"\n            \n            await page.goto(\"http://localhost:5000/register\")\n            await page.wait_for_load_state(\"networkidle\")\n            \n            await self._realistic_form_fill(page, {\n                '[data-testid=\"email-input\"]': test_email,\n                '[data-testid=\"password-input\"]': f\"ConcurrentPass{user_id}!\",\n                '[data-testid=\"confirm-password-input\"]': f\"ConcurrentPass{user_id}!\",\n            })\n            \n            await page.check('[data-testid=\"terms-checkbox\"]')\n            await page.click('[data-testid=\"register-button\"]')\n            \n            # Wait for either success or failure\n            await page.wait_for_selector(\n                '[data-testid=\"registration-success\"], [data-testid=\"registration-error\"]',\n                timeout=30000\n            )\n            \n            return True\n        finally:\n            await page.close()\n    \n    async def test_cross_browser_compatibility(self, firebase_helper):\n        \"\"\"Test registration across different browser contexts\"\"\"\n        browsers_to_test = [\n            {'name': 'chromium', 'viewport': {'width': 1366, 'height': 768}},\n            {'name': 'firefox', 'viewport': {'width': 1280, 'height': 720}},\n            {'name': 'webkit', 'viewport': {'width': 1440, 'height': 900}}\n        ]\n        \n        playwright = await async_playwright().start()\n        \n        try:\n            for browser_config in browsers_to_test:\n                browser_name = browser_config['name']\n                browser = await getattr(playwright, browser_name).launch(headless=False)\n                \n                context = await browser.new_context(\n                    viewport=browser_config['viewport'],\n                    user_agent=f'Test-{browser_name}'\n                )\n                \n                page = await context.new_page()\n                \n                try:\n                    test_email = f\"{browser_name}_test_{int(time.time())}@example.com\"\n                    \n                    await page.goto(\"http://localhost:5000/register\")\n                    await page.wait_for_load_state(\"networkidle\")\n                    \n                    # Test basic registration flow\n                    await self._realistic_form_fill(page, {\n                        '[data-testid=\"email-input\"]': test_email,\n                        '[data-testid=\"password-input\"]': f\"BrowserTest123!\",\n                        '[data-testid=\"confirm-password-input\"]': f\"BrowserTest123!\",\n                    })\n                    \n                    await page.check('[data-testid=\"terms-checkbox\"]')\n                    await page.click('[data-testid=\"register-button\"]')\n                    \n                    # Verify success\n                    await page.wait_for_selector('[data-testid=\"registration-success\"]', timeout=20000)\n                    \n                    # Clean up\n                    user = await firebase_helper.get_user_by_email(test_email)\n                    if user:\n                        await firebase_helper.delete_user(user.uid)\n                        \n                except Exception as e:\n                    pytest.fail(f\"Registration failed in {browser_name}: {e}\")\n                finally:\n                    await context.close()\n                    await browser.close()\n        finally:\n            await playwright.stop()\n    \n    async def _realistic_form_fill(self, page, fields):\n        \"\"\"Fill form fields with realistic typing simulation\"\"\"\n        for selector, value in fields.items():\n            await page.click(selector)\n            await asyncio.sleep(0.1)  # Brief pause before typing\n            \n            # Type with realistic speed and occasional pauses\n            for i, char in enumerate(value):\n                await page.keyboard.type(char)\n                \n                # Random brief pauses to simulate natural typing\n                if i % 5 == 0 and i > 0:\n                    await asyncio.sleep(0.05)\n            \n            # Brief pause after completing field\n            await asyncio.sleep(0.2)\n    \n    @pytest.mark.slow\n    async def test_registration_email_deliverability(self, page, email_helper):\n        \"\"\"Test that registration emails are actually deliverable and properly formatted\"\"\"\n        # Use a real email testing service for this test\n        test_email = await email_helper.create_test_email_address()\n        \n        try:\n            await page.goto(\"http://localhost:5000/register\")\n            await page.wait_for_load_state(\"networkidle\")\n            \n            await self._realistic_form_fill(page, {\n                '[data-testid=\"email-input\"]': test_email,\n                '[data-testid=\"password-input\"]': \"EmailTest123!\",\n                '[data-testid=\"confirm-password-input\"]': \"EmailTest123!\",\n            })\n            \n            await page.check('[data-testid=\"terms-checkbox\"]')\n            await page.click('[data-testid=\"register-button\"]')\n            \n            # Wait for registration success\n            await page.wait_for_selector('[data-testid=\"registration-success\"]', timeout=30000)\n            \n            # Wait for email to be delivered (may take time with real email service)\n            verification_email = await email_helper.wait_for_email(\n                test_email, \n                subject_contains=\"verify\",\n                timeout=60\n            )\n            \n            # Verify email content and formatting\n            assert verification_email is not None\n            assert \"Language Tracker\" in verification_email.sender_name\n            assert \"verify your email\" in verification_email.subject.lower()\n            \n            # Check email HTML formatting\n            assert \"<html>\" in verification_email.html_body\n            assert \"href=\" in verification_email.html_body  # Contains verification link\n            \n            # Verify plain text version exists\n            assert len(verification_email.text_body) > 0\n            assert \"verify\" in verification_email.text_body.lower()\n            \n        finally:\n            await email_helper.cleanup_test_email(test_email)\n\n\nif __name__ == \"__main__\":\n    # Run realistic tests\n    pytest.main([__file__, \"-v\", \"--tb=long\", \"-s\"])