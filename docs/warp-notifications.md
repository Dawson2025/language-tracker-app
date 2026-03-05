---
resource_id: "0176e42a-8913-403b-ab8e-12deb4c0772d"
---
# Warp AI Assistant Notification System
*For Language Tracker Project*

<!-- section_id: "09fef86e-f50a-43d4-96e5-303ae60d7e31" -->
## Overview
This notification system alerts the developer when Warp AI Assistant completes a turn and is ready for feedback or next instructions.

<!-- section_id: "3c345207-2981-4482-8eb4-564d48381976" -->
## Notification Triggers

<!-- section_id: "4822b1c7-3e89-48a7-867a-af64e0d879af" -->
### 1. Task Completion
**Trigger:** When Warp completes a development task
**Message:** "🟢 Warp AI: Task completed - Ready for review"
**Details:** Summary of changes made, files modified, tests run

<!-- section_id: "ac14b047-8686-4467-9ee1-973d9b32744e" -->
### 2. Blocked on Input
**Trigger:** When Warp needs clarification or decisions
**Message:** "🟡 Warp AI: Waiting for input - Decision required"
**Details:** Specific question or choice needed

<!-- section_id: "6252cc55-d36b-401b-9c73-10ac5ffddba4" -->
### 3. Error Encountered
**Trigger:** When Warp encounters errors it cannot resolve
**Message:** "🔴 Warp AI: Error encountered - Assistance needed"
**Details:** Error description and attempted solutions

<!-- section_id: "1f85bf9c-34ed-4128-858a-84fe3382da11" -->
### 4. TODO List Updated
**Trigger:** When Warp modifies the TODO list
**Message:** "📝 Warp AI: TODO updated - Progress checkpoint"
**Details:** Current TODO status and next planned actions

<!-- section_id: "6ad4e1b3-231f-4c7a-a09c-0313df0e59a4" -->
## Implementation

<!-- section_id: "60634ec4-725b-4815-a721-b7c9fd86c55b" -->
### Windows Toast Notifications (PowerShell)
```powershell
# Add to Warp completion scripts
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
$notify.BalloonTipText = "Warp AI: Task completed - Ready for review"
$notify.BalloonTipTitle = "Language Tracker Development"
$notify.Visible = $true
$notify.ShowBalloonTip(5000)
```

<!-- section_id: "21036aa6-8cca-407a-9729-937e8dfb74d5" -->
### Sound Notifications
```powershell
# Different tones for different notification types
[System.Media.SystemSounds]::Asterisk.Play()  # Task completed
[System.Media.SystemSounds]::Question.Play()  # Input needed
[System.Media.SystemSounds]::Exclamation.Play()  # Error
```

<!-- section_id: "7788ecdd-d92e-45cd-b9ba-1c9600264b4c" -->
### Integration with Warp Workflow

#### Session End Notification
```markdown
---
**Warp AI Session Summary**
- Files modified: [list]
- Tests run: [status]
- TODO items completed: [count]
- Next session focus: [area]

*Ready for your review and next instructions*
---
```

#### Automatic Trigger Points
1. After completing implementation tasks
2. Before context switches (changing features/components)
3. When test results are available
4. When documentation is updated
5. When encountering merge conflicts or errors

<!-- section_id: "f71e9d91-7ad6-478e-9204-4f1c80e54b88" -->
### Configuration

#### Enable/Disable Notifications
```json
{
  "warp_notifications": {
    "enabled": true,
    "types": {
      "task_completion": true,
      "input_required": true,
      "errors": true,
      "todo_updates": false
    },
    "sound_enabled": true,
    "toast_duration": 5000
  }
}
```

#### Custom Notification Messages
- **GitHub Spec Kit Integration:** "Spec Kit step completed - Review generated specifications"
- **TDD Workflow:** "Tests updated - All tests passing, ready for next feature"
- **Constitution Compliance:** "Code review complete - All standards met"

<!-- section_id: "60a814ec-062d-4648-89b7-3dbe9a85f11b" -->
## Usage Examples

<!-- section_id: "ab630c33-780a-486d-977e-c5adf0345559" -->
### Typical Development Flow
1. Developer starts Warp session with `/init`
2. Warp loads context and creates TODO list
3. **Notification:** "Warp AI ready - Context loaded, TODO created"
4. Warp implements feature following Spec Kit workflow
5. **Notification:** "Feature implementation complete - Tests passing"
6. Developer reviews code and provides feedback
7. Warp refines based on feedback
8. **Notification:** "Refinements complete - Ready for deployment"

<!-- section_id: "93639cee-e79d-4bf1-88c2-1a67084f26a5" -->
### Integration with Other Tools
- **Git hooks:** Notify on successful commits
- **Test runners:** Notify when test suite completes
- **Deployment scripts:** Notify on successful deployments
- **Code quality tools:** Notify on linting/type check completion

<!-- section_id: "2e9a5c8f-ee37-4b9e-bf96-ba703d3380fb" -->
## Best Practices

1. **Keep notifications actionable** - Always include next steps
2. **Provide context** - Include relevant file names and changes
3. **Respect focus time** - Don't interrupt during active coding
4. **Batch similar notifications** - Combine related updates
5. **Allow customization** - Let developer adjust frequency and types

<!-- section_id: "2d771c03-bad6-4e2f-b12f-04a2ef78d1f5" -->
## Troubleshooting

<!-- section_id: "f54a0ad6-9c32-4e13-a1e5-e47dd7c21f8b" -->
### Notifications Not Appearing
1. Check Windows notification settings
2. Verify PowerShell execution policy
3. Ensure System.Windows.Forms is available

<!-- section_id: "3fac6edd-7eea-4edd-b083-b5b2ef422916" -->
### Too Many Notifications
1. Adjust notification types in configuration
2. Increase batching threshold
3. Set quiet hours for focused work

---
*Project: Language Tracker*
*Agent: Warp AI Assistant*
*Environment: WSL Ubuntu + Windows Host*