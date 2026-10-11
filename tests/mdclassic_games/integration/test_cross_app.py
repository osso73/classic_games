"""Real-widget cross-app routes, settings, and image-provider regressions."""

import pytest

from test_shell import run_shell_script


pytestmark = pytest.mark.gui

ROUTES = ["pong", "ahorcado", "memory", "fifteen", "2048", "buscaminas", "snake"]


def test_classic_purple_app_bar_and_light_controls_on_every_screen(gui_environment, tmp_path):
    run_shell_script(tmp_path, f'''
        from kivy.clock import Clock
        from kivy.lang import Builder
        from pytest import approx
        from kivy.utils import get_color_from_hex
        from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle, MDActionTopAppBarButton

        purple = get_color_from_hex("#673AB7")
        white = get_color_from_hex("#FFFFFF")
        for route in {["menu"] + ROUTES!r}:
            app.change_screen(route)
            for _ in range(4):
                Clock.tick()
            Builder.sync()
            screen = app.sm.get_screen(route)
            bar = next(widget for widget in screen.walk() if isinstance(widget, MDTopAppBar))
            # Inspect the actual canvas and rendered title/icon colors, not just theme inputs.
            background = bar.canvas.get_group("md-top-app-bar-color")
            assert len(background) == 1, route
            assert background[0].rgba == approx(purple), (route, background[0].rgba, bar.md_bg_color, bar.theme_bg_color)
            title = next(widget for widget in bar.walk() if isinstance(widget, MDTopAppBarTitle))
            assert title.color == approx(white), (route, title.color)
            buttons = [widget for widget in bar.walk() if isinstance(widget, MDActionTopAppBarButton)]
            assert buttons, route
            assert all(button.color == approx(white) for button in buttons), route
    ''')


def test_classic_purple_chips_and_dialog_button(gui_environment, tmp_path):
    run_shell_script(tmp_path, '''
        from kivy.clock import Clock
        from kivy.lang import Builder
        from kivy.utils import get_color_from_hex
        from kivymd.uix.button import MDButton, MDButtonText
        from kivymd.uix.chip import MDChip, MDChipText
        from pytest import approx

        # Assert final colors without waiting on KivyMD's theme-color animations.
        app.theme_cls.theme_style_switch_animation = False
        purple = get_color_from_hex("#673AB7")
        white = get_color_from_hex("#FFFFFF")
        for route in ["memory", "fifteen", "2048"]:
            app.change_screen(route)
            for _ in range(4):
                Clock.tick()
            Builder.sync()
            chips = [widget for widget in app.sm.get_screen(route).walk() if isinstance(widget, MDChip)]
            assert chips, route
            for chip in chips:
                assert chip.md_bg_color == approx(purple), route
                labels = [widget for widget in chip.walk() if isinstance(widget, MDChipText)]
                assert labels, route
                assert all(label.color == approx(white) for label in labels), route

        app.root.ids.my_drawer.about()
        for _ in range(4):
            Clock.tick()
        dialog = next(widget for widget in Window.children if isinstance(widget, MDDialog))
        button = next(widget for widget in dialog.walk() if isinstance(widget, MDButton))
        assert button.md_bg_color == approx(purple), ("dialog background", button.md_bg_color, button.theme_bg_color)
        label = next(widget for widget in button.walk() if isinstance(widget, MDButtonText))
        assert label.color == approx(white), ("dialog label", label.color, label.theme_text_color)
        button.dispatch("on_release")
        assert not dialog._is_open
    ''')


def test_puzzle_reference_image_scales_without_deprecated_properties(gui_environment, tmp_path):
    result = run_shell_script(tmp_path, '''
        from kivy.clock import Clock
        from kivy.graphics.texture import Texture
        from pytest import approx

        app.change_screen("fifteen")
        for _ in range(4):
            Clock.tick()
        reference = app.sm.get_screen("fifteen").ids.sample
        card = reference.children[0]
        card.texture = Texture.create(size=(20, 10))
        card.size = (200, 200)
        assert card.norm_image_size == approx([200, 100])
    ''')
    output = result.stdout + result.stderr
    assert "name=allow_stretch" not in output
    assert "name=keep_ratio" not in output


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
