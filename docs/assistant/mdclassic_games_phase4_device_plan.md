# MDclassic_games Phase 4 runbook - Android device validation

Reviewed: 2026-10-09. Progress updated: 2026-10-11. Status: **Phase 3 complete and handed off; the full manual checkpoint matrix on a Google Pixel 10 (Android 17 / API 37) is complete. All 12 checkpoints pass. Four Android defects found (audio guard, edge-to-edge system bars, 15-puzzle portrait layout, Snake phantom swipe) were fixed and rebuilt; the third change moved the Phase 4 artifact from `7d3416aa…` to `be6e6196…` and the fourth to `8bc32723…`. Checkpoints 1-6 remain valid on `7d3416aa…`, checkpoints 7-10 on `be6e6196…`, and checkpoints 11-12 on the final artifact `8bc32723…`, re-confirmed by the final-artifact regression (startup, seven game entries/basic controls, settings persistence, representative audio, one rotation/background cycle). Final input state has a full desktop pass (112/112) and logcat review. Phase 4 is complete; Phase 5 checkpoint 1 (evidence reconciliation) is next. Landscape layout is a recorded pre-existing limitation deferred to a separate task by user decision.**

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 3 runbook](mdclassic_games_phase3_android_plan.md), and [the validation record](mdclassic_games_validation.md). This runbook expands master-plan Phase 4 only. Use the final inspected Phase 3 artifact, not an older APK from `releases/`.

## Progress tracker

| Checkpoint | Task | Status | Evidence / remaining work |
| --- | --- | --- | --- |
| 1 | Identify device, artifact, and isolated test data | Complete | PASS 2026-10-10. Artifact `7d3416aa…e9d3cc91` (53,223,301 bytes) hash matches; package `org.games.clasicgames`, versionName 1.2, versionCode 1024102, launcher `org.kivy.android.PythonActivity`, min/target API 24/36, arm64-v8a, v2-signed; clean tree (no unbuilt change). Target: Google Pixel 10 `61190DLCR000VV`, physical, **Android 17 / API 37** (upgraded since Phase 3 handoff), arm64-v8a, 1080x2424 @ 460 dpi, 3-button nav. Existing install is the prior test data (`4c45da83…`); user approved uninstall/clear for fresh defaults. Samsung S24 not attached. Pending review/commit |
| 2 | Install fresh and validate startup/defaults | Complete | PASS 2026-10-10 on Pixel 10 `61190DLCR000VV` (Android 17/API 37) with artifact `7d3416aa…e9d3cc91`: uninstalled prior test install, fresh `adb install` (exit 0), cold launch `am start -W` TotalTime 299 ms, main loop reached, providers incl. `audio_sdl2`, fresh `.main.ini` defaults exact match, immersive bars `visible=false`, no app-fatal errors (only non-fatal Kivy logo-copy), seven tiles/drawer/About(v1.2)/CLOSE/first control PASS (user). Logcat `phase4-checkpoint2/logcat-full.txt` |
| 3 | Validate shell/navigation/settings on touch | Complete | PASS 2026-10-10 on Pixel 10 (`7d3416aa…`): five settings panels applied before/after game creation and persisted across a cold relaunch (`.main.ini` identical); all seven games tile/drawer/re-entry PASS; About v1.2/CLOSE/dismissal/Exit PASS; no session log errors. Evidence `phase4-checkpoint3/` |
| 4 | Pong | Complete | PASS 2026-10-10 on Pixel 10 (`7d3416aa…`): all 7 items - tile entry, start/restart, both paddles touch, side-exit scoring/serve, pause/resume icon+motion, speed/skin effect, drawer return/reopen. Pong has no sound/mute (recorded not present). Config `speed=30, skin=jupiter`. Evidence `phase4-checkpoint4/` |
| 5 | Ahorcado | Complete | PASS 2026-10-10 on Pixel 10 (`7d3416aa…`): tile/drawer entry, new word, correct-letter reveal (all occurrences), wrong-letter failed-list + man image, readable Spanish chars, one-hint control, mute toggle, keyboard/man settings, restart, live loss popup. Win not observed live (recorded). Evidence `phase4-checkpoint5/` |
| 6 | Memory | Complete | PASS 2026-10-10 on Pixel 10 (`7d3416aa…`): tile/drawer entry, build, mismatch hides (~2 s)+Moves count, match stays revealed+count, level/theme chips+settings (level=20), all six selectable themes build 20-pair boards with all backs/faces, cartoons `.ico` decode, start/match/completion sounds+mute, restart. Evidence `phase4-checkpoint6/` |
| 7 | 15 puzzle | Complete | PASS 2026-10-11 on Pixel 10, artifact `be6e6196…` (first attempt on `7d3416aa…` FAILED: reference picture filled the bottom row, chips unusable in portrait; fixed and retested). Tile/drawer entry, adjacent move+Moves count, non-adjacent ignored, restart/shuffle, 3x3/4x4/5x5 sizes, all 14 complete themes with matching reference image and no blank tiles, half-image/half-chips bottom row, drawer return/reopen. Evidence `phase4-checkpoint7/` |
| 8 | 2048 | Complete | PASS 2026-10-11 on Pixel 10 (`be6e6196…`): tile/drawer entry, start with two tiles Score 0, joystick directions shift+spawn on valid move/no spawn on invalid, merges double value and Score increases, undo reverts move+score, target chip cycles 256/512/1024/2048, win/loss popups reachable, mute silences sounds, return/reopen works. Evidence `phase4-checkpoint8/` |
| 9 | Buscaminas | Complete | PASS 2026-10-11 on Pixel 10 (`be6e6196…`): tile/drawer entry, level 1 (9x9/10) start with timer, reveal/flood, flag mode + mine counter, chording (open_adjacent), levels 1→2→3 resize/counts correct, win/loss states+sounds, mute, return/reopen. Evidence `phase4-checkpoint9/` |
| 10 | Snake | Complete | PASS 2026-10-11 on Pixel 10 (`be6e6196…`): tile/drawer entry, start + turns in all four directions via board swipes, eating food increments score and grows the snake, wall/self collision game-over + restart, pause/resume halts and resumes motion with icon toggle, speed/size/mode/start-level settings within supported ranges (board + progress indicator usable), running-round drawer return/reopen with no duplicate/accelerated motion and direction swipes still working, mute silences sounds. Evidence `phase4-checkpoint10/` |
| 11 | Lifecycle, rotation, audio, and external Help | Complete | PASS 2026-10-11 on Pixel 10 (entry artifact `be6e6196…`, Snake-fix rebuild `8bc32723…`): Back behavior documented (About closes via CLOSE, not Back), background/foreground resumes, screen lock/unlock recovers, Help browser round trip, normal exit and cold force-stop relaunch with settings persistence, repeated re-entry x3 (Snake initially flipped direction, fixed and retested), audio/mute incl. after foregrounding, ICO/GIF/font providers incl. after rotation. Landscape layout is not responsive for most screens/games - recorded pre-existing limitation, deferred by user decision. Evidence `phase4-checkpoint11/` |
| 12 | Final artifact regression and handoff | Complete | PASS 2026-10-11 on Pixel 10 (`8bc32723…`): hash re-confirmed (53,223,401 bytes) and matching on-device `base.apk` byte-for-byte; cold startup + menu, all seven game entries/basic controls + snake drawer re-entry, settings persistence (incl. programmatic force-stop/cold-relaunch with on-device `files/.main.ini` unchanged), representative audio/mute, one rotation/background cycle all PASS. Full desktop suite 112/112 on final inputs; logcat session clean (no Traceback/FATAL/AndroidRuntime; single process for the exercise, onPause/onResume confirmed). Tree clean, `main.ini` untouched. Evidence `phase4-checkpoint12/`. Phase 4 complete; hand off to Phase 5 |

