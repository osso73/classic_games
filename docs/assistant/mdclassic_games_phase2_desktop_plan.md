# MDclassic_games Phase 2 runbook - Desktop compatibility

Progress updated: 2026-10-08. Status: **checkpoint 9 (Buscaminas) automated checks complete; manual desktop exercise pending**.

## Progress tracker

**Current position:** shell compatibility migration, Pong, Ahorcado, Memory, 15 puzzle, and 2048 checkpoints are complete. Buscaminas automated checks are complete; its manual desktop exercise remains. **Desktop acceptance: pending.**

**Active baseline:** Python 3.11, Kivy 2.3.1, and the PyPI `KivyMD 2.0.0` artifact locked by uv. This replaced the earlier checkpoint-1 Git commit source in commit `a1beac1`; checkpoint 3 was revalidated against the current lock. See the [validation record](mdclassic_games_validation.md) for installation evidence and test results.

| Checkpoint | Task | Status | Evidence / remaining work |
| --- | --- | --- | --- |
| 1 | Repair framework installation | Complete | Fresh resource installation verified; committed `f1d0148` |
| 2 | Establish test foundation | Complete | 10 unit tests passed; committed `0f5642d`; GUI fixtures still need executable isolation checks |
| 3 | Repair shell startup | Complete | Committed `b5e27b1`; revalidated against the current PyPI KivyMD lock with 10 unit, 3 GUI, and 13 full-suite tests passing |
| 4 | Pong | Complete | Real-widget behavior regression and full manual exercise pass, including repaired pause/resume; committed `b4406c4` |
| 5 | Ahorcado | Complete | Five real-widget behavior regressions and full manual exercise pass; committed `e7662c9` |
| 6 | Memory | Complete | KivyMD 2 compatibility repair, eight real-widget behavior regressions, and full manual exercise pass |
| 7 | 15 puzzle | Complete | KivyMD 2 migration, complete-theme filtering, six behavior regressions, and manual exercise pass |
| 8 | 2048 | Complete | KivyMD 2 migration, seven real-widget behavior regressions, and manual desktop exercise pass |
| 9 | Buscaminas | In progress | Toolbar callback and desktop right-click multitouch repairs plus six behavior regressions passed; right-click manual recheck passed, remaining game exercise pending |
| 10 | Snake | Pending | Compatibility, behavior tests, manual exercise |
| 11 | Cross-app regressions and CI | Pending | Settings, navigation, resources, full suite, CI workflow and passing jobs |
| 12 | Desktop acceptance and handoff | Pending | Interactive gameplay, audio, layout, persistence, final review and commit |

**Next exact action:** manually launch Buscaminas from `source/MDclassic_games` with `uv run --locked python main.py` and complete the remaining exercise: new board, safe reveal, mine/cleared outcomes if reachable, drawer return/re-entry, and representative sound. The desktop right-click recheck already passed. Record observations before review; do not begin checkpoint 10.

**Status convention:** Complete means required checkpoint checks passed and changes were reviewed and committed. Use In progress or Blocked for partial work, distinguishing implementation, automated checks, manual checks, and review/commit in the evidence column. Pending means the checkpoint has not been executed; Next identifies the immediate pending checkpoint. These are checkpoint counts, not an estimate of effort or overall percentage complete.

Update this tracker and the master plan's phase summary alongside the validation record at every checkpoint handoff. Keep detailed commands, observations, counts, and failures in the validation record. The entries above summarize recorded evidence; no runtime checks were rerun for this documentation update.

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 1 runbook](mdclassic_games_phase1_uv_plan.md), and [the validation record](mdclassic_games_validation.md) before editing. This runbook expands master-plan Phase 2 only. It is deliberately split into small checkpoints: complete one checkpoint, review it, commit it, and only then begin the next.

Phase 2 tests the combined application on **desktop**. Do not build or install APKs during this phase. Android packaging belongs to Phase 3; one resulting APK will contain all seven games, and Android/device validation belongs to Phase 4.

## Objective and boundaries

Restore desktop compatibility with the locked Python 3.11, Kivy 2.3.1, and KivyMD 2.0.0 baseline while preserving the seven games, rules, controls, navigation, settings, sounds, and assets. Build a maintained pytest suite for the combined app before beginning Android work.

Allowed changes:

