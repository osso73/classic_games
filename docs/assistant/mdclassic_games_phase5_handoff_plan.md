# MDclassic_games Phase 5 runbook - Final documentation and handoff

Reviewed: 2026-10-09. Status: **not executed; requires Phases 3-4 acceptance**.

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 3 runbook](mdclassic_games_phase3_android_plan.md), [the Phase 4 runbook](mdclassic_games_phase4_device_plan.md), and [the validation record](mdclassic_games_validation.md). This runbook expands master-plan Phase 5 only. Turn recorded working procedures into accurate setup/test/build instructions and verify them in a fresh desktop environment.

## Progress tracker

| Checkpoint | Task | Status | Evidence / remaining work |
| --- | --- | --- | --- |
| 1 | Audit acceptance evidence and documentation | Pending | Final tested matrix; stale instructions inventory |
| 2 | Generate and verify runtime requirements export | Pending | Functional export; dev/Android tools excluded; isolated pip check |
| 3 | Reconcile setup/build/test documentation | Pending | Consistent commands, prerequisites, limits, test contribution notes |
| 4 | Follow instructions in a fresh environment | Pending | Locked setup, desktop launch/full suite, matching build evidence |
| 5 | Final scope review and completion handoff | Pending | All gates, review/commit, final summary and known issues |

**Next exact action:** complete Phase 4 and its final-artifact regression gate, then execute checkpoint 1 only. Documentation may record a blocker earlier, but that does not permit marking Phase 5 or modernization complete.

Complete means required checks passed and changes were reviewed and committed. Update this tracker, the master summary, and actual evidence at checkpoint handoffs. Preserve historical failure entries; append corrections rather than rewriting failed runs as successes.

## Objective and boundaries

Allowed changes:

- MD-app sections of `README.md` and `docs/getting-started.md`.
- Root `requirements.txt`, generated from the authoritative uv project.
- Runbook status/link corrections and validation records under `docs/assistant/`.

Dependencies, application code, spec, tests, and CI should already be accepted. If this phase discovers a defect, reopen the owning checkpoint, make the smallest evidenced repair, and repeat its affected gates before returning here. Do not hide it in a documentation change. Do not edit standalone games/instructions beyond clarifying their separation, `resources/`, assets, application version, `main.ini`, generated `site/`, or `releases/`.

## Checkpoint workflow

1. Inspect `git status --short` and preserve existing edits and settings.
2. Execute one checkpoint only, with explicit working directories and actual version/status evidence.
3. Record commands, outcomes, counts, logs, decisions, and next exact action using the master-plan template.
4. Run `git diff --check`, review tracked diffs and new files, and stop for review.
5. Commit only on user request. Confirm reviewed changes are committed before advancing. Missing required evidence remains blocked, even if its documentation is committed.

Session instruction (replace `N`):

> Read the Phase 5 runbook, master plan, and validation record. Execute checkpoint N only. Preserve existing changes, verify documentation against actual recorded inputs/results, update evidence and next action, and stop for review. Do not commit or begin the next checkpoint.

## Checkpoint 1 - Audit evidence and stale instructions

From repository root:

```bash
git status --short
uv --version
uv lock --check
```

