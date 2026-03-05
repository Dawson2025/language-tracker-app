---
resource_id: "9b945776-862f-47ef-b8a5-11b45a6fd0a1"
---
# Universal Instructions - Trickle-Down Level 0

<!-- section_id: "a139bb2d-69e3-472c-a6c9-3d2a6971e3f4" -->
## 📋 Document Hierarchy Overview

This document represents **Trickle-Down Level 0** - the foundation layer that applies universally across all projects, team members, and AI agents. Everyone must read and understand this level before proceeding to higher trickle-down levels.

<!-- section_id: "91b1e7be-3f7e-46a0-b3bf-d63dd9869f90" -->
### 📊 Trickle-Down Hierarchy Structure

```
Level 0 (Universal)    → Applies to: Everything, everywhere
Level 1 (Project)      → Applies to: This specific project  
Level 2 (Features)     → Applies to: Specific feature domains
Level 3 (Components)   → Applies to: Individual components/modules
Level 4 (Implementation) → Applies to: Specific code implementations
```

<!-- section_id: "9a19c11f-f722-4ad9-b711-c55a6fe4c27e" -->
### 🔍 Reading Order (MANDATORY)

**All team members and AI agents MUST follow this sequence:**

1. **START HERE**: Read ALL Trickle-Down 0 documents completely
2. **THEN**: Read ALL Trickle-Down 1 documents relevant to the project
3. **THEN**: Read relevant Trickle-Down 2 documents for your feature area
4. **THEN**: Read relevant Trickle-Down 3 documents for your component
5. **FINALLY**: Read Trickle-Down 4 documents for specific implementation details

**❌ NEVER skip levels or read out of order**

<!-- section_id: "ba595db2-8048-4395-a065-20a316519157" -->
## 🌐 Universal Principles

<!-- section_id: "811f2371-0991-4ad1-924f-23f67eac8bd5" -->
### Communication Standards
- **Clarity First**: All communication must be clear, concise, and unambiguous
- **Documentation-Driven**: All decisions, changes, and processes must be documented
- **Asynchronous by Default**: Assume team members work across time zones
- **Context Sharing**: Always provide sufficient context for decisions and changes

<!-- section_id: "a2d8041f-e834-4b0c-a73b-11bc2e2a5b20" -->
### Quality Standards
- **Test-Driven Development**: All code changes require corresponding tests
- **User Story Validation**: Every change must map to a specific user story
- **Code Review**: All changes require peer review before integration
- **Continuous Integration**: Automated testing and validation at every stage

<!-- section_id: "38440f8a-b42a-41df-97a3-5866466dc8e0" -->
### Collaboration Standards  
- **Respectful Communication**: Professional, constructive, and inclusive interactions
- **Knowledge Sharing**: Document learnings and share knowledge proactively
- **Feedback Culture**: Give and receive constructive feedback regularly
- **Continuous Learning**: Stay current with best practices and technologies

<!-- section_id: "7b509963-726b-4572-bb22-c34f8d41fa0e" -->
### Security Standards
- **Security by Design**: Consider security implications in all decisions
- **Least Privilege**: Grant minimum necessary permissions and access
- **Data Protection**: Handle all data with appropriate protection measures
- **Incident Response**: Report security concerns immediately

<!-- section_id: "2a91cee7-c8e0-469a-9dc7-33be540d335d" -->
## 📂 Universal File Organization

<!-- section_id: "10cdf944-57a2-4274-a43d-e80d1c99c782" -->
### Directory Naming Conventions
```
kebab-case-for-directories/
snake_case_for_files.extension
PascalCaseForClasses
camelCaseForVariables
UPPER_CASE_FOR_CONSTANTS
```

<!-- section_id: "e24698f8-c076-4118-ae39-8fe34f34ef2f" -->
### Document Categories
- **Instructions**: How to do things (`INSTRUCTIONS_*.md`)
- **Logs**: Records of what happened (`LOG_*.md`)
- **Explanations**: Why things are the way they are (`EXPLANATION_*.md`)
- **References**: Quick lookup information (`REFERENCE_*.md`)
- **Archives**: Historical documents (`ARCHIVE_*.md`)

<!-- section_id: "7160ba4e-dd5e-4a57-858e-9a5cd16e9617" -->
### Version Control Standards
```
feat: add new feature (relates to US-XXX)
fix: bug fix (relates to US-XXX) 
docs: documentation changes
refactor: code refactoring
test: adding or updating tests
chore: maintenance tasks
```

<!-- section_id: "5d021402-fecb-4f11-88eb-bf6f8dd9bf1f" -->
## 🔄 Change Management Process

<!-- section_id: "4050e58f-e890-4ccf-b999-e87fab5866dd" -->
### Before Making ANY Change
1. ✅ Identify which user story this relates to (US-XXX)
2. ✅ Read relevant trickle-down documentation (0→1→2→3→4)
3. ✅ Understand current system state from logs
4. ✅ Plan the change with proper testing strategy
5. ✅ Get necessary approvals/reviews