- Necessary runtime `.py` and `.kv` files under `source/MDclassic_games`, excluding `resources/`.
- Root `tests/mdclassic_games/` test suite.
- Root pytest configuration in `pyproject.toml`.
- Focused `.github/workflows/` test workflow.
- Validation records and this runbook under `docs/assistant/`.
- Dependency metadata and generated `uv.lock` only for a demonstrated, documented incompatibility.

Do not change standalone games, application version, Android packaging, `requirements.txt`, asset selection, configuration section/key names, or the app-directory launch contract. Adapt against the pinned official KivyMD 2.0.0 source; do not switch to floating master or assume current development examples match that commit.

## Checkpoint workflow

Every checkpoint follows this sequence:

1. Inspect `git status --short`; preserve existing work and `source/MDclassic_games/main.ini`.
2. Make only the checkpoint's bounded changes. Add meaningful regression tests with a reproduced compatibility or behavior fix.
3. Run the checkpoint's required checks and capture the first meaningful failure rather than making speculative changes.
4. Update `docs/assistant/mdclassic_games_validation.md` using the master-plan template, including commands, working directory, test counts, observations, failure classification, and next exact action.
5. Stop for user review. Summarize changed files, behavior, checks, and open decisions.
6. Commit the fix, its tests, and its validation note together only after the user requests a commit.

A passed checkpoint is not a passed Phase 2. Execute checkpoints in order and stop after each for review. The user may make the commit themselves; do not commit automatically. Confirm the reviewed changes are committed before proceeding. Checkpoint 2 establishes the test foundation before application compatibility changes in checkpoints 3-10.

If manual testing requires the user's desktop, provide the exact launch directory, command, and exercise checklist, then record those checks as NOT RUN until the user supplies observations. Review approval or a commit alone is not evidence that a runtime check passed. A blocked checkpoint may have its diagnostic notes reviewed and committed, but remains blocked.

For a new session, use this instruction (replace `N` with the checkpoint number):

> Read the Phase 2 runbook, master plan, and validation record. Execute checkpoint N only. Preserve existing changes, run its checks, append the results and next exact action to the validation record, and stop for review. Do not commit or begin the next checkpoint.

Keep the Phase 1 record intact. For each checkpoint record status, environment/version inventory, files changed, commands and working directories, automated counts, manual observations, first relevant failure/log location, and next exact action. Use PASS / FAIL / NOT RUN for individual checks. Review both tracked diffs and new files before handoff; keep logs and generated output outside tracked source.

## Checkpoint 1 - Repair the KivyMD resource installation

**Completed historical procedure:** the steps below describe the original 1.2.0 investigation. Its failed resource build led to the explicitly approved immutable 2.0.0 remedy recorded in the validation record. Do not repeat these steps as an instruction to revert the active baseline.

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
2. Compare the archive resource inventory, package build configuration, and installed distribution manifest. Check Python source as well as resources against the intended release: a metadata version of `1.2.0` alone does not prove the installed source is consistent with that release. Do not migrate against a mixed or stale installation.
3. Reproduce the locked installation in an isolated temporary environment.
4. Identify whether the omission is local installation damage, a source-distribution packaging defect, or a build/install defect.
5. Select the smallest reproducible remedy supported by evidence. Any dependency-source change must be immutable, declared in project metadata, locked, and recorded.
6. Verify the remedy from a fresh environment, accounting for cached built wheels when diagnosing a build defect. Record the artifact hash, build inputs, and commands used; avoid deleting global caches as a generic remedy. Do not accept manually copying files into `.venv`.

Record actual Python patch, uv, Kivy, KivyMD, Pillow, materialyoucolor, and pytest versions. After any dependency decision, regenerate the lock with uv, rerun locked sync and `uv pip check`, and update the inventory. Never edit `uv.lock` by hand. If no supported reproducible 1.2.0 remedy can be established, stop with the evidence and a proposed plan decision rather than silently changing the framework baseline.

Attempt startup with working directory `source/MDclassic_games` using `uv run --locked python main.py`. Preserve `main.ini` before launch, record the first meaningful traceback and log location, and check for automatic config writes afterward.

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
    conftest.py
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
- Keep shared conftest and unit tests free of Kivy and GUI-dependent application imports. Unit tests may import genuinely pure application helpers, such as `ahorcado.general`, after checking that their package initialization also has no GUI side effects.
- Defer Kivy and application imports in GUI tests until a GUI fixture or test executes.
- Isolate writable Kivy home/log/config state with `tmp_path` and environment variables set before importing Kivy.
- Redirect the app's actual config file to temporary storage and assert that tracked `main.ini` is unchanged.
- Use the app directory as the GUI-test working directory.
- Clean scheduled Clock events, Window bindings, widgets, and app state between tests. Use finite-timeout subprocess isolation when in-process cleanup is not reliable.
- Make random choices deterministic at their production lookup point; advance scheduled callbacks deliberately rather than sleeping.
- Mark every display-dependent test `gui`. Do not set a default marker expression that excludes these tests from the full suite, or globally replace Kivy with dummy classes. Registering a marker does not itself apply it to tests.

