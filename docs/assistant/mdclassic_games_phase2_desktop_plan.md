# MDclassic_games Phase 2 runbook - Desktop compatibility

Reviewed: 2026-09-13. Status: **not executed**.

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 1 runbook](mdclassic_games_phase1_uv_plan.md), and [the validation record](mdclassic_games_validation.md) before editing. This runbook expands master-plan Phase 2 only. It is deliberately split into small checkpoints: complete one checkpoint, review it, commit it, and only then begin the next.

Phase 2 tests the combined application on **desktop**. Do not build or install APKs during this phase. Android packaging belongs to Phase 3; one resulting APK will contain all seven games, and Android/device validation belongs to Phase 4.

## Objective and boundaries

Restore desktop compatibility with the locked Python 3.11, Kivy 2.3.1, and KivyMD 1.2.0 baseline while preserving the seven games, rules, controls, navigation, settings, sounds, and assets. Build a maintained pytest suite for the combined app before beginning Android work.

Allowed changes:

- Necessary runtime `.py` and `.kv` files under `source/MDclassic_games`, excluding `resources/`.
- Root `tests/mdclassic_games/` test suite.
- Root pytest configuration in `pyproject.toml`.
- Focused `.github/workflows/` test workflow.
- Validation records and this runbook under `docs/assistant/`.
- Dependency metadata and generated `uv.lock` only for a demonstrated, documented incompatibility.

Do not change standalone games, application version, Android packaging, `requirements.txt`, asset selection, configuration section/key names, or the app-directory launch contract. Do not use KivyMD master or 2.x to avoid adapting the pinned 1.2.0 API.

## Checkpoint workflow

Every checkpoint follows this sequence:

1. Inspect `git status --short`; preserve existing work and `source/MDclassic_games/main.ini`.
2. Make only the checkpoint's bounded changes. Add meaningful regression tests with a reproduced compatibility or behavior fix.
3. Run the checkpoint's required checks and capture the first meaningful failure rather than making speculative changes.
4. Update `docs/assistant/mdclassic_games_validation.md` using the master-plan template, including commands, working directory, test counts, observations, failure classification, and next exact action.
5. Stop for user review. Summarize changed files, behavior, checks, and open decisions.
6. Commit the fix, its tests, and its validation note together only after the user requests a commit.

A passed checkpoint is not a passed Phase 2. Do not start a dependent checkpoint until its predecessor is reviewed and committed, except for the test foundation in checkpoint 2, which is a prerequisite for all later code changes.

## Checkpoint 1 - Repair the KivyMD resource installation

### Entry condition

Phase 1 passed environment validation but recorded this startup blocker:

```text
FileNotFoundError: .../kivymd/uix/label/label.kv
```

The installed KivyMD 1.2.0 directory lacks that resource. Resolve this installation/resource problem before treating later errors as application API incompatibilities.

### Steps

From repository root:

```bash
git status --short
uv lock --check
uv sync --locked --group dev
uv pip check
uv run --locked python -c "from importlib.metadata import distribution; d = distribution('kivymd'); p = d.locate_file('kivymd/uix/label/label.kv'); print('Version:', d.version); print('Resource:', p); print('Exists:', p.is_file()); print('KV files in manifest:', sum(str(f).endswith('.kv') for f in (d.files or [])))"
```

Then:

1. Inspect the exact KivyMD source archive and hash selected in `uv.lock`.
2. Compare the archive resource inventory, package build configuration, and installed distribution manifest.
3. Reproduce the locked installation in an isolated temporary environment.
4. Identify whether the omission is local installation damage, a source-distribution packaging defect, or a build/install defect.
5. Select the smallest reproducible remedy supported by evidence. Any dependency-source change must be immutable, declared in project metadata, locked, and recorded.
6. Verify the remedy from a fresh environment. Do not accept manually copying files into `.venv`.

Classify results:

| Result | Action |
| --- | --- |
| Fresh installation provides resources | Repair the local environment and rerun startup. |
| Source contains resources but installed package omits them | Document build/install cause and a reproducible remedy. |
| Published artifact lacks resources | Stop for review of the dependency-source decision. |
| Startup reaches a new application traceback | Record it as the input to checkpoint 3. |
| Display, GL, or audio provider fails | Record an environment blocker separately. |

### Gate

