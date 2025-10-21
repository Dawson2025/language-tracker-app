# Warp AI Sound Notification System

This notification system plays sounds when Warp AI completes turns, providing audible feedback for development work.

## Files Created

### Windows Components
- `C:\Users\Dawson\bin\warp-notify.ps1` - Main PowerShell notification script
- `C:\Users\Dawson\bin\warp-notify.bat` - Convenient .bat wrapper

### Project Components
- `scripts/notify.sh` - WSL proxy script that calls Windows PowerShell
- `tools/mcp-notify/server.mjs` - MCP server exposing sound_notify tool
- `tools/mcp-notify/package.json` - Dependencies for the MCP server

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

## Warp Rule Configuration

Create a Warp Rule to automatically play sounds after each AI turn:

**Title:** "Notify on turn completion"

**Content:**
```
After composing your reply, call the MCP tool notify.sound_notify with a brief message summarizing completion (e.g., 'Response ready'). Keep calls idempotent and do not block on the tool's output.
```

Apply this rule to chats where you want audio notifications.

## Manual Testing

### From Windows PowerShell:
```powershell
C:\Users\Dawson\bin\warp-notify.ps1 -Title "Warp AI" -Message "Test notification"
```

### From WSL:
```bash
./scripts/notify.sh "Warp AI" "WSL test"
```

### Via MCP Tool (in Warp Chat):
The AI agent can call: `notify.sound_notify` with parameters:
- `title`: "Warp AI"
- `message`: "Turn complete"
- `sound`: "Windows Notify System Generic.wav"

## Sound Files

Default sounds are located in `C:\Windows\Media\`:
- Windows Notify System Generic.wav (default)
- Windows Background.wav
- Windows Foreground.wav
- Windows Hardware Fail.wav
- Windows Hardware Insert.wav
- Windows Information Bar.wav

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

## Troubleshooting

### No Sound Playing
1. Check if Windows Media files exist: `Test-Path "C:\Windows\Media\Windows Notify System Generic.wav"`
2. Verify ExecutionPolicy allows script execution
3. Check if Focus Assist/Quiet Hours is suppressing sounds
4. Look for MCP server logs in Warp

### Script Execution Issues
- All scripts use `-ExecutionPolicy Bypass` to avoid policy blocks
- Paths are absolute to ensure reliability
- Fallback beep is included if WAV files are unavailable

### WSL → Windows Communication
- The WSL script uses the full path to PowerShell: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- Output is filtered with `tr -d '\r'` to remove Windows carriage returns

## Advanced Options

### Windows Toast Notifications
To add visual toasts with sound:
1. Download SnoreToast.exe
2. Place in C:\Users\Dawson\bin\
3. Uncomment the popup section in warp-notify.ps1

### Different Sounds
Pass different sound file names:
```powershell
warp-notify.ps1 -Sound "Windows Background.wav"
```

### Custom Beep Tones
Modify the beep parameters:
```powershell
warp-notify.ps1 -BeepHz 1000 -BeepMs 300
```