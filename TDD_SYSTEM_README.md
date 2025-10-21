# Test-Driven Development (TDD) System for Language Tracker

## 🎯 Overview

This project implements a comprehensive Test-Driven Development framework that ensures all code changes are validated through automated testing with user story validation. Every change must correspond to a user story with both fast and realistic test coverage using Playwright MCP with headed Chromium browsers.

## 📋 Core Requirements

### Change Management Rule
**MANDATORY**: Every code change MUST:
1. Reference a specific user story (US-XXX format)
2. Include corresponding test implementations
3. Pass all existing tests in parallel execution
4. Update documentation as needed

### Test Types Required

#### Fast Tests (`<30 seconds`)
- Minimal UI interactions
- Mock external dependencies
- Focus on core functionality validation
- Located in: `tests/user_stories/fast/`

#### Realistic Tests (`<5 minutes`)
- Full end-to-end workflows
- Real Firebase/backend interactions
- Complete user journey validation  
- Located in: `tests/user_stories/realistic/`

## 🏗️ Directory Structure

```
tests/
└── user_stories/
    ├── automations/           # Test orchestration and configuration
    │   ├── test_config.py     # Parallel execution orchestrator
    │   └── user_stories_config.json  # User story test configuration
    ├── fast/                  # Fast test implementations (<30s)
    │   ├── test_us001_registration_fast.py
    │   ├── test_us002_login_fast.py
    │   └── ...
    ├── realistic/             # Realistic test implementations (<5min)  
    │   ├── test_us001_registration_realistic.py
    │   ├── test_us002_login_realistic.py
    │   └── ...
    ├── reports/               # Test execution reports
    └── run_user_story_tests.py  # Main test runner
```

## 📖 Documentation Structure

### Core Documents
- **`CONSTITUTION.md`**: TDD rules and environment setup
- **`USER_STORIES.md`**: Complete user story definitions with features
- **`TDD_SYSTEM_README.md`**: This comprehensive guide

### User Story Format
Each user story follows this structure:
```markdown
### US-XXX: [Story Title]
**As a** [user role]  
**I want** [goal/desire]  
**So that** [benefit/value]

#### Features
- Feature 1
  - Sub-feature 1.1
  - Sub-feature 1.2

#### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## 🚀 Usage

### Running Tests

#### Check Test Coverage
```bash
python tests/user_stories/run_user_story_tests.py --coverage
```

#### Run Fast Tests (Development)
```bash
python tests/user_stories/run_user_story_tests.py --type=fast --environment=dev
```

#### Run Realistic Tests (Integration)
```bash
python tests/user_stories/run_user_story_tests.py --type=realistic --environment=test
```

#### Run All Tests with Parallel Execution
```bash
python tests/user_stories/run_user_story_tests.py --type=both --environment=staging --parallel
```

#### Run Specific User Stories
```bash
python tests/user_stories/run_user_story_tests.py --stories US-001 US-002 --type=fast
```

### Adding New User Stories

1. **Update USER_STORIES.md**
   - Add new user story with proper format
   - Include features, sub-features, and acceptance criteria

2. **Update Configuration**
   - Add entry to `tests/user_stories/automations/user_stories_config.json`
   - Include timing estimates, dependencies, and environment compatibility

3. **Create Test Files**
   - Fast test: `tests/user_stories/fast/test_usXXX_[name]_fast.py`
   - Realistic test: `tests/user_stories/realistic/test_usXXX_[name]_realistic.py`

4. **Reference in Code Changes**
   - All code changes must reference the user story ID (US-XXX)
   - Include story ID in commit messages

## 🔧 Test Configuration

### User Story Configuration Schema
```json
{
  "story_id": "US-001",
  "title": "User Registration",  
  "fast_test_file": "tests/user_stories/fast/test_us001_registration_fast.py",
  "realistic_test_file": "tests/user_stories/realistic/test_us001_registration_realistic.py",
  "dependencies": [],
  "priority": 1,
  "estimated_duration_fast": 15,
  "estimated_duration_realistic": 120,
  "parallel_safe": true,
  "environments": ["dev", "test", "staging"]
}
```

### Environment Tiers
1. **Development** (`dev`) - Feature development and initial testing
2. **Testing** (`test`) - Automated testing and QA validation  
3. **Staging** (`staging`) - Pre-production validation
4. **Production** (`prod`) - Read-only tests on live environment

## 🎭 Playwright MCP Integration

### Browser Configuration
- **Engine**: Chromium (headed mode for MCP)
- **Visual Validation**: Screenshots and video recording
- **Realistic Interactions**: Slow motion, realistic typing speed
- **Cross-browser**: Support for Chromium, Firefox, and WebKit

### Test Structure Template
```python
import pytest
from playwright.async_api import async_playwright

class TestUSXXX:
    @pytest.fixture
    async def browser_context(self):
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)  # Headed for MCP
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        yield context
        await context.close()
        await browser.close()
        await playwright.stop()
    
    async def test_user_story_validation(self, browser_context):
        # Test implementation
        pass
```

## ⚡ Parallel Execution

### Execution Groups
Tests are organized into parallel execution groups:

- **Group 1**: High priority, no dependencies
- **Group 2**: Medium priority or dependent on Group 1
- **Group 3**: Lower priority or complex dependencies  
- **Sequential**: Must run sequentially due to conflicts

### Time Estimation
The system automatically estimates execution time:
- Individual test duration estimates
- Parallel execution speedup calculation
- Resource usage optimization

## 📊 Test Reporting

### Automated Reports
- JSON format with detailed results
- Execution time analysis
- Success/failure rates
- Test artifact collection (screenshots, videos)

### Report Location
Reports are saved to: `tests/user_stories/reports/report_[timestamp].json`

## 🔍 Validation

### System Validation
Run the validation script to ensure proper setup:
```bash
python demo_tdd_system.py
```

This checks:
- Constitution includes TDD requirements
- User stories documentation is complete
- Test directory structure exists
- Configuration files are valid
- Test templates have proper structure

### Coverage Validation
The system validates that:
- All user stories have corresponding test files
- Test configurations are complete
- Dependencies are properly specified
- Environment compatibility is defined

## 🛡️ Quality Assurance

### Mandatory Checks
Before any code merge:
1. ✅ User story reference (US-XXX) in changes
2. ✅ Fast test implementation and passing
3. ✅ Realistic test implementation and passing  
4. ✅ All existing tests continue to pass
5. ✅ Documentation updated if needed

### Firebase Integration
- Tests work with all four Firebase environments
- Service account credentials properly configured
- Database operations are environment-isolated
- Authentication workflows are fully tested

## 🚀 Next Steps

1. **Implement Missing Tests**: Use coverage check to identify gaps
2. **Run Demo**: Execute `python demo_tdd_system.py` to see system overview
3. **Start Development**: Follow TDD workflow for all new features
4. **Monitor Coverage**: Regularly check test coverage and execution times
5. **Optimize Performance**: Use parallel execution for faster feedback

## 📚 Additional Resources

- **Playwright MCP Documentation**: Integration with headed Chromium
- **Firebase Testing Guide**: Multi-environment testing strategies  
- **User Story Templates**: Examples for different feature types
- **Test Automation Best Practices**: Performance and reliability guidelines

---

*This TDD system ensures high-quality, validated development with comprehensive test coverage and automated validation of all user story requirements.*