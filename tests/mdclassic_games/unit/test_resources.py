from importlib.metadata import distribution
from configparser import ConfigParser
import ast
import json
from pathlib import Path
import re
import tomllib

import pytest


APP_DIR = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"
GAME_FOLDERS = ["pong", "ahorcado", "memory", "game_15puzzle", "game_2048", "buscaminas", "snake"]


@pytest.fixture
def app_spec():
    spec = ConfigParser(interpolation=None)
    spec.read(APP_DIR / "buildozer.spec")
    return spec["app"]


def spec_list(spec, key):
    return {part.strip() for part in spec.get(key, "").split(",") if part.strip()}


def assert_packaged_resource(spec, path):
    relative = path.relative_to(APP_DIR)
    assert path.is_file() and path.stat().st_size > 0, relative
    assert path.suffix[1:] in spec_list(spec, "source.include_exts"), relative
    assert path.suffix[1:] not in spec_list(spec, "source.exclude_exts"), relative
    # Buildozer 1.6.0 excludes source-relative directory prefixes, not basenames.
    assert not any(
        relative.as_posix().startswith(directory.rstrip("/") + "/")
        for directory in spec_list(spec, "source.exclude_dirs")
    ), relative
    assert not any(part.startswith(".") for part in relative.parts), relative


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


def test_required_runtime_resources_are_present(app_spec):
    paths = ["menu.kv", "drawer.kv", "images/icon.png", "images/splash.png",
             "fonts/magnetob.ttf", "ahorcado/lista_palabras.txt"]
    menu_images = re.findall(r"source: '([^']+)'", (APP_DIR / "menu.kv").read_text())
    assert len(menu_images) == 7
    paths += menu_images
    paths += [f"{folder}/settings.json" for folder in
              ["pong", "ahorcado", "memory", "game_15puzzle", "snake"]]
    for relative in paths:
        assert_packaged_resource(app_spec, APP_DIR / relative)
    sounds = list((APP_DIR / "audio").glob("*.ogg"))
    assert len(sounds) == 15
    for sound in sounds:
        assert_packaged_resource(app_spec, sound)
    sources = list(APP_DIR.glob("*.py"))
    for folder in GAME_FOLDERS:
        sources.extend((APP_DIR / folder).rglob("*.py"))
    for source in sources:
        assert_packaged_resource(app_spec, source)
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
        for path in images:
            if path.is_file() and path.suffix in {".png", ".jpg", ".gif", ".ico"}:
                assert_packaged_resource(app_spec, path)
        for font in (APP_DIR / folder).rglob("*.ttf"):
            assert_packaged_resource(app_spec, font)


def test_packaging_includes_runtime_formats_and_excludes_examples(app_spec):
    extensions = spec_list(app_spec, "source.include_exts")
    assert {"py", "png", "jpg", "kv", "ogg", "json", "ttf", "txt", "gif", "ico"} <= extensions
    excluded = spec_list(app_spec, "source.exclude_dirs")
    assert {"tests", "bin", "build", "resources", ".buildozer", ".venv"} <= excluded
    assert app_spec["source.dir"] == "."
    assert "ini" not in extensions
    # No include pattern may re-enable excluded trees; no exclude pattern may
    # silently drop nested runtime assets. Extensions still filter pattern matches.
    assert not spec_list(app_spec, "source.include_patterns")
    assert not spec_list(app_spec, "source.exclude_patterns")


@pytest.mark.parametrize("theme", [control for control in json.loads(
    (APP_DIR / "memory/settings.json").read_text()
) if control.get("key") == "theme"][0]["options"])
def test_memory_theme_resources_are_packaged(app_spec, theme):
    directory = APP_DIR / "memory/images/themes" / theme
    assert_packaged_resource(app_spec, directory / "back.jpg")
    cards = sorted(directory.glob("image*"))
    assert len(cards) >= 20
    for card in cards:
        assert_packaged_resource(app_spec, card)
    if theme == "cartoons":
        assert len(list(directory.glob("*.ico"))) == 5


