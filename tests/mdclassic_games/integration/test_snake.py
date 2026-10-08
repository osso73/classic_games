"""GUI regressions for the combined application's Snake screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_snake_script(tmp_path, body):
    """Run one Snake scenario in a fresh Kivy process."""

    config_path = tmp_path / "main.ini"
    script = textwrap.dedent(
        f"""
        import os

        from kivy.clock import Clock
        from kivy.core.window import Window
        from main import MainApp
        from snake.grid_elements import Wall

        app = MainApp()
        app.get_application_config = lambda: {str(config_path)!r}
        app.load_config()
        app.root = app.build()
        app.sm = app.root.ids.screen_manager
        Window.add_widget(app.root)
        app.change_screen("snake")
        for _ in range(4):
            Clock.tick()

        screen = app.sm.get_screen("snake")
        game = screen.ids.game
        game.mute = True

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
def test_snake_screen_constructs_and_toolbar_start_pause_controls_work(gui_environment, tmp_path):
    """The KivyMD 2 screen keeps its progress indicator and real toolbar actions."""

    run_snake_script(
        tmp_path,
        """
        assert next(widget for widget in screen.walk() if widget.__class__.__name__ == "MDLinearProgressIndicator")
        controls = [widget for widget in screen.walk() if getattr(widget, "icon", None)]
        start = next(button for button in controls if button.icon == "play-circle-outline")
        pause = next(button for button in controls if button.icon == "pause")
        start.dispatch("on_release")
        assert game.active
        assert len(game.snake_parts) == 3
        pause.dispatch("on_release")
        assert game.pause
        assert pause.icon == "play"
        pause.dispatch("on_release")
        assert not game.pause
        assert pause.icon == "pause"
        """,
    )


@pytest.mark.gui
def test_snake_moves_and_rejects_an_immediate_reverse_turn(gui_environment, tmp_path):
    """A running snake advances one grid cell and cannot turn back into itself."""

    run_snake_script(
        tmp_path,
        """
        game.start_game()
        game.move_x, game.move_y = 1, 0
        head = game.snake_parts[0]
        head.pos_nm = [4, 4]
        game.snake_parts[1].pos_nm = [3, 4]
        game.snake_parts[2].pos_nm = [2, 4]
        game.food.pos_nm = [10, 10]
        game.change_direction("LEFT")
        assert (game.move_x, game.move_y) == (1, 0)
        game.update()
        assert head.pos_nm == [5, 4]
        assert game.snake_parts[1].pos_nm == [4, 4]
        """,
    )


@pytest.mark.gui
def test_snake_eating_food_grows_updates_score_and_respawns_food(gui_environment, tmp_path):
    """Eating uses the production food metadata to grow, score, and respawn."""

    run_snake_script(
        tmp_path,
        """
        game.start_game()
        game.move_x, game.move_y = 1, 0
        head = game.snake_parts[0]
        head.pos_nm = [4, 4]
        game.snake_parts[1].pos_nm = [3, 4]
        game.snake_parts[2].pos_nm = [2, 4]
        game.food.current = {"score": 3, "length": 1, "speed": 1}
        game.food.pos_nm = [5, 4]
        game.food.spawn = lambda occupied: setattr(game.food, "pos_nm", [10, 10])
        game.update()
        assert game.score == 3
        assert len(game.snake_parts) == 4
        assert game.food.pos_nm == [10, 10]
        """,
    )


@pytest.mark.gui
def test_snake_wall_and_body_collisions_end_the_game(gui_environment, tmp_path):
    """Both relevant collision types stop the real running game."""

    run_snake_script(
        tmp_path,
        """
        game.start_game()
        game.move_x, game.move_y = 1, 0
        head = game.snake_parts[0]
        head.pos_nm = [4, 4]
        game.snake_parts[1].pos_nm = [5, 4]
        game.snake_parts[2].pos_nm = [3, 4]
        game.food.pos_nm = [10, 10]
        game.update()
        assert not game.active
        assert head.crashed

        game.start_game()
        game.move_x, game.move_y = 1, 0
        head = game.snake_parts[0]
        head.pos_nm = [4, 4]
        game.snake_parts[1].pos_nm = [3, 4]
        game.snake_parts[2].pos_nm = [2, 4]
        wall = Wall()
        game.add_widget(wall)
        wall.pos_nm = [5, 4]
        game.wall.append(wall)
        game.food.pos_nm = [10, 10]
        game.update()
        assert not game.active
        assert head.crashed
        """,
    )


@pytest.mark.gui
def test_snake_restart_and_settings_update_the_existing_game(gui_environment, tmp_path):
    """Restart resets state and Snake settings update the lazily created board."""

    run_snake_script(
        tmp_path,
        """
        game.start_game()
        game.score = 9
        game.start_game()
        assert game.score == 0
        assert game.active
        screen.config_change(app.config, "Snake", "speed", "2")
        assert game.speed_factor == 2
        screen.config_change(app.config, "Snake", "mode", "0")
        assert not game.story
        screen.config_change(app.config, "Snake", "level_start", "99")
        assert app.config.getint("Snake", "level_start") == 12
        """,
    )
