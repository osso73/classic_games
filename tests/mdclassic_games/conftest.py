"""Shared, display-independent test setup for the combined application."""

import hashlib
import sys
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPOSITORY_ROOT / "source" / "MDclassic_games"
TRACKED_CONFIG = APP_DIR / "main.ini"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture(scope="session", autouse=True)
def preserve_tracked_config():
    """Detect accidental writes to the tracked application configuration."""

    before = hashlib.sha256(TRACKED_CONFIG.read_bytes()).digest()
    yield
    after = hashlib.sha256(TRACKED_CONFIG.read_bytes()).digest()
    assert after == before, "tests modified source/MDclassic_games/main.ini"
