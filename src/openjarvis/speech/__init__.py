"""Speech subsystem — speech-to-text and text-to-speech backends."""

import importlib
import os

# Priority local backends first
for _mod in ("faster_whisper", "kokoro_tts"):
    try:
        importlib.import_module(f".{_mod}", __name__)
    except ImportError:
        pass

# Cloud backends loaded only if API keys are configured
_cloud_stt = []
if os.environ.get("OPENAI_API_KEY"):
    _cloud_stt.append("openai_whisper")
if os.environ.get("DEEPGRAM_API_KEY"):
    _cloud_stt.append("deepgram")
for _mod in _cloud_stt:
    try:
        importlib.import_module(f".{_mod}", __name__)
    except ImportError:
        pass

_cloud_tts = []
if os.environ.get("OPENAI_API_KEY"):
    _cloud_tts.append("openai_tts")
if os.environ.get("ELEVENLABS_API_KEY"):
    _cloud_tts.append("elevenlabs_tts")
if os.environ.get("CARTESIA_API_KEY"):
    _cloud_tts.append("cartesia_tts")
for _mod in _cloud_tts:
    try:
        importlib.import_module(f".{_mod}", __name__)
    except ImportError:
        pass
