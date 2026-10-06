"""GUI regressions for the combined application's Ahorcado screen."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_ahorcado_script(tmp_path, body):
    """Run one Ahorcado scenario in a fresh Kivy process."""

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
        app.change_screen("ahorcado")

        screen = app.sm.get_screen("ahorcado")
        screen.mute = True
        word = screen.target_word

        def set_word(screen, value):
            screen.target_word.word = value
            screen.reset_game()

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
def test_ahorcado_correct_letters_reveal_every_occurrence_and_win(gui_environment, tmp_path):
    """Correct Spanish input reveals all matching letters and completes the word."""

    run_ahorcado_script(
        tmp_path,
        """
        set_word(screen, "AÑO")
        screen.check_letter("A")
        assert word.current == "A--"
        screen.check_letter("Ñ")
        assert word.current == "AÑ-"
        screen.check_letter("O")
        assert word.current == "AÑO"
        assert screen.good_letters == "AÑO"
        assert not screen.active
        """,
    )


@pytest.mark.gui
def test_ahorcado_wrong_repeated_and_invalid_letters(gui_environment, tmp_path):
    """Only new valid wrong letters advance the failure state."""

    run_ahorcado_script(
        tmp_path,
        """
        set_word(screen, "CASA")
        screen.check_letter("Z")
        assert screen.num_errors == 1
        assert screen.failed_letters == "Z"
        assert screen.errors.error_string == "Z_________"
        assert screen.drawing.status == "ADDDDDDDDD"
        screen.check_letter("Z")
        screen.check_letter("?")
        assert screen.num_errors == 1
        assert screen.failed_letters == "Z"
        """,
    )


@pytest.mark.gui
def test_ahorcado_tenth_wrong_letter_ends_the_game(gui_environment, tmp_path):
    """Ten distinct wrong letters reveal the full drawing and end a game."""

    run_ahorcado_script(
        tmp_path,
        """
        set_word(screen, "A")
        for letter in "BCDEFGHIJK":
            screen.check_letter(letter)
        assert screen.num_errors == 10
        assert screen.failed_letters == "BCDEFGHIJK"
        assert screen.errors.error_string == "BCDEFGHIJK"
        assert screen.drawing.status == "A" * 10
        assert word.current == "A"
        assert not screen.active
        """,
    )


@pytest.mark.gui
def test_ahorcado_keyboard_and_hint_use_the_current_screen(gui_environment, tmp_path):
    """Keyboard keys and one deterministic hint submit letters through game logic."""

    run_ahorcado_script(
        tmp_path,
        """
        import ahorcado.screen as screen_module

        set_word(screen, "CASA")
        key_a = next(key for key in screen.keyboard.children if key.letter == "A")
        key_a.push()
        assert key_a.disabled
        assert word.current == "-A-A"

        screen_module.choice = lambda letters: "C"
        screen.give_hint()
        assert word.current == "CA-A"
        assert not screen.allow_hint
        """,
    )


@pytest.mark.gui
def test_ahorcado_settings_update_keyboard_and_man(gui_environment, tmp_path):
    """Keyboard and man settings update existing widgets and isolated config."""

    run_ahorcado_script(
        tmp_path,
        """
        screen.config_change(app.config, "Ahorcado", "keyboard", "keyboard2")
        screen.config_change(app.config, "Ahorcado", "man", "man2")
        assert all("ahorcado/images/keyboard2/" in key.skin for key in screen.keyboard.children)
        assert screen.drawing.skin == 2
        assert os.path.isfile(app.get_application_config())
        """,
    )
