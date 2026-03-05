---
resource_id: "4a6e3584-8635-4ba2-9f34-48fa4fcf0aa6"
---
# TTS Fix Instructions

<!-- section_id: "c7d222e9-3db8-45d1-9dea-86e88f6eb6ec" -->
## Problem Identified

The TTS is not working because:

1. **Azure Speech SDK Import Issue**: The Azure module can't be imported when running outside the virtual environment
2. **Missing Environment Variables**: Azure Speech Service credentials are not configured  
3. **Virtual Environment**: The app needs to run with the virtual environment activated

<!-- section_id: "e5ac9c3c-84b7-47f5-a876-fd8df8f02a4d" -->
## Current Status

- ✅ Azure Speech SDK is installed (`azure-cognitiveservices-speech 1.46.0`)
- ✅ TTS engine code is working (falls back to fake TTS)
- ❌ Azure credentials not configured
- ❌ App not running in virtual environment

<!-- section_id: "8fe3358b-1cb8-46e3-b678-dd180afa2259" -->
## Solution

<!-- section_id: "a4ed290e-2a0d-4959-8df2-88d058f12add" -->
### 1. Always Run in Virtual Environment

**Instead of:**
```bash
wsl python app.py
```

**Use:**
```bash
wsl bash -c "cd /home/dawson/code/lang-trak-in-progress && source .venv/bin/activate && PORT=5001 python app.py"
```

<!-- section_id: "7833100d-81c9-44ee-b353-90068ae3b175" -->
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

<!-- section_id: "2c9a59d4-08d6-48b8-b8ff-470fdea66aa6" -->
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

<!-- section_id: "918612ef-69db-4bb1-9aac-aab037ce546e" -->
## Quick Fix Commands

<!-- section_id: "0d2e24c0-9c3b-45d3-a17c-ec263914b3d9" -->
### Run Flask App with TTS Working:
```bash
wsl bash -c "cd /home/dawson/code/lang-trak-in-progress && source .venv/bin/activate && PORT=5001 python app.py"
```

<!-- section_id: "37beeff7-0bed-4c44-92a1-55b12225a3af" -->
### Test TTS API Endpoint:
```bash
curl -X POST http://localhost:5001/api/tts/ipa \
  -H "Content-Type: application/json" \
  -d '{"ipa": "hɛloʊ"}'
```

<!-- section_id: "ae80f5b2-e9e9-40ca-9677-48aa5ff16d97" -->
## Current Fallback

The TTS engine automatically falls back to fake TTS when:
- Azure SDK is not available
- Azure credentials are not configured  
- `FORCE_FAKE_TTS=true` is set

The fake TTS returns a deterministic base64-encoded WAV file, so the app still works for development and testing.

<!-- section_id: "cd04ed08-1437-4824-afa3-10803f78c141" -->
## Expected Behavior

- **With Azure configured**: Real TTS audio in MP3 format
- **Without Azure configured**: Fake TTS audio in WAV format (240 characters of base64 data)
- **Both modes**: TTS API endpoint works and returns JSON response

---

**Status**: ✅ TTS is working (with fake audio). Configure Azure for real TTS.