# MDclassic_games Phase 3 runbook - Android toolchain and debug APK

Reviewed: 2026-10-09. Status: **not executed; blocked on Phase 2 acceptance**.

Read [the master plan](mdclassic_games_upgrade_plan.md), [the Phase 2 runbook](mdclassic_games_phase2_desktop_plan.md), and [the validation record](mdclassic_games_validation.md) before editing. This runbook expands master-plan Phase 3 only. Build one combined debug APK containing all seven games. Installation and interactive Android acceptance belong to [Phase 4](mdclassic_games_phase4_device_plan.md).

## Progress tracker

| Checkpoint | Task | Status | Evidence / remaining work |
| --- | --- | --- | --- |
| 1 | Verify entry gate and select a coherent toolchain | Pending | Phase 2 gate; exact version/source matrix; native dependency feasibility |
| 2 | Declare and verify the host build environment | Pending | Locked `android` group; OS/JDK/SDK prerequisites |
| 3 | Update spec and packaging regressions | Pending | Immutable p4a, Python recipes, arm64, runtime assets |
| 4 | Build the first debug APK | Pending | Complete log, recipe versions, artifact identity |
| 5 | Inspect APK contents | Pending | Manifest, native libraries, nested Python bundle, assets |
| 6 | Reproduce from a clean app build directory | Pending | Second build and inspection; desktop regression gate |
| 7 | Review and hand off the final artifact | Pending | Final evidence, review/commit, Phase 4 inputs |

**Next exact action:** finish Phase 2 checkpoints 11-12 and its required CI/manual gates. Then execute Phase 3 checkpoint 1 only. Planning these steps does not satisfy the entry gate.

Use Pending / In progress / Blocked / Complete in this table. Complete means the checkpoint checks passed and its changes were reviewed and committed. Update this tracker and the master plan's summary at each handoff; append actual results to the validation record. Selected, built, inspected, and device-tested are different statuses.

## Objective and boundaries

Allowed changes:

- Root `pyproject.toml` build dependency group and generated `uv.lock`.
- `source/MDclassic_games/buildozer.spec` and narrowly scoped output ignores in `.gitignore`.
- Packaging/resource regressions under `tests/mdclassic_games/`.
- Android setup notes in `docs/getting-started.md` and records/runbooks under `docs/assistant/`.
- Runtime dependencies or application `.py`/`.kv` only for an evidenced compatibility failure, with corresponding regression checks.

Preserve Python 3.11, Kivy 2.3.1, the locked PyPI KivyMD 2.0.0 baseline, package ID `org.games.clasicgames`, title `Classic games`, and application version `1.2`. Read the current metadata again at execution time; any approved change since this review must be explained by the validation record.

Do not change assets, standalone games, `resources/`, `main.ini`, `requirements.txt`, iOS settings, release signing, or `releases/`. Do not add custom p4a recipes, change the Python minor/framework major, or remove a runtime dependency to bypass an unsupported build. Those conflicts require a documented plan decision first. Do not install or test on a device in this phase.

## Checkpoint workflow

1. Inspect `git status --short` and preserve pre-existing work and `main.ini`.
2. Execute one checkpoint only, using exact release/source documentation. Make one bounded change and read its first meaningful failure before changing more inputs.
3. Record commands with working directories, environment, logs, version decisions, test counts, and PASS / FAIL / NOT RUN observations using the master-plan template.
4. Review tracked diffs and new files; run `git diff --check`.
5. Stop for user review. Commit only when requested; confirm the reviewed checkpoint is committed before beginning the next one. A committed diagnostic note is not a passed gate.

Session instruction (replace `N`):

> Read the Phase 3 runbook, master plan, and validation record. Execute checkpoint N only. Preserve existing changes, run its checks, append evidence and the next exact action, and stop for review. Do not commit or begin the next checkpoint.

