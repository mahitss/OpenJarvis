"""Tests for desktop_control tool."""

from __future__ import annotations

from unittest.mock import patch
from openjarvis.tools.desktop_control import DesktopControlTool


def test_desktop_control_spec() -> None:
    tool = DesktopControlTool()
    assert tool.spec.name == "desktop_control"
    assert "open_url" in tool.spec.parameters["properties"]["action"]["enum"]
    assert "search_web" in tool.spec.parameters["properties"]["action"]["enum"]
    assert "open_app" in tool.spec.parameters["properties"]["action"]["enum"]
    assert "open_folder" in tool.spec.parameters["properties"]["action"]["enum"]
    assert "system_status" in tool.spec.parameters["properties"]["action"]["enum"]


def test_desktop_control_open_url() -> None:
    tool = DesktopControlTool()
    with patch("webbrowser.open") as mock_open:
        res = tool.execute(action="open_url", target="google.com")
        assert res.success is True
        mock_open.assert_called_once_with("https://google.com")


def test_desktop_control_search_web() -> None:
    tool = DesktopControlTool()
    with patch("webbrowser.open") as mock_open:
        res = tool.execute(action="search_web", target="quantum computing", search_engine="google")
        assert res.success is True
        assert "google.com/search?q=quantum+computing" in mock_open.call_args[0][0]


def test_desktop_control_system_status() -> None:
    tool = DesktopControlTool()
    res = tool.execute(action="system_status")
    assert res.success is True
    assert "CPU" in res.content
