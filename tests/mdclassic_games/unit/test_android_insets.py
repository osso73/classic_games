import importlib.util
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"


def _load_android_insets():
    spec = importlib.util.spec_from_file_location(
        "android_insets", APP_DIR / "android_insets.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_non_android_platform_reports_no_insets():
    module = _load_android_insets()
    assert module.system_bar_insets("linux") == (0, 0)
    assert module.system_bar_insets("win") == (0, 0)
    assert module.system_bar_insets("macosx") == (0, 0)


def test_android_platform_degrades_gracefully_without_pyjnius():
    module = _load_android_insets()
    assert module.system_bar_insets("android") == (0, 0)


def test_hide_system_bars_is_noop_off_android():
    module = _load_android_insets()
    assert module.hide_system_bars("linux") is None
    assert module.hide_system_bars("win") is None


def test_hide_system_bars_degrades_gracefully_without_android_module():
    module = _load_android_insets()
    assert module.hide_system_bars("android") is None