Keep large logs, downloaded sources, SDKs, and APKs outside tracked files. Use an ignored or external evidence directory whose absolute path is recorded and which survives app-cache cleanup. Replace every `<...>` placeholder below with a verified value before running its command; never paste placeholders into metadata or the spec.

## Checkpoint 1 - Verify entry gate and select the toolchain

### Entry checks

From repository root:

```bash
git status --short
uv --version
uv lock --check
```

1. Locate Phase 2's final full-suite counts, desktop manual observations, and passing focused CI jobs. Pending CI, unrun audio, or an untested game blocks Android execution.
2. Read the current `pyproject.toml`, `uv.lock`, `.python-version`, app spec, and `tests/mdclassic_games/unit/test_resources.py`. Phase 2 checkpoint 11 may have expanded the tests since this runbook was written.
3. Record build-host OS/distribution/version, architecture, available disk space, network/proxy constraints, and whether the workspace is local or synchronized. Use a supported Linux host. If a synchronized path causes filesystem/build problems, use a recorded local checkout of the reviewed state; do not silently build older committed code while fixes exist only in the original worktree.
4. Identify the intended Phase 4 target ABI. Default is `arm64-v8a`. An x86_64 emulator cannot be assumed to run an arm64-only APK. Prefer an arm64 device; add another ABI only for an actual target and record that decision.

### Select before installing or building

Consult Buildozer releases/source and p4a releases/source. Start at the master plan's reference links, then record permalinks for the chosen versions and full p4a commit. Read Buildozer's Android target implementation to verify spec option names and how it checks out p4a. A floating documentation page is a discovery aid, not evidence for a pinned implementation.

Fill this matrix in the validation record. No value may remain “latest”, “default”, or “TBD” when checkpoint 1 passes.

| Selection | Exact value to record | Evidence/check required |
| --- | --- | --- |
| Host | Distribution/version, architecture, host Python patch, uv version | Chosen toolchain supports the host and Python 3.11 |
| Buildozer | Released version and source URL | Supports the selected p4a checkout mechanism and host |
| Host tools | Cython and any required setuptools/build tools with exact versions | Buildozer/p4a installation and recipe requirements, not guessed historical pins |
| p4a | Release/tag, full immutable commit, repository URL | Tag resolved to commit; verified Buildozer option names |
| Python recipes | `python3` and `hostpython3` exact versions | Recipe source, supported override syntax, compatibility with Python 3.11 |
| JDK | Major, vendor, actual patch and `JAVA_HOME` | Compatible with selected p4a's Gradle/Android Gradle plugin |
| Android tools | SDK command-line tools, platform-tools, build-tools versions | Actual selected tool versions and download/source references |
| Android platform | Target API, minimum API, NDK revision and NDK API | Supported together by p4a; NDK API normally equals minimum API |
| Runtime | Kivy/KivyMD/Pillow/materialyoucolor and required transitives | Exact source/version, recipe or pure-Python route, native dependencies |
| Bootstrap / ABI | SDL2 and `arm64-v8a` (plus any justified target ABI) | Supported by selected p4a and test target |

The desktop `.python-version` does not choose the Python embedded in the APK. The Buildozer host interpreter, p4a's generated hostpython, and target Python are three separate entries. Do not require their patch numbers to match without toolchain evidence; do require compatible 3.11 recipe selections and log the actual values.

### Native dependency feasibility audit

At review time the lock contains Pillow 12.3.0, materialyoucolor 3.0.4, asynckivy 0.6.4, asyncgui 0.6.3, materialshapes 0.3, and pycairo 1.29.1. Re-read the lock and package metadata rather than treating this inventory as an Android recommendation.

For each runtime package:

