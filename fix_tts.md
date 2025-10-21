# TTS Fix Instructions

## Problem Identified

The TTS is not working because:

1. **Azure Speech SDK Import Issue**: The Azure module can't be imported when running outside the virtual environment
2. **Missing Environment Variables**: Azure Speech Service credentials are not configured  
3. **Virtual Environment**: The app needs to run with the virtual environment activated

## Current Status

- ✅ Azure Speech SDK is installed (`azure-cognitiveservices-speech 1.46.0`)
- ✅ TTS engine code is working (falls back to fake TTS)
- ❌ Azure credentials not configured
- ❌ App not running in virtual environment

## Solution

### 1. Always Run in Virtual Environment

**Instead of:**
```bash
wsl python app.py
```

**Use:**
```bash
wsl bash -c "cd /home/dawson/code/lang-trak-in-progress && source .venv/bin/activate && PORT=5001 python app.py"
```

### 2. Configure Azure Speech Service (Optional)

If you want real TTS instead of fake audio:

1. **Create Azure Speech Service**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a "Speech Services" resource
   - Get your Key and Region

2. **Set Environment Variables**:
   ```bash
   export AZURE_SPEECH_KEY="your-azure-key-here"
   export AZURE_SPEECH_REGION="your-region-here"  # e.g., "eastus"
   ```

3. **Or add to your shell profile** (`~/.bashrc` or `~/.zshrc`):
   ```bash
   echo 'export AZURE_SPEECH_KEY="your-key"' >> ~/.bashrc
   echo 'export AZURE_SPEECH_REGION="your-region"' >> ~/.bashrc
   source ~/.bashrc
   ```

### 3. Test TTS Functionality

Create a simple test:

```bash
wsl bash -c "cd /home/dawson/code/lang-trak-in-progress && source .venv/bin/activate && python -c '
import sys
sys.path.append(\".\")
from src.tts_ipa import ipa_tts
print(\"TTS Status:\", ipa_tts.get_status_report())
result = ipa_tts.generate_ipa_audio(\"hɛloʊ\")
print(f\"Audio generated: {len(result) if result else 0} chars, Backend: {ipa_tts.last_backend}\")
'"
```

## Quick Fix Commands

### Run Flask App with TTS Working:
```bash
wsl bash -c "cd /home/dawson/code/lang-trak-in-progress && source .venv/bin/activate && PORT=5001 python app.py"
```

### Test TTS API Endpoint:
```bash
curl -X POST http://localhost:5001/api/tts/ipa \
  -H "Content-Type: application/json" \
  -d '{"ipa": "hɛloʊ"}'
```

## Current Fallback

The TTS engine automatically falls back to fake TTS when:
- Azure SDK is not available
- Azure credentials are not configured  
- `FORCE_FAKE_TTS=true` is set

The fake TTS returns a deterministic base64-encoded WAV file, so the app still works for development and testing.

## Expected Behavior

- **With Azure configured**: Real TTS audio in MP3 format
- **Without Azure configured**: Fake TTS audio in WAV format (240 characters of base64 data)
- **Both modes**: TTS API endpoint works and returns JSON response

---

**Status**: ✅ TTS is working (with fake audio). Configure Azure for real TTS.