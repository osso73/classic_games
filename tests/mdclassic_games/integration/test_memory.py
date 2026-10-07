"""GUI regressions for the combined application's Memory screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_memory_script(tmp_path, body):
    """Run one Memory scenario in a fresh Kivy process."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        import os

        from kivy.core.window import Window

        from main import MainApp

        app = MainApp()
        app.get_application_config = lambda: {str(config_path)!r}
        app.load_config()
        app.root = app.build()
        app.sm = app.root.ids.screen_manager
        Window.add_widget(app.root)
        app.change_screen("memory")

        screen = app.sm.get_screen("memory")
        mat = screen.ids.mat_area
        mat.mute = True

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
def test_memory_start_creates_matching_pairs(gui_environment, tmp_path):
    """Starting a game creates two cards for every selected image."""

    run_memory_script(
        tmp_path,
        """
        from collections import Counter

        mat.num_pairs = 4
        mat.start_game()
        assert len(mat.children) == 8
        assert all(count == 2 for count in Counter(card.image for card in mat.children).values())
        assert mat.moves == 0
        assert mat.columns == 2
        """,
    )


@pytest.mark.gui
def test_memory_only_cycles_complete_themes_at_the_largest_level(gui_environment, tmp_path):
    """Every selectable theme supports the configured maximum of 20 pairs."""

    run_memory_script(
        tmp_path,
        """
        assert set(mat.theme_list) == {
            "animals", "cartoons", "food", "misc", "starwars", "technology"
        }
        mat.num_pairs = 20
        for theme in mat.theme_list:
            mat.current_theme = theme
            mat.start_game()
            assert len(mat.children) == 40
        """,
    )


@pytest.mark.gui
def test_memory_uses_a_complete_theme_when_config_is_stale(gui_environment, tmp_path):
    """A removed legacy theme in config does not prevent a game from starting."""

    run_memory_script(
        tmp_path,
        """
        from memory.mat import Mat

        app.config.set("Memory", "theme", "varios")
        stale_mat = Mat()
        stale_mat.mute = True
        assert stale_mat.current_theme in stale_mat.theme_list
        stale_mat.start_game()
        assert len(stale_mat.children) == stale_mat.num_pairs * 2

        assert mat.current_theme in mat.theme_list
        mat.current_theme = "varios"
        mat.change_theme()
        assert mat.current_theme == mat.theme_list[0]
        """,
    )


@pytest.mark.gui
def test_memory_match_stays_revealed_and_counts_one_move(gui_environment, tmp_path):
    """A matching pair remains face-up and clears the pending selection."""

    run_memory_script(
        tmp_path,
        """
        mat.start_game()
        first, second = mat.children[:2]
        second.image = first.image
        first.turn()
        second.turn()
        mat.current_cards = [first, second]
        assert first.shown and second.shown
        assert mat.current_cards == []
        assert mat.moves == 1
        """,
    )


@pytest.mark.gui
def test_memory_mismatch_hides_cards_after_resolution(gui_environment, tmp_path):
    """A nonmatching pair returns face-down after its scheduled resolution."""

    run_memory_script(
        tmp_path,
        """
        import memory.mat as mat_module

        mat.start_game()
        first, second = mat.children[:2]
        second.image = "not-" + first.image
        mat_module.sleep = lambda delay: None
        first.turn()
        second.turn()
        mat.current_cards = [first, second]
        assert not first.shown and not second.shown
        assert mat.current_cards == []
        assert mat.moves == 1
        """,
    )


@pytest.mark.gui
def test_memory_completed_cards_do_not_count_again(gui_environment, tmp_path):
    """Already resolved cards cannot create another move or match."""

    run_memory_script(
        tmp_path,
        """
        mat.start_game()
        first, second = mat.children[:2]
        second.image = first.image
        first.turn()
        second.turn()
        mat.current_cards = [first, second]
        first.click()
        second.click()
        assert first.shown and second.shown
        assert mat.current_cards == []
        assert mat.moves == 1
        """,
    )


@pytest.mark.gui
def test_memory_completion_reports_the_finished_board(gui_environment, tmp_path):
    """A board with every card revealed reports game completion once."""

    run_memory_script(
        tmp_path,
        """
        import memory.mat as mat_module

        messages = []
        mat_module.PopupButton = lambda **kwargs: messages.append(kwargs)
        mat.start_game()
        for card in mat.children:
            card.shown = True
        mat.check_end()
        assert messages == [{"title": "End", "msg": "Well done!\\nYou found all pairs"}]
        """,
    )


@pytest.mark.gui
def test_memory_settings_update_existing_mat_and_config(gui_environment, tmp_path):
    """Theme and level settings update the real mat and isolated config."""

    run_memory_script(
        tmp_path,
        """
        screen.config_change(app.config, "Memory", "theme", "cartoons")
        screen.config_change(app.config, "Memory", "level", "21")
        assert mat.current_theme == "cartoons"
        assert mat.num_pairs == 20
        assert app.config.get("Memory", "level") == "20"
        assert os.path.isfile(app.get_application_config())
        """,
    )
