"""GUI regressions for the combined application's shell."""

import os
import subprocess
import sys
import textwrap

import pytest


@pytest.mark.gui
def test_shell_builds_with_isolated_config(gui_environment, tmp_path):
    """Build the real shell and exercise its migrated KivyMD components."""

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

        menu = app.sm.get_screen("menu")
        tiles = [widget for widget in menu.walk() if isinstance(widget, MyTile)]
        assert [tile.screen for tile in tiles] == [
            "pong", "ahorcado", "memory", "fifteen", "2048", "buscaminas", "snake"
        ]
        assert all(tile._image.source == tile.source for tile in tiles)

        drawer = app.root.ids.my_drawer
        assert drawer.screen == "menu"
        drawer.set_state("open")
        drawer.set_state("close")

        assert issubclass(TempMsg, MDSnackbar)
        snackbar = TempMsg(text="Loading pong...")
        assert any(
            isinstance(widget, MDSnackbarText) and widget.text == "Loading pong..."
            for widget in snackbar.ids.label_container.children
        )
        snackbar.open()
        snackbar.dismiss()

        requested_urls = []
        drawer_module.webbrowser.open = requested_urls.append
        drawer.open_help()
        assert requested_urls == [
            "https://osso73.github.io/classic_games/games/classic_games/"
        ]

        drawer.about()
        dialog = next(
            widget for widget in Window.children if isinstance(widget, MDDialog)
        )
        dialog.dismiss()

        assert os.path.isfile({str(config_path)!r})

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
        Clock.schedule_once(lambda dt: app.change_screen("pong"), 0.5)
        Clock.schedule_once(lambda dt: app.play("bye"), 1)
        Clock.schedule_once(app.stop, 2)
        app.run()

        assert "bye.ogg" in app.sounds
        assert len(app.sounds) == 15
        assert app.sm.has_screen("pong")
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
