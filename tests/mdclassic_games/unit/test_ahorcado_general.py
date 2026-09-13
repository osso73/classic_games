from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import ahorcado.general as general
from ahorcado.general import replace_letter


@pytest.mark.parametrize(
    ("original", "position", "letter", "expected"),
    [
        ("POTATO", 2, "!", "PO!ATO"),
        ("AÑO", 1, "Ñ", "AÑO"),
        ("ESTRELLA", 3, "X", "ESTXELLA"),
    ],
)
def test_replace_letter_replaces_one_character(original, position, letter, expected):
    assert replace_letter(original, position, letter) == expected


@pytest.mark.parametrize("position", [7, 18])
def test_replace_letter_rejects_positions_beyond_the_string(position):
    with pytest.raises(IndexError, match="pos > len"):
        replace_letter("POTATO", position, "!")


@pytest.mark.parametrize("letter", ["", "LL"])
def test_replace_letter_requires_exactly_one_character(letter):
    with pytest.raises(Exception, match="single character"):
        replace_letter("POTATO", 2, letter)


def test_pure_helper_import_does_not_initialize_kivy():
    app_dir = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import ahorcado.general; "
            "assert not any(name == 'kivy' or name.startswith('kivy.') for name in sys.modules)",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(app_dir)},
    )
    assert result.returncode == 0, result.stderr


def test_helper_resolves_from_the_combined_app_only():
    app_dir = Path(__file__).resolve().parents[3] / "source" / "MDclassic_games"
    assert Path(general.__file__).resolve().is_relative_to(app_dir)
