#!/usr/bin/env python3
# resource_id: 680456b7-81bd-47a0-a075-4256140cfb17
"""
TTS Test Script
Debug TTS functionality and Azure configuration
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_azure_import():
    """Test if Azure TTS can be imported"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        print("✅ Azure Speech SDK imported successfully")
        print(f"   Version: {speechsdk.__version__ if hasattr(speechsdk, '__version__') else 'Unknown'}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Azure Speech SDK: {e}")
        return False

def test_environment_variables():
    """Check Azure TTS environment variables"""
    env_vars = [
        'AZURE_SPEECH_KEY',
        'AZURE_SPEECH_REGION', 
        'AZURE_SPEECH_KEY_WEST',
        'AZURE_SPEECH_REGION_WEST',
        'AZURE_SPEECH_KEY_EAST',
        'AZURE_SPEECH_REGION_EAST',
        'FORCE_FAKE_TTS'
    ]
    
    print("🔍 Environment Variables:")
    found_any = False
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {'*' * min(len(value), 4)}...")
            found_any = True
        else:
            print(f"   ❌ {var}: Not set")
    
    return found_any

def test_tts_engine():
    """Test the TTS engine itself"""
    try:
        from src.tts_ipa import ipa_tts
        print("✅ TTS engine imported successfully")
        
        # Get status report
        status = ipa_tts.get_status_report()
        print("\n📊 TTS Status Report:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test audio generation
        print("\n🎵 Testing audio generation...")
        test_ipa = "hɛloʊ"
        result = ipa_tts.generate_ipa_audio(test_ipa)
        
        if result:
            print(f"   ✅ Generated {len(result)} characters of audio data")
            print(f"   Backend used: {ipa_tts.last_backend}")
        else:
            print("   ❌ No audio generated")
            
        return True
        
    except Exception as e:
        print(f"❌ TTS engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔧 TTS Troubleshooting Script")
    print("=" * 40)
    
    # Test 1: Azure import
    print("\n1. Testing Azure Speech SDK import...")
    azure_available = test_azure_import()
    
    # Test 2: Environment variables
    print("\n2. Checking environment variables...")
    env_configured = test_environment_variables()
    
    # Test 3: TTS Engine
    print("\n3. Testing TTS engine...")
    tts_working = test_tts_engine()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 SUMMARY:")
    print(f"   Azure SDK Available: {'✅' if azure_available else '❌'}")
    print(f"   Environment Configured: {'✅' if env_configured else '❌'}")  
    print(f"   TTS Engine Working: {'✅' if tts_working else '❌'}")
    
    if not azure_available:
        print("\n💡 RECOMMENDATIONS:")
        print("   1. Ensure you're running in the virtual environment:")
        print("      source .venv/bin/activate")
        print("   2. Install Azure Speech SDK:")
        print("      pip install azure-cognitiveservices-speech")
    
    if azure_available and not env_configured:
        print("\n💡 AZURE CONFIGURATION NEEDED:")
        print("   Set up Azure Speech Service credentials:")
        print("   export AZURE_SPEECH_KEY='your-key'")
        print("   export AZURE_SPEECH_REGION='your-region'")
    
    if not tts_working:
        print("\n💡 TTS ENGINE ISSUES:")
        print("   Check the error details above for specific problems")

if __name__ == "__main__":
    main()