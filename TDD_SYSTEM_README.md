---
resource_id: "6a876fef-d2da-456f-84cf-b855ef0cd225"
---
# Test-Driven Development (TDD) System for Language Tracker

<!-- section_id: "ba7a056e-3f01-4ca4-bc6b-e109c07444e7" -->
## 🎯 Overview

This project implements a comprehensive Test-Driven Development framework that ensures all code changes are validated through automated testing with user story validation. Every change must correspond to a user story with both fast and realistic test coverage using Playwright MCP with headed Chromium browsers.

<!-- section_id: "b4333729-157c-43d6-94b5-e246b87418eb" -->
## 📋 Core Requirements

<!-- section_id: "933e85c4-0d17-4dd7-99f4-f78419a88358" -->
### Change Management Rule
**MANDATORY**: Every code change MUST:
1. Reference a specific user story (US-XXX format)
2. Include corresponding test implementations
3. Pass all existing tests in parallel execution
4. Update documentation as needed

<!-- section_id: "1f18bbb2-5eb5-43ce-807b-0377462a3b78" -->
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

<!-- section_id: "3f6d1d79-b405-4dc8-8c78-07aa5d88e936" -->
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

<!-- section_id: "62a9cda9-f3fe-4c1b-bd51-9d050b8d8a70" -->
## 📖 Documentation Structure

<!-- section_id: "ccbac6ed-2063-4701-b92b-f2926ce52c0c" -->
### Core Documents
- **`CONSTITUTION.md`**: TDD rules and environment setup
- **`USER_STORIES.md`**: Complete user story definitions with features
- **`TDD_SYSTEM_README.md`**: This comprehensive guide

<!-- section_id: "3dadfbd8-be7f-4381-8c62-897a145a26cc" -->
### User Story Format
Each user story follows this structure:
```markdown
<!-- section_id: "648ed7f9-2b21-4ae2-bd59-15bab666d307" -->
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

<!-- section_id: "95ff9081-bd2a-4649-9cf5-bf2fd5467c75" -->
## 🚀 Usage

<!-- section_id: "fccc8850-d155-46f5-8854-3d338e4fb567" -->
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

<!-- section_id: "6ec6fb57-ed0c-4757-b41d-3e19fc04c5c8" -->
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

<!-- section_id: "f6ba74e1-be46-443a-b1fa-89bf38e32f72" -->
## 🔧 Test Configuration

<!-- section_id: "b3f44983-c6d6-4d11-ab62-bd1ca7806420" -->
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

<!-- section_id: "497b7e2c-b7ee-48ba-89e4-d75f4171dc07" -->
### Environment Tiers
1. **Development** (`dev`) - Feature development and initial testing
2. **Testing** (`test`) - Automated testing and QA validation  
3. **Staging** (`staging`) - Pre-production validation
4. **Production** (`prod`) - Read-only tests on live environment

<!-- section_id: "aeff0142-10b6-4ed7-8ce2-2d508dc4dea1" -->
## 🎭 Playwright MCP Integration

<!-- section_id: "903a44bb-de56-4650-a78d-5dc4e8d9dee8" -->
### Browser Configuration
- **Engine**: Chromium (headed mode for MCP)
- **Visual Validation**: Screenshots and video recording
- **Realistic Interactions**: Slow motion, realistic typing speed
- **Cross-browser**: Support for Chromium, Firefox, and WebKit

<!-- section_id: "4ac483c8-0d21-4514-baa3-5038de605fd7" -->
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

<!-- section_id: "9c440f9a-4a32-4890-a2de-88fbfb6f42ae" -->
## ⚡ Parallel Execution

<!-- section_id: "2edbfaab-df77-4520-a94b-d0a1b8ead741" -->
### Execution Groups
Tests are organized into parallel execution groups:

- **Group 1**: High priority, no dependencies
- **Group 2**: Medium priority or dependent on Group 1
- **Group 3**: Lower priority or complex dependencies  
- **Sequential**: Must run sequentially due to conflicts

<!-- section_id: "105651de-69c2-4b5c-a85f-4f7400d6560c" -->
### Time Estimation
The system automatically estimates execution time:
- Individual test duration estimates
- Parallel execution speedup calculation
- Resource usage optimization

<!-- section_id: "c045057c-7d1a-402b-bafb-6bec57ab8449" -->
## 📊 Test Reporting

<!-- section_id: "be4abc5c-73f5-4295-b959-d815e4f44b7e" -->
### Automated Reports
- JSON format with detailed results
- Execution time analysis
- Success/failure rates
- Test artifact collection (screenshots, videos)

<!-- section_id: "ff006c72-413c-4f74-b18b-522a52430025" -->
### Report Location
Reports are saved to: `tests/user_stories/reports/report_[timestamp].json`

<!-- section_id: "0e1df7bc-1823-4da6-b8e9-98089308b579" -->
## 🔍 Validation

<!-- section_id: "0c2171a6-c7ce-4158-b7bc-8cc315e6a85f" -->
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

<!-- section_id: "c30cff8d-690d-4ef1-bdd3-cbd273ce0347" -->
### Coverage Validation
The system validates that:
- All user stories have corresponding test files
- Test configurations are complete
- Dependencies are properly specified
- Environment compatibility is defined

<!-- section_id: "57da4400-98d6-4fae-8791-514b04a9e468" -->
## 🛡️ Quality Assurance

<!-- section_id: "d192103e-9d94-4416-b77c-81da74a99253" -->
### Mandatory Checks
Before any code merge:
1. ✅ User story reference (US-XXX) in changes
2. ✅ Fast test implementation and passing
3. ✅ Realistic test implementation and passing  
4. ✅ All existing tests continue to pass
5. ✅ Documentation updated if needed

<!-- section_id: "060dffe4-1405-4f55-a049-7553cd7694c0" -->
### Firebase Integration
- Tests work with all four Firebase environments
- Service account credentials properly configured
- Database operations are environment-isolated
- Authentication workflows are fully tested

<!-- section_id: "a90cf7cb-6ce3-44df-8e9f-459a65444776" -->
## 🚀 Next Steps

1. **Implement Missing Tests**: Use coverage check to identify gaps
2. **Run Demo**: Execute `python demo_tdd_system.py` to see system overview
3. **Start Development**: Follow TDD workflow for all new features
4. **Monitor Coverage**: Regularly check test coverage and execution times
5. **Optimize Performance**: Use parallel execution for faster feedback

<!-- section_id: "f4d8eb25-2056-4445-a8e4-f648e95cb674" -->
## 📚 Additional Resources

- **Playwright MCP Documentation**: Integration with headed Chromium
- **Firebase Testing Guide**: Multi-environment testing strategies  
- **User Story Templates**: Examples for different feature types
- **Test Automation Best Practices**: Performance and reliability guidelines

---

*This TDD system ensures high-quality, validated development with comprehensive test coverage and automated validation of all user story requirements.*