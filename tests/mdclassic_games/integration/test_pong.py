"""GUI regressions for the combined application's Pong screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_pong_script(tmp_path, body):
    """Run one Pong scenario in a fresh Kivy process."""

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
        app.change_screen("pong")

        screen = app.sm.get_screen("pong")
        board = screen.ids.pong
        board.pos = (0, 0)
        board.size = (800, 600)
        ball = board.ball
        left = board.player1
        right = board.player2

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
def test_pong_start_and_serve(gui_environment, tmp_path):
    """Starting Pong resets scores and serves from the board centre."""

    run_pong_script(
        tmp_path,
        """
        board.start_game()
        assert board.active
        assert (left.score, right.score) == (0, 0)
        assert ball.center == board.center
        assert tuple(ball.velocity) == (10, 0)
        """,
    )


@pytest.mark.gui
def test_pong_scores_and_reserves(gui_environment, tmp_path):
    """A ball leaving either side scores once and starts a new serve."""

    run_pong_script(
        tmp_path,
        """
        board.start_game()
        ball.x = -20
        ball.velocity = (-1, 0)
        board.update()
        assert (left.score, right.score) == (0, 1)
        assert ball.center == board.center
        assert tuple(ball.velocity) == (10, 0)

        ball.x = board.width + 20
        ball.velocity = (1, 0)
        board.update()
        assert (left.score, right.score) == (1, 1)
        assert ball.center == board.center
        assert tuple(ball.velocity) == (-10, 0)
        """,
    )


@pytest.mark.gui
def test_pong_wall_and_paddle_collisions(gui_environment, tmp_path):
    """Walls reverse vertical movement and paddles reverse horizontal movement."""

    run_pong_script(
        tmp_path,
        """
        board.start_game()
        ball.pos = (board.center_x, -1)
        ball.velocity = (1, -3)
        board.update()
        assert ball.velocity_y == 3

        ball.center = left.center
        ball.velocity = (-5, 0)
        ball.max_vel = 50
        board.update()
        assert ball.velocity_x == 5.5
        """,
    )


@pytest.mark.gui
def test_pong_speed_limit(gui_environment, tmp_path):
    """A paddle bounce cannot increase speed beyond the configured limit."""

    run_pong_script(
        tmp_path,
        """
        ball.velocity = (10, 0)
        ball.max_vel = 10
        ball.increase_velocity((5, 0))
        assert tuple(ball.velocity) == (5, 0)
        """,
    )


@pytest.mark.gui
def test_pong_pause_control(gui_environment, tmp_path):
    """The real app-bar pause action toggles state and its icon."""

    run_pong_script(
        tmp_path,
        """
        board.start_game()
        pause_control = screen.ids.pause_control
        pause_control.dispatch("on_release")
        assert not board.active
        assert pause_control.icon == "play"
        pause_control.dispatch("on_release")
        assert board.active
        assert pause_control.icon == "pause"
        """,
    )


@pytest.mark.gui
def test_pong_settings_apply_to_board(gui_environment, tmp_path):
    """Pong settings update the existing board and persist in isolated config."""

    run_pong_script(
        tmp_path,
        """
        screen.config_change(app.config, "Pong", "speed", "12")
        screen.config_change(app.config, "Pong", "max-speed", "30")
        screen.config_change(app.config, "Pong", "skin", "tennis")
        assert board.initial_vel == 12
        assert ball.max_vel == 30
        assert ball.source.endswith("pong/images/tennis/ball.gif")
        assert left.source.endswith("pong/images/tennis/paddle.gif")
        assert right.source.endswith("pong/images/tennis/paddle.gif")
        assert os.path.isfile(app.get_application_config())
        """,
    )