**Next exact action (2026-10-11):** Phase 4 checkpoint 12 passed and Phase 4 is complete. Final artifact `8bc32723de30b90e290e5904338eab561d4968400021c0e167b0578d71e6848e` (53,223,401 bytes) was re-confirmed on file and byte-identical to the on-device install; the full acceptance set (startup, seven games, settings persistence incl. programmatic force-stop/cold-relaunch, representative audio, one rotation/background cycle) passed; the full desktop suite passed 112/112 on the final state; the session logcat had no app-fatal messages and a single process ran the whole exercise; the tree is clean with `main.ini` unchanged. Hand off to [Phase 5](mdclassic_games_phase5_handoff_plan.md) checkpoint 1 (evidence reconciliation). The known display-cutout gap (only `systemBars()` insets) and the deferred landscape layout remain recorded limits.

## Phase 4 repair log - Android compatibility fixes (2026-10-10 / 2026-10-11)

Three Android defects (two runtime, one portrait layout) were repaired under the repair loop. Each has a display-independent desktop regression and a rebuilt, reinstalled, retested APK; because the third repair changed the artifact, its hash and the checkpoint coverage are tracked explicitly.

| # | Symptom | Root cause | Fix | Regression |
| --- | --- | --- | --- | --- |
| 1 | Tapping Play (or any sound) crashed; every `SoundLoader.load()` returned `None` | `main.py` set `SDL_AUDIODRIVER=alsa` for any platform reporting `sys.platform == 'linux'`, which includes Android, so `AudioSDL2` failed to initialise and no OGG loaded | Moved the guard into `source/MDclassic_games/audio_env.py:configure_audio_environment`, which skips `kivy.utils.platform == 'android'` before Kivy import and keeps `setdefault` so a user's explicit driver is preserved | `tests/mdclassic_games/unit/test_audio_env.py` |
| 2 | Status bar clock overlapped the top app bar and its buttons were unclickable; the navigation bar overlapped the bottom of a game board | The app targets API 36, so Android 15+ forces edge-to-edge drawing; no system-bar handling existed and Kivy 2.3.1 exposes no insets | Added `source/MDclassic_games/android_insets.py`: `hide_system_bars` requests immersive mode (both bars hidden, swipe-to-reveal), `system_bar_insets` pads `content` as a fallback; the root KV was wrapped in a `BoxLayout id="content"` | `tests/mdclassic_games/unit/test_android_insets.py` |
| 3 | 15 puzzle: on a portrait phone the bottom reference picture filled the whole bottom row (nearly the board size) and pushed the Theme/Level chips off-access, making them unreadable/unusable | `game_15puzzle/sample.py:initialize_grid` sized the reference square to `min(parent.height, parent.width)`; in portrait `parent.height > parent.width`, so it took the full width and left no room for the chips (the code assumed a landscape bottom row) | Capped the reference square at half the parent width (`min(parent.height, parent.width / 2)`), so the bottom row is half reference image and half chip area; the chips `FloatLayout` then keeps the other half | `tests/mdclassic_games/integration/test_15puzzle.py::test_fifteen_reference_picture_leaves_the_controls_usable` (fails on the old sizing, passes on the fix) |
| 4 | Snake: leaving a running round through the drawer and re-entering changed the snake's direction to vertical | `snake/gameboard.py:on_touch_up` compared against instance `swipe_x`/`swipe_y` last set by any earlier `on_touch_down`; a release whose down did not reach the board (a drawer/toolbar tap) used those stale coordinates and could register a phantom swipe | Stored the start point in the touch's own user data (`touch.ud['snake_swipe']`) and ignore a `on_touch_up` with no such record, so only a touch that began on the board steers the snake | `tests/mdclassic_games/integration/test_snake.py::test_snake_ignores_a_release_without_a_matching_board_touch_down` (fails on the old code, passes on the fix) |