1. Verify Phase 2 desktop manual/full-suite/CI gates, Phase 3 first and clean builds plus APK inspection, and Phase 4 final-device gates. Record exact validation entries and commit/input states. A selected toolchain matrix without build/device evidence is incomplete.
2. Read final metadata, lock, `.python-version`, spec, pytest configuration, tests/fixtures, and the actual focused CI workflow. Confirm Phase 2 created `.github/workflows/mdclassic-games-tests.yml`; document the real filename if an approved change selected another name.
3. Inventory stale statements in `README.md`, `docs/getting-started.md`, and active runbook summaries. At review time the public docs still describe the historical KivyMD 1.2.0 resource failure, `requirements.txt` as awaiting export, and setup as provisional. `docs/getting-started.md` also refers to `game.spec` rather than the combined app's `buildozer.spec`.
4. Clarify the Phase 1 runbook's historical “not executed” header if still present, linking its completion record and the later approved dependency change. Preserve its original 1.2.0 procedure as historical instructions; do not silently replace historical evidence with the final baseline.
5. Build a tested matrix for the final docs:

   | Area | Values and evidence to include |
   | --- | --- |
   | Desktop | OS/architecture, Python minor and observed patch, uv, Kivy/KivyMD, Pillow/materialyoucolor, relevant native/transitive differences |
   | Test environment | pytest, display/GL/audio setup, unit/GUI/full counts and date, focused CI run URL/result/input revision |
   | Android host | OS/architecture, host Python, uv, Buildozer, Cython/required build tools, JDK, SDK tools |
   | Android embedded | p4a commit, Python/hostpython, runtime/native dependency versions, API/minimum/NDK/NDK API, ABIs |
   | Artifact | Debug APK path/hash, input state, build/inspection/clean-reproduction references |
   | Device | Model/emulator image, Android release/API/ABI, tested artifact and date, required manual observations |

Use separate “selected”, “built/inspected”, and “device-tested” columns or explicit labels. Do not imply all desktop patches/operating systems or every API above minSdk were tested.

### Gate

All prerequisite acceptance evidence exists and matches final inputs; stale statements and the final tested matrix are identified. If a required gate is pending, record the exact missing evidence and stop final acceptance work.

## Checkpoint 2 - Generate a functional runtime requirements export

`pyproject.toml` and `uv.lock` remain authoritative. Root `requirements.txt` retains its MD-app runtime purpose; it is not an inventory for every standalone game and must not become a comment-only file.

1. Read current uv group configuration. Confirm `android` is not a default group and there are no other non-runtime default groups. With the current intended setup only `dev` is default, and `--no-dev` excludes it. If configuration changed, resolve and document the export/group policy rather than quietly publishing build tools as runtime requirements.
2. From repository root run the master-plan command exactly:

   ```bash
   uv export --locked --no-dev --format requirements-txt --output-file requirements.txt
   ```

3. Review the generated file. It must contain real runtime dependencies and locked transitive versions, with generated headers/hashes/markers intact. Do not hand-edit generated pins or delete hashes to make installation succeed.
4. Confirm pytest and its test-only dependency closure, Buildozer, Cython, and other **host-only** tools are absent. A package shared with the runtime closure is legitimate; use the graph, not a blanket name ban, for ambiguous dependencies.
5. Verify the locked KivyMD source matches the approved artifact and Python/platform markers are usable. Root project is intentionally non-packaged; the export must not require installing the app as an editable package or building a nonexistent backend.
6. Verify the export with real pip in a fresh temporary Python 3.11 environment outside the repository. Replace these placeholders with an absolute disposable path and the export's absolute path:

   ```bash
   uv venv --python 3.11 --seed "<temporary-export-venv>"
   "<temporary-export-venv>/bin/python" -m pip install -r "<repository-root>/requirements.txt"
   "<temporary-export-venv>/bin/python" -m pip check
   "<temporary-export-venv>/bin/python" -c "from importlib.metadata import version; print({p: version(p) for p in ('kivy', 'kivymd', 'pillow', 'materialyoucolor')})"
   ```

   Record interpreter/pip versions, installed runtime inventory, command results, and native host prerequisites needed. Use no `--system-site-packages`. This proves the export installs dependencies, not that Android or every standalone game works.
7. Rerun the export command with unchanged inputs and verify it introduces no further content diff relative to the first generated result. If runtime dependencies later change, regenerate and reverify the export.

Do not add tests that merely mirror every line of generated requirements. Actual isolated installation and dependency checks are the meaningful verification here. Resolver/network/native-host errors remain explicit blockers rather than reasons to publish an empty or unpinned requirements file.

### Gate

Export is functional and repeatable, installs consistently with pip on the recorded desktop host, contains the locked runtime closure, and excludes dev/Android-only tooling.

## Checkpoint 3 - Reconcile public setup, Android, and test instructions

Keep `README.md` concise and link the detailed MD-app section in `docs/getting-started.md`. Preserve standalone-game instructions in their own clearly labeled section. Make command directories visible; selecting a uv project alone does not change the app's working directory.

