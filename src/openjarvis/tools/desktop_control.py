"""Desktop control tool — launch apps, open URLs, search web, control Windows, and take screenshots."""

from __future__ import annotations

import os
import subprocess
import time
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec


@ToolRegistry.register("desktop_control")
class DesktopControlTool(BaseTool):
    """Control the Windows laptop: open apps, open websites, search web, open folders, and capture screen."""

    tool_id = "desktop_control"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="desktop_control",
            description=(
                "Control the Windows laptop with full access. Actions:\n"
                "- 'open_url': Open any website URL in the browser.\n"
                "- 'search_web': Search Google or YouTube directly in the browser.\n"
                "- 'open_app': Open any application (e.g. chrome, edge, notepad, calc, spotify, code, explorer, settings).\n"
                "- 'open_folder': Open a folder (downloads, desktop, documents, or custom path) in File Explorer.\n"
                "- 'system_status': Get current battery, CPU, RAM, and system info.\n"
                "- 'take_screenshot': Capture the current desktop screen.\n"
                "- 'press_key': Press a key or hotkey combination (e.g. 'enter', 'ctrl+c', 'win')."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "open_url",
                            "search_web",
                            "open_app",
                            "open_folder",
                            "system_status",
                            "take_screenshot",
                            "press_key",
                        ],
                        "description": "The desktop action to perform.",
                    },
                    "target": {
                        "type": "string",
                        "description": (
                            "Target for the action: URL for 'open_url', search query for 'search_web', "
                            "app name for 'open_app', folder name/path for 'open_folder', "
                            "or key name for 'press_key'."
                        ),
                    },
                    "search_engine": {
                        "type": "string",
                        "enum": ["google", "youtube", "bing"],
                        "description": "Search engine for 'search_web'. Defaults to 'google'.",
                    },
                },
                "required": ["action"],
            },
            category="system",
            requires_confirmation=False,
            timeout_seconds=15.0,
        )

    def execute(self, **params: Any) -> ToolResult:
        action = params.get("action", "")
        target = str(params.get("target", "")).strip()
        search_engine = str(params.get("search_engine", "google")).lower()

        if action == "open_url":
            if not target:
                return ToolResult(tool_name="desktop_control", content="Error: No URL provided.", success=False)
            if not target.startswith(("http://", "https://")):
                target = "https://" + target
            try:
                webbrowser.open(target)
                return ToolResult(tool_name="desktop_control", content=f"Successfully opened URL: {target}", success=True)
            except Exception as e:
                return ToolResult(tool_name="desktop_control", content=f"Failed to open URL: {e}", success=False)

        elif action == "search_web":
            if not target:
                return ToolResult(tool_name="desktop_control", content="Error: No search query provided.", success=False)
            encoded = urllib.parse.quote_plus(target)
            if search_engine == "youtube":
                url = f"https://www.youtube.com/results?search_query={encoded}"
            elif search_engine == "bing":
                url = f"https://www.bing.com/search?q={encoded}"
            else:
                url = f"https://www.google.com/search?q={encoded}"
            try:
                webbrowser.open(url)
                return ToolResult(
                    tool_name="desktop_control",
                    content=f"Opened {search_engine.capitalize()} search for '{target}' in browser: {url}",
                    success=True,
                )
            except Exception as e:
                return ToolResult(tool_name="desktop_control", content=f"Failed to search web: {e}", success=False)

        elif action == "open_app":
            if not target:
                return ToolResult(tool_name="desktop_control", content="Error: No application name provided.", success=False)
            app_lower = target.lower()
            app_map = {
                "chrome": "chrome",
                "google chrome": "chrome",
                "edge": "msedge",
                "microsoft edge": "msedge",
                "browser": "msedge",
                "notepad": "notepad",
                "calc": "calc",
                "calculator": "calc",
                "code": "code",
                "vs code": "code",
                "vscode": "code",
                "spotify": "spotify:",
                "explorer": "explorer",
                "files": "explorer",
                "file explorer": "explorer",
                "terminal": "wt",
                "powershell": "powershell",
                "cmd": "cmd",
                "settings": "ms-settings:",
                "task manager": "taskmgr",
            }
            cmd_target = app_map.get(app_lower, target)
            try:
                if cmd_target.endswith(":") or ":" in cmd_target:
                    webbrowser.open(cmd_target)
                elif hasattr(os, "startfile"):
                    os.startfile(cmd_target)
                else:
                    subprocess.Popen(f"start {cmd_target}", shell=True)
                return ToolResult(
                    tool_name="desktop_control",
                    content=f"Successfully launched application: {target}",
                    success=True,
                )
            except Exception as e:
                try:
                    subprocess.Popen(f"start {cmd_target}", shell=True)
                    return ToolResult(tool_name="desktop_control", content=f"Launched application '{target}' via shell.", success=True)
                except Exception as exc:
                    return ToolResult(tool_name="desktop_control", content=f"Failed to launch '{target}': {exc}", success=False)

        elif action == "open_folder":
            folder_lower = target.lower() if target else "downloads"
            user_home = Path.home()
            folder_map = {
                "downloads": user_home / "Downloads",
                "download": user_home / "Downloads",
                "desktop": user_home / "Desktop",
                "documents": user_home / "Documents",
                "document": user_home / "Documents",
                "pictures": user_home / "Pictures",
                "photos": user_home / "Pictures",
                "videos": user_home / "Videos",
                "music": user_home / "Music",
            }
            resolved_path = folder_map.get(folder_lower, Path(target).expanduser() if target else user_home)
            try:
                if resolved_path.exists():
                    os.startfile(str(resolved_path))
                    return ToolResult(
                        tool_name="desktop_control",
                        content=f"Opened folder in File Explorer: {resolved_path}",
                        success=True,
                    )
                else:
                    return ToolResult(
                        tool_name="desktop_control",
                        content=f"Folder not found: {resolved_path}",
                        success=False,
                    )
            except Exception as e:
                return ToolResult(tool_name="desktop_control", content=f"Failed to open folder: {e}", success=False)

        elif action == "system_status":
            info = []
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    status = "Plugged in" if battery.power_plugged else "On battery"
                    info.append(f"Battery: {battery.percent}% ({status})")
                info.append(f"CPU Usage: {psutil.cpu_percent(interval=0.1)}%")
                mem = psutil.virtual_memory()
                info.append(f"RAM: {mem.percent}% used ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")
            except Exception:
                info.append("System status: Operational")
            return ToolResult(tool_name="desktop_control", content="\n".join(info), success=True)

        elif action == "take_screenshot":
            try:
                import pyautogui
                save_dir = Path.home() / "Pictures" / "Jarvis_Screenshots"
                save_dir.mkdir(parents=True, exist_ok=True)
                filename = target if target else f"screenshot_{int(time.time())}.png"
                if not filename.endswith((".png", ".jpg")):
                    filename += ".png"
                save_path = save_dir / filename
                pyautogui.screenshot(str(save_path))
                return ToolResult(
                    tool_name="desktop_control",
                    content=f"Screenshot captured and saved to: {save_path}",
                    success=True,
                )
            except Exception as e:
                return ToolResult(tool_name="desktop_control", content=f"Failed to capture screenshot: {e}", success=False)

        elif action == "press_key":
            if not target:
                return ToolResult(tool_name="desktop_control", content="Error: No key provided.", success=False)
            try:
                import pyautogui
                keys = [k.strip().lower() for k in target.split("+")]
                if len(keys) > 1:
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(keys[0])
                return ToolResult(
                    tool_name="desktop_control",
                    content=f"Pressed key combination: {target}",
                    success=True,
                )
            except Exception as e:
                return ToolResult(tool_name="desktop_control", content=f"Failed to press key: {e}", success=False)

        return ToolResult(tool_name="desktop_control", content=f"Unknown action: {action}", success=False)