Fresh declared-and-locked inputs reproducibly install required KivyMD resources. Record any next startup traceback, but do not repair application APIs in this checkpoint.

## Checkpoint 2 - Establish the test foundation

Create a test harness before editing game behavior. Use:

```text
tests/mdclassic_games/
  conftest.py
  unit/
  integration/
```

Add this root configuration to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests/mdclassic_games"]
addopts = "--strict-markers"
markers = [
    "gui: requires a working Kivy display and OpenGL context",
]
```

Requirements:

- Resolve the app directory relative to test files, never the invoking directory.
- Ensure imports target only `source/MDclassic_games`, not standalone or vendored modules with overlapping names.
- Keep root conftest and unit tests free of Kivy/application imports.
- Defer Kivy and application imports in GUI tests until a GUI fixture or test executes.
- Isolate writable Kivy home/log/config state with `tmp_path` and environment variables set before importing Kivy.
- Redirect the app's actual config file to temporary storage and assert that tracked `main.ini` is unchanged.
- Use the app directory as the GUI-test working directory.
- Clean scheduled Clock events, Window bindings, widgets, and app state between tests. Use finite-timeout subprocess isolation when in-process cleanup is not reliable.
- Make random choices deterministic at their production lookup point; advance scheduled callbacks deliberately rather than sleeping.

Start with meaningful display-independent tests, such as resource presence and Ahorcado's `replace_letter` helper. Do not make a placeholder or zero-test suite the gate.

Run from repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
```

### Gate

Nonzero unit tests collect and pass without a display, GUI imports are not initialized by unit collection, and tracked configuration remains untouched.

## Checkpoint 3 - Repair shell startup

Use the first startup traceback after checkpoint 1 and the verified installed KivyMD 1.2.0 source. Make one coherent fix at a time.

| Files | Work | Verify |
| --- | --- | --- |
| `menu.py`, `menu.kv` | Replace `SmartTileWithLabel` with supported `MDSmartTile` composition | Seven square, two-column tiles retain image, label, route, and one-click navigation |
| `menu.kv`, all seven game `screen.py` modules | Replace `MDToolbar` using pinned `MDTopAppBar` API | Titles, action ordering/callbacks, usable height, and elevation are preserved |
| `main.py` | Adapt `TempMsg` only as required by the actual snackbar API | First-entry loading text opens and dismisses |
| `drawer.py`, `drawer.kv`, root KV | Verify layout, open/close actions, and observable `screen` binding | Tile and drawer navigation work; return to menu works |
| `drawer.py` | Retain About and Help behavior | Text/version correct, CLOSE dismisses, Help requests existing URL |

If the inherited drawer widget lacks the required observable property, declare `screen = StringProperty('menu')` on `MyDrawer`. Do not replace it with an ordinary Python attribute.

Launch from **`source/MDclassic_games`**:

```bash
uv run --locked python main.py
```

Add real-widget shell regression tests as the shell becomes available.

### Gate

The menu renders with seven visible tiles; tile and drawer navigation, drawer open/close, About, and Help work. Record remaining lazy game-screen tracebacks for the appropriate game checkpoint.

## Checkpoints 4-10 - Repair one game at a time

Complete each row independently: implement only its compatibility fix, add its deterministic tests, run its checks, perform its desktop manual exercise, update the validation record, stop for review, and commit before advancing.

| Checkpoint | Game folder / screen ID | Required automated behavior | Required desktop exercise |
| --- | --- | --- | --- |
| 4 | Pong / `pong` | Paddle/wall collisions, exit scoring, serve/reset, speed limits using explicit updates | Start/restart, pause/resume, paddle control, ball/score, skin and speed settings |
| 5 | Ahorcado / `ahorcado` | Fixed-word correct/wrong/repeated input, win/loss, Spanish characters | New word, letters, keyboard/man settings, word/image display |
| 6 | Memory / `memory` | Pairs, match stays revealed, mismatch hides after scheduled resolution, completion | Matching/nonmatching pair, restart, size/theme, cartoons ICO images |
| 7 | 15 puzzle / `fifteen` | Legal/illegal moves, solved state, shuffle preserves tiles and existing solvability | Move, shuffle/restart, size/theme, reference image |
| 8 | 2048 / `2048` | Four directions, one merge per tile, score, no-op, undo; control spawning | Direction buttons, merge/score, undo, target-score control, restart |
| 9 | Buscaminas / `buscaminas` | Fixed-layout counts including edges, flood reveal, flags, mine/cleared outcome | New board, reveal, flag control, outcome popup if reachable |
| 10 | Snake / `snake` | Movement, eating/growth/score, food update, relevant collisions, restart | Start, turn, eat, collision/game-over, restart, speed/size/mode |

