"""Shared SDL audio-driver selection for the desktop host and the Android build."""
import os
import sys


def configure_audio_environment(platform_name, environ=None):
    """Default the desktop to ALSA without overriding Android's audio backend.

    Kivy's bundled SDL mixer deadlocks through the desktop PulseAudio bridge, so
    Linux desktops use ALSA. Android also reports ``sys.platform`` as ``linux``
    but only exposes its native audio backend; forcing ALSA there makes
    ``AudioSDL2`` fail and every sound load return ``None``.
    """
    if environ is None:
        environ = os.environ
    if sys.platform.startswith("linux") and platform_name != "android":
        environ.setdefault("SDL_AUDIODRIVER", "alsa")