1. Read its metadata and any import-time native requirements in the locked source. In particular trace `KivyMD -> materialshapes -> pycairo`, plus materialyoucolor's compiled extension and Pillow's image support.
2. In the selected p4a commit, find the recipe (if present), its version, dependencies, patches, and supported architectures. Record immutable recipe links. Include Cairo/native libraries needed by pycairo and SDL2 image/audio dependencies.
3. Classify it as recipe-built native, pure Python, or unsupported. A desktop manylinux wheel is not an Android binary. An exact version override on an existing recipe does not prove its patches support that version.
4. Inspect how p4a resolves Python dependencies. Decide which pure-Python transitives must be explicitly pinned in Android requirements to avoid floating resolution; retain recipe-managed native dependencies through the supported mechanism. Record recipe-derived versions separately.
5. Assess the old explicit `requests`, `urllib3`, `chardet`, and `idna` using runtime metadata and recipes. Retain required dependencies and remove obsolete duplicates only with evidence. Do not copy the entire desktop lock into `requirements`.
6. If a supporting native version is incompatible, prefer a supported version common to desktop and Android. Document the exact proposed adjustment, constraints, and affected desktop checks. Any platform-only difference must be explicit. Keep Kivy/KivyMD aligned.

If a required native dependency has no supported build route, record the package, first conflicting constraint, inspected recipe sources, and next decision. **Stop here** rather than attempting hours of builds, disabling material widgets, or inventing a recipe. A source-based feasibility pass is permission to try the build, not proof it will succeed.

### Gate

Phase 2 passed; the matrix is complete and evidenced; required native dependencies have supported candidate build paths; no unresolved interpreter/framework decision remains. Review the selection before installing or changing the spec.

## Checkpoint 2 - Declare and verify the host environment

1. Install the OS/JDK prerequisites listed by the selected releases. Record exact package-manager commands and installed versions in the validation record and Android build instructions. Have the user perform privileged installation if necessary. Missing packages remain blockers.
2. Declare exact host tool pins under a new root `[dependency-groups].android` group. Use the verified versions from checkpoint 1, for example this **template** from repository root:

   ```bash
   uv add --group android "buildozer==<selected-version>" "cython==<selected-version>"
   ```

   Include Cython and other tools only as required by the selected toolchain; add those required tools with exact pins in the same group. Do not add them to `[project].dependencies`. Do not install floating p4a with pip if Buildozer is meant to check out the pinned source.
3. Let uv generate `uv.lock`. Review changes for unintended runtime upgrades. If checkpoint 1 approved a supporting-runtime adjustment, apply only that adjustment, update the matrix, and run the full desktop suite and affected manual checks before proceeding.
4. Verify Java selection and `PATH`/`JAVA_HOME`. Record SDK/NDK locations; different global tools must not silently override the documented selection. If Buildozer provisions the SDK during checkpoint 4, record that plan now and verify the actual tools afterward.
5. Ensure the chosen p4a subprocess invocation uses the intended uv host interpreter and can find all required build tools. `uv run` does not guarantee that every subprocess ignores global executables; inspect the first build log later.

From repository root:

```bash
uv lock --check
uv sync --locked --group android
uv pip check
uv run --locked --group android python --version
uv run --locked --group android buildozer --version
java -version
javac -version
```

Record host package versions through `importlib.metadata` without importing the GUI. `uv.lock` locks host Python packages, not the cross-compiled runtime, JDK, SDK, or NDK. The default dev group may also be installed by uv; that must not cause pytest to enter Android requirements or packaged app assets.

### Gate

Locked host sync and consistency checks pass; actual host tools match the selection; reproducible prerequisite instructions exist. Every required runtime-pin change has desktop revalidation. Do not change the spec until this checkpoint is reviewed.

## Checkpoint 3 - Update the spec and resource regressions

Edit `source/MDclassic_games/buildozer.spec` in place, retaining unrelated comments and settings.