For 2048, cover the pre-spawn case `[2, 2, 2, 2]` moving left becoming `[4, 4, 0, 0]`.

For Memory, 15 puzzle, and 2048, inspect actual `MDChip` properties/events before modifying their KV. Preserve displayed values, callbacks, and live bindings; do not substitute static labels for interactive controls.

For every game:

1. Open through its tile.
2. Exercise the listed controls.
3. Return through the drawer, then reopen through the drawer.
4. Confirm an existing screen is reused and no duplicate update behavior appears.
5. Exercise relevant settings before and after lazy screen creation.
6. Run affected unit or GUI tests.

Do not silently change a pre-existing gameplay rule to satisfy a new test. Record the observed and intended behavior for review instead. Required scenarios cannot be satisfied by a skip or non-strict `xfail`.

## Checkpoint 11 - Complete cross-app regressions and CI

Complete test coverage for:

- All five settings panels: Pong, Ahorcado, Memory, 15 puzzle, and Snake.
- Settings changed before/after game creation and persistence through temporary-config reload.
- Tile and drawer routes to all seven screen IDs, including re-entry without duplicate screens.
- Loading snackbar and About dialog construction/dismissal with real widgets.
- Required JSON, words, images, fonts, and audio assets.
- Representative GIF and ICO decoding through the real runtime provider, including Memory cartoons.
- Help URL and requested sound playback through stubs while retaining real provider/asset-loading checks where supported.

Add `.github/workflows/mdclassic-games-tests.yml`, triggered by push and pull request, with explicit Python 3.11 and recorded uv version. It needs:

| Job | Command |
| --- | --- |
| Unit | `uv run --locked --group dev pytest tests/mdclassic_games/unit` |
| GUI | `xvfb-run -a uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration` |

The GUI job must document the verified Linux SDL/OpenGL/software-rendering prerequisites, set a finite timeout, and preserve failure logs. Xvfb is a display server, not proof that required GL/audio providers work. Missing providers are failures/blockers, not passing skips.

Run from repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
uv run --locked --group dev pytest
```

### Gate

Both test layers collect nonzero tests and pass. All game scenarios in checkpoints 4-10 are covered. Settings and state isolation work. CI is passing, or remote execution is explicitly recorded as pending rather than claimed as passing.

## Checkpoint 12 - Desktop acceptance and Phase 2 handoff

Run the complete suite from repository root with a real display, GL context, and audio output:

```bash
uv run --locked --group dev pytest
```

Record collection and passed/failed/skipped/xfail counts.

Then launch from `source/MDclassic_games`:

```bash
uv run --locked python main.py
```

Perform and record observations for:

- All seven games through tiles and drawer, menu return, re-entry, and first-entry notification.
- Every game exercise listed in checkpoints 4-10.
- All five settings panels and persistence after restart.
- About CLOSE, Help URL, and Exit.
- Representative sounds and mute controls where offered.
- Portrait/landscape resize and leaving/re-entering running games.

Back up and restore only test-generated changes to `main.ini`. A headless import, compilation check, or green unit suite does not substitute for this manual gate.

Before review:

```bash
git diff --check
git status --short --untracked-files=all
git diff --stat
```

### Phase 2 completion gate

- [ ] Framework resources install reproducibly from declared locked inputs.
- [ ] Shell, seven games, controls, settings, sounds, and resources pass desktop acceptance.
- [ ] Unit and GUI suites collect meaningful tests and pass.
- [ ] Tests preserve tracked configuration and isolate state.
- [ ] Focused CI passes, or its remote status is honestly pending.
- [ ] Validation record contains commands, counts, observations, failures, decisions, and the next action.
- [ ] Review and commit Phase 2 as the final checkpoint.

Only then hand off to Phase 3A: select the Android toolchain. Phase 3 builds one combined APK; Phase 4 installs that APK on a suitable device/emulator and repeats the relevant gameplay checks with Android-specific lifecycle, touch, rotation, and audio validation.