Devices / interactive acceptance (both Android 16 / API 36 / `arm64-v8a`):
- **Google Pixel 10** - 1080x2424, punch-hole cutout 173 px, 3-button navigation: menu, drawer, settings/help, game entry and audio confirmed working; status and navigation bars hidden (`dumpsys window displays` shows `visible=false`). Screenshot `/home/oriol/android-build/evidence/pixel10-after-insets.png`.
- **Samsung Galaxy S24 `SM-S921B`** (serial `RFCWC0ZFEFD`) - 1080x2340, cutout 103 px, gesture navigation: same checks confirmed working; bars hidden. Screenshot `/home/oriol/android-build/evidence/s24-menu-immersive.png`.

Artifact installed during the first interactive pass: `source/MDclassic_games/bin/clasicgames-1.2-arm64-v8a-debug.apk`, SHA-256 `4c45da83721aaf2f0bd6f8e7319ea99e7371534a23714ab650e2c5ce2102bf44`, 53,223,137 bytes (interim rebuilt hash after fix 1: `c47a457d3bfa208ba16c6824a9740d8a2af86a2c8ccef5133406a56d7f3dd07c`). Build logs: `/home/oriol/android-build/evidence/build-phase4-fix.log`, `build-phase4-immersive.log`.

Artifact history (device matrix): Phase 3 checkpoints 6-7 recorded the clean-build artifact SHA-256 `7d3416aaa7f882b4ffd54295ae297f452bf4594a2f2410b899d74f55e9d3cc91` (53,223,301 bytes), content-identical to `4c45da83…` (both nested bundle listings byte-for-byte identical, only signing/build timestamps differ). Checkpoints 1-6 were validated on `7d3416aa…`. Fix 3 (15-puzzle layout) superseded it with SHA-256 `be6e619e657ec8308396f35a0d23e3ef6371237d267483895ec3089a449c19c1`, 53,223,341 bytes, built from `92a185f` by `uv run --locked --group android buildozer -v android debug` (build start `2026-10-11T01:33:32+02:00`, exit 0 `2026-10-11T01:33:59+02:00`; log `/home/oriol/android-build/evidence/build-phase4-fix-fifteen-layout.log`). The only source delta is the one-line `sample.py` cap plus its regression test; the bundled `game_15puzzle/sample.pyc` was disassembled to confirm the `/ 2` is present. From checkpoint 7 onward, validate on `be6e6196…`, preserved at `/home/oriol/android-build/evidence/phase4-fix-fifteen-layout/clasicgames-1.2-arm64-v8a-debug-FIXED.apk`. Manifest re-inspected: `org.games.clasicgames`, versionName 1.2, versionCode 1024102, min/target 24/36, `arm64-v8a`, v2-signed.

