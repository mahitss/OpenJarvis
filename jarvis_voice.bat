@echo off
title J.A.R.V.I.S. - Hands-Free Voice Assistant
cd /d "%~dp0"
set JARVIS_SKIP_RUNTIME_PANEL=1
set JARVIS_SKIP_MODEL_PICK=1
echo ========================================================
echo        J.A.R.V.I.S. Hands-Free Conversational Voice
echo ========================================================
echo.
echo Initializing speech models (Whisper STT + Kokoro TTS)...
echo When J.A.R.V.I.S. greets you, simply speak aloud.
echo Pause speaking to send your message.
echo Say 'goodbye' or 'exit' (or press Ctrl+C) to finish.
echo ========================================================
echo.
.\.venv\Scripts\jarvis.exe voice --auto-approve --skip-runtime-panel
pause
