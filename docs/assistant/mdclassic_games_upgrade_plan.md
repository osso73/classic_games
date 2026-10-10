# MDclassic_games modernization execution plan

Original review: 2026-09-13. Progress updated: 2026-10-10. Status: **Phases 1-2 complete; Phase 3 checkpoints 1-2 complete, checkpoint 3 changes are implemented with all checks passing and await review/commit**.

## Progress summary

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Reproducible desktop environment | Complete; recorded environment checks passed, committed `763f139` |
| 2 | Desktop compatibility and validation | Complete; desktop/visual acceptance approved; 80 local tests pass; final CI run [38006783012](https://github.com/osso73/classic_games/actions/runs/38006783012) passed at `3d55d2b` |
| 3 | Android toolchain and debug APK | In progress; checkpoints 1-2 complete (toolchain selection, host setup authenticated/committed `c29c7b0`); checkpoint 3 spec/resource update implemented and awaiting review/commit |
| 4 | Android device validation | Pending; requires built APK |
| 5 | Final documentation and handoff | Pending |

See the [Phase 2 progress tracker](mdclassic_games_phase2_desktop_plan.md#progress-tracker) for completed tasks and the [validation record](mdclassic_games_validation.md) for evidence. Phase 2 desktop and remote CI acceptance passed on its recorded baseline. Phase 3 checkpoint 2 installed common Pillow 11.3.0 / pycairo 1.28.0 in the project environment and exact user-local Java/Android tools; all 80 desktop tests and the user's focused visual recheck pass, and checkpoint 2 is committed as `c29c7b0`. Checkpoint 3 updated the spec to the reviewed immutable toolchain/runtime matrix (p4a `v2026.05.09` commit `58d21141f17c889bf8585f5665921d72028f8831`, Python 3.11.14 recipes, Kivy 2.3.1/KivyMD 2.0.0/Pillow 11.3.0/pycairo 1.28.0 materialyoucolor 3.0.4, API 36 / min/NDK API 24 / NDK 28c, arm64-v8a, ICO inclusion, scoped `.buildozer`/`bin` ignores) and extended the packaging/resource regressions; its 40 unit tests and a real-Buildozer staging audit pass, and the changes await review/commit. No APK build or Android runtime acceptance has occurred yet.

**Baseline change:** Phase 2 checkpoint 1 replaced the defective KivyMD 1.2.0 source build with official KivyMD 2.0.0 at immutable commit `2d8a7b458897a01a400770e3bc10ebffd946b91d`. Commit `a1beac1` subsequently selected the released PyPI `kivymd==2.0.0` artifact instead; checkpoint 3 and Pong automated checks were rerun successfully against that locked artifact. Python 3.11 and Kivy 2.3.1 remain the baseline. Android compatibility is still unvalidated.

This document owns scope, phase order, compatibility work, Android work, and final acceptance. Each detailed runbook expands its own phase. These phase numbers supersede the previous plan: desktop compatibility now precedes Android packaging.

Detailed runbooks:

- [Phase 1 - Reproducible desktop environment](mdclassic_games_phase1_uv_plan.md)
- [Phase 2 - Desktop compatibility](mdclassic_games_phase2_desktop_plan.md)
- [Phase 3 - Android toolchain and debug APK](mdclassic_games_phase3_android_plan.md)
- [Phase 4 - Android device validation](mdclassic_games_phase4_device_plan.md)
- [Phase 5 - Final documentation and handoff](mdclassic_games_phase5_handoff_plan.md)

The Phase 3 runbook tracks completed toolchain-selection and host-setup checkpoints; Phase 4-5 runbooks remain planning documents. Runbook instructions are not execution evidence: consult the validation record for observed results. These phases follow Phase 2's one-checkpoint-at-a-time review workflow; commits require an explicit user request.

## 1. Objective and boundaries

Restore the combined KivyMD application on desktop and Android with reproducible dependencies and minimal compatibility changes. Preserve seven games, their rules, existing controls, navigation, settings, sounds, and assets. Use Python **3.11** as the inherited baseline; changing that minor version requires an explicit plan decision supported by toolchain evidence.

In scope during future execution:

- Runtime code and KV under `source/MDclassic_games`, excluding `resources/`.
- Root `pyproject.toml`, `uv.lock`, `.python-version`, and narrowly scoped `.gitignore` changes.
- `source/MDclassic_games/buildozer.spec` and reproducible host build-tool declarations.
- MD-app instructions in `README.md`, `docs/getting-started.md`, and execution records under `docs/assistant/`.
- Root `requirements.txt` only in the final documentation phase, as specified below.
- A maintained pytest suite under root `tests/mdclassic_games/`, test configuration/dependencies, and a focused GitHub Actions test workflow under `.github/workflows/`.

Out of scope: standalone sibling games under `source/`, example applications and vendored libraries under `resources/`, broad gameplay refactoring, new features, asset replacement, iOS/macOS packaging, Play Store publishing/signing, release uploads, generated `site/`, and existing APKs in `releases/`. Small behavior-preserving extractions of game-rule functions for testing are allowed when necessary; do not redesign the application architecture. Do not rename the Android package, change the app version, or reformat unrelated files.

## 2. Findings grounded in this checkout

| Finding | Consequence for execution |
| --- | --- |
| No root `pyproject.toml` or lockfile; four unpinned root requirements | Establish a desktop environment before editing application code. |
| `.gitignore` ignores `.python-version` | Explicitly unignore the root selector; `.venv` is already ignored. |
| `menu.py` and `drawer.py` load bare KV filenames at import time; KV and settings reference relative assets | Launch with **working directory `source/MDclassic_games`**. Selecting a uv project does not itself fix asset paths. |
| `menu.py` subclasses `SmartTileWithLabel`; menu and all seven `screen.py` files use `MDToolbar` | Compatibility migration extends beyond the shell's five files. |
| Memory, 15 puzzle, and 2048 use old `MDChip` properties/callbacks | Exercise their interactive controls, not just screen creation. |
| `main.py` subclasses `Snackbar` and calls `TempMsg(text=...).open()` | Preserve loading notifications when adapting the pinned API. |
| Drawer navigation uses `MyDrawer.screen`, set in KV and bound through `on_screen` in `main.py` | Verify the property is observable on the chosen KivyMD version; explicitly declare a `StringProperty` if needed. |
| Screens are created lazily in `change_screen` and `on_config_change` | Initial launch alone does not validate the games or settings callbacks. |
| `MainApp.play` assumes `SoundLoader.load` succeeded | Distinguish missing audio providers from UI/API faults; test OGG playback. |
| `main.ini` is tracked; game controls write config | Preserve existing local settings and exclude test-generated config changes. Android must also work with defaults, since `.ini` is not in the package extension list. |
| Build spec has Kivy 2.0.0, a floating KivyMD master ZIP, old SDL pin, and singular `android.arch = armeabi-v7a` | Select a coherent modern p4a toolchain and build arm64. |
| Memory's cartoons theme includes `.ico`; spec omits `ico` | Include those assets and verify their decoding on Android. |
| `resources/examples/tests` contains historical tests importing standalone `main` modules | These are not an established regression suite for this combined app; do not use blanket pytest discovery or modernize examples. |

These are static review findings, not claims that every suspected API issue was reproduced. Versions in the previous plan and its observed local Python/uv versions are not a tested compatibility matrix.

## 3. Execution rules for the implementing model

1. Read this plan and the Phase 1 runbook before editing. Inspect `git status --short` and preserve pre-existing work. Do not create branches or commits unless requested.
2. Execute phases in order. Within a phase, make one small, coherent change at a time, run its check, and read the first meaningful traceback before changing more files.
3. Use documentation/source for the **pinned release and commit**. The active baseline is the locked PyPI KivyMD 2.0.0 artifact; the approved official commit is an API reference after verifying it matches the artifact's relevant source. Current development examples may differ. Never solve a failure by silently switching to a floating Git URL, disabling a game, or suppressing exceptions.
4. Keep environment failures, application failures, and Android recipe failures separate. Missing display/GL/audio, network access, SDK, or device is a recorded blocker, not a passing test.
5. A phase gate must pass before dependent work starts. Phase 1 deliberately permits a documented application API failure; Phase 2 resolves it. Documentation may record partial progress while a later phase is blocked.
6. After each phase update `docs/assistant/mdclassic_games_validation.md` (create during execution) with the template below. Report the next exact action so another model can resume. Do not mark modernization complete while required checks remain blocked or unrun.
7. Once Phase 2 establishes pytest, use it throughout the remaining phases. Run affected tests after each application/configuration fix and the full suite at each phase's completion. Add a regression test for a reproduced defect wherever it can be meaningfully exercised on desktop; retain a documented device reproduction for Android-only defects. Reuse a passing full-suite result only when tested code, dependencies, packaging configuration, and test environment have not changed; cite that result explicitly. Desktop pytest results do not replace APK builds or device validation.

### Execution record template

```text
Phase / task:
Status: pending | in progress | passed | blocked
Files changed:
Environment: OS/architecture, Python patch, uv, Kivy, KivyMD, Pillow, materialyoucolor
Command and working directory:
Expected / observed result:
Manual checks: PASS / FAIL / NOT RUN, with observation
Automated checks: command, collected/passed/failed/skipped counts, CI result
Failure: first relevant traceback, log location, classification
Decision: selected versions / source URL / reason (if applicable)
Next exact action:
```

Do not put fabricated results in the record. Record Android build-host Python separately from the Python embedded in the APK.

## 4. Phase 1 — Reproducible desktop environment

Follow [the detailed runbook](mdclassic_games_phase1_uv_plan.md).

Deliver: root non-packaged uv project, Python selector, generated lockfile, pinned pytest development dependency, root selector ignore exception, provisional MD-app setup instructions, and validation record. Test implementation and discovery configuration belong to Phase 2.

Original Phase 1 dependency policy began with `kivy==2.3.1` and `kivymd==1.2.0` as conservative candidate releases, not a claim that they were latest or already validated. Phase 2 checkpoint 1 explicitly superseded the KivyMD selection with the pinned official 2.0.0 commit above; its API migration is now in scope. Resolve and record supporting dependency pins using release metadata rather than copying unverified Pillow/materialyoucolor versions. Later Android evidence may require a documented supporting-dependency adjustment and revalidation.

**Gate:** locked sync, Python 3.11, dependency consistency, and version inventory pass. Attempt desktop startup from the correct directory and record its outcome. An API failure is Phase 2 input; a missing graphical environment leaves GUI validation explicitly pending. A resolver/install failure blocks completion of Phase 1.

## 5. Phase 2 — Desktop compatibility, then smoke validation

Follow [the detailed Phase 2 runbook](mdclassic_games_phase2_desktop_plan.md). Complete its checkpoints in order: review and commit each checkpoint before starting the next; the test foundation precedes compatibility changes, and game fixes are handled one game at a time.

Allowed edits: necessary runtime `.py`/`.kv` files inside the app, root test suite, pytest configuration, focused CI workflow, and validation notes. Change runtime dependencies only for a demonstrated incompatibility, updating the lock and version record together. Set up the test harness described in 2D before editing game rules; add regression tests alongside 2A/2B fixes, then complete 2D before this phase ends.

### 2A. Repair shell startup

1. Use the post-remedy Phase 2 checkpoint 1 startup traceback and installed pinned KivyMD 2.0.0 source/docs to identify the first broken API. Widget names below are investigation starting points; verify composition, properties, and events against the pinned source.
2. In `menu.py` / `menu.kv`, migrate `SmartTileWithLabel` to the supported image-list composition (inspect `MDSmartTile`). Preserve square two-column image tiles, visible labels, source images, and existing `screen` routing. Check whether release events belong on the tile or a child; one click must navigate once.
3. Replace `MDToolbar` with the pinned release's top app bar API (inspect `MDTopAppBar`) in `menu.kv` and all seven game `screen.py` embedded KV strings. Preserve titles, action icon ordering, callbacks and their arguments. Check elevation/height visually rather than assuming old values have identical meaning.
4. In `main.py`, adapt `TempMsg` to the actual snackbar API (inspect `MDSnackbar` and its text content). Preserve notification text and callers where practical; a class rename alone may not preserve `text=` construction.
5. In `drawer.py` / `drawer.kv` and root KV in `main.py`, verify navigation layout structure, open/close actions, list widgets, and `screen` event binding. If the inherited widget lacks the required property, declare `screen = StringProperty('menu')` on `MyDrawer`; do not replace observable navigation with an ordinary Python attribute.
6. Verify About dialog text, version, CLOSE button, drawer font, and icons. Retain APIs that still work; avoid rewriting working list/dialog widgets merely because newer examples differ.

**Check:** the window renders the menu; all seven tile labels/images are visible; drawer opens/closes; About opens and closes. Capture remaining lazy-screen errors for 2B.

### 2B. Repair game-screen compatibility

Work through `pong`, `ahorcado`, `memory`, `game_15puzzle`, `game_2048`, `buscaminas`, `snake` in that order. Folder names and screen IDs differ: 15 puzzle uses `fifteen`, and 2048 uses `2048`.

1. Open each game using a tile, return to the menu through the drawer, then open it through the drawer. Exercise it before proceeding to the next game.
2. Check `MDChip` in Memory, 15 puzzle, and 2048 against the installed release's `kivymd/uix/chip/` implementation. In particular, verify the old `text` and `icon` properties and `on_release` event; adapt only unsupported properties or composition. Preserve displayed values, click actions, and bindings. Do not substitute static labels for interactive chips or assume current development examples match the pinned 2.0.0 source.
3. Inspect remaining KivyMD properties used in embedded KV: labels/font styles, palette colors, progress bars, grid/box layouts. Fix only observed unsupported APIs or visual regressions.
4. Open all five settings panels: Pong, Ahorcado, Memory, 15 puzzle, Snake. On a fresh launch, change a setting **before opening its game**, then verify the lazily created screen; repeat after opening the game. Preserve config section/key names and defaults.
5. Check images, fonts, word-list loading, and audio. Keep the documented app-directory launch contract; do not start a repository-wide path refactor to support arbitrary working directories.

### 2C. Desktop acceptance checklist

Run with a real display/GL context and audio output. For every row record observation, not just “no exception”.

| Area | Required exercise |
| --- | --- |
| Navigation | All seven games from tiles and drawer, return to menu, revisit an existing screen, loading notification on first entry. |
| Pong | Start/restart, pause/resume, paddle control, ball movement, score change, skin and speed settings. |
| Ahorcado | New word, correct/wrong letter, keyboard/man settings, word and image display. |
| Memory | Reveal a matching and nonmatching pair, restart, size/theme controls; include cartoons theme and its ICO images. |
| 15 puzzle | Legal tile move, restart/shuffle, size and theme controls, matching reference image. |
| 2048 | Direction controls, merge/score, undo, target-score chip, restart. |
| Buscaminas | New board, reveal cell, flag action using existing controls, outcome popup if reachable. |
| Snake | Start, turn, eat/score, collision/game-over, restart, speed/size/mode settings. |
| Shell/settings | Five panels load and settings persist after restart; About CLOSE; Help launches the existing URL; Exit works. |
| Audio/layout | Representative start/move/win-or-loss sounds and mute where offered; portrait/landscape resize; leave/re-enter running games without new crashes or duplicate update behavior. |

Preserve existing timing/lifecycle behavior unless a concrete modernization regression needs a minimal fix. Record unrelated pre-existing defects separately. Back up existing `main.ini` before interactive tests and restore only changes caused by the test, preserving user edits.

**Manual gate:** shell and all game/control/settings checks pass on desktop. A headless import or compile check cannot substitute for this gate. The automated gate in 2D is also required before Android work starts.

### 2D. Build a maintained automated test suite

Deliver a real regression suite for the combined app, not copies of the historical standalone tests. Use those tests only as a reference for scenarios after checking their assumptions against the current implementation.

#### Task 1 — Establish discovery and isolation

1. Use root `tests/mdclassic_games/unit/` for display-independent rules/data checks and `tests/mdclassic_games/integration/` for Kivy widget/app checks. Keep shared fixtures in `tests/mdclassic_games/conftest.py` and GUI-specific fixtures inside the integration directory.
2. Configure `[tool.pytest.ini_options]` in root `pyproject.toml`: `testpaths = ["tests/mdclassic_games"]`, `addopts = "--strict-markers"`, and register a `gui` marker for tests requiring Kivy's display/GL context. Do not collect `resources/examples/tests` or sibling games. Do not add a global marker expression that silently excludes GUI tests from the full suite.
3. Resolve the combined-app source directory relative to the test file, not the invoking working directory. Configure imports to target that directory only; verify that `main`, `pong`, etc. resolve there rather than to legacy games or vendored examples. Do not import application/GUI modules from root conftest or unit tests merely to obtain constants.
4. Unit tests must collect and run without a display. GUI integration tests must defer Kivy/application imports until a GUI fixture/test is executing, so selecting unit tests cannot initialize a window. Do not globally monkeypatch Kivy into dummy classes.
5. Isolate writable state with `tmp_path`: config files, Kivy home/logs, and any generated data. Set environment variables before importing Kivy. Use the app-directory working directory for GUI tests, but redirect the app's actual config filename to temporary storage; changing `KIVY_HOME` alone is not proof that tracked `main.ini` is protected. Assert that tests leave tracked source/config untouched.
6. Control random choices with explicit fixtures/monkeypatching at the source used by the game. Advance scheduled callbacks deliberately; avoid arbitrary sleeps. Clean up scheduled events, widgets, bindings, and running-app state between tests. Use subprocess isolation for whole-app lifecycle tests if global Builder/Clock state cannot be reliably reset, and give each subprocess a finite timeout.

#### Task 2 — Cover game rules and boundary cases

Create one test module per game. Read the actual rule methods first; assert externally meaningful board/state/score outcomes with small fixed examples. Do not reimplement the algorithm in the test or assert only that a mock was called.

| Game | Minimum behavior scenarios |
| --- | --- |
| 2048 | Movement/compression in each direction; a tile merges at most once per move (e.g. `[2, 2, 2, 2]` becomes `[4, 4, 0, 0]` moving left before spawning); score increment; no-op move; undo restores prior board/score. Control spawning when asserting exact boards. |
| 15 puzzle | Adjacent tile moves into the empty cell; nonadjacent move leaves state unchanged; solved-state recognition; shuffle preserves the tile set and follows the existing solvable-shuffle behavior. |
| Memory | Board has matching pairs; match remains revealed; mismatch is hidden after the scheduled resolution; already resolved cards do not count as new matches; completion state. |
| Buscaminas | Adjacent-mine counts on a fixed layout, including edges/corners; safe reveal/flood behavior; flags and reveal interaction; mine-hit and cleared-board outcomes. |
| Snake | Movement and growth on eating; score/food updates; wall/body collision under the relevant existing mode; restart resets relevant state. |
| Ahorcado | Correct letter reveals all occurrences; wrong letter advances failure state; repeated input follows existing behavior; win/loss; supported Spanish characters. Use a fixed word. |
| Pong | Paddle and wall collisions, score when the ball exits, reset/serve, configured speed limits. Drive explicit update steps rather than wall-clock simulation. |

Where rules are currently embedded in Kivy widgets, test the real widget in the GUI integration suite or extract a small pure helper used by production code. For an extraction, first characterize existing behavior, preserve signatures/callers where practical, and verify the production code uses the extracted helper. Do not create a parallel rules engine just for tests. Not every game needs a pure unit module if its current rules require widgets, but every game needs the stated automated behavior coverage.

For an apparent pre-existing bug, record the observed/intended behavior and leave the issue explicit rather than silently changing gameplay to satisfy a new test. Any temporary `xfail` must be strict, narrowly targeted, and linked to a documented issue; required acceptance scenarios cannot be counted as passing through `xfail` or skips.

#### Task 3 — Add shell and resource integration regressions

1. Build the actual app with the pinned framework and load its real KV. Assert all seven menu entries route to their expected screen IDs, through both tile and drawer events. Verify return/re-entry reuses the existing screen rather than adding duplicates.
2. Exercise changed toolbar/chip callbacks and assert resulting state changes. Verify loading snackbar and About dialog construction/dismissal using the real pinned widgets.
3. Test all five settings panels and setting changes before/after game creation. Write/reload temporary config and assert persistence without modifying tracked `main.ini`.
4. Add display-independent resource checks for required settings JSON, word data, images/fonts/audio and the package extension/exclusion rules. Decode representative ICO/GIF images through the runtime provider in GUI tests. Add the ICO packaging assertion when Phase 3 updates the spec; do not make Phase 2 depend on a not-yet-authorized spec change.
5. Stub external browser launch and actual audio playback in automated interaction tests, asserting the requested URL/sound. Keep asset/provider-loading checks real where supported. Manual checks remain responsible for audible output, appearance, touch ergonomics, and Android lifecycle behavior.

#### Task 4 — Commands, CI, and acceptance

Document these commands, all from repository root:

```bash
uv sync --locked --group dev
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
uv run --locked --group dev pytest
```

Mark every display-dependent test `gui`; full-suite execution includes both layers and requires a display. A missing display/provider must fail or be reported as a blocker for that job, not turn the GUI suite into a passing run of skips.

Add a small GitHub Actions workflow triggered by pushes and pull requests, using Python 3.11 and a recorded uv version. Run a display-independent unit job and a Linux GUI job with Xvfb plus the SDL/OpenGL/software-rendering prerequisites actually verified for the pinned Kivy version. The GUI command is `xvfb-run -a uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration`. Set a job timeout, preserve failure logs, and use the lockfile; no Android build/device CI is required in this phase. Xvfb supplies a virtual display, not an OpenGL or audio implementation by itself.

**Automated gate:** both test layers collect nonzero tests and pass; all seven games have behavior/boundary assertions; shell/settings regressions pass; tests do not write user config or depend on execution order; the focused CI jobs pass (or remain explicitly pending if remote execution is unavailable). No arbitrary coverage-percentage target is required. Run affected tests during fixes and the full suite at the end of the phase and after later shared dependency changes. Record commands and counts, including any skips/xfails; a green run with required scenarios skipped is not completion.

## 6. Phase 3 — Reproducible Android toolchain and debug APK

Follow [the detailed Phase 3 runbook](mdclassic_games_phase3_android_plan.md). Its checkpoints separate toolchain/native-dependency feasibility, host setup, spec/resource checks, build, nested APK inspection, and clean-app-build reproduction. No Android toolchain combination is claimed validated by this plan.

### 3A. Select the toolchain before editing the spec

Allowed edits: root build dependency group/lock, app build spec, narrowly scoped generated-output ignores, build instructions, validation record. Application changes require a reproduced Android compatibility problem.

1. On a supported Linux build host, consult selected Buildozer and python-for-android (p4a) installation/release documentation. Record URLs and versions. Inspect p4a's Python/hostpython, Kivy, Pillow, SDL2, and materialyoucolor recipes/dependency handling against the desktop set.
2. Fill in the following matrix with **exact values and supporting references before building**. Do not choose API/NDK/JDK versions independently by “latest”. If no supported Python 3.11 combination can be established, stop and report the conflict instead of silently upgrading Python or writing a custom recipe.

| Required selection | Evidence required |
| --- | --- |
| Host OS/architecture and Python patch | Supported by the chosen Buildozer/p4a releases. |
| Buildozer version; host Cython/build dependencies | Exact pins in a root `android` dependency group; follow chosen toolchain requirements. |
| p4a immutable revision | Release tag resolved to commit, pinned using settings supported by this Buildozer version. |
| Embedded Python and hostpython recipe versions | Both compatible and actually selected in build logs; desktop `.python-version` does not control them. |
| JDK, SDK target API, minimum API, NDK, NDK API | Coherent values documented for this p4a revision; NDK API normally matches minimum API. |
| Kivy, KivyMD, Pillow, materialyoucolor and required transitives | Compare desktop pins with recipe support; record any platform-specific constraint explicitly. |

3. Install documented OS/JDK prerequisites and sync the pinned host group. `uv.lock` controls the host environment, **not** the Android cross-compiled dependency graph. Ensure Buildozer can invoke its required Python tooling in that environment.
4. Keep Kivy/KivyMD aligned with the desktop baseline. If a native supporting package needs a different supported version, prefer a common version on both platforms, regenerate the lock, and rerun the automated suite and affected manual desktop checks. Do not blindly copy every desktop transitive into Android requirements or blindly remove recipe-required dependencies. Keep pytest and other test-only dependencies out of Android requirements and packaged runtime assets.

### 3B. Update `source/MDclassic_games/buildozer.spec`

1. Replace the master ZIP with the exact KivyMD release; update Kivy and explicit runtime/native requirements according to 3A. Remove the historical `sdl2_ttf==2.0.15` override unless the selected toolchain specifically requires it. Assess `requests`, `urllib3`, `chardet`, `idna` through actual package/recipe dependencies, not just application imports.
2. Set the supported plural architecture setting `android.archs = arm64-v8a`; remove the obsolete singular active setting. Additional ABIs are optional only if needed for the chosen test device/emulator.
3. Set explicit `android.api`, `android.minapi`, `android.ndk`, `android.ndk_api` and immutable p4a selection using verified option names. Pin recipe Python versions using the selected toolchain's supported mechanism.
4. Preserve package identity **`org.games.clasicgames`**, title, version extraction, icon/splash, orientation, and existing permission intent. Do not “correct” the package-name spelling or add permissions speculatively.
5. Add `ico` to `source.include_exts`. Audit packaged runtime assets: nested themes, GIFs, PNG/JPG/ICO images, OGG audio, TTF font, JSON settings, KV and Ahorcado text data. Keep `resources` excluded and avoid packaging the root environment or examples.
6. Add scoped ignores for app `.buildozer/` and `bin/` output if needed. Do not add APKs, SDKs or generated build trees to version control.

### 3C. Build and inspect

From repository root:

```bash
uv sync --locked --group android
```

With working directory `source/MDclassic_games`:

```bash
uv run --locked --group android buildozer -v android debug
```

Record command, complete build log location, embedded versions, and exact artifact path. Verify the APK's package ID, arm64 native libraries, expected runtime assets, and absence of examples. Inspect the packaged Python asset bundle if nested inside the APK.

On failure, identify the first failing recipe/tool and repair that cause. Clean only the relevant app build cache when toolchain changes make it stale; do not delete global SDK/uv caches as a generic remedy. Once the build succeeds, verify one rebuild from a clean **app build directory** with the documented pinned setup.

Before closing this phase, run the full Phase 2 pytest suite in the desktop test environment, including the packaging/resource checks updated for the final spec (especially ICO inclusion). Record results separately from the Android build. A build-host environment lacking a display does not waive the GUI tests; run them in the established GUI test environment/CI.

**Gate:** the full pytest suite passes and a debug APK is generated and inspected, including a successful clean-app-build reproduction. A captured toolchain blocker is useful progress but is not completion. AAB/release signing is not required.

## 7. Phase 4 — Android device validation

Follow [the detailed Phase 4 runbook](mdclassic_games_phase4_device_plan.md). It provides exact-artifact/device selection, safe fresh-data testing, full logcat capture, one-game-at-a-time touch checks, lifecycle scenarios, and the fix/rebuild/retest loop.

Use a physical arm64 device or compatible emulator for the built ABI. Record device model, Android API, ABI, installation result, artifact path, and logcat observations.

With working directory `source/MDclassic_games`:

```bash
uv run --locked --group android buildozer android deploy run
uv run --locked --group android buildozer android logcat
```

1. Verify fresh-install startup/default settings using a test device/profile without valuable app data; do not remove an existing user's installation to obtain a clean test.
2. Repeat Phase 2C gameplay/navigation checks using touch, including ICO/GIF images, font, all settings, OGG audio, About and external Help.
3. Exercise Android Back, rotation (spec allows all orientations), background/foreground, exit/relaunch, and settings persistence. Require no newly introduced crash, frozen screen, or lost controls. Preserve existing lifecycle behavior rather than inventing background-play features.
4. Inspect logs for Python tracebacks and missing assets/providers. APK generation or a splash screen alone does not prove the app works.
5. For each fix arising from device testing, run affected pytest tests and add a meaningful regression where desktop automation can reproduce it. After the final fix, rerun the full suite, rebuild the APK if its inputs changed, and repeat affected device checks on that artifact. If no tested inputs changed, reference the preceding full-suite pass instead of running an identical suite again.

**Gate:** installed app passes required checks on at least one recorded device/emulator, and the final code/dependency/spec state has a recorded full pytest pass. Without device access this phase remains blocked, and Android runtime support must not be advertised as validated.

## 8. Phase 5 — Final docs and handoff

Follow [the detailed Phase 5 runbook](mdclassic_games_phase5_handoff_plan.md). Its checkpoints cover evidence reconciliation, a functional runtime requirements export, public setup/test/build instructions, fresh-environment verification, and final acceptance.

1. Reconcile MD-app sections of `README.md` and `docs/getting-started.md`: uv installation link, Python baseline, locked sync, correct working directory, desktop command, host prerequisites, pinned Android group/build/deploy commands. Keep standalone instructions separate. Correct the relevant `game.spec` reference to `buildozer.spec`.
2. Keep `pyproject.toml` / `uv.lock` authoritative. Replace root `requirements.txt` with a **functional generated export**, retaining its existing MD-app dependency purpose, and explain that it does not cover every standalone game. Generate from root with `uv export --locked --no-dev --format requirements-txt --output-file requirements.txt`; confirm the export excludes the Android group. Never replace requirements with a comment-only file that makes `pip install -r` silently install nothing. Regenerate after runtime dependency changes.
3. Publish the actual tested version matrix and link the validation record. Distinguish selected, built, and device-tested values, with platform-specific differences.
4. Follow documented setup/build steps in a fresh environment without relying on a global KivyMD/Buildozer install; reuse Phase 3 clean-build evidence if instructions and pins are unchanged.
5. Review final file scope and diffs. Exclude test-generated `main.ini` changes, caches, artifacts, and changes to sibling games/examples. Summarize compatibility edits and open unrelated issues.
6. Document test layout, unit/full/GUI commands, GUI system prerequisites, CI workflow, deterministic fixtures, and how to add a game regression test. Confirm the runtime requirements export excludes development/test dependencies. Include automated results in the validation record and run the documented full test command in the fresh desktop environment.

**Final acceptance:** Phases 1–5 pass; all seven games and existing controls work on desktop and the tested Android target; the maintained automated suite and focused CI pass; setup/build/test instructions are reproducible. Any required failed or unrun check means the result is partial, not “modernization complete”.

## Reference starting points

- uv projects and locking: <https://docs.astral.sh/uv/guides/projects/>
- Active KivyMD **2.0.0** source: <https://github.com/kivymd/KivyMD/tree/2d8a7b458897a01a400770e3bc10ebffd946b91d>. Use this pinned source for API details when matching versioned documentation is unavailable; do not substitute development documentation. Original 1.2.0 artifact investigation is retained in the validation record.
- Kivy packaging: <https://kivy.org/doc/stable/guide/packaging-android.html>
- Buildozer installation: <https://buildozer.readthedocs.io/en/latest/installation.html>
- p4a releases and recipe sources: <https://github.com/kivy/python-for-android/releases>

Use these to locate version-specific evidence during execution; these links are not evidence that an untested combination works.