@pytest.mark.parametrize("theme", [control for control in json.loads(
    (APP_DIR / "game_15puzzle/settings.json").read_text()
) if control.get("key") == "theme"][0]["options"])
def test_puzzle_theme_tiles_and_reference_resources_are_packaged(app_spec, theme):
    directory = APP_DIR / "game_15puzzle/images/themes" / theme
    # Both Card15 and CardSample use these numbered JPGs; the reference is a
    # complete tiled board, including the last tile hidden during gameplay.
    for board_size in (3, 4, 5):
        for tile in range(1, board_size**2 + 1):
            assert_packaged_resource(app_spec, directory / str(board_size) / f"{tile}.jpg")
    for original in directory.glob("*.jpg"):
        assert_packaged_resource(app_spec, original)


def test_android_identity_and_appearance_are_preserved(app_spec):
    assert app_spec["package.domain"] + "." + app_spec["package.name"] == "org.games.clasicgames"
    assert app_spec["title"] == "Classic games"
    assert "version" not in app_spec
    assert app_spec["version.filename"] == "%(source.dir)s/main.py"
    assert re.search(app_spec["version.regex"], (APP_DIR / "main.py").read_text()).group(1) == "1.2"
    assert app_spec["icon.filename"] == "%(source.dir)s/images/icon.png"
    assert app_spec["presplash.filename"] == "%(source.dir)s/images/splash.png"
    assert app_spec["orientation"] == "all"
    assert app_spec["fullscreen"] == "0"
    assert "android.permissions" not in app_spec


def test_android_toolchain_is_immutable_and_arm64(app_spec):
    assert app_spec["android.archs"] == "arm64-v8a"
    assert "android.arch" not in app_spec
    assert app_spec["android.api"] == "36"
    assert app_spec["android.minapi"] == app_spec["android.ndk_api"] == "24"
    assert app_spec["android.ndk"] == "28c"
    assert app_spec["p4a.url"] == "https://github.com/kivy/python-for-android.git"
    assert app_spec["p4a.branch"] == "v2026.05.09"
    assert app_spec["p4a.commit"] == "58d21141f17c889bf8585f5665921d72028f8831"
    assert not app_spec.get("p4a.source_dir")
    assert app_spec["p4a.bootstrap"] == "sdl2"
    assert app_spec.getboolean("android.skip_update")
    tools = Path.home() / ".local/share/classic-games-android"
    assert Path(app_spec["android.sdk_path"]).expanduser() == tools / "sdk"
    assert Path(app_spec["android.ndk_path"]).expanduser() == tools / "android-ndk-r28c"


def test_android_requirements_keep_runtime_pins_and_omit_host_tools(app_spec):
    requirements = spec_list(app_spec, "requirements")
    assert {"python3==3.11.14", "hostpython3==3.11.14",
            "chardet==5.2.0", "six==1.17.0", "setuptools==79.0.1"} <= requirements
    assert all("==" in requirement for requirement in requirements)
    assert not any("master" in requirement or "://" in requirement for requirement in requirements)
    names = {requirement.split("==")[0].lower() for requirement in requirements}
    assert "sdl2_ttf" not in names
    assert not {"pytest", "buildozer", "cython", "pip", "meson", "ninja", "build", "wheel"} & names
    # Compare shared runtime pins with the real lock instead of a duplicate spec fixture.
    lock = tomllib.loads((APP_DIR.parents[1] / "uv.lock").read_text())
    versions = {package["name"]: package["version"] for package in lock["package"]}
    shared = {"kivy", "kivymd", "pillow", "pycairo", "materialyoucolor",
              "asynckivy", "asyncgui", "materialshapes", "kivy-garden", "docutils",
              "pygments", "filetype", "requests", "urllib3", "idna", "certifi",
              "charset-normalizer"}
    assert {f"{name}=={versions[name]}" for name in shared} <= requirements


def test_installed_kivymd_resource_is_available():
    kivymd = distribution("kivymd")
    resource = kivymd.locate_file("kivymd/uix/label/label.kv")

    assert resource.is_file()
    assert sum(str(file).endswith(".kv") for file in kivymd.files or []) > 0
