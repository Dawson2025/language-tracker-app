#!/usr/bin/env python3
"""
User Story Test Runner with Playwright MCP Integration

This script orchestrates the execution of user story tests using Playwright MCP
with headed Chromium browsers for both fast and realistic test suites.

Usage:
    python run_user_story_tests.py --type=fast --environment=dev
    python run_user_story_tests.py --type=realistic --environment=test  
    python run_user_story_tests.py --type=both --environment=staging --parallel
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from automations.test_config import (
    UserStoryTestOrchestrator, 
    run_parallel_tests,
    TEST_COMMANDS
)


class UserStoryTestRunner:
    """Main test runner for user story validation"""
    
    def __init__(self, environment: str = "dev"):
        self.environment = environment
        self.orchestrator = UserStoryTestOrchestrator()
        self.results: Dict[str, Dict] = {}
        
    async def run_tests(self, 
                       test_type: str = "both", 
                       parallel: bool = True,
                       story_filter: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Run user story tests with specified configuration
        
        Args:
            test_type: "fast", "realistic", or "both"
            parallel: Whether to run tests in parallel groups
            story_filter: Optional list of specific story IDs to run
            
        Returns:
            Dictionary mapping story IDs to success/failure status
        """
        print(f"🚀 Starting User Story Tests")
        print(f"📋 Type: {test_type}, Environment: {self.environment}, Parallel: {parallel}")
        
        if story_filter:
            print(f"🎯 Filtering stories: {', '.join(story_filter)}")
        
        start_time = time.time()
        
        try:
            if parallel:
                results = await self._run_parallel_tests(test_type, story_filter)
            else:
                results = await self._run_sequential_tests(test_type, story_filter)
            
            execution_time = time.time() - start_time
            await self._generate_test_report(results, execution_time, test_type)
            
            return results
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return {}
    
    async def _run_parallel_tests(self, test_type: str, story_filter: Optional[List[str]]) -> Dict[str, bool]:
        """Execute tests using parallel orchestration"""
        print("🔄 Using parallel test execution")
        
        # Filter stories if specified
        if story_filter:
            original_configs = dict(self.orchestrator.test_configs)
            self.orchestrator.test_configs = {
                k: v for k, v in original_configs.items() 
                if k in story_filter
            }
        
        results = await run_parallel_tests(
            self.orchestrator,
            test_type=test_type,
            environment=self.environment
        )
        
        return results
    
    async def _run_sequential_tests(self, test_type: str, story_filter: Optional[List[str]]) -> Dict[str, bool]:
        """Execute tests sequentially (for debugging or resource constraints)"""
        print("🔄 Using sequential test execution")
        
        results = {}
        configs_to_run = self.orchestrator.test_configs.values()
        
        if story_filter:
            configs_to_run = [
                config for config in configs_to_run 
                if config.story_id in story_filter
            ]
        
        # Sort by priority
        sorted_configs = sorted(configs_to_run, key=lambda x: x.priority)
        
        for config in sorted_configs:
            if self.environment not in config.environments:
                print(f"⏭️  Skipping {config.story_id} (not configured for {self.environment})")
                continue
                
            print(f"🧪 Running {config.story_id}: {config.title}")
            
            # Run fast test
            if test_type in ["fast", "both"]:
                fast_result = await self._execute_single_test(
                    config.story_id, 
                    config.fast_test_file, 
                    "fast"
                )
                results[f"{config.story_id}_fast"] = fast_result
            
            # Run realistic test
            if test_type in ["realistic", "both"]:
                realistic_result = await self._execute_single_test(
                    config.story_id, 
                    config.realistic_test_file, 
                    "realistic"
                )
                results[f"{config.story_id}_realistic"] = realistic_result
        
        return results
    
    async def _execute_single_test(self, story_id: str, test_file: str, test_type: str) -> bool:
        """Execute a single test file"""
        try:
            # Construct pytest command
            cmd_parts = [
                "python", "-m", "pytest",
                test_file,
                f"--environment={self.environment}",
                "--headed",  # Always use headed Chromium for MCP
                "-v",
                "--tb=short"
            ]
            
            if test_type == "realistic":
                cmd_parts.extend(["-s", "--tb=long"])  # More verbose for realistic tests
            
            # Execute test
            process = await asyncio.create_subprocess_exec(
                *cmd_parts,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Parse results
            success = process.returncode == 0
            
            # Store detailed results
            self.results[f"{story_id}_{test_type}"] = {
                "success": success,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "return_code": process.returncode
            }
            
            if success:
                print(f"✅ {story_id} ({test_type}) - PASSED")
            else:
                print(f"❌ {story_id} ({test_type}) - FAILED")
                if stderr:
                    print(f"   Error: {stderr.decode()[:200]}...")
            
            return success
            
        except Exception as e:
            print(f"❌ {story_id} ({test_type}) - EXCEPTION: {e}")
            return False
    
    async def _generate_test_report(self, results: Dict[str, bool], execution_time: float, test_type: str):
        """Generate and save test execution report"""
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment": self.environment,
            "test_type": test_type,
            "execution_time_seconds": round(execution_time, 2),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": round(success_rate, 1)
            },
            "detailed_results": results,
            "test_artifacts": self._collect_test_artifacts()
        }
        
        # Save report
        report_path = Path(f"tests/user_stories/reports/report_{int(time.time())}.json")
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📊 Test Execution Summary")
        print(f"═══════════════════════════")
        print(f"Environment: {self.environment}")
        print(f"Test Type: {test_type}")
        print(f"Execution Time: {execution_time:.1f} seconds")
        print(f"Tests Run: {total_tests}")
        print(f"Passed: ✅ {passed_tests}")
        print(f"Failed: ❌ {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Report saved: {report_path}")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for test_id, success in results.items():
                if not success:
                    print(f"   • {test_id}")
    
    def _collect_test_artifacts(self) -> Dict[str, str]:
        """Collect test artifacts like screenshots, videos, logs"""
        artifacts = {}
        
        # Check for Playwright artifacts
        artifacts_dir = Path("test-results")
        if artifacts_dir.exists():
            for artifact in artifacts_dir.rglob("*"):
                if artifact.is_file():
                    artifacts[str(artifact)] = artifact.stat().st_size
        
        return artifacts
    
    async def validate_story_coverage(self) -> Dict[str, List[str]]:
        """Validate that all user stories have corresponding tests"""
        print("🔍 Validating user story test coverage...")
        
        coverage_report = {
            "missing_fast_tests": [],
            "missing_realistic_tests": [],
            "missing_stories": []
        }
        
        for story_id, config in self.orchestrator.test_configs.items():
            # Check if fast test file exists
            fast_test_path = Path(config.fast_test_file)
            if not fast_test_path.exists():
                coverage_report["missing_fast_tests"].append(story_id)
            
            # Check if realistic test file exists
            realistic_test_path = Path(config.realistic_test_file)
            if not realistic_test_path.exists():
                coverage_report["missing_realistic_tests"].append(story_id)
        
        # Print coverage report
        if any(coverage_report.values()):
            print("⚠️  Test Coverage Issues Found:")
            for issue_type, stories in coverage_report.items():
                if stories:
                    print(f"   {issue_type}: {', '.join(stories)}")
        else:
            print("✅ All user stories have complete test coverage")
        
        return coverage_report


async def main():
    """Main entry point for the test runner"""
    parser = argparse.ArgumentParser(description="User Story Test Runner")
    
    parser.add_argument(
        "--type", 
        choices=["fast", "realistic", "both"], 
        default="both",
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "--environment", 
        choices=["dev", "test", "staging", "prod"], 
        default="dev",
        help="Environment to test against"
    )
    
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel groups"
    )
    
    parser.add_argument(
        "--sequential", 
        action="store_true",
        help="Run tests sequentially (overrides --parallel)"
    )
    
    parser.add_argument(
        "--stories", 
        nargs="+",
        help="Specific user stories to test (e.g., US-001 US-002)"
    )
    
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Check test coverage without running tests"
    )
    
    args = parser.parse_args()
    
    # Create runner
    runner = UserStoryTestRunner(environment=args.environment)
    
    # Handle coverage check
    if args.coverage:
        await runner.validate_story_coverage()
        return
    
    # Determine execution mode
    parallel = args.parallel and not args.sequential
    
    # Run tests
    results = await runner.run_tests(
        test_type=args.type,
        parallel=parallel,
        story_filter=args.stories
    )
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    sys.exit(1 if failed_tests > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())