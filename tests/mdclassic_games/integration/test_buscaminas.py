"""GUI regressions for the combined application's Buscaminas screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_buscaminas_script(tmp_path, body):
    """Run one Buscaminas scenario in a fresh Kivy process."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        import os

        from main import MainApp
        from kivy.config import Config
        from kivy.clock import Clock
        from kivy.core.window import Window
        from buscaminas.area import Area

        app = MainApp()
        app.get_application_config = lambda: {str(config_path)!r}
        app.load_config()
        app.root = app.build()
        app.sm = app.root.ids.screen_manager
        Window.add_widget(app.root)
        app.change_screen("buscaminas")
        for _ in range(4):
            Clock.tick()

        screen = app.sm.get_screen("buscaminas")
        field = screen.ids.field
        field.mute = True

        def set_field(columns, rows, mines):
            field.clear_widgets()
            field.cols = columns
            field.rows = rows
            field.mines = len(mines)
            field.game_active = True
            for y in range(rows):
                for x in range(columns):
                    field.add_widget(Area(location=[x, y], value=9 if (x, y) in mines else 0))
            field.find_adjacent_mines()

        def area_at(x, y):
            return next(area for area in field.children if area.location == [x, y])

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


@pytest.mark.gui
def test_buscaminas_disables_mouse_multitouch_markers(gui_environment, tmp_path):
    """Right-click remains available for flags without red synthetic touches."""

    run_buscaminas_script(
        tmp_path,
        """
        assert Config.get("input", "mouse") == "mouse,disable_multitouch"
        """,
    )


@pytest.mark.gui
def test_buscaminas_screen_constructs_and_toolbar_starts_a_new_board(gui_environment, tmp_path):
    """The real screen retains its board and interactive toolbar controls."""

    run_buscaminas_script(
        tmp_path,
        """
        field.start_game()
        assert field.game_active, field.game_active
        assert len(field.children) == 81, len(field.children)
        assert sum(area.value == 9 for area in field.children) == 10, [area.value for area in field.children]

        controls = [
            widget for widget in screen.walk()
            if getattr(widget, "icon", None) in {
                "menu", "play-circle-outline", "bomb", "numeric-1-box", "volume-high", "help-circle-outline"
            }
        ]
        assert {button.icon for button in controls} == {
            "menu", "play-circle-outline", "bomb", "numeric-1-box", "volume-high", "help-circle-outline"
        }, [button.icon for button in controls]
        level_button = next(button for button in controls if button.icon == "numeric-1-box")
        mode_button = next(button for button in controls if button.icon == "bomb")
        level_button.dispatch("on_release")
        assert field.level == 2
        assert level_button.icon == "numeric-2-box"
        mode_button.dispatch("on_release")
        assert field.mode == "flag"
        assert mode_button.icon == "flag"
        """,
    )


@pytest.mark.gui
def test_buscaminas_counts_adjacent_mines_at_corners_and_edges(gui_environment, tmp_path):
    """A fixed corner mine produces the expected edge and diagonal counts."""

    run_buscaminas_script(
        tmp_path,
        """
        set_field(3, 3, {(0, 0)})
        assert area_at(0, 0).value == 9
        assert area_at(1, 0).value == 1
        assert area_at(0, 1).value == 1
        assert area_at(1, 1).value == 1
        assert area_at(2, 0).value == 0
        assert area_at(2, 2).value == 0
        """,
    )


@pytest.mark.gui
def test_buscaminas_reveals_connected_safe_cells(gui_environment, tmp_path):
    """Revealing a zero recursively reveals its safe connected region."""

    run_buscaminas_script(
        tmp_path,
        """
        set_field(3, 3, {(0, 0)})
        area_at(2, 2).uncover()
        assert not area_at(0, 0).uncovered
        assert all(
            area.uncovered for area in field.children if area.value != 9
        )
        """,
    )


@pytest.mark.gui
def test_buscaminas_flag_mode_prevents_reveal_and_updates_counter(gui_environment, tmp_path):
    """Flag mode changes a covered tile without revealing it."""

    run_buscaminas_script(
        tmp_path,
        """
        set_field(2, 2, {(0, 0)})
        mine = area_at(0, 0)
        field.mode = "flag"
        mine.switch_flag()
        assert mine.flag
        assert not mine.uncovered
        assert field.mines == 0
        mine.uncover()
        assert not mine.uncovered
        mine.switch_flag()
        assert not mine.flag
        assert field.mines == 1
        """,
    )


@pytest.mark.gui
def test_buscaminas_reports_mine_and_cleared_board_outcomes(gui_environment, tmp_path):
    """Mine hits lose the board, while safe cells plus flags win it."""

    run_buscaminas_script(
        tmp_path,
        """
        set_field(2, 2, {(0, 0)})
        area_at(0, 0).uncover()
        assert not field.game_active
        assert screen.ids.start_button.button_face.endswith("lost.png")
        assert all(area.uncovered for area in field.children if area.value == 9)

        set_field(2, 2, {(0, 0)})
        for area in field.children:
            if area.value != 9:
                area.uncover()
        mine = area_at(0, 0)
        mine.switch_flag()
        assert not field.game_active
        assert screen.ids.start_button.button_face.endswith("won.png")
        """,
    )