Use one behavior-test module per game, normally in `integration/` because current rules are widget-bound. Test real production methods and observable state. Small behavior-preserving pure-helper extractions are allowed only when needed, characterized before extraction, and used by production callers; do not build a parallel rules engine for tests.

Start with meaningful display-independent tests, such as resource presence and Ahorcado's `replace_letter` helper. Do not make a placeholder or zero-test suite the gate.

Run from repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
```

### Gate

Nonzero unit tests collect and pass without a display, GUI imports are not initialized by unit collection, and tracked configuration remains untouched. Establish the fixture structure here; actual app lifecycle/config-isolation checks become executable with the shell in checkpoint 3 and must pass there. Do not claim an unexercised fixture proves isolation.

## Checkpoint 3 - Repair shell startup

Use the first startup traceback after checkpoint 1 and the verified installed KivyMD 2.0.0 source at the pinned commit. Make one coherent fix at a time. API names in the table are investigation starting points: verify supported widget composition, properties, and events against that source before implementing replacements.

`main.py` imports all game screen modules eagerly even though it constructs screens lazily. If a game-module import or KV registration blocks shell startup, a minimal import/API repair belongs here; record that cross-game change and defer gameplay verification to its game checkpoint. Do not disable game imports or substitute fake screens to obtain a passing shell.

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

The real menu renders with seven visible tiles; drawer open/close, About, and Help work. Shell integration tests exercise available shell behavior and verify temporary config isolation. Verify tile/drawer route declarations and attempt their events, recording lazy game-construction failures for checkpoints 4-10. Successful entry into every game is required at those checkpoints and checkpoint 11, not at this shell gate. Capture observations of loading messages where entry can proceed; do not count a failed game entry as a successful navigation test.

## Checkpoints 4-10 - Repair one game at a time

Complete each row independently: implement only its compatibility fix, add its deterministic tests, run its checks, perform its desktop manual exercise, update the validation record, stop for review, and commit before advancing.

| Checkpoint | Game / screen ID | Required automated behavior | Required desktop exercise |
| --- | --- | --- | --- |
| 4 | Pong / `pong` | Paddle/wall collisions, exit scoring, serve/reset, speed limits using explicit updates | Start/restart, pause/resume, paddle control, ball/score, skin and speed settings |
| 5 | Ahorcado / `ahorcado` | Fixed-word correct input reveals all occurrences; wrong/repeated input, win/loss, Spanish characters | New word, letters, keyboard/man settings, word/image display |
| 6 | Memory / `memory` | Pairs, match stays revealed, mismatch hides after scheduled resolution, resolved cards do not count as new matches, completion | Matching/nonmatching pair, restart, size/theme, cartoons ICO images |
| 7 | 15 puzzle / `fifteen` | Legal/illegal moves, solved state, shuffle preserves tiles and existing solvability | Move, shuffle/restart, size/theme, reference image |
| 8 | 2048 / `2048` | Four directions, one merge per tile, score, no-op, undo; control spawning | Direction buttons, merge/score, undo, target-score control, restart |
| 9 | Buscaminas / `buscaminas` | Fixed-layout counts including edges, flood reveal, flags, mine/cleared outcome | New board, reveal, flag control, outcome popup if reachable |
| 10 | Snake / `snake` | Movement, eating/growth/score, food update, relevant collisions, restart | Start, turn, eat, collision/game-over, restart, speed/size/mode |

For 2048, cover the pre-spawn case `[2, 2, 2, 2]` moving left becoming `[4, 4, 0, 0]`.

Folder names are lowercase game names except 15 puzzle (`game_15puzzle`) and 2048 (`game_2048`). Their screen IDs are respectively `fifteen` and `2048`. In Buscaminas include corner counts and flag/reveal interaction; in 2048 verify undo restores both board and score.

For Memory, 15 puzzle, and 2048, inspect actual `MDChip` properties/events before modifying their KV. Preserve displayed values, callbacks, and live bindings; do not substitute static labels for interactive controls.

For every game:

1. Open through its tile.
2. Exercise the listed controls.
3. Return through the drawer, then reopen through the drawer.
4. Confirm an existing screen is reused and no duplicate update behavior appears.
5. On a fresh launch, change a relevant setting before opening its game and verify the lazily created screen; repeat after opening the game. Preserve section names and defaults.
6. Run affected unit or GUI tests.

Do not silently change a pre-existing gameplay rule to satisfy a new test. Record the observed and intended behavior for review instead. Any temporary `xfail` must be strict, narrowly targeted, and linked to a documented issue. Required scenarios cannot be satisfied by skips or any `xfail`, including strict ones.

Run affected tests after each fix. After a shared shell, fixture, or dependency change, also run the established suite for previously completed checkpoints. Later tests not yet written are not passing results. If a game needs no compatibility edit, its tests and recorded manual checks still form its checkpoint deliverable.

## Checkpoint 11 - Complete cross-app regressions and CI

Complete test coverage for:

- All five settings panels: Pong, Ahorcado, Memory, 15 puzzle, and Snake.
- Settings changed before/after game creation and persistence through temporary-config reload.
- Tile and drawer routes to all seven screen IDs, including re-entry without duplicate screens.
- Loading snackbar and About dialog construction/dismissal with real widgets.
- Required JSON, words, images, fonts, and audio assets.
- Representative GIF and ICO decoding through the real runtime provider, including Memory cartoons.
- Help URL and requested sound playback through stubs while retaining real provider/asset-loading checks where supported.

Audit existing package extension/exclusion rules in resource tests, but defer the known ICO-inclusion assertion until Phase 3 changes `buildozer.spec`. Record this handoff explicitly; do not make Phase 2 tests require an out-of-scope Android spec edit.

Add `.github/workflows/mdclassic-games-tests.yml`, triggered by push and pull request, with explicit Python 3.11 and recorded uv version. It needs:

| Job | Command |
| --- | --- |
| Unit | `uv run --locked --group dev pytest tests/mdclassic_games/unit` |
| GUI | `xvfb-run -a uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration` |

Both jobs must use an explicit runner image and run `uv sync --locked --group dev` before testing. The GUI job must document the verified Linux SDL/OpenGL/software-rendering prerequisites, set a finite timeout, and preserve failure logs. Xvfb is a display server, not proof that required GL/audio providers work. Missing required providers are failures/blockers, not passing skips. Automated interaction tests may stub audible playback as described above; CI does not verify audible output.

Run from repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
uv run --locked --group dev pytest
```

