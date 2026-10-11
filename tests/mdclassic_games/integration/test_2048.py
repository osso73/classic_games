"""GUI regressions for the combined application's 2048 screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_2048_script(tmp_path, body):
    """Run one 2048 scenario in a fresh Kivy process."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        import os

        from kivy.clock import Clock
        from kivy.core.window import Window

        from main import MainApp
        import game_2048.constants as constants

        app = MainApp()
        app.get_application_config = lambda: {str(config_path)!r}
        app.load_config()
        app.root = app.build()
        app.sm = app.root.ids.screen_manager
        Window.add_widget(app.root)
        app.change_screen("2048")

        screen = app.sm.get_screen("2048")
        board = screen.ids.board
        board.num_pixels = 400
        board.mute = True
        constants.MOVE_TILE = 0
        constants.MOVE_DURATION = 0

        def set_board(rows):
            board.start_game()
            board.add_tile = lambda: None
            for tile in board.children:
                tile.value = 0
                tile._previous = 0
                tile.merged = False
            for y, row in enumerate(rows):
                for x, value in enumerate(row):
                    tile = board.get_tile([x, y])
                    tile.value = value
                    tile._previous = value
            board.score = 0

        def board_values():
            return [
                [board.get_tile([x, y]).value for x in range(4)]
                for y in range(4)
            ]

        def move(direction):
            board.move(direction)
            for _ in range(8):
                Clock.tick()

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
def test_2048_screen_constructs_and_its_controls_start_and_change_target(gui_environment, tmp_path):
    """The KivyMD 2 screen retains interactive restart and target controls."""

    run_2048_script(
        tmp_path,
        """
        chip = next(widget for widget in screen.walk() if widget.__class__.__name__ == "MDChip")
        chip_text = next(widget for widget in chip.walk() if getattr(widget, "text", None) == "2048")
        assert chip_text.text == "2048"
        chip.dispatch("on_release")
        assert board.win_score == 256
        board.start_game()
        assert board.active_game
        assert len(board.children) == 16
        assert sum(bool(tile.value) for tile in board.children) == 2
        controls = [
            widget for widget in screen.walk()
            if widget.__class__.__name__ == "ButtonJoystick"
        ]
        assert {button.text for button in controls} == {"^", "<", "O", ">", "v"}
        set_board([[0, 2, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        next(button for button in controls if button.text == "<").dispatch("on_release")
        for _ in range(8):
            Clock.tick()
        assert board_values()[0] == [4, 0, 0, 0]
        """,
    )


@pytest.mark.gui
@pytest.mark.parametrize(
    ("direction", "initial", "expected"),
    [
        ("left", [[0, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[4, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        ("right", [[2, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        ("up", [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0]]),
        ("down", [[2, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0]], [[4, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ],
)
def test_2048_moves_and_merges_in_every_direction(gui_environment, tmp_path, direction, initial, expected):
    """Production moves compress and merge each row or column in all directions."""

    run_2048_script(
        tmp_path,
        f"""
        set_board({initial!r})
        move({direction!r})
        assert board_values() == {expected!r}, board_values()
        assert board.score == 4
        """,
    )


@pytest.mark.gui
def test_2048_merges_each_tile_once_and_records_the_score(gui_environment, tmp_path):
    """Four equal tiles become two pairs before spawning a new tile."""

    run_2048_script(
        tmp_path,
        """
        set_board([[2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        move("left")
        assert board_values() == [[4, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], board_values()
        assert board.score == 8, board.score
        """,
    )


@pytest.mark.gui
def test_2048_no_op_does_not_spawn_and_undo_restores_board_and_score(gui_environment, tmp_path):
    """A blocked move is inert, while undo restores the saved move state."""

    run_2048_script(
        tmp_path,
        """
        set_board([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        spawned = []
        board.add_tile = lambda: spawned.append(True)
        before = board_values()
        move("left")
        assert board_values() == before
        assert spawned == []
        assert len(board.last_move) == 16
        assert sorted(tile["value"] for tile in board.last_move) == [0] * 15 + [2]

        set_board([[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        before = board_values()
        move("left")
        assert board.score == 4
        board.back_button()
        assert board_values() == before
        assert board.score == 0
        """,
    )
