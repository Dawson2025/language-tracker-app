---
resource_id: "7da5af04-5a8b-4fe5-bb85-3ee44e7c1857"
---
# Warp AI Sound Notification System

This notification system plays sounds when Warp AI completes turns, providing audible feedback for development work.

<!-- section_id: "337ea637-9227-4f85-88f1-4e58bcc21249" -->
## Files Created

<!-- section_id: "8fc29b89-e70b-4627-bed6-58f2150d5730" -->
### Windows Components
- `C:\Users\Dawson\bin\warp-notify.ps1` - Main PowerShell notification script
- `C:\Users\Dawson\bin\warp-notify.bat` - Convenient .bat wrapper

<!-- section_id: "1bd0a534-3241-480c-8971-509b0fdc2593" -->
### Project Components
- `scripts/notify.sh` - WSL proxy script that calls Windows PowerShell
- `tools/mcp-notify/server.mjs` - MCP server exposing sound_notify tool
- `tools/mcp-notify/package.json` - Dependencies for the MCP server

<!-- section_id: "99c914a2-2ca4-4e2a-a4f1-fa912161da69" -->
## MCP Server Configuration

Add this to your Warp MCP servers configuration:

```json
{
  "mcpServers": {
    "notify": {
      "command": "node",
      "args": ["C:\\home\\dawson\\code\\lang-trak-in-progress\\tools\\mcp-notify\\server.mjs"]
    }
  }
}
```

Or in Warp Settings → MCP Servers:
- Name: notify
- Command: node
- Args: C:\home\dawson\code\lang-trak-in-progress\tools\mcp-notify\server.mjs

<!-- section_id: "271bea29-fc47-47e9-9b7b-45d6b691abcd" -->
## Warp Rule Configuration

Create a Warp Rule to automatically play sounds after each AI turn:

**Title:** "Notify on turn completion"

**Content:**
```
After composing your reply, call the MCP tool notify.sound_notify with a brief message summarizing completion (e.g., 'Response ready'). Keep calls idempotent and do not block on the tool's output.
```

Apply this rule to chats where you want audio notifications.

<!-- section_id: "c71fc19f-a515-43bd-a2e5-01b1d5000756" -->
## Manual Testing

<!-- section_id: "1ef93848-aa40-42ee-ab23-dd26d4ba6e3f" -->
### From Windows PowerShell:
```powershell
C:\Users\Dawson\bin\warp-notify.ps1 -Title "Warp AI" -Message "Test notification"
```

<!-- section_id: "9ddcefe1-736e-4744-8a2a-97d8ebf293d3" -->
### From WSL:
```bash
./scripts/notify.sh "Warp AI" "WSL test"
```

<!-- section_id: "b336ce3a-f65d-4a4f-832e-849364e0392e" -->
### Via MCP Tool (in Warp Chat):
The AI agent can call: `notify.sound_notify` with parameters:
- `title`: "Warp AI"
- `message`: "Turn complete"
- `sound`: "Windows Notify System Generic.wav"

<!-- section_id: "8ea291a7-0ee9-4ecd-bda7-44e3795654ff" -->
## Sound Files

Default sounds are located in `C:\Windows\Media\`:
- Windows Notify System Generic.wav (default)
- Windows Background.wav
- Windows Foreground.wav
- Windows Hardware Fail.wav
- Windows Hardware Insert.wav
- Windows Information Bar.wav

<!-- section_id: "502264e0-5494-4115-a287-3ebc173de5a2" -->
## Workflow Integration (Optional)

Create a Warp Workflow named "Play notify sound":

**Windows Command:**
```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Dawson\bin\warp-notify.ps1" -Title "Warp AI" -Message "Manual trigger"
```

**WSL Command:**
```
./scripts/notify.sh "Warp AI" "Manual trigger"
```

<!-- section_id: "d879b415-ef73-4b39-99f6-bf29b8ee272c" -->
## Troubleshooting

<!-- section_id: "82669831-bed6-462b-ab04-c78182aab44c" -->
### No Sound Playing
1. Check if Windows Media files exist: `Test-Path "C:\Windows\Media\Windows Notify System Generic.wav"`
2. Verify ExecutionPolicy allows script execution
3. Check if Focus Assist/Quiet Hours is suppressing sounds
4. Look for MCP server logs in Warp

<!-- section_id: "498dbec3-870b-42f2-b65f-1c6547a171d3" -->
### Script Execution Issues
- All scripts use `-ExecutionPolicy Bypass` to avoid policy blocks
- Paths are absolute to ensure reliability
- Fallback beep is included if WAV files are unavailable

<!-- section_id: "226efd11-9ebd-46fe-a032-f15b895c0877" -->
### WSL → Windows Communication
- The WSL script uses the full path to PowerShell: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- Output is filtered with `tr -d '\r'` to remove Windows carriage returns

<!-- section_id: "18dc3ca3-244e-4268-83c1-8724f0524bbb" -->
## Advanced Options

<!-- section_id: "40bad2c6-d9b7-49e0-ac3f-48d705a13b0c" -->
### Windows Toast Notifications
To add visual toasts with sound:
1. Download SnoreToast.exe
2. Place in C:\Users\Dawson\bin\
3. Uncomment the popup section in warp-notify.ps1

<!-- section_id: "1679ebd0-b49b-4eeb-a53f-db89aded0d35" -->
### Different Sounds
Pass different sound file names:
```powershell
warp-notify.ps1 -Sound "Windows Background.wav"
```

<!-- section_id: "cf6b5c39-becf-463d-a336-ba18fae69691" -->
### Custom Beep Tones
Modify the beep parameters:
```powershell
warp-notify.ps1 -BeepHz 1000 -BeepMs 300
```