### Gate

Both test layers collect nonzero tests and pass. All game scenarios in checkpoints 4-10 are covered. Settings and state isolation work without execution-order dependence. If remote CI execution is unavailable, record local verification separately and leave remote acceptance pending. Checkpoint 12's manual checks may still proceed, but pending CI is not a completed Phase 2 gate.

## Checkpoint 12 - Desktop acceptance and Phase 2 handoff

Run the complete suite from repository root with the established display/GL test environment (the verified Xvfb setup is acceptable for automation):

```bash
uv run --locked --group dev pytest
```

Record collection and passed/failed/skipped/xfail counts.

Reuse checkpoint 11's full-suite result if code, dependencies, configuration, fixtures, and test environment are unchanged; cite that result explicitly. Rerun after a fix or changed input rather than repeating an identical suite merely for the checkpoint boundary.

For manual acceptance use a real interactive display, GL context, and audible output. Launch from `source/MDclassic_games`:

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

- [x] Framework resources install reproducibly from declared locked inputs.
- [ ] Shell, seven games, controls, settings, sounds, and resources pass desktop acceptance.
- [ ] Unit and GUI suites collect meaningful tests and pass.
- [ ] Tests preserve tracked configuration and isolate state.
- [ ] Focused CI passes. If remote execution is unavailable, record it as pending and keep Phase 2 acceptance partial.
- [ ] Validation record contains commands, counts, observations, failures, decisions, and the next action.
- [ ] Review and commit Phase 2 as the final checkpoint.

Only then hand off to Phase 3A: select the Android toolchain. Phase 3 builds one combined APK; Phase 4 installs that APK on a suitable device/emulator and repeats the relevant gameplay checks with Android-specific lifecycle, touch, rotation, and audio validation.