Repair #4 (Snake phantom swipe, checkpoint 11) superseded `be6e6196…` with SHA-256 `8bc32723de30b90e290e5904338eab561d4968400021c0e167b0578d71e6848e`, 53,223,401 bytes, built from the `/home/oriol/android-build/mdclassic_games` worktree by `run-checkpoint4-build.sh phase4-checkpoint11-snake-fix` (exit 0, `2026-10-11T14:43:44+02:00` to `2026-10-11T14:44:11+02:00`; log `/home/oriol/android-build/evidence/phase4-checkpoint11-snake-fix.log`). The only source delta is `snake/gameboard.py` plus its regression test; the packaged `snake/gameboard.pyc` was inspected and contains `snake_swipe` with no `swipe_x`/`swipe_y`. It is preserved at `/home/oriol/android-build/evidence/phase4-checkpoint11/clasicgames-1.2-arm64-v8a-debug-SNAKEFIX.apk`. Checkpoints 1-6 are valid on `7d3416aa…`, checkpoints 7-10 on `be6e6196…`, and checkpoint 11 onward on `8bc32723…`; checkpoint 12 must re-confirm the final hash.

Known limit: only `WindowInsets.Type.systemBars()` is padded, not the display-cutout safe inset. On a wide-notch (non-punch-hole) device the top app bar could render near the cutout; neither test device exercises this.

Known limit: the app layouts are not responsive. In landscape most screens and games are not usable (the drawer shows only the fixed entries, Ahorcado/Memory stretch, 15-puzzle loses its bottom controls); only Pong behaves. `orientation = all` is pre-existing since the first version and landscape was never designed for. The user deferred landscape work to a separate task during checkpoint 11, so it is recorded rather than fixed here.

Complete means required checks passed and the checkpoint was reviewed and committed. Pending / In progress / Blocked describe remaining work. Update this tracker and the master summary at every handoff. Record each manual row as PASS / FAIL / NOT RUN with an observation, tester, date, device, and artifact hash.

## Objective and boundaries

Validate all seven games and existing controls using touch on at least one compatible physical device or emulator, including real display and audible output. Preserve game rules, configuration keys, package identity/version, and existing lifecycle intent.

Allowed changes are validation records, precise Android instructions, and minimal reproduced Android compatibility fixes under the combined app, its spec/dependency declarations, and `tests/mdclassic_games/`. A spec/dependency/native-toolchain fix reopens the relevant Phase 3 checks. Do not edit assets, standalone games, `resources/`, historical APKs, or root `requirements.txt` here. Do not add background services, new gestures, gameplay-state persistence, or speculative permissions.

## Checkpoint workflow and evidence

1. Inspect `git status --short`, preserve user edits and desktop `main.ini`, and confirm the artifact currently installed matches the intended input state.
2. Execute one checkpoint only. When manual work is delegated to the user, provide exact actions and ask for observations per row. Keep them NOT RUN until reported; “looks good” without knowing what was exercised does not fill unrun rows.
3. Record commands/directories, test counts, manual results, artifact/device IDs, log locations and timestamps, first meaningful failure, and next action using the master template.
4. Stop for review. Commit only on request and confirm the reviewed checkpoint is committed before advancing. A blocker report may be committed but remains blocked.

Session instruction (replace `N`):

> Read the Phase 4 runbook, master plan, and validation record. Execute checkpoint N only on the recorded APK/device. Preserve existing work and app data, collect observations/logs, run required regression checks after any fix, update evidence, and stop for review. Do not commit or begin the next checkpoint.

Use this per-scenario record:

```text
Scenario ID / checkpoint:
Tester / timestamp:
Device model / Android release and API / ABI / orientation:
APK path / SHA-256 / input revision or diff:
Initial state (fresh defaults / persisted settings / running game):
Actions:
Expected result:
Observed result: PASS | FAIL | NOT RUN, with visible/audible/state details
Logcat path and time range / screenshot if useful:
Failure classification / regression test / rebuild and retest reference:
Next exact action:
```

Store full logs and screenshots outside tracked source; record their locations and relevant excerpts. Do not commit unrelated device logs. Replace `<adb-path>`, `<serial>`, `<apk-path>`, and other placeholders below with exact recorded values before execution.

## Checkpoint 1 - Identify the target and preserve existing data

### Artifact gate

1. Locate Phase 3's completed clean build, inspection, and final full pytest results. Verify the local artifact hash equals that record.
2. Record package `org.games.clasicgames`, versionName/versionCode, actual launcher component from the APK manifest, ABI list, minimum/target API, and signing certificate information. A changed artifact requires its own inspection/evidence.
3. Verify there are no unbuilt runtime/spec/dependency changes. If code changed since Phase 3, build and inspect those inputs before using this phase to accept them.

### Device gate

Use the selected SDK's ADB. From any working directory, with explicit executable and target:

