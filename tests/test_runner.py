#!/usr/bin/env python3
# resource_id: b919dab1-8550-4f3f-803e-f8e0e9bf471b
"""
Comprehensive Test Runner for Hard Testing Rule Enforcement
Language Tracker - CI/CD Integration

Features:
- Performance benchmarking and metrics collection
- Parallel test execution with optimization
- Firebase environment validation
- Coverage reporting and enforcement
- CI notification systems
- Hard rule compliance checking
"""

import os
import sys
import time
import json
import subprocess
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

# Add fixtures to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fixtures'))

from database_fixtures import (
    TestDatabaseManager, TestDataFactory, FirebaseTestConfig, 
    TestMetricsCollector
)


class TestSuite:
    """Represents a test suite with execution parameters."""
    
    def __init__(self, name: str, path: str, timeout: int, parallel_workers: int = 1):
        self.name = name
        self.path = path
        self.timeout = timeout
        self.parallel_workers = parallel_workers
        self.results = None
        self.execution_time = 0
        self.coverage = 0.0


class HardTestingRuleRunner:
    """Main test runner that enforces the hard testing rule."""
    
    def __init__(self, environment: str = 'test', coverage_threshold: float = 90.0):
        self.environment = environment
        self.coverage_threshold = coverage_threshold
        self.start_time = None
        self.db_manager = None
        self.metrics_collector = None
        self.results = {}
        
        # Define test suites with performance benchmarks
        self.test_suites = [
            TestSuite('unit_tests', 'features/authentication/tests/unit/', 30, 4),
            TestSuite('integration_tests', 'features/authentication/tests/integration/', 60, 2),
            TestSuite('e2e_tests', 'tests/e2e/', 180, 2),
            TestSuite('user_story_fast', 'tests/user_stories/fast/', 60, 4),
            TestSuite('user_story_realistic', 'tests/user_stories/realistic/', 600, 1),
        ]
    
    def setup_environment(self):
        """Set up test environment and infrastructure."""
        print("🚀 Setting up Hard Testing Rule environment...")
        
        self.start_time = time.time()
        
        # Set up test database
        self.db_manager = TestDatabaseManager(self.environment)
        db_path = self.db_manager.create_test_database()
        print(f"✅ Test database initialized: {os.path.basename(db_path)}")
        
        # Set up metrics collection
        self.metrics_collector = TestMetricsCollector(self.db_manager)
        
        # Create test data fixtures
        factory = TestDataFactory(self.db_manager)
        users = factory.create_test_users(5)
        sessions = factory.create_test_sessions([user['id'] for user in users[:3]])
        progress = factory.create_language_progress([user['id'] for user in users])
        
        print(f"✅ Test fixtures created: {len(users)} users, {len(sessions)} sessions")
        
        # Validate Firebase configuration
        self._validate_firebase_config()
        
        # Set environment variables
        os.environ['NODE_ENV'] = 'test'
        os.environ['COVERAGE_THRESHOLD'] = str(self.coverage_threshold)
        
        print("✅ Test environment ready")
    
    def _validate_firebase_config(self):
        """Validate Firebase configuration for testing."""
        try:
            config = FirebaseTestConfig.get_config(self.environment)
            has_credentials = FirebaseTestConfig.validate_credentials(self.environment)
            
            print(f"🔥 Firebase project: {config['project_id']}")
            
            if has_credentials:
                print("✅ Firebase service account credentials found")
            else:
                print("⚠️  Firebase service account credentials not found")
                print(f"   Create {config['service_account_file']} for full Firebase testing")
                
        except ValueError as e:
            print(f"❌ Firebase configuration error: {e}")
    
    def run_test_suite(self, suite: TestSuite) -> Dict[str, Any]:
        """Run a single test suite with performance monitoring."""
        print(f"\n🧪 Running {suite.name}...")
        start_time = time.time()
        
        # Determine test command based on suite type
        if suite.name in ['unit_tests', 'integration_tests']:
            cmd = self._build_pytest_command(suite)
        else:
            cmd = self._build_playwright_command(suite)
        
        print(f"⚡ Command: {' '.join(cmd)}")
        
        # Execute with timeout
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=suite.timeout,
                cwd=os.getcwd()
            )
            
            execution_time = time.time() - start_time
            suite.execution_time = execution_time
            
            # Parse results
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            # Record metrics
            self.metrics_collector.record_test_execution(
                suite.name,
                f"{suite.name}_full_suite",
                int(execution_time * 1000),
                'passed' if success else 'failed',
                self.environment
            )
            
            # Extract coverage if available
            coverage = self._extract_coverage(output)
            suite.coverage = coverage
            
            suite_result = {
                'name': suite.name,
                'success': success,
                'execution_time': execution_time,
                'coverage': coverage,
                'output': output,
                'return_code': result.returncode
            }
            
            if success:
                print(f"✅ {suite.name} passed in {execution_time:.2f}s")
                if coverage > 0:
                    print(f"📊 Coverage: {coverage:.1f}%")
            else:
                print(f"❌ {suite.name} failed in {execution_time:.2f}s")
                print(f"🔍 Output: {output[:200]}...")
            
            return suite_result
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"⏰ {suite.name} timed out after {suite.timeout}s")
            
            # Record timeout
            self.metrics_collector.record_test_execution(
                suite.name,
                f"{suite.name}_timeout",
                suite.timeout * 1000,
                'timeout',
                self.environment
            )
            
            return {
                'name': suite.name,
                'success': False,
                'execution_time': execution_time,
                'coverage': 0.0,
                'output': f"Test suite timed out after {suite.timeout} seconds",
                'return_code': 124  # Timeout return code
            }
    
    def _build_pytest_command(self, suite: TestSuite) -> List[str]:
        """Build pytest command for Python test suites."""
        cmd = [
            'python', '-m', 'coverage', 'run', '--append', '--source=features',
            '-m', 'pytest', 
            suite.path,
            '--verbose',
            '--tb=short',
            f'--workers={suite.parallel_workers}' if suite.parallel_workers > 1 else '--workers=1',
            '--junit-xml=test-results/junit.xml',
            '--cov-report=xml:test-results/coverage.xml',
            '--cov-report=html:test-results/htmlcov',
            f'--cov-fail-under={self.coverage_threshold}'
        ]
        
        return [arg for arg in cmd if arg]  # Filter empty strings
    
    def _build_playwright_command(self, suite: TestSuite) -> List[str]:
        """Build Playwright command for E2E test suites."""
        cmd = [
            'npx', 'playwright', 'test',
            suite.path,
            '--headed',  # CRITICAL: Use headed Chromium
            '--reporter=json',
            '--output-dir=test-results',
            f'--workers={suite.parallel_workers}',
            f'--timeout={suite.timeout * 1000}',  # Convert to ms
            '--project=chromium-headed'
        ]
        
        return cmd
    
    def _extract_coverage(self, output: str) -> float:
        """Extract coverage percentage from test output."""
        import re
        
        # Look for coverage patterns
        patterns = [
            r'TOTAL.*?(\d+)%',
            r'coverage.*?(\d+)%',
            r'(\d+)%\s+coverage'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            if matches:
                try:
                    return float(matches[-1])
                except ValueError:
                    continue
        
        return 0.0
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites in sequence (for proper dependency management)."""
        print("\n🚨 HARD TESTING RULE ENFORCEMENT STARTED")
        print("=" * 60)
        
        total_start_time = time.time()
        all_results = []
        overall_success = True
        
        for suite in self.test_suites:
            result = self.run_test_suite(suite)
            all_results.append(result)
            
            if not result['success']:
                overall_success = False
                print(f"🚫 HARD RULE VIOLATION: {suite.name} failed")
        
        total_execution_time = time.time() - total_start_time
        
        # Generate comprehensive report
        report = self._generate_report(all_results, total_execution_time, overall_success)
        
        # Enforce hard rule
        if not overall_success:
            print("\n🚨 HARD TESTING RULE VIOLATION DETECTED")
            print("❌ ALL PROGRESSION IS BLOCKED")
            print("🔒 Fix all failing tests before continuing")
            
            # Save failure report
            self._save_failure_report(report)
            
            sys.exit(1)  # Hard exit - no progression allowed
        
        print("\n✅ HARD TESTING RULE COMPLIANCE VERIFIED")
        print("🎉 All tests passed - progression allowed")
        
        # Save success report
        self._save_success_report(report)
        
        return report
    
    def _generate_report(self, results: List[Dict[str, Any]], 
                        total_time: float, success: bool) -> Dict[str, Any]:
        """Generate comprehensive test execution report."""
        
        # Calculate totals
        total_coverage = sum(r['coverage'] for r in results if r['coverage'] > 0)
        covered_suites = sum(1 for r in results if r['coverage'] > 0)
        avg_coverage = total_coverage / covered_suites if covered_suites > 0 else 0
        
        passed_suites = sum(1 for r in results if r['success'])
        failed_suites = len(results) - passed_suites
        
        # Get performance metrics
        performance_summary = self.metrics_collector.get_performance_summary()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'environment': self.environment,
            'hard_rule_compliance': success,
            'summary': {
                'total_suites': len(results),
                'passed_suites': passed_suites,
                'failed_suites': failed_suites,
                'total_execution_time': total_time,
                'average_coverage': avg_coverage,
                'coverage_threshold': self.coverage_threshold,
                'coverage_compliance': avg_coverage >= self.coverage_threshold
            },
            'suite_results': results,
            'performance_metrics': performance_summary,
            'next_actions': self._get_next_actions(success, avg_coverage)
        }
        
        return report
    
    def _get_next_actions(self, success: bool, coverage: float) -> List[str]:
        """Get recommended next actions based on test results."""
        actions = []
        
        if not success:
            actions.extend([
                "🚨 IMMEDIATE: Fix all failing tests before any code changes",
                "🔍 Review test output and error messages above",
                "🛠️ Address root causes of test failures",
                "✅ Re-run tests to verify fixes",
                "📝 Update documentation if test changes were needed"
            ])
        
        if coverage < self.coverage_threshold:
            actions.extend([
                f"📊 COVERAGE: Increase test coverage from {coverage:.1f}% to {self.coverage_threshold}%",
                "🧪 Add unit tests for uncovered code paths",
                "🔄 Review integration test coverage",
                "📋 Update test documentation"
            ])
        
        if success and coverage >= self.coverage_threshold:
            actions.extend([
                "✅ All tests passing - ready for development progression",
                "🚀 CI/CD pipeline can proceed",
                "📦 Code is ready for deployment consideration",
                "🎯 Consider additional test scenarios for edge cases"
            ])
        
        return actions
    
    def _save_success_report(self, report: Dict[str, Any]):
        """Save success report for CI/CD reference."""
        os.makedirs('test-results', exist_ok=True)
        
        with open('test-results/test-success-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also create a simple status file
        with open('test-results/hard-rule-status.txt', 'w') as f:
            f.write(f"HARD_RULE_STATUS=PASSED\n")
            f.write(f"TIMESTAMP={report['timestamp']}\n")
            f.write(f"COVERAGE={report['summary']['average_coverage']:.1f}%\n")
            f.write(f"TOTAL_TIME={report['summary']['total_execution_time']:.1f}s\n")
    
    def _save_failure_report(self, report: Dict[str, Any]):
        """Save failure report for debugging."""
        os.makedirs('test-results', exist_ok=True)
        
        with open('test-results/test-failure-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Create failure status file
        with open('test-results/hard-rule-status.txt', 'w') as f:
            f.write(f"HARD_RULE_STATUS=FAILED\n")
            f.write(f"TIMESTAMP={report['timestamp']}\n")
            f.write(f"FAILED_SUITES={report['summary']['failed_suites']}\n")
            f.write(f"COVERAGE={report['summary']['average_coverage']:.1f}%\n")
    
    def cleanup(self):
        """Clean up test environment."""
        if self.db_manager:
            self.db_manager.cleanup()
        
        print("🧹 Test environment cleaned up")


class CINotificationSystem:
    """Handles CI/CD notifications for test results."""
    
    @staticmethod
    def send_slack_notification(webhook_url: str, report: Dict[str, Any]):
        """Send Slack notification (placeholder for implementation)."""
        # In real implementation, would send to Slack webhook
        print(f"📨 Slack notification would be sent to {webhook_url}")
    
    @staticmethod
    def send_email_notification(report: Dict[str, Any]):
        """Send email notification (placeholder for implementation)."""
        # In real implementation, would send email
        print("📧 Email notification would be sent")
    
    @staticmethod
    def update_github_status(report: Dict[str, Any]):
        """Update GitHub commit status (placeholder for implementation)."""
        # In real implementation, would update GitHub status
        status = "success" if report['hard_rule_compliance'] else "failure"
        print(f"📝 GitHub status would be updated to: {status}")


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hard Testing Rule Enforcement Runner')
    parser.add_argument('--environment', default='test', choices=['dev', 'test', 'staging', 'prod'],
                       help='Test environment')
    parser.add_argument('--coverage-threshold', type=float, default=90.0,
                       help='Coverage threshold percentage')
    parser.add_argument('--suite', help='Run specific test suite only')
    parser.add_argument('--notify', action='store_true', help='Send notifications')
    
    args = parser.parse_args()
    
    # Create and run test runner
    runner = HardTestingRuleRunner(args.environment, args.coverage_threshold)
    
    try:
        runner.setup_environment()
        
        if args.suite:
            # Run specific suite
            suite = next((s for s in runner.test_suites if s.name == args.suite), None)
            if not suite:
                print(f"❌ Unknown test suite: {args.suite}")
                sys.exit(1)
            
            result = runner.run_test_suite(suite)
            success = result['success']
        else:
            # Run all tests
            report = runner.run_all_tests()
            success = report['hard_rule_compliance']
            
            # Send notifications if requested
            if args.notify:
                notifications = CINotificationSystem()
                notifications.update_github_status(report)
    
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
        success = False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        success = False
    finally:
        runner.cleanup()
    
    # Exit with appropriate code for CI/CD
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()