| Setting | Required action |
| --- | --- |
| `requirements` | Pin selected Python recipes, Kivy 2.3.1, released KivyMD 2.0.0, and the evidenced runtime dependency set. Remove the master ZIP. Remove `sdl2_ttf==2.0.15` unless the chosen toolchain specifically requires it. |
| Architectures | Set active `android.archs = arm64-v8a`; remove the active singular `android.arch`. Include another ABI only if checkpoint 1 justified it. |
| APIs / NDK | Activate exact `android.api`, `android.minapi`, `android.ndk`, and `android.ndk_api` selections. |
| p4a | Use the verified immutable checkout setting (for example `p4a.commit` only if supported). If a branch is also required for fetching, it must not replace the commit pin. |
| Python | Use the chosen toolchain's verified recipe-version syntax, including compatible hostpython selection. Host `.python-version` alone is insufficient. |
| Source | Retain `source.dir = .`; add `ico` to `source.include_exts`; preserve recursive asset paths and exclusions. |
| Identity / appearance | Preserve `package.name = clasicgames`, `package.domain = org.games`, title, regex-based version, icon/splash, `orientation = all`, and `fullscreen = 0`. |
| Permissions | Preserve existing intent. `android.permissions` is currently commented. Do not enable INTERNET or storage permissions merely to fix external Help or asset access. |

Do not blindly paste a spec from current online examples. Verify each new option in the selected Buildozer source. If a declared override is ignored, the build is not reproducibly pinned.

### Source inventory and meaningful regressions

1. Enumerate runtime paths from the actual app and settings JSON, including nested themes. Reuse Phase 2's inventory/tests rather than building a second unrelated test framework.
2. Extend `tests/mdclassic_games/unit/test_resources.py` (or the existing resource module established in Phase 2) with display-independent assertions for the final spec. Parse using `ConfigParser(interpolation=None)` so the spec's `%(source.dir)s` is not accidentally expanded by the test.
3. Assert required extensions include `py`, `kv`, `json`, `txt`, `png`, `jpg`, `gif`, `ico`, `ogg`, and `ttf`; assert exclusion of `resources` and test/build directories. Check real representative paths exist, not just that an extension token is present.
4. Cover all five settings JSONs, Ahorcado word data, menu images, icon/splash, drawer font, all OGGs, Memory cartoons ICOs, and complete 15 puzzle theme tiles/reference images. Derive filenames from current sources; do not invent sample names.
5. Assert package identity, plural arm64 architecture, and no active floating KivyMD/master requirement. Do not duplicate the whole spec as a test fixture or treat these source assertions as APK inspection.
6. Confirm `main.ini`, pytest, root `.venv`, sibling games, and vendored `resources` will not be staged. Check Buildozer's actual source-filter semantics; patterns and extension lists are not interchangeable.
7. Add root-anchored ignores for `/source/MDclassic_games/.buildozer/` and `/source/MDclassic_games/bin/` if needed. Keep generated trees and APKs untracked; leave existing release APKs alone.

From repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
git diff --check
git status --short --untracked-files=all
```

### Gate

Spec matches the reviewed matrix; the resource/packaging unit checks pass; identity and source scope are preserved. APK contents and decoding remain unvalidated until subsequent checkpoints/Phase 4.

## Checkpoint 4 - Build the first debug APK

From repository root:

```bash
uv sync --locked --group android
```

With working directory **`source/MDclassic_games`**:

```bash
uv run --locked --group android buildozer -v android debug
```

Capture complete stdout/stderr in the evidence directory. When using `tee`, enable the shell's `pipefail` and check the Buildozer exit status, not just `tee`'s. A long build exceeding an agent timeout is not automatically a recipe failure: check whether the process is still running before starting another build against the same cache.

1. Record start/end times, exact command, host interpreter, SDK/NDK/JDK, disk availability, and log path. Follow the selected toolchain's license prompts; do not enable automatic acceptance as a speculative build fix.
2. Verify the p4a checkout's actual `git rev-parse HEAD` equals the selected commit. Read its path from the log rather than assuming cache layout.
3. Inspect recipe/build logs for actual target Python, hostpython, Kivy, Pillow, materialyoucolor, pycairo/Cairo, SDL2 family, and pure-Python dependency versions. Compare with the selection matrix; an ignored version pin fails this gate even if compilation succeeds.
4. Record the exact generated APK path from successful output. Hash that file with SHA-256 and record file size and input revision/state. Do not select “the newest APK” from `releases/` or deploy an old file left in `bin/`.
5. Keep full logs through checkpoint 6; copy evidence out of the app cache before any clean operation.

### Failure classification and repair loop

| First meaningful failure | Next action |
| --- | --- |
| Download, TLS, proxy, unavailable URL | Verify network and pinned URL; retry unchanged inputs only after the environment is corrected. |
| Missing executable, JDK/SDK/license, disk exhaustion | Repair the specific host prerequisite; record it in reproducible setup instructions. |
| Native compilation/link error | Identify recipe, version, architecture, failing command, and first compiler error before the final p4a exception. Compare recipe patches and native dependencies with checkpoint 1. |
| Native Python dependency falling through to pip | Verify recipe recognition and dependency names; do not install a desktop wheel into the APK or use `--no-deps` to hide the missing native path. |
| Python/KV/assets missing in staging | Check source directory, include/exclude rules, and package data. Repair declarations, not cached generated copies. |
| Stale distribution after an input change | Use the selected p4a/Buildozer documented clean mechanism for the affected app build. Verify its scope first. |
| Unsupported Python/framework/native combination | Stop with evidence and a proposed decision. Do not silently upgrade Python, downgrade KivyMD, or write custom recipes. |

Change one cause, run affected desktop tests for application/dependency/spec changes, then retry with a new log. Any toolchain change reopens the matrix and relevant prior gate. Do not manually patch `.buildozer` and count that as a reproducible fix. Do not delete global `~/.buildozer`, SDK, uv, or unrelated app caches as a generic remedy.

### Gate

Build exits successfully, actual versions match documented selections, and the artifact has an exact path/hash. This is build success only; proceed to inspection after review.

## Checkpoint 5 - Inspect the built APK

Use the exact checkpoint-4 artifact. Record inspection-tool executable paths/versions from the chosen SDK. These are command templates; replace paths first:

```bash
"<sdk-build-tools>/aapt" dump badging "<apk-path>"
"<sdk-build-tools>/aapt" dump permissions "<apk-path>"
"<sdk-build-tools>/apksigner" verify --verbose "<apk-path>"
```

If the selected SDK supplies another supported manifest inspector, document the exact equivalent. Open the APK with Python `zipfile` or a ZIP listing tool. An APK is a ZIP archive, but its application Python/data bundle may be a nested archive rather than loose files.

1. Verify manifest package `org.games.clasicgames`, version name `1.2`, debug build, target/minimum API, requested permissions, and launchable activity. Record versionCode and resolved launcher component without changing them. Debug signing verification is required for installability, not release-signing work.
2. Verify arm64 native libraries exist under the APK's ABI paths and correspond to the selected architecture. Inspect nested compiled Python extensions too. Record additional ABIs if selected; a filename containing “arm64” is insufficient.
3. Identify the app/private Python bundle by reading the selected p4a bootstrap packaging source and archive inventory. Its filename/format may differ across p4a revisions. Use the corresponding decompressor/archive reader in a scratch directory; do not assume all contents are a ZIP or tar.
4. Compare the actual bundled runtime paths against checkpoint 3's source inventory. Confirm main/menu/drawer, all seven game modules, KV, settings JSON, word data, images including ICO/GIF and complete themes, OGGs, font, and framework KV/fonts are present with correct case and nonempty contents.
5. Verify KivyMD's packaged resources, especially `kivymd/uix/label/label.kv`, given the historical installation defect. Include async libraries/materialshapes and native materialyoucolor/pycairo dependencies according to the selected packaging layout.
6. Compare hashes for representative unchanged app assets between source and packaged data. Build transformations may affect Python files; do not demand source-file hash equality for compiled `.pyc` files.
7. Verify app `resources/`, standalone examples, pytest/tests, `.venv`, host build tools, and tracked `main.ini` are absent. Framework-owned runtime directories named `resources` may be legitimate: inspect ownership rather than rejecting every matching basename.
8. Record inventory/log paths and PASS/FAIL for every category. Listing only the outer APK does not verify its nested asset bundle.

An asset present in the bundle is not proof it decodes on Android. ICO/GIF decoding, native imports, audible OGG playback, and real startup remain Phase 4 checks.

### Gate

Manifest, signing, ABI, packaged runtime dependencies/resources, and exclusions pass on the identified artifact. Any spec/dependency correction returns to checkpoint 4 for a new build/hash and repeats this inspection.

## Checkpoint 6 - Clean-app-build reproduction and desktop gate

1. Freeze the reviewed inputs and record their revision plus any pending diff. Save the first APK, hash, and logs outside the app build directory.
2. Identify the effective app build directory from the spec/log (normally `source/MDclassic_games/.buildozer`). Check that it contains generated app build state only. If a custom path points at shared SDKs or other projects, stop and separate those locations first.
3. With no build process running, move that entire app-generated build directory to a recorded external backup, or remove only that verified generated directory. An incremental Gradle clean alone is insufficient. Never run broad `git clean -fdx` or delete a global tool cache.
4. Ensure the new attempt cannot be mistaken for the previous `bin/` artifact: preserve the old artifact externally and record its timestamp/hash. `bin/` is output, not evidence of a new successful build by itself.
5. Repeat checkpoint 4 with identical pinned setup. Shared SDK/download caches may remain; record them. This proves clean **app build** reproducibility, not a network-offline or empty-global-cache build.
6. Verify the fresh p4a checkout revision and embedded versions again; repeat checkpoint 5 on the newly produced artifact. Record its distinct build log and SHA-256. APKs need not be byte-identical because signing/build timestamps may differ.
7. Use the final spec/dependencies in the established desktop test environment, including working display/GL. From repository root:

   ```bash
   uv sync --locked --group dev
   uv pip check
   uv run --locked --group dev pytest
   ```

   Record collected/passed/failed/skipped/xfail counts and final-state CI results where applicable. Required checks cannot pass through skips. A build host without a display does not waive the GUI suite; use the verified desktop/CI environment. Run affected manual desktop checks if runtime/dependencies changed.

### Gate

A second debug APK builds from clean app-generated state with the same declarations, inspection passes on it, and the full desktop suite including packaging checks passes. Record the final artifact for Phase 4; do not pass along the earlier APK by habit.

## Checkpoint 7 - Review and Phase 4 handoff

Before review, from repository root:

```bash
git diff --check
git status --short --untracked-files=all
git diff --stat
```

Review new files as well as tracked diffs. Restore only known test-generated configuration changes while preserving user edits. Confirm no APKs, caches, SDKs, or keys are staged.

### Phase 3 completion gate

- [ ] Version/source matrix is complete with immutable p4a and exact host/runtime selections.
- [ ] Locked host setup and documented OS/JDK prerequisites work.
- [ ] Spec preserves identity/version and includes arm64 plus required runtime assets, including ICOs.
- [ ] First build and clean-app-build reproduction pass with logs showing actual selected versions.
- [ ] Final APK manifest, ABI, dependencies, nested assets, and exclusions pass inspection.
- [ ] Full desktop pytest suite passes on the final input state; affected desktop manual checks pass after relevant changes.
- [ ] Validation record identifies final artifact path, SHA-256, size, input state, tool versions, logs, and inspection evidence.
- [ ] Changes are reviewed and committed; trackers identify Phase 4 checkpoint 1 as next.

Pass Phase 4 the final artifact/hash, package ID and launcher component, minimum/target APIs, supported ABIs, build/inspection logs, desktop/CI evidence, and any unrelated known issues. **Android runtime support remains unvalidated** until the Phase 4 device gate passes.