```bash
"<adb-path>" version
"<adb-path>" devices -l
"<adb-path>" -s "<serial>" shell getprop ro.product.model
"<adb-path>" -s "<serial>" shell getprop ro.build.version.release
"<adb-path>" -s "<serial>" shell getprop ro.build.version.sdk
"<adb-path>" -s "<serial>" shell getprop ro.product.cpu.abilist
"<adb-path>" -s "<serial>" shell pm path org.games.clasicgames
```

1. Ask the user to enable debugging and approve the host connection if needed. `unauthorized`/`offline` is a device-access blocker, not an install failure. Use `-s` on every ADB command so another attached device is not selected accidentally.
2. Record whether this is physical hardware or an emulator, screen size/density, navigation mode, Android build/API, ABI, and available browser/audio output. Verify API is at least the APK minimum and the target supports a built ABI. Record emulator system-image identity if used.
3. Choose a disposable test device/profile/emulator with no valuable installation data. If the package already exists, determine whose data it contains. Do not uninstall, run `pm clear`, or use a reinstall as a substitute for a fresh-default test on a user's installation.
4. Prefer a new disposable emulator/profile for clean startup. Multi-user profiles need explicit user-aware install/launch commands verified for that Android version; otherwise use a dedicated test device to avoid ambiguity.
5. Record test-data consent and starting state. On a disposable existing installation only, explicit user approval may permit clearing/uninstalling for the clean test. Record exactly what was removed. Protect existing debug keystores as well as app data; signing mismatch is not a reason to erase a user's installation.

### Gate

One authorized, explicitly selected, compatible target and a safe fresh-data strategy exist. The exact Phase 3 artifact is available and matches its hash. If only an x86_64 emulator is available for an arm64-only build, return to the Phase 3 ABI decision rather than declaring device tests skipped/passed.

## Checkpoint 2 - Install fresh and validate startup/defaults

### Capture before launch

The spec currently has `android.logcat_filters = *:S python:D`. That can hide AndroidRuntime, linker, SDL, native crashes, and activity errors. Keep a full-device capture in a separate terminal for the bounded test session:

```bash
"<adb-path>" -s "<serial>" logcat -v threadtime
```

Save stdout/stderr to a recorded external log file using the terminal/tool's capture facility and record launch timestamps. Stop capture after the session. Do not use `logcat -c` to erase unrelated device logs; use time ranges for analysis. An optional package/PID filter can aid reading, but retain the full bounded capture because PIDs change on restart and native messages may come from other processes.

### Install and launch exact artifact

On the clean dedicated target:

```bash
"<adb-path>" -s "<serial>" install "<apk-path>"
"<adb-path>" -s "<serial>" shell am start -W -n "<manifest-launcher-component>"
```

Record exit status and full install/launch output. Do not add `-r` on the first install merely to hide a pre-existing installation. `INSTALL_FAILED_NO_MATCHING_ABIS`, minimum-SDK failures, and signature conflicts require their respective ABI/API/data decisions, not a package-name change.

The master-plan convenience commands remain available from **`source/MDclassic_games`** when exactly one intended device is selected and Buildozer's output is verified as the recorded APK:

```bash
uv run --locked --group android buildozer android deploy run
uv run --locked --group android buildozer android logcat
```

Use explicit ADB installation when artifact or device selection would otherwise be ambiguous. Do not count Buildozer's Python-filtered log alone as a complete crash capture.

### Startup exercise

1. Wait through splash and loading to the usable menu; record approximate startup duration. A displayed splash or activity-start success is not app startup success.
2. Verify seven tile images/labels, readable drawer font/icons, drawer open/close, and About/CLOSE. Confirm at least one control responds after the first render.
3. Confirm no packaged `main.ini` supplied local desktop settings. Open settings and compare fresh values with current `MainApp.build_config`, not with the developer's desktop config. At review time defaults are:

   | Section | Defaults to verify |
   | --- | --- |
   | `Pong` | speed 10, max-speed 50, skin original |
   | `Ahorcado` | man1, keyboard2 |
   | `Memory` | level 6, theme starwars |
   | `fifteen` | level 1, theme numbers |
   | `Snake` | speed 1, size 11, mode 1, level_start 1 |

   Read defaults again if an approved prior fix changed them. Do not require numeric config values to have a particular Python type in the visible settings UI.
4. Inspect startup logs for Python tracebacks, native import/link failures, missing KV/font/image/audio resources, and configuration-write failures. Separate harmless system messages from app failures with timestamps/process context.

### Specific risk: desktop guards running on Android

`main.py` currently uses `sys.platform.startswith('linux')` before Kivy imports to set `SDL_AUDIODRIVER=alsa` and configure mouse multitouch. Android's Python can report Linux through `sys.platform`; the prior record's “Linux-only” intent is not proof these branches exclude Android.