### Desktop setup

Include uv installation link, Python 3.11 baseline, observed supported host/prerequisites, and authoritative metadata/lock explanation. Show:

```bash
# Repository root
uv sync --locked
```

Then explicitly tell readers to change into `source/MDclassic_games`:

```bash
# Working directory: source/MDclassic_games
uv run --locked python main.py
```

Explain that `.python-version` selects a minor, not a fixed patch. Document actual display/GL/audio dependencies verified earlier, including host-specific audio setup if still relevant. Do not present dummy audio or headless tests as interactive acceptance. Explain the generated requirements alternative, its Python baseline and pip command, scope, regeneration command, and lack of Android host tools. Do not present both dependency files as independent editable sources.

### Android build/install instructions

Use the Phase 3 verified Linux host/JDK/SDK/NDK/tool versions and exact prerequisite commands. Explain host Python versus embedded Python, immutable p4a selection, and that uv locks host packages but not the cross-compiled graph. Link the tested matrix/evidence rather than recommending “latest”.

Show the established commands with separate working-directory blocks:

```bash
# Repository root
uv sync --locked --group android
```

```bash
# Working directory: source/MDclassic_games
uv run --locked --group android buildozer -v android debug
uv run --locked --group android buildozer android deploy run
uv run --locked --group android buildozer android logcat
```

State the actual output location, debug-only scope, ABI/device requirements, and how to select the exact artifact/device when using the explicit ADB procedure from Phase 4. Explain that the spec's Python log filter may omit native crash evidence and link the full-logcat procedure. Preserve package ID spelling and refer to `source/MDclassic_games/buildozer.spec`, correcting the relevant `game.spec` reference.

Do not imply existing files in `releases/` are the newly tested build. Distinguish historical downloads from the locally built validated artifact. Include the Phase 3 clean-app-build procedure or link it; avoid destructive blanket cache-cleaning commands.

### Maintained test suite and contribution notes

Document all commands from repository root:

```bash
uv sync --locked --group dev
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
uv run --locked --group dev pytest
```

Explain:

- Discovery is restricted to `tests/mdclassic_games`; historical `resources/examples/tests` and sibling games are outside this suite.
- `unit/` is display-independent; every display-dependent integration test is `gui`. Full pytest includes both and needs working display/GL.
- Shared fixtures avoid GUI imports at collection, preserve tracked config, and use temporary state. Document the actual subprocess fixture/helper used by the final tests, including bounded timeouts and cleanup.
- Tests control random choices at the production lookup point and scheduled callbacks deliberately. New regressions must assert real board/score/control outcomes rather than reimplement rules or globally mock Kivy.
- For a reproduced game bug, add a focused case to that game's existing test module; run it with the actual filename, then the full suite when shared inputs change. Do not provide nonexistent fixture/function names as examples.
- Browser/audio interaction stubs do not prove audible output, external browser behavior, or device lifecycle. Device-only reproduction steps belong in the validation record.
- Document the actual CI workflow, triggers, runner/Python/uv, verified OS/Xvfb/GL prerequisites, timeout, and failure-log handling. Include its GUI command: `xvfb-run -a uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration`.
- Missing display/provider is a blocker, not a passing job of skipped tests. Include actual focused CI evidence and how to locate its logs.

Link the validation record and final tested matrix. Remove provisional/outdated failure claims only when their replacements are supported by evidence. Keep unrelated known issues and untested platforms explicit.

### Gate

Both public documents agree on the baseline, working directories, authoritative dependency policy, supported build procedure, test commands, and actual acceptance status. Every technical prerequisite/claim is traceable to a verified run or clearly marked untested scope.

## Checkpoint 4 - Follow the instructions in a fresh environment

