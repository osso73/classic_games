import importlib.util
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"


def _load_audio_env():
    spec = importlib.util.spec_from_file_location("audio_env", APP_DIR / "audio_env.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_android_leaves_sdl_audio_driver_untouched():
    module = _load_audio_env()
    environ = {}
    module.configure_audio_environment("android", environ)
    assert "SDL_AUDIODRIVER" not in environ


def test_linux_desktop_defaults_to_alsa():
    module = _load_audio_env()
    environ = {}
    module.configure_audio_environment("linux", environ)
    assert environ.get("SDL_AUDIODRIVER") == "alsa"


def test_existing_audio_driver_is_preserved():
    module = _load_audio_env()
    environ = {"SDL_AUDIODRIVER": "pulseaudio"}
    module.configure_audio_environment("linux", environ)
    assert environ["SDL_AUDIODRIVER"] == "pulseaudio"
