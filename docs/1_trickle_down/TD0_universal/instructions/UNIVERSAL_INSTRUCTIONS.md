# Universal Instructions - Trickle-Down Level 0

## 📋 Document Hierarchy Overview

This document represents **Trickle-Down Level 0** - the foundation layer that applies universally across all projects, team members, and AI agents. Everyone must read and understand this level before proceeding to higher trickle-down levels.

### 📊 Trickle-Down Hierarchy Structure

```
Level 0 (Universal)    → Applies to: Everything, everywhere
Level 1 (Project)      → Applies to: This specific project  
Level 2 (Features)     → Applies to: Specific feature domains
Level 3 (Components)   → Applies to: Individual components/modules
Level 4 (Implementation) → Applies to: Specific code implementations
```

### 🔍 Reading Order (MANDATORY)

**All team members and AI agents MUST follow this sequence:**

1. **START HERE**: Read ALL Trickle-Down 0 documents completely
2. **THEN**: Read ALL Trickle-Down 1 documents relevant to the project
3. **THEN**: Read relevant Trickle-Down 2 documents for your feature area
4. **THEN**: Read relevant Trickle-Down 3 documents for your component
5. **FINALLY**: Read Trickle-Down 4 documents for specific implementation details

**❌ NEVER skip levels or read out of order**

## 🌐 Universal Principles

### Communication Standards
- **Clarity First**: All communication must be clear, concise, and unambiguous
- **Documentation-Driven**: All decisions, changes, and processes must be documented
- **Asynchronous by Default**: Assume team members work across time zones
- **Context Sharing**: Always provide sufficient context for decisions and changes

### Quality Standards
- **Test-Driven Development**: All code changes require corresponding tests
- **User Story Validation**: Every change must map to a specific user story
- **Code Review**: All changes require peer review before integration
- **Continuous Integration**: Automated testing and validation at every stage

### Collaboration Standards  
- **Respectful Communication**: Professional, constructive, and inclusive interactions
- **Knowledge Sharing**: Document learnings and share knowledge proactively
- **Feedback Culture**: Give and receive constructive feedback regularly
- **Continuous Learning**: Stay current with best practices and technologies

### Security Standards
- **Security by Design**: Consider security implications in all decisions
- **Least Privilege**: Grant minimum necessary permissions and access
- **Data Protection**: Handle all data with appropriate protection measures
- **Incident Response**: Report security concerns immediately

## 📂 Universal File Organization

### Directory Naming Conventions
```
kebab-case-for-directories/
snake_case_for_files.extension
PascalCaseForClasses
camelCaseForVariables
UPPER_CASE_FOR_CONSTANTS
```

### Document Categories
- **Instructions**: How to do things (`INSTRUCTIONS_*.md`)
- **Logs**: Records of what happened (`LOG_*.md`)
- **Explanations**: Why things are the way they are (`EXPLANATION_*.md`)
- **References**: Quick lookup information (`REFERENCE_*.md`)
- **Archives**: Historical documents (`ARCHIVE_*.md`)

### Version Control Standards
```
feat: add new feature (relates to US-XXX)
fix: bug fix (relates to US-XXX) 
docs: documentation changes
refactor: code refactoring
test: adding or updating tests
chore: maintenance tasks
```

## 🔄 Change Management Process

### Before Making ANY Change
1. ✅ Identify which user story this relates to (US-XXX)
2. ✅ Read relevant trickle-down documentation (0→1→2→3→4)
3. ✅ Understand current system state from logs
4. ✅ Plan the change with proper testing strategy
5. ✅ Get necessary approvals/reviews

### During Implementation
1. ✅ Follow TDD practices (tests first)
2. ✅ Update documentation as you work
3. ✅ Maintain clear commit messages with user story references
4. ✅ Ensure backwards compatibility where possible
5. ✅ Test across all relevant environments

### After Implementation  
1. ✅ Update all relevant trickle-down documentation
2. ✅ Create/update log entries documenting the change
3. ✅ Verify all tests pass in parallel execution
4. ✅ Update user story status/acceptance criteria
5. ✅ Share knowledge and lessons learned

## 🎯 AI Agent Integration

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

### AI Agent Responsibilities
- **Never assume context**: Always read the full documentation hierarchy
- **Maintain consistency**: Follow established patterns and conventions
- **Document everything**: Your work must be understandable to humans
- **Test comprehensively**: Both fast and realistic test coverage required
- **Reference user stories**: Every change must map to a specific US-XXX

## 🚨 Universal Enforcement

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

### Violation Consequences
- **Failing tests automatically block all progression** (enforced by CI)
- Changes without user story references will be rejected
- Undocumented changes will be reverted
- Missing test coverage blocks integration
- Skipping trickle-down hierarchy reading leads to rework

## 📚 Universal Resources

### Essential Reading Order for ANY Project Work
1. This document (UNIVERSAL_INSTRUCTIONS.md)
2. Project Constitution (Trickle-Down 1)
3. User Stories documentation (Trickle-Down 1)
4. Relevant feature documentation (Trickle-Down 2)
5. Component-specific documentation (Trickle-Down 3)
6. Implementation details (Trickle-Down 4)

### Documentation Maintenance
- Review and update documentation with every significant change
- Archive outdated documents rather than deleting them
- Maintain clear changelog entries for documentation updates
- Ensure documentation accuracy through regular reviews

## 🔗 Next Steps

After completing this document, proceed to:
**Trickle-Down Level 1**: `/docs/trickle-down-1-project/`

---

*This Universal Instructions document establishes the foundation for all project work. It must be read and understood before engaging with any aspect of the project.*