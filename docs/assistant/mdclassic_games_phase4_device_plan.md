# MDclassic_games Phase 4 runbook - Android device validation

Reviewed: 2026-10-09. Status: **not executed; requires the Phase 3 inspected APK**.

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 3 runbook](mdclassic_games_phase3_android_plan.md), and [the validation record](mdclassic_games_validation.md). This runbook expands master-plan Phase 4 only. Use the final inspected Phase 3 artifact, not an older APK from `releases/`.

## Progress tracker

| Checkpoint | Task | Status | Evidence / remaining work |
| --- | --- | --- | --- |
| 1 | Identify device, artifact, and isolated test data | Pending | ABI/API match; authorized ADB target; artifact hash |
| 2 | Install fresh and validate startup/defaults | Pending | Installation, full logcat, usable shell, default configuration |
| 3 | Validate shell/navigation/settings on touch | Pending | All routes; five panels before/after game creation; persistence |
| 4 | Pong | Pending | Touch control, score, pause, settings, sound |
| 5 | Ahorcado | Pending | Keyboard/man, word/image, correct/wrong input |
| 6 | Memory | Pending | Pairs, size/themes, maximum-level themes, ICO decoding |
| 7 | 15 puzzle | Pending | Moves, shuffle, levels/themes, reference image |
| 8 | 2048 | Pending | Direction controls, merges/score, undo, target control |
| 9 | Buscaminas | Pending | Touch reveal/flag mode, levels, outcome |
| 10 | Snake | Pending | Turn/eat/collision, pause, settings, restart |
| 11 | Lifecycle, rotation, audio, and external Help | Pending | Back, background/foreground, relaunch, layout, native logs |
| 12 | Final artifact regression and handoff | Pending | Device matrix, final desktop suite, build provenance, review |

**Next exact action:** complete Phase 3, then execute checkpoint 1 only. Without device/emulator access, record Phase 4 as blocked and request the checkpoint-1 information; do not infer runtime success from an APK or desktop tests.

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
