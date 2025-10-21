"""
User Story Test Automation Configuration

This module defines the configuration for parallel execution of user story tests
using Playwright MCP with headed Chromium browsers.
"""

import asyncio
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class TestConfig:
    """Configuration for a user story test"""
    story_id: str
    title: str
    fast_test_file: str
    realistic_test_file: str
    dependencies: List[str]  # Other story IDs this depends on
    priority: int  # 1 = highest priority, 5 = lowest
    estimated_duration_fast: int  # seconds
    estimated_duration_realistic: int  # seconds
    parallel_safe: bool  # Can run in parallel with other tests
    environments: List[str]  # Which environments to test against

class UserStoryTestOrchestrator:
    """Orchestrates parallel execution of user story tests"""
    
    def __init__(self, config_path: str = "tests/user_stories/automations/user_stories_config.json"):
        self.config_path = Path(config_path)
        self.test_configs: Dict[str, TestConfig] = {}
        self.load_configurations()
    
    def load_configurations(self):
        """Load test configurations from JSON file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                configs = json.load(f)
                for config_data in configs['user_stories']:
                    config = TestConfig(**config_data)
                    self.test_configs[config.story_id] = config
    
    def get_execution_plan(self, test_type: str = "both") -> Dict[str, List[TestConfig]]:
        """
        Create an execution plan for parallel test runs
        
        Args:
            test_type: "fast", "realistic", or "both"
            
        Returns:
            Dictionary with execution groups that can run in parallel
        """
        execution_plan = {
            "group_1": [],  # High priority, no dependencies
            "group_2": [],  # Medium priority or dependent on group_1
            "group_3": [],  # Lower priority or complex dependencies
            "sequential": []  # Must run sequentially due to conflicts
        }
        
        # Sort by priority and dependencies
        sorted_configs = sorted(
            self.test_configs.values(),
            key=lambda x: (x.priority, len(x.dependencies))
        )
        
        for config in sorted_configs:
            if not config.parallel_safe:
                execution_plan["sequential"].append(config)
            elif not config.dependencies:
                execution_plan["group_1"].append(config)
            elif self._dependencies_in_previous_groups(config, execution_plan):
                execution_plan["group_2"].append(config)
            else:
                execution_plan["group_3"].append(config)
        
        return execution_plan
    
    def _dependencies_in_previous_groups(self, config: TestConfig, plan: Dict[str, List[TestConfig]]) -> bool:
        """Check if all dependencies are in previous execution groups"""
        all_previous_stories = set()
        for group in ["group_1"]:  # Only check earlier groups
            for test_config in plan[group]:
                all_previous_stories.add(test_config.story_id)
        
        return all(dep in all_previous_stories for dep in config.dependencies)
    
    def estimate_total_time(self, execution_plan: Dict[str, List[TestConfig]], test_type: str = "both") -> int:
        """Estimate total execution time for the plan"""
        total_time = 0
        
        for group_name, configs in execution_plan.items():
            if group_name == "sequential":
                # Sequential tests run one after another
                for config in configs:
                    if test_type in ["fast", "both"]:
                        total_time += config.estimated_duration_fast
                    if test_type in ["realistic", "both"]:
                        total_time += config.estimated_duration_realistic
            else:
                # Parallel tests - take the maximum time in the group
                if configs:
                    max_time = 0
                    for config in configs:
                        config_time = 0
                        if test_type in ["fast", "both"]:
                            config_time += config.estimated_duration_fast
                        if test_type in ["realistic", "both"]:
                            config_time += config.estimated_duration_realistic
                        max_time = max(max_time, config_time)
                    total_time += max_time
        
        return total_time

# Test execution commands for different environments
TEST_COMMANDS = {
    "fast": {
        "dev": "python -m pytest tests/user_stories/fast/ --environment=dev --headed --parallel",
        "test": "python -m pytest tests/user_stories/fast/ --environment=test --headed --parallel",
        "staging": "python -m pytest tests/user_stories/fast/ --environment=staging --headed --parallel",
        "prod": "python -m pytest tests/user_stories/fast/ --environment=prod --headed --parallel --read-only"
    },
    "realistic": {
        "dev": "python -m pytest tests/user_stories/realistic/ --environment=dev --headed --parallel",
        "test": "python -m pytest tests/user_stories/realistic/ --environment=test --headed --parallel",
        "staging": "python -m pytest tests/user_stories/realistic/ --environment=staging --headed --parallel",
        "prod": "python -m pytest tests/user_stories/realistic/ --environment=prod --headed --parallel --read-only"
    }
}

async def run_parallel_tests(orchestrator: UserStoryTestOrchestrator, 
                           test_type: str = "both", 
                           environment: str = "dev") -> Dict[str, bool]:
    """
    Execute user story tests in parallel groups
    
    Args:
        orchestrator: Test orchestrator instance
        test_type: "fast", "realistic", or "both"
        environment: Target environment
        
    Returns:
        Dictionary mapping story IDs to success/failure status
    """
    execution_plan = orchestrator.get_execution_plan(test_type)
    results = {}
    
    print(f"Estimated total time: {orchestrator.estimate_total_time(execution_plan, test_type)} seconds")
    
    # Execute groups sequentially, but tests within groups in parallel
    for group_name, configs in execution_plan.items():
        if not configs:
            continue
            
        print(f"Executing {group_name} ({len(configs)} tests)...")
        
        if group_name == "sequential":
            # Run sequential tests one by one
            for config in configs:
                result = await _run_single_test(config, test_type, environment)
                results[config.story_id] = result
        else:
            # Run parallel tests concurrently
            tasks = []
            for config in configs:
                task = _run_single_test(config, test_type, environment)
                tasks.append(task)
            
            group_results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(group_results):
                story_id = configs[i].story_id
                results[story_id] = result if not isinstance(result, Exception) else False
    
    return results

async def _run_single_test(config: TestConfig, test_type: str, environment: str) -> bool:
    """Run a single user story test"""
    try:
        # This would integrate with the actual Playwright MCP test execution
        print(f"Running {config.story_id}: {config.title} ({test_type}) on {environment}")
        
        # Simulate test execution
        await asyncio.sleep(1)  # Replace with actual test execution
        
        return True  # Replace with actual test result
    except Exception as e:
        print(f"Test {config.story_id} failed: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    orchestrator = UserStoryTestOrchestrator()
    plan = orchestrator.get_execution_plan("both")
    
    print("Execution Plan:")
    for group, configs in plan.items():
        print(f"{group}: {[c.story_id for c in configs]}")