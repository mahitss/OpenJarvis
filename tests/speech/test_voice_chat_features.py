"""Tests for real-time continuous hands-free voice chat features."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from openjarvis.cli._voice_chat import (
    VOICE_EXIT,
    VoiceSession,
    _clean_text_for_speech,
    read_voice_input,
    record_voice,
)
from openjarvis.speech.voice_io import record_until_silence


def test_clean_text_for_speech() -> None:
    raw = (
        "# Status Report\n"
        "**Good evening, sir.** All systems are *operational*.\n"
        "Refer to [Documentation](http://example.com) for details.\n"
        "```python\nprint('hello')\n```\n"
        "- Task 1: Complete\n"
        "> Quote here\n"
        "Value is `test_val`."
    )
    cleaned = _clean_text_for_speech(raw)
    assert "**" not in cleaned
    assert "#" not in cleaned
    assert "print('hello')" not in cleaned
    assert "Documentation" in cleaned
    assert "http://example.com" not in cleaned
    assert "Good evening, sir. All systems are operational." in cleaned
    assert "Value is test_val." in cleaned


def test_continuous_voice_input_routes_to_record_voice() -> None:
    console = MagicMock()
    session = MagicMock(spec=VoiceSession)

    with patch("openjarvis.cli._voice_chat.record_voice", return_value="hello jarvis") as mock_rec:
        result = read_voice_input(console, session, continuous=True)
        assert result == "hello jarvis"
        mock_rec.assert_called_once_with(console, session, continuous=True)


def test_continuous_voice_exit_phrases() -> None:
    console = MagicMock()
    session = MagicMock(spec=VoiceSession)
    backend = MagicMock()
    backend.transcribe.return_value = MagicMock(text="goodbye jarvis")
    session.get_stt_backend.return_value = backend
    session.get_stt_language.return_value = None

    with patch("openjarvis.speech.voice_io.record_until_silence", return_value=b"fake_wav"):
        result = record_voice(console, session, continuous=True)
        assert result is VOICE_EXIT
