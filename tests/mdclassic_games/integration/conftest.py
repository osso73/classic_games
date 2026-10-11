"""Fixtures for GUI tests; Kivy imports must remain inside tests or fixtures."""

from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"


@pytest.fixture
def gui_environment(tmp_path, monkeypatch):
    """Provide per-test Kivy writable state before a GUI test imports Kivy."""

    kivy_home = tmp_path / "kivy"
    monkeypatch.setenv("KIVY_HOME", str(kivy_home))
    monkeypatch.setenv("KIVY_NO_FILELOG", "1")
    monkeypatch.chdir(APP_DIR)
    yield kivy_home
