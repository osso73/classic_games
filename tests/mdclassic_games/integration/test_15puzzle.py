"""GUI regressions for the combined application's 15 Puzzle screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_fifteen_script(tmp_path, body):
    """Run one 15 Puzzle scenario in a fresh Kivy process."""

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
        app.change_screen("fifteen")

        screen = app.sm.get_screen("fifteen")
        puzzle = screen.ids.puzzle
        sample = screen.ids.sample
        screen.play = lambda sound: None

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
def test_fifteen_starts_a_solvable_board_with_every_tile(gui_environment, tmp_path):
    """Starting the real screen creates one solvable tile set at each level."""

    run_fifteen_script(
        tmp_path,
        """
        for level in (1, 2, 3):
            sample.change_size(level)
            puzzle.start_game()
            tiles = [card.name for card in puzzle.children]
            assert sorted(tiles, key=lambda name: (name == '', int(name or 0))) == [
                *(str(number) for number in range(1, sample.board_size ** 2)), ''
            ]
            assert puzzle.is_solvable(tiles)
        """,
    )


@pytest.mark.gui
def test_fifteen_uses_only_complete_themes_and_repairs_stale_config(gui_environment, tmp_path):
    """Empty legacy theme directories cannot be selected or break future starts."""

    run_fifteen_script(
        tmp_path,
        """
        from game_15puzzle.sample import Sample

        expected_themes = [
            "bike", "blonde", "breakfast", "bulb", "carnival", "eve", "landscape",
            "milky_way", "money", "numbers", "ship", "shore", "squirrel", "tree",
        ]
        assert sample.available_themes() == expected_themes
        app.config.set("fifteen", "theme", "elefante")
        stale_sample = Sample()
        assert stale_sample.theme == expected_themes[0]
        assert app.config.get("fifteen", "theme") == expected_themes[0]
        """,
    )


@pytest.mark.gui
def test_fifteen_moves_only_an_adjacent_tile(gui_environment, tmp_path):
    """An adjacent tile occupies the blank space and increments the score."""

    run_fifteen_script(
        tmp_path,
        """
        sample.change_size(1)
        puzzle.start_game()
        empty = puzzle.find_empty()
        tile = next(
            card for card in puzzle.children
            if card.name and abs(card.position[0] - empty.position[0])
            + abs(card.position[1] - empty.position[1]) == 1
        )
        old_empty_position = list(empty.position)
        old_tile_position = list(tile.position)
        tile.move()
        assert tile.position == old_empty_position
        assert empty.position == old_tile_position
        assert puzzle.moves == 1
        """,
    )


@pytest.mark.gui
def test_fifteen_ignores_a_nonadjacent_tile(gui_environment, tmp_path):
    """A nonadjacent tile does not alter the board or move count."""

    run_fifteen_script(
        tmp_path,
        """
        sample.change_size(1)
        puzzle.start_game()
        empty = puzzle.find_empty()
        tile = next(
            card for card in puzzle.children
            if card.name and abs(card.position[0] - empty.position[0])
            + abs(card.position[1] - empty.position[1]) > 1
        )
        before = [(card.name, list(card.position)) for card in puzzle.children]
        tile.move()
        assert [(card.name, list(card.position)) for card in puzzle.children] == before
        assert puzzle.moves == 0
        """,
    )


@pytest.mark.gui
def test_fifteen_recognizes_a_solved_board(gui_environment, tmp_path):
    """The production solved-state check accepts the ordered board."""

    run_fifteen_script(
        tmp_path,
        """
        sample.change_size(1)
        puzzle.start_game()
        for card in puzzle.children:
            number = int(card.name) if card.name else sample.board_size ** 2
            card.position = [
                (number - 1) % sample.board_size,
                (number - 1) // sample.board_size,
            ]
        assert puzzle.check_win()
        """,
    )


@pytest.mark.gui
def test_fifteen_settings_update_the_existing_sample_and_config(gui_environment, tmp_path):
    """Theme and level settings update the constructed screen and temp config."""

    run_fifteen_script(
        tmp_path,
        """
        app.config.set("fifteen", "level", "3")
        screen.config_change(app.config, "fifteen", "level", "3")
        app.config.set("fifteen", "theme", "tree")
        screen.config_change(app.config, "fifteen", "theme", "tree")
        assert sample.board_size == 5
        assert sample.theme == "tree"
        assert app.config.get("fifteen", "level") == "3"
        assert app.config.get("fifteen", "theme") == "tree"
        assert os.path.isfile(app.get_application_config())
        """,
    )