1. Create a disposable local checkout/copy of the reviewed final files outside the working repository. Record revision and any explicitly included pending documentation/export diff. Do not copy `.venv`, `.buildozer`, `bin`, caches, local `main.ini`, or APKs into the fresh environment. Preserve the original user's state.
2. Provision Python 3.11 and uv as documented, using no global KivyMD/Buildozer or system-site-packages. Record actual patch, uv, OS, and native system prerequisites. Retaining uv's download cache is acceptable; the project environment itself must be new.
3. From the fresh repository root follow the documented locked sync. Verify environment interpreter and distribution versions with `importlib.metadata`, then run `uv pip check` and `uv lock --check`. If setup unexpectedly requires an undeclared package, repair the instructions/declaration and repeat in a new environment.
4. From the fresh `source/MDclassic_games` directory run the documented desktop launch. Confirm usable menu, one game entry, and normal exit with temporary/disposable settings. This fresh-setup smoke test supplements the prior complete desktop manual matrix.
5. In the same fresh checkout run from its root:

   ```bash
   uv sync --locked --group dev
   uv run --locked --group dev pytest
   ```

   Use the documented real/virtual display and native providers. Record collected/passed/failed/skipped/xfail counts and temporary config isolation. Do not reuse an earlier full-suite run for this required fresh-environment test.
6. Verify the Android instructions against Phase 3's clean-build evidence, comparing spec, runtime/host pins, prerequisites, command, and working directory. Reuse that evidence explicitly if all build inputs/instructions are unchanged; another expensive Android rebuild is not required solely for a documentation boundary. If the procedure or inputs changed, execute the new clean-app-build procedure and inspect the new artifact; repeat affected Phase 4 checks for changed runtime inputs.
7. Confirm focused CI evidence applies to final tested code/dependencies/configuration. If relevant changes need a remote run and remote execution is unavailable, leave CI acceptance pending. Do not fabricate a CI pass from local Xvfb results.

### Gate

Documented fresh desktop setup, launch, and full test command pass without hidden global Python packages. Functional pip export has checkpoint-2 evidence. Android instructions have matching clean-build and device evidence. Any newly discovered failure is fixed and revalidated at its owning phase.

## Checkpoint 5 - Final scope review and completion handoff

From repository root:

```bash
git diff --check
git status --short --untracked-files=all
git diff --stat
```

Review the full modernization change range against the recorded pre-modernization base as well as current diffs; do not select an arbitrary base commit. Inspect new file contents separately. Confirm:

- Changes remain within approved app/dependency/test/CI/docs/spec scope.
- No test-generated `main.ini` changes, SDKs, generated `site/`, caches, APKs, device logs, keys, or sibling-game/example edits are included.
- Runtime export matches final metadata/lock and no accidental broad upgrades occurred.
- Package ID `org.games.clasicgames`, app version/title, assets, and controls are preserved except documented behavior-preserving repairs.
- Compatibility edits and any intentionally repaired behavior defects are summarized with their regressions; unrelated open issues remain visible.

### Final acceptance checklist

- [ ] Phase 1 reproducible environment is recorded as complete with later approved baseline decisions linked.
- [ ] Phase 2 desktop manual, meaningful unit/GUI/full tests, isolation, and focused CI pass.
- [ ] Phase 3 pinned host/native toolchain, debug build, inspection, and clean-app-build reproduction pass.
- [ ] Phase 4 required game/touch/settings/provider/lifecycle checks pass on a named target and final artifact.
- [ ] Root requirements export is functional, generated, runtime-only, and isolated-install verified.
- [ ] Public docs give consistent working directories, prerequisites, setup/build/deploy/test commands, tested matrix, and accurate scope.
- [ ] Fresh desktop setup/launch/full-suite checks pass; matching Android build evidence is cited or rerun.
- [ ] All phase trackers and master summary reflect actual evidence with no pending required checks hidden.
- [ ] Final changes are reviewed and committed only on user request.

Update the validation record with final commands/counts, artifact/device matrix, CI references, compatibility summary, known unrelated issues, and completion status. If any required check failed or was not run, label the outcome **partial**, name the blocker, and provide the next exact action rather than marking modernization complete.

The final user handoff should state where to find desktop/build/test instructions, the tested version/device matrix, the debug APK path/hash (without adding it to git), and validation evidence. No release upload, Play Store publishing, signing migration, or new feature work is part of this handoff.
