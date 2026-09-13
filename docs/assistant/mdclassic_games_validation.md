# MDclassic_games validation record

Phase / task: Phase 1 - Reproducible desktop environment
Status: passed
Files changed: `.gitignore`, `.python-version`, `pyproject.toml`, `uv.lock`, `README.md`, `docs/getting-started.md`, `docs/assistant/mdclassic_games_validation.md`
Environment: Linux 7.2.3-2-MANJARO x86_64; CPython 3.11.14; uv 0.12.10; Kivy 2.3.1; KivyMD 1.2.0; Pillow 12.3.0; materialyoucolor 3.0.4
Command and working directory: repository root unless noted below
Expected / observed result: `uv python install 3.11` provisioned CPython 3.11.14. `uv add --bounds exact pillow materialyoucolor` selected `pillow==12.3.0` and `materialyoucolor==3.0.4`; `uv add --group dev --bounds exact pytest` selected `pytest==9.1.1`. KivyMD metadata requires Pillow; materialyoucolor metadata requires Pillow. Both remain explicit runtime dependencies.
Manual checks: FAIL - startup attempted from `source/MDclassic_games`; the window, OpenGL, and SDL2 audio providers initialized, but the application did not construct. `main.ini` was unchanged.
Automated checks: `uv lock --check` PASS; `uv sync --locked --group dev` PASS; `uv pip check` PASS; `uv run --locked --group dev pytest --version` reported pytest 9.1.1. No test discovery was run in Phase 1.
Failure: `FileNotFoundError: .../site-packages/kivymd/uix/label/label.kv` while importing `kivymd.uix.snackbar.Snackbar` from `source/MDclassic_games/main.py:21`. `importlib.metadata.files('kivymd')` confirms the installed distribution does not contain that resource. Kivy log: `/home/oriol/.kivy/logs/kivy_26-09-13_0.txt`. Classification: Phase 2 desktop compatibility input.
Decision: Use `kivy==2.3.1` and `kivymd==1.2.0` as specified. The resolver selected exact available supporting versions compatible with Python 3.11. The generated lockfile pins packages but not the CPython patch, OS libraries, or Android SDK.
Next exact action: Phase 2 - inspect the pinned KivyMD 1.2.0 release/resource packaging and resolve the first desktop startup failure without changing the framework major or Python minor version.
