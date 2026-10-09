"""GUI regressions for the combined application's shell."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_shell_script(tmp_path, body):
    """Run one shell scenario in a fresh Kivy process."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        import os

        from kivy.core.window import Window
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

        import drawer as drawer_module
        from main import MainApp, TempMsg
        from menu import MyTile

        MainApp.get_application_config = lambda self: {str(config_path)!r}
        app = MainApp()
        app.load_config()
        app.root = app.build()
        app.sm = app.root.ids.screen_manager
        Window.add_widget(app.root)

        {textwrap.indent(textwrap.dedent(body), '        ')}

        # Kivy's global window and Clock state are not reliably reset in-process.
        os._exit(0)
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        cwd=os.getcwd(),
        env=os.environ.copy(),
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return result


@pytest.mark.gui
def test_shell_menu_tiles_route_and_render_images(gui_environment, tmp_path):
    """The real menu exposes every combined-app screen route and image."""

    run_shell_script(
        tmp_path,
        """
        menu = app.sm.get_screen("menu")
        tiles = [widget for widget in menu.walk() if isinstance(widget, MyTile)]
        assert [tile.screen for tile in tiles] == [
            "pong", "ahorcado", "memory", "fifteen", "2048", "buscaminas", "snake"
        ]
        assert all(tile._image.source == tile.source for tile in tiles)
        """,
    )


@pytest.mark.gui
def test_shell_drawer_state_and_screen_property(gui_environment, tmp_path):
    """The drawer has an observable initial route and accepts open/close actions."""

    run_shell_script(
        tmp_path,
        """
        drawer = app.root.ids.my_drawer
        assert drawer.screen == "menu"
        drawer.set_state("open")
        drawer.set_state("close")
        """,
    )


@pytest.mark.gui
def test_shell_loading_snackbar_constructs_and_dismisses(gui_environment, tmp_path):
    """The migrated snackbar retains loading text and opens without an FBO error."""

    run_shell_script(
        tmp_path,
        """
        assert issubclass(TempMsg, MDSnackbar)
        snackbar = TempMsg(text="Loading pong...")
        assert any(
            isinstance(widget, MDSnackbarText) and widget.text == "Loading pong..."
            for widget in snackbar.ids.label_container.children
        )
        snackbar.open()
        snackbar.dismiss()
        """,
    )


@pytest.mark.gui
def test_shell_help_requests_existing_url(gui_environment, tmp_path):
    """Help delegates to the existing public documentation URL."""

    run_shell_script(
        tmp_path,
        """
        requested_urls = []
        drawer_module.webbrowser.open = requested_urls.append
        app.root.ids.my_drawer.open_help()
        assert requested_urls == [
            "https://osso73.github.io/classic_games/games/classic_games/"
        ]
        """,
    )


@pytest.mark.gui
def test_shell_about_dialog_constructs_and_dismisses(gui_environment, tmp_path):
    """About builds the real KivyMD dialog and retains its CLOSE behavior."""

    run_shell_script(
        tmp_path,
        """
        app.root.ids.my_drawer.about()
        dialog = next(
            widget for widget in Window.children if isinstance(widget, MDDialog)
        )
        from kivymd.uix.button import MDButton, MDButtonText
        texts = [getattr(widget, "text", "") for widget in dialog.walk()]
        assert any(str(app.version) in text for text in texts)
        close = next(widget for widget in dialog.walk()
                     if isinstance(widget, MDButton)
                     and any(isinstance(child, MDButtonText) and child.text == "CLOSE"
                             for child in widget.walk()))
        close.dispatch("on_release")
        assert not dialog._is_open
        """,
    )


@pytest.mark.gui
def test_shell_uses_temporary_config(gui_environment, tmp_path):
    """Shell construction writes only the subprocess's temporary configuration."""

    run_shell_script(
        tmp_path,
        """
        assert os.path.isfile(app.get_application_config())
        """,
    )


@pytest.mark.gui
def test_shell_startup_preloads_audio(gui_environment, tmp_path):
    """Start the real event loop and verify that audio initialization completes."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        from kivy.clock import Clock

        from main import MainApp

        app = MainApp()
        app.get_application_config = lambda: {str(config_path)!r}
        requested = []
        def verify_startup(dt):
            assert len(app.sounds) == 15
            assert all(sound is not None for sound in app.sounds.values())
            app.sounds["bye.ogg"].play = lambda: requested.append("bye")
            app.play("bye")
            app.change_screen("pong")
            app.stop()
        original_start = app.on_start
        def start():
            original_start()
            Clock.schedule_once(verify_startup)
        app.on_start = start
        app.run()

        assert "bye.ogg" in app.sounds
        assert len(app.sounds) == 15
        assert app.sm.has_screen("pong")
        assert requested == ["bye"]
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        cwd=os.getcwd(),
        env=os.environ.copy(),
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