If logs show audio/input initialization problems, record actual Android platform/environment and SDL/provider selection. Inspect pinned Kivy platform detection and p4a startup environment. If reproduced, make the smallest guard correction that reliably separates desktop Linux from Android **before provider initialization**, preserves a user's explicit SDL driver, and retains the desktop workaround. Add a display-independent subprocess regression for the guard decision where practical, plus existing desktop audio/input regressions. Do not set Android to ALSA or dummy audio, remove sounds, or treat an emulator mute setting as a successful audible check. Follow the repair loop below before retesting startup.

### Gate

Fresh installation reaches a responsive menu with correct defaults and resources, without app-fatal log errors. Record audible verification later; successful startup does not complete every provider/game check.

## Checkpoint 3 - Shell, navigation, and settings through touch

### Settings before and after game creation

Begin a fresh process for each settings panel. A fresh process means terminate and relaunch this test app, not clear its settings. Verify it starts at the menu; do not open the corresponding game first. `MainApp.on_config_change` itself may create that game's screen, which is the behavior under test.

For each of Pong, Ahorcado, Memory, 15 puzzle, and Snake:

1. Relaunch to a menu-only process and open its settings panel.
2. Change one visible setting, record key and old/new values, then open its game and verify the selected value is applied. Use actual panel ranges/options.
3. Change a relevant setting again after the screen exists; verify both displayed setting and game behavior/image/board update. If a setting applies at next restart, start a new round before judging it.
4. Exit normally, relaunch without clearing data, reopen panel/game, and verify the chosen values persist.
5. Retain these values as recorded test data, or restore them through the UI for a later defaults scenario. Do not modify the repository's desktop `main.ini`.

### Navigation matrix

Relaunch to a menu-only process after the settings exercises so first-entry notification checks do not accidentally reuse screens constructed by settings callbacks. For `pong`, `ahorcado`, `memory`, `fifteen`, `2048`, `buscaminas`, and `snake`:

1. Tap the menu tile once and observe the correct screen/title. On first lazy entry, observe the loading notification; it must not crash or block controls.
2. Return to menu through the drawer, open the same game through its drawer entry, and repeat return/re-entry. Verify controls work and there is no duplicate screen or accelerated update behavior.
3. Record a separate result for tile route, drawer route, and re-entry per game. Do not count visiting Pong as proof of all seven lazy constructors.

Verify About text/version, CLOSE, settings-panel dismissal, and drawer Exit. Keep Help's actual browser and Back behavior for checkpoint 11. Any game construction failure blocks the relevant navigation row; apply the repair loop, then repeat it before closing this checkpoint.

### Gate

All seven tile/drawer/re-entry routes pass using touch. All five panels work before/after screen creation and persist settings across restart. No required row is silently deferred as passed.

## Checkpoints 4-10 - Validate one game at a time

Complete each row as a separate checkpoint, including observations, logs, any minimal fix/regression, review, and commit. Read its actual `screen.py`, board/widget handlers, and settings JSON first; use existing on-screen controls, not invented gestures or a hardware keyboard.

For every row: enter via tile, perform the exercise, return via drawer, reopen via drawer, and verify retained controls/state follow existing behavior. Check the listed controls in portrait and landscape; record visible clipping, wrong touch targets, and unusable controls as failures. Checkpoint 11 adds rotation **during** play and backgrounding.

| Checkpoint | Game / source folder | Required actions and observable results |
| --- | --- | --- |
| 4 | Pong / `pong` | Start and restart; ball visibly moves; drag both paddles using actual touch areas; let a ball exit and observe the correct score increment/serve. Tap pause and confirm motion stops, then resume and confirm one normal-speed update stream and correct icon. Change speed/max-speed and skin via settings; verify effect on a new round where needed. Hear a representative game sound and exercise mute if present. |
| 5 | Ahorcado / `ahorcado` | Start a new word; use the on-screen keyboard for a correct and a wrong letter; verify repeated occurrences reveal and wrong input changes the man image. Exercise keyboard/man choices and any existing hint control without inventing a new rule. Verify Spanish characters are readable, images update, and restart works. Observe a win/loss if practical; record actual reachability rather than claiming an unseen outcome. |
| 6 | Memory / `memory` | Reveal a mismatching pair and verify both return hidden under existing timing; find a match and verify it remains revealed/count updates. Restart; exercise level/theme chips and settings. Cycle every selectable theme and start a 20-pair board in each (the current maximum); verify backs/faces exist. Explicitly reveal cartoons `.ico` faces. Check matching/mismatch/completion sound where reachable. A frame/placeholder without an actual face is not a decoding pass. |
| 7 | 15 puzzle / `game_15puzzle` | Move an adjacent tile into the gap and verify nonadjacent taps do not move tiles. Shuffle/restart; cycle all supported 3x3/4x4/5x5 sizes and selectable complete themes. Verify all numbered/image tiles and matching reference image, with usable chips and board touch targets. Return/re-enter and exercise another legal move. |
| 8 | 2048 / `game_2048` | Use all four on-screen direction controls. Reach a visible merge and check score increment; undo and verify previous board and score return. Exercise target-score chip and restart. Attempt a no-op direction when reachable and check no spurious move/score. Do not inject debug boards into the accepted APK; exact four-tile boundary cases remain covered by desktop regressions. |
| 9 | Buscaminas / `buscaminas` | Start a board with the face control, reveal cells, change level, and restart. Tap toolbar flag mode, tap a covered cell to flag/unflag, verify counter/icon, switch back to reveal, and verify flagged cells are protected. Use touch flag mode, not desktop right-click. Trigger mine-hit/loss and check displayed outcome; test cleared-board outcome if reachable and report if not. Exercise mute/help controls where offered. |
| 10 | Snake / `snake` | Start and turn using existing touch controls; eat food and observe growth/score; test collision/game-over and restart. Pause/resume and verify motion/icon. Exercise speed, size, mode, and starting-level settings within supported ranges; verify board/progress indicator remains usable. Return/re-enter a running round and check for duplicate motion or lost direction controls. |