<!-- section_id: "7939861f-da05-442e-b89a-a4fd2c67cdbb" -->
### During Implementation
1. ✅ Follow TDD practices (tests first)
2. ✅ Update documentation as you work
3. ✅ Maintain clear commit messages with user story references
4. ✅ Ensure backwards compatibility where possible
5. ✅ Test across all relevant environments

<!-- section_id: "16a93634-225f-44fa-8a45-171331710f94" -->
### After Implementation  
1. ✅ Update all relevant trickle-down documentation
2. ✅ Create/update log entries documenting the change
3. ✅ Verify all tests pass in parallel execution
4. ✅ Update user story status/acceptance criteria
5. ✅ Share knowledge and lessons learned

<!-- section_id: "31c99326-b29c-497a-9414-62a5f5485839" -->
## 🎯 AI Agent Integration

<!-- section_id: "50002cf1-0087-4eb3-a47b-0245a8de8732" -->
### For AI Agents Working on This Project
You MUST follow this exact sequence when engaging with any task:

1. **Context Gathering Phase**
   - Read this Universal Instructions document completely
   - Identify which trickle-down levels are relevant to your task
   - Read all relevant trickle-down documentation in order (0→1→2→3→4)
   - Review recent log entries for current project state

2. **Planning Phase**
   - Identify the user story (US-XXX) this work relates to
   - Understand dependencies and constraints from documentation
   - Plan approach that aligns with project standards and practices
   - Identify what documentation updates will be needed

3. **Execution Phase**
   - Follow TDD practices with both fast and realistic tests
   - Reference user story ID in all work and commits
   - Update documentation as you implement
   - Maintain consistency with existing patterns and practices

4. **Documentation Phase**
   - Update all relevant trickle-down documentation levels
   - Create log entries documenting what was accomplished
   - Update user story status and acceptance criteria
   - Ensure knowledge is preserved for future reference

<!-- section_id: "26431ea5-a6b9-4632-a66b-04b60f8ebf82" -->
### AI Agent Responsibilities
- **Never assume context**: Always read the full documentation hierarchy
- **Maintain consistency**: Follow established patterns and conventions
- **Document everything**: Your work must be understandable to humans
- **Test comprehensively**: Both fast and realistic test coverage required
- **Reference user stories**: Every change must map to a specific US-XXX

<!-- section_id: "6461c6f6-11f3-4407-9114-895817ab00d4" -->
## 🚨 Universal Enforcement

<!-- section_id: "2d28d537-3ea6-4a97-b570-249c70b03f6b" -->
### Non-Negotiable Requirements
These apply to ALL work, regardless of urgency or scope:

**🚨 HARD RULE: All automated tests must pass before any progression**
- No exceptions to this rule under any circumstances
- Applies to all development work, feature implementation, and bug fixes
- Must be enforced through CI/CD pipeline automation
- Gates batch progressions, PR merges to main, and releases
- This rule is universal across all projects and AI agents

1. **User Story Reference**: Every change MUST reference a user story (US-XXX)
2. **Documentation Updates**: All relevant trickle-down levels MUST be updated
3. **Test Coverage**: Both fast (<30s) and realistic (<5min) tests required
4. **Review Process**: All changes require appropriate review
5. **Log Entries**: Significant changes MUST be logged with context

<!-- section_id: "b686a7c6-92b4-4bfb-b8fe-f9313340f31e" -->
### Violation Consequences
- **Failing tests automatically block all progression** (enforced by CI)
- Changes without user story references will be rejected
- Undocumented changes will be reverted
- Missing test coverage blocks integration
- Skipping trickle-down hierarchy reading leads to rework

<!-- section_id: "66d341e3-682e-4088-b4d4-61154e784fb1" -->
## 📚 Universal Resources

<!-- section_id: "600c8552-3db6-4d52-953a-1ddef1f55a20" -->
### Essential Reading Order for ANY Project Work
1. This document (UNIVERSAL_INSTRUCTIONS.md)
2. Project Constitution (Trickle-Down 1)
3. User Stories documentation (Trickle-Down 1)
4. Relevant feature documentation (Trickle-Down 2)
5. Component-specific documentation (Trickle-Down 3)
6. Implementation details (Trickle-Down 4)

<!-- section_id: "b9822f39-3b9b-4229-a6f8-af1ec3973324" -->
### Documentation Maintenance
- Review and update documentation with every significant change
- Archive outdated documents rather than deleting them
- Maintain clear changelog entries for documentation updates
- Ensure documentation accuracy through regular reviews

<!-- section_id: "d6f06626-7b90-408d-8dee-05e69a7db982" -->
## 🔗 Next Steps

After completing this document, proceed to:
**Trickle-Down Level 1**: `/docs/trickle-down-1-project/`

---

*This Universal Instructions document establishes the foundation for all project work. It must be read and understood before engaging with any aspect of the project.*