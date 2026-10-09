"""Real-widget cross-app routes, settings, and image-provider regressions."""

import pytest

from test_shell import run_shell_script


pytestmark = pytest.mark.gui

ROUTES = ["pong", "ahorcado", "memory", "fifteen", "2048", "buscaminas", "snake"]


@pytest.mark.parametrize("entry", ["tile", "drawer"])
def test_all_routes_create_once_and_reuse_screens(gui_environment, tmp_path, entry):
    run_shell_script(tmp_path, f'''
        from kivy.clock import Clock
        from kivymd.uix.list import MDListItem, MDListItemHeadlineText

        drawer = app.root.ids.my_drawer
        items = {{
            label.text: item
            for item in drawer.walk() if isinstance(item, MDListItem)
            for label in item.walk() if isinstance(label, MDListItemHeadlineText)
        }}
        tiles = {{tile.screen: tile for tile in app.sm.get_screen("menu").walk()
                 if isinstance(tile, MyTile)}}
        labels = {{"fifteen": "15 puzzle"}}
        notifications = []
        original_open = TempMsg.open
        def record_open(message):
            notifications.append(message)
            original_open(message)
        TempMsg.open = record_open
        for route in {ROUTES!r}:
            control = tiles[route] if {entry!r} == "tile" else items[labels.get(route, route)]
            control.dispatch("on_release")
            for _ in range(4):
                Clock.tick()
            screen = app.sm.get_screen(route)
            assert app.sm.current == route
            assert len(notifications) == 1
            assert any(isinstance(widget, MDSnackbarText) and "Loading" in widget.text
                       for widget in notifications[0].ids.label_container.children)
            notifications[0].dismiss()
            items["Main menu"].dispatch("on_release")
            assert app.sm.current == "menu"
            items[labels.get(route, route)].dispatch("on_release")
            assert app.sm.current == route
            assert app.sm.get_screen(route) is screen
            assert app.sm.screen_names.count(route) == 1
            assert len(notifications) == 1
            items["Main menu"].dispatch("on_release")
            notifications.clear()
        assert set(app.sm.screen_names) == set({ROUTES!r} + ["menu"])
    ''')


@pytest.mark.parametrize("section,route,key,before,after,expression", [
    ("Pong", "pong", "speed", "7", "9", "screen.ids.pong.initial_vel"),
    ("Ahorcado", "ahorcado", "man", "man2", "man1", "screen.drawing.skin"),
    ("Memory", "memory", "level", "8", "10", "screen.ids.mat_area.num_pairs"),
    ("fifteen", "fifteen", "level", "2", "3", "screen.ids.sample.board_size - 2"),
    ("Snake", "snake", "speed", "2", "3", "screen.ids.game.speed_factor"),
])
def test_settings_before_after_creation_and_reload(
    gui_environment, tmp_path, section, route, key, before, after, expression
):
    run_shell_script(tmp_path, f'''
        from kivy.clock import Clock
        from kivy.config import ConfigParser
        from kivy.uix.settings import SettingItem

        settings = app.create_settings()
        panels = list(settings.interface.content.panels.values())
        assert {{panel.title for panel in panels}} == {{"Pong", "Ahorcado", "Memory", "15 puzzle", "Snake"}}
        item = next(widget for panel in panels for widget in panel.walk()
                    if isinstance(widget, SettingItem)
                    and widget.section == {section!r} and widget.key == {key!r})
        assert not app.sm.has_screen({route!r})
        item.value = {before!r}
        for _ in range(4):
            Clock.tick()
        screen = app.sm.get_screen({route!r})
        assert {expression} == int({before!r}.removeprefix("man"))
        app.change_screen({route!r})
        item.value = {after!r}
        assert app.sm.get_screen({route!r}) is screen
        assert {expression} == int({after!r}.removeprefix("man"))
        assert app.sm.screen_names.count({route!r}) == 1
        reloaded = ConfigParser()
        reloaded.read(app.get_application_config())
        assert reloaded.get({section!r}, {key!r}) == {after!r}
    ''')
    # A fresh process must also construct the game from the persisted values.
    run_shell_script(tmp_path, f'''
        from kivy.clock import Clock
        assert app.config.get({section!r}, {key!r}) == {after!r}
        app.change_screen({route!r})
        for _ in range(4):
            Clock.tick()
        screen = app.sm.get_screen({route!r})
        assert {expression} == int({after!r}.removeprefix("man"))
    ''')


@pytest.mark.parametrize("pattern", [
    "pong/images/football/ball.gif", "memory/images/themes/cartoons/*.ico"
])
def test_runtime_image_provider_decodes_gif_and_cartoon_ico(gui_environment, tmp_path, pattern):
    run_shell_script(tmp_path, f'''
        from pathlib import Path
        from kivy.core.image import Image as CoreImage

        paths = sorted(Path(".").glob({pattern!r}))
        assert paths
        for path in paths:
            image = CoreImage(str(path))
            assert image.texture is not None, path
            assert image.width > 0 and image.height > 0, path
    ''')


def test_sound_request_and_mute_control(gui_environment, tmp_path):
    run_shell_script(tmp_path, '''
        from types import SimpleNamespace
        from kivy.clock import Clock

        requested = []
        app.sounds = {"move.ogg": SimpleNamespace(play=lambda: requested.append("move"))}
        app.change_screen("fifteen")
        for _ in range(4):
            Clock.tick()
        screen = app.sm.get_screen("fifteen")
        screen.play("move")
        assert requested == ["move"]
        mute = next(widget for widget in screen.walk() if getattr(widget, "icon", None) == "volume-high")
        mute.dispatch("on_release")
        assert mute.icon == "volume-off"
        screen.play("move")
        assert requested == ["move"]
    ''')