For chance-dependent outcomes, use normal play on a small/easy supported board. Do not alter game rules or ship a debug menu to make validation easier. The master plan allows an outcome popup “if reachable” for Buscaminas; annotate such conditional outcomes honestly. If a required nonconditional action cannot be exercised, keep the row blocked rather than replacing it with a desktop test.

### Per-game gate

Required actions pass on the recorded device/artifact, with observable board/score/control results and relevant provider logs checked. A fixed game is retested on the rebuilt APK, not only through a desktop regression. Keep a table of checkpoints and artifact hashes when a repair changes the APK midway through the phase.

## Checkpoint 11 - Lifecycle, rotation, providers, and external Help

Use full logcat capture again. Record initial settings and app/game state so a restart can be distinguished from an actual resume. Do not require saved in-progress games where the existing app has no such feature; require usable behavior, persistent settings, and no newly introduced crash/freeze/lost controls.

| Scenario | Exact exercise | Passing observation |
| --- | --- | --- |
| Android Back | From menu, an open drawer, About, settings, and each game, press system Back; relaunch if it exits | Document actual existing dismissal/exit behavior; no traceback, stuck overlay, or unusable controls. Do not impose a new Back-to-menu feature. |
| Rotation | With auto-rotate enabled, rotate portrait -> landscape -> portrait at menu, settings, and during each game; exercise a control after each change | Board/labels/dialogs redraw, touch coordinates still match visible targets, controls remain accessible; no new duplicate updates. |
| Background/foreground | During Pong, Snake, a Memory mismatch, and a 2048 move, press Home, wait a recorded interval (e.g. 10 seconds), then return through recents | Record whether process resumes or restarts; either follows existing supported behavior without crash/freeze or unusable controls. No requirement for newly invented background play. |
| Screen lock | During a running game, lock then unlock the device and return | Display/GL/audio recover; inputs respond; no new fatal provider error. |
| Help round trip | Open drawer Help and existing game-specific Help where provided; verify the requested URL/browser, then return | Existing URL opens and app remains usable. No browser or unavailable network is an explicit blocker for that check, not justification for adding INTERNET speculatively. |
| Normal exit/relaunch | Exit via drawer, launch again, check changed values in all five settings panels and start a game | Settings persist, app remains usable. Do not require preservation of the in-progress board. |
| Cold process relaunch | On the dedicated test installation, force-stop `org.games.clasicgames`, relaunch, then inspect settings/game | Settings persist independently of in-memory screen state. Do not use `pm clear`, which deletes the data being tested. |
| Repeated re-entry | Leave/re-enter running Pong and Snake three times through the drawer; pause/resume afterward | No visibly multiplied speed, repeated callbacks, crashes, or lost controls. |
| Audio/mute | Hear representative start/move/win-or-loss sounds; toggle existing mute controls off/on; repeat after foregrounding | Actual audible output and mute behavior, not merely a successful `SoundLoader` call. |
| Image/font providers | Display cartoons ICOs, representative app GIFs, font/icons, themed images; revisit after rotation/foreground | Real decoded images/glyphs, no blanks/missing-asset errors. Expect GIF animation only where the existing app uses it. |

For a cold process relaunch, the targeted command is:

```bash
"<adb-path>" -s "<serial>" shell am force-stop org.games.clasicgames
"<adb-path>" -s "<serial>" shell am start -W -n "<manifest-launcher-component>"
```

Read `MainApp` and pinned Kivy/p4a lifecycle behavior before fixing a failure. There are currently no explicit app `on_pause`/`on_resume` methods in the reviewed source. Do not blindly add `on_pause: return True`: retaining a process without restoring GL/widgets/audio can make lifecycle behavior worse. Reproduce the failure, identify the relevant event/resource, and repair only that behavior. Record pre-existing unrelated lifecycle limitations separately, with evidence for that classification.

