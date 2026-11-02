"""J.A.R.V.I.S. Autonomous Desktop Launcher

Orchestrates the complete JARVIS experience:
1. Verifies Ollama is running (starts it if needed).
2. Verifies OpenJarvis API server is running on port 8000.
3. Verifies OpenJarvis Web UI is running on port 5173.
4. Opens the sleek native App Window on screen.
5. Starts hands-free voice interaction with full laptop control (single-instance).
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / ".venv" / "Scripts" / "python.exe"
VENV_JARVIS = BASE_DIR / ".venv" / "Scripts" / "jarvis.exe"
VOICE_BAT = BASE_DIR / "jarvis_voice.bat"
FRONTEND_DIR = BASE_DIR / "frontend"
EDGE_PATH = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")


def is_port_listening(url: str, timeout: float = 1.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as res:
            return res.status == 200 or res.status == 404
    except Exception:
        return False


def ensure_ollama() -> None:
    if not is_port_listening("http://127.0.0.1:11434/api/tags"):
        print("[JARVIS] Starting Ollama...")
        subprocess.Popen(
            ["ollama", "serve"],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        time.sleep(2)


def ensure_backend() -> None:
    if not is_port_listening("http://127.0.0.1:8000/health"):
        # Remove any stale server records if port is dead
        cfg_dir = Path.home() / ".openjarvis"
        for stale in ["server.pid", "server.json"]:
            try:
                (cfg_dir / stale).unlink(missing_ok=True)
            except Exception:
                pass
        print("[JARVIS] Starting OpenJarvis API Server (port 8000)...")
        log_file = open(Path.home() / ".openjarvis" / "server.log", "a", encoding="utf-8")
        subprocess.Popen(
            [str(VENV_PYTHON), "-m", "openjarvis.cli", "serve", "--port", "8000"],
            cwd=str(BASE_DIR),
            stdout=log_file,
            stderr=log_file,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        # Wait up to 10s for API server to bind
        for _ in range(20):
            if is_port_listening("http://127.0.0.1:8000/health", timeout=0.5):
                break
            time.sleep(0.5)


def ensure_frontend() -> None:
    if not is_port_listening("http://localhost:5173/"):
        print("[JARVIS] Starting OpenJarvis Web UI (port 5173)...")
        subprocess.Popen(
            ["npm.cmd" if sys.platform == "win32" else "npm", "run", "dev"],
            cwd=str(FRONTEND_DIR),
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        # Wait up to 6s for Vite dev server
        for _ in range(12):
            if is_port_listening("http://localhost:5173/", timeout=0.5):
                break
            time.sleep(0.5)


def open_app_window() -> None:
    url = "http://localhost:5173/"
    print("[JARVIS] Opening Desktop App Window on screen...")
    if EDGE_PATH.exists():
        subprocess.Popen(
            [
                str(EDGE_PATH),
                f"--app={url}",
                "--window-size=1280,820",
                "--app-id=OpenJarvis",
            ]
        )
    else:
        import webbrowser
        webbrowser.open(url)


def is_voice_already_running() -> bool:
    """Check if hands-free voice assistant is already active using Windows Named Mutex."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.CreateMutexW(None, False, "OpenJarvisVoiceAssistantMutex")
        if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            if handle:
                kernel32.CloseHandle(handle)
            return True
        if handle:
            kernel32.CloseHandle(handle)
        return False
    except Exception:
        return False


def run_voice_assistant() -> None:
    if is_voice_already_running():
        print("[JARVIS] Hands-Free Voice Assistant is already active and listening.")
        return

    print("[JARVIS] Launching Hands-Free Voice Assistant with Full Laptop Control...")
    if sys.platform == "win32" and VOICE_BAT.exists():
        # Launch in a visible terminal window so user can see transcription and tool feedback
        subprocess.Popen(
            ["cmd.exe", "/c", "start", "J.A.R.V.I.S. - Voice Assistant", str(VOICE_BAT)],
            cwd=str(BASE_DIR),
        )
    else:
        subprocess.run(
            [str(VENV_JARVIS), "voice", "--full-access"],
            cwd=str(BASE_DIR),
        )


def main() -> None:
    print("=" * 60)
    print("       J.A.R.V.I.S. - Autonomous System & Voice Assistant")
    print("=" * 60)
    ensure_ollama()
    ensure_backend()
    ensure_frontend()
    open_app_window()
    run_voice_assistant()


if __name__ == "__main__":
    main()
