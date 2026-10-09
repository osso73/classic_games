from importlib.metadata import distribution
from configparser import ConfigParser
import ast
import json
from pathlib import Path

import pytest


APP_DIR = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"
GAME_FOLDERS = ["pong", "ahorcado", "memory", "game_15puzzle", "game_2048", "buscaminas", "snake"]


@pytest.mark.parametrize("folder,section", [
    ("pong", "Pong"), ("ahorcado", "Ahorcado"), ("memory", "Memory"),
    ("game_15puzzle", "fifteen"), ("snake", "Snake"),
])
def test_settings_json_has_valid_controls(folder, section):
    controls = json.loads((APP_DIR / folder / "settings.json").read_text())
    assert controls
    keys = [control["key"] for control in controls if control["type"] != "title"]
    assert len(keys) == len(set(keys))
    for control in controls:
        if control["type"] == "title":
            continue
        assert control["section"] == section
        assert control["type"] in {"numeric", "options", "bool", "string"}
        if control["type"] == "options":
            assert control["options"]


def test_required_runtime_resources_are_present():
    paths = ["menu.kv", "drawer.kv", "images/icon.png", "images/splash.png",
             "fonts/magnetob.ttf", "ahorcado/lista_palabras.txt"]
    paths += [f"{folder}/images/icon.{extension}" for folder, extension in [
        ("pong", "jpg"), ("ahorcado", "jpg"), ("memory", "png"),
        ("game_15puzzle", "png"), ("game_2048", "png"), ("buscaminas", "png"),
        ("snake", "png"),
    ]]
    for relative in paths:
        assert (APP_DIR / relative).stat().st_size > 0, relative
    sounds = list((APP_DIR / "audio").glob("*.ogg"))
    assert len(sounds) == 15
    assert all(sound.stat().st_size > 0 for sound in sounds)
    sources = list(APP_DIR.glob("*.py"))
    for folder in GAME_FOLDERS:
        sources.extend((APP_DIR / folder).rglob("*.py"))
    for source in sources:
        for node in ast.walk(ast.parse(source.read_text())):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "play" and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)):
                assert (APP_DIR / "audio" / f"{node.args[0].value}.ogg").is_file(), source
    assert (APP_DIR / "ahorcado/lista_palabras.txt").read_text().splitlines()
    for folder in GAME_FOLDERS:
        images = list((APP_DIR / folder / "images").rglob("*"))
        assert any(path.is_file() and path.stat().st_size > 0 for path in images)


def test_packaging_includes_runtime_formats_and_excludes_examples():
    spec = ConfigParser(interpolation=None)
    spec.read(APP_DIR / "buildozer.spec")
    extensions = set(spec["app"]["source.include_exts"].split(","))
    assert {"py", "png", "jpg", "kv", "ogg", "json", "ttf", "txt", "gif"} <= extensions
    excluded = {part.strip() for part in spec["app"]["source.exclude_dirs"].split(",")}
    assert {"tests", "bin", "resources"} <= excluded
    assert spec["app"]["source.dir"] == "."
    assert "ini" not in extensions
    # ICO inclusion is a Phase 3 spec change; desktop decoding is tested now.


def test_installed_kivymd_resource_is_available():
    kivymd = distribution("kivymd")
    resource = kivymd.locate_file("kivymd/uix/label/label.kv")

    assert resource.is_file()
    assert sum(str(file).endswith(".kv") for file in kivymd.files or []) > 0