### Gate

Required lifecycle, touch/layout, provider, audio, and browser round-trip observations pass. Logcat has no unexplained app-fatal Python/native/AndroidRuntime errors in the tested intervals. Environmental limitations leave specific checks blocked.

## Repair loop - Use after any failed checkpoint

1. Record exact artifact hash, device, starting state, shortest reproduction, timestamp, and first relevant log excerpt. Keep the full log. Classify installation/toolchain, packaged asset/native dependency, application compatibility, environment/device, or pre-existing unrelated behavior.
2. Reproduce once with the same inputs. Verify the installed artifact and do not repeatedly rebuild unchanged code for an ADB/network issue.
3. Make the smallest in-scope repair. Use the pinned sources for Kivy/KivyMD/p4a APIs. Do not catch and discard errors, substitute blank images, disable sound/games, or reset all settings as a generic fix.
4. Add a meaningful desktop regression where reproducible. Use `tests/mdclassic_games/integration/test_<game>.py` for real widget/control defects, unit resource tests for source/spec omissions, and the existing subprocess fixtures for provider/bootstrap isolation. Record Android-only reproduction steps when desktop tests cannot exercise it.
5. Run affected pytest tests from repository root. For shared shell, lifecycle, configuration, or dependency changes run the established cross-app suite as well. Use the established display/GL environment; no passing required skips.
6. If runtime, dependencies, spec, or packaged inputs changed, rebuild with Phase 3's exact command from `source/MDclassic_games`; inspect the new APK and record its new hash. A toolchain/recipe/ABI change also requires a renewed clean-app-build reproduction. Update Phase 3 evidence rather than silently continuing with an unrecorded toolchain.
7. Install the new APK on the dedicated test installation. For a same-signature update preserving test settings, use `adb -s <serial> install -r <apk-path>` with actual executable/paths. Record update versus fresh install. Resolve signing conflicts without deleting valuable data.
8. Repeat the failing scenario, the complete affected checkpoint, and shell startup/navigation. For shared dependency/provider fixes, repeat all potentially affected game/resource/lifecycle checks. Repeat fresh-default startup on a disposable clean installation when bootstrap/default/config behavior changed.
9. After the final fix run the full desktop suite and finish the final-artifact coverage review below. Never apply results from an old APK to changed behavior without a documented retest.

## Checkpoint 12 - Final artifact acceptance and Phase 5 handoff

1. Freeze final runtime/spec/dependency inputs. Identify the exact final APK path/hash and build/inspection evidence. If it changed during Phase 4, record why and which previous rows were invalidated.
2. Build a coverage table listing every checkpoint/scenario, device, tested APK hash, observation, and final-artifact retest or explicit unchanged-input justification. Repeat all affected checks after a fix. On the final artifact, always confirm startup, all seven game entries/basic controls, settings persistence, representative audio, and one rotation/background cycle to catch installation mix-ups.
3. Locate the full desktop pass for this final state. Reuse Phase 3's pass only if tested code, dependencies, spec, fixtures, and environment did not change; cite the exact entry. Otherwise run from repository root in the established GUI environment:

   ```bash
   uv sync --locked --group dev
   uv run --locked --group dev pytest
   ```

   Record counts, failures/skips/xfails, and applicable CI results. Device tests and pytest are separate gates.
4. Review logcat for all tested intervals and classify outstanding messages. Keep failures/open unrelated issues explicit. Do not advertise validation on Android versions/ABIs that were not tested.
5. From repository root run `git diff --check`, `git status --short --untracked-files=all`, and `git diff --stat`; review new files and preserve desktop `main.ini`. Confirm no test data, APKs, keys, caches, or device logs are staged.

### Phase 4 completion gate

- [ ] Fresh-default installation/startup passes on at least one named compatible target.
- [ ] All seven games, touch controls, navigation, and five settings panels pass; settings survive relaunch.
- [ ] Required ICO/GIF/font/audio, Back, rotation, foreground/background, exit, and Help checks pass.
- [ ] No required check is hidden by a skip or unreported environmental limitation.
- [ ] Every fix has appropriate regression evidence and required APK rebuild/inspection/device retest.
- [ ] Final input state has a full pytest pass and final-artifact device evidence.
- [ ] Validation record contains device/OS/API/ABI, artifact hash, commands, observations, logs, known issues, and next action.
- [ ] Changes are reviewed and committed; trackers identify Phase 5 checkpoint 1 as next.

Hand off to [Phase 5](mdclassic_games_phase5_handoff_plan.md) with the actual tested matrix and exact limits of Android validation. If device access or required observations are unavailable, hand off a blocker report instead and leave modernization partial.
