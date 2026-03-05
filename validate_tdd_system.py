#!/usr/bin/env python3
# resource_id: 4407d1f6-6045-4b83-871d-5064579801a5
"""
TDD System Validation Script

This script validates that the Test-Driven Development system is correctly implemented
and demonstrates the user story testing framework functionality.

Usage:
    python validate_tdd_system.py
"""

import asyncio
import json
from pathlib import Path
from tests.user_stories.automations.test_config import UserStoryTestOrchestrator


def validate_constitution():
    """Validate that the constitution includes TDD requirements"""
    constitution_path = Path("CONSTITUTION.md")
    
    if not constitution_path.exists():
        return False, "CONSTITUTION.md not found"
    
    content = constitution_path.read_text()
    
    required_sections = [
        "Test-Driven Development (TDD) Requirements",
        "Change Management Rule",
        "User Story Validation Requirements", 
        "Playwright MCP Testing Standards",
        "Test Organization Structure",
        "Enforcement Protocol"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        return False, f"Missing sections: {', '.join(missing_sections)}"
    
    return True, "Constitution includes all required TDD sections"


def validate_user_stories_documentation():
    """Validate that user stories are properly documented"""
    stories_path = Path("USER_STORIES.md")
    
    if not stories_path.exists():
        return False, "USER_STORIES.md not found"
    
    content = stories_path.read_text()
    
    # Check for required story format elements
    required_elements = [
        "**US-001**: User Registration",
        "**As a**",
        "**I want**", 
        "**So that**",
        "#### Features",
        "#### Acceptance Criteria"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        return False, f"Missing elements: {', '.join(missing_elements)}"
    
    return True, "User stories documentation is properly formatted"


def validate_test_structure():
    """Validate that test directory structure is correct"""
    required_paths = [
        "tests/user_stories",
        "tests/user_stories/automations", 
        "tests/user_stories/fast",
        "tests/user_stories/realistic",
        "tests/user_stories/reports"
    ]
    
    missing_paths = []
    for path_str in required_paths:
        path = Path(path_str)
        if not path.exists():
            missing_paths.append(path_str)
    
    if missing_paths:
        return False, f"Missing directories: {', '.join(missing_paths)}"
    
    return True, "Test directory structure is correct"


def validate_test_configuration():
    """Validate test configuration files"""
    config_path = Path("tests/user_stories/automations/user_stories_config.json")
    
    if not config_path.exists():
        return False, "User stories config JSON not found"
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        # Validate config structure
        required_keys = ["version", "user_stories", "test_execution_notes"]
        for key in required_keys:
            if key not in config:
                return False, f"Config missing key: {key}"
        
        # Validate user story entries
        if not config["user_stories"]:
            return False, "No user stories defined in config"
        
        first_story = config["user_stories"][0]
        required_story_keys = [
            "story_id", "title", "fast_test_file", "realistic_test_file",
            "dependencies", "priority", "estimated_duration_fast", 
            "estimated_duration_realistic", "parallel_safe", "environments"
        ]
        
        for key in required_story_keys:
            if key not in first_story:
                return False, f"Story config missing key: {key}"
        
        return True, f"Configuration valid with {len(config['user_stories'])} user stories"
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in config file: {e}"


def validate_test_orchestrator():
    """Validate that test orchestrator can load and process configurations"""
    try:
        orchestrator = UserStoryTestOrchestrator()
        
        if not orchestrator.test_configs:
            return False, "Orchestrator loaded no test configurations"
        
        # Test execution plan generation
        execution_plan = orchestrator.get_execution_plan("both")
        
        required_groups = ["group_1", "group_2", "group_3", "sequential"]
        for group in required_groups:
            if group not in execution_plan:
                return False, f"Execution plan missing group: {group}"
        
        # Test time estimation
        estimated_time = orchestrator.estimate_total_time(execution_plan, "both")
        if estimated_time <= 0:
            return False, "Time estimation returned invalid result"
        
        total_stories = len(orchestrator.test_configs)
        return True, f"Orchestrator working correctly with {total_stories} stories, estimated time: {estimated_time}s"
        
    except Exception as e:
        return False, f"Orchestrator validation failed: {e}"


def validate_test_templates():
    """Validate that test templates exist and have proper structure"""
    template_files = [
        "tests/user_stories/fast/test_us001_registration_fast.py",
        "tests/user_stories/realistic/test_us001_registration_realistic.py"
    ]
    
    missing_templates = []
    for template_path_str in template_files:
        template_path = Path(template_path_str)
        if not template_path.exists():
            missing_templates.append(template_path_str)
            continue
        
        # Check template content
        content = template_path.read_text()
        required_elements = [
            "playwright.async_api",
            "@pytest.fixture",
            "async def",
            "headed",  # Should use headed Chromium
            "US-001"  # Should reference user story
        ]
        
        for element in required_elements:
            if element not in content:
                return False, f"Template {template_path_str} missing: {element}"
    
    if missing_templates:
        return False, f"Missing test templates: {', '.join(missing_templates)}"
    
    return True, "Test templates exist and have proper structure"


async def main():
    """Run all validation checks"""
    print("🔍 Validating TDD System Implementation")
    print("=" * 50)
    
    validations = [
        ("Constitution TDD Requirements", validate_constitution),
        ("User Stories Documentation", validate_user_stories_documentation),
        ("Test Directory Structure", validate_test_structure), 
        ("Test Configuration Files", validate_test_configuration),
        ("Test Orchestrator Functionality", validate_test_orchestrator),
        ("Test Template Structure", validate_test_templates)
    ]
    
    all_passed = True
    results = []
    
    for name, validation_func in validations:
        try:
            success, message = validation_func()
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {name}: {message}")
            results.append((name, success, message))
            
            if not success:
                all_passed = False
                
        except Exception as e:
            print(f"❌ FAIL {name}: Exception occurred - {e}")
            results.append((name, False, f"Exception: {e}"))
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 TDD System Validation: ALL CHECKS PASSED")
        print("\n🚀 System Ready for Test-Driven Development!")
        print("\nNext steps:")
        print("1. Run: python tests/user_stories/run_user_story_tests.py --coverage")
        print("2. Implement missing test files as needed")
        print("3. Run fast tests: python tests/user_stories/run_user_story_tests.py --type=fast")
        print("4. Run realistic tests: python tests/user_stories/run_user_story_tests.py --type=realistic")
    else:
        print("❌ TDD System Validation: SOME CHECKS FAILED")
        print("\n🔧 Fix the following issues before proceeding:")
        for name, success, message in results:
            if not success:
                print(f"   • {name}: {message}")
    
    print("\n📖 TDD Rules Summary:")
    print("   • Every code change MUST reference a user story (US-XXX)")
    print("   • Each user story requires both fast and realistic tests")
    print("   • All tests use Playwright MCP with headed Chromium")
    print("   • Tests must support parallel execution")
    print("   • Update USER_STORIES.md when adding new stories")


if __name__ == "__main__":
    asyncio.run(main())