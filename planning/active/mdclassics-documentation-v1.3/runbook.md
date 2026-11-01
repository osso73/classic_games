# MDClassics documentation and v1.3 execution runbook

Created: 2026-10-11. Status: **all checkpoints executed; awaiting final user review**.

Read the [scope and decisions](plan.md)
before executing. This runbook is intended for a smaller model using bounded,
explicit checkpoints. It implements the follow-up documentation/release task,
not the earlier modernization phases.

## Progress tracker

| Checkpoint | Status | Evidence / next action |
| --- | --- | --- |
| 1 — Audit and changelog draft | Approved | User approved the exact v1.3 entry; release date confirmed as **2026-10-12** |
| 2 — Version and MkDocs | Passed | `main.py`/`pyproject.toml` = 1.3; MkDocs 1.6.1 pinned in dev; lock/sync/pip-check pass; runtime export excludes MkDocs |
| 3 — Planning lifecycle and relocation | Passed | Modernization reconciled/archived to `planning/archive/2026-10-mdclassics-modernization/`; this plan/runbook moved to `planning/active/mdclassics-documentation-v1.3/`; tool moved to `tools/`; `planning/README.md` created |
| 4 — README and developer guide | Passed | `README.md` rewritten (no Android instructions); new `DEVELOPMENT.md` covers environment, tests, Android, release, docs and the AI planning workflow |
| 5 — Website reconciliation | Passed | index/getting-started/about/combined help updated; Android moved to DEVELOPMENT.md link; changelog copied byte-identical; strict build passes; all 7 Help anchors present; Pages settings unverified (`gh` unavailable) |
| 6 — Verification and handoff | Passed (awaiting final user review) | `uv lock --check`/`uv pip check` pass; unit 47 passed; full suite 112 passed (display `:1`); versions 1.3; changelog copy byte-identical; diffs clean; no deployment/commit; v1.3 APK build/inspection pending |

## Operating instructions

1. Read this runbook, its companion plan, and only the relevant source/evidence
   for the current checkpoint. Do not load all historical plans unnecessarily.
2. Inspect `git status --short` before editing. Preserve existing user work.
3. Update one checkpoint at a time. Keep the tracker and an execution log at the
   bottom of this file current. After relocation, update the new copy.
4. Use the patch/edit tools for file changes. Use explicit working directories
   for commands. Paths in this runbook are relative to repository root unless
   a different working directory is specified.
5. Do not spawn subagents. Do not commit, tag, push, deploy the website, upload an
   APK, or change GitHub settings without an explicit request.
6. Record actual results. Network, native-provider, SDK and device failures are
   blockers, not successful skipped checks. Read the first relevant error and
   fix its cause rather than changing broad dependency ranges.
7. Checkpoint 1 must end with a user-visible changelog and a stop. On resumption,
   verify approval exists before starting checkpoint 2.

Suggested execution prompt:

> Read the MDClassics documentation/release plan and runbook. Execute checkpoint
> N only, preserve existing changes, record commands/results and the next action,
> and stop for review. Do not commit or publish anything. For checkpoint 1, show
> the exact proposed changelog and wait for my approval.

## Checkpoint 1 — Audit and draft the changelog

### Read and establish facts

```bash
# Repository root
git status --short
git log --oneline -30
```

Read:
- `source/MDclassic_games/CHANGELOG.md` (currently a pointer with a broken link).
- `docs/changelogs/classic_games_changelog.md` (actual complete combined history).
- Root `CHANGELOG.md`, `pyproject.toml`, `.python-version`.
- `source/MDclassic_games/main.py` version declaration and `buildozer.spec`
  version extraction, requirements, ABIs and package identity.
- Relevant final modernization validation entries in
  `planning/archive/2026-10-mdclassics-modernization/mdclassic_games_validation.md` and commits for the release fixes.

Do not assume an old plan header represents current acceptance. Existing history
records a 112-test desktop result; the future guide should not hard-code a count
as a permanent guarantee.

### Edit only the authoritative app changelog

1. Copy the entire published combined-app history into the app changelog,
   retaining all old entries and dates.
2. Add an empty `Unreleased` heading above a proposed v1.3 entry.
3. Use the companion plan's draft as the starting point and verify each claim.
4. Retain the versioning convention unless the user changes it. Revise the old
   blanket claim that every version has an APK in `releases/`: a drafted v1.3
   is not yet a published artifact.
5. Use `YYYY-MM-DD` explicitly as a draft date if a release date is not agreed;
   ask for the date in the review response. Do not silently date publication.
6. Do not copy the draft to the website yet. Do not implement other checkpoints.

```bash
git diff --check
git diff -- source/MDclassic_games/CHANGELOG.md
```

### Gate and mandatory stop

Present the complete proposed v1.3 entry, describe that the existing history was
preserved, and request approval/date clarification. Record **awaiting approval**.
Checkpoint 2 cannot start until the user explicitly approves this actual draft.

## Checkpoint 2 — Bump the approved version and add MkDocs

### Preconditions

Record the user's changelog approval and selected date. Finalize that date if
provided; do not interpret changelog approval as permission to publish.

### Changes

1. Set `__version__ = '1.3'` in `source/MDclassic_games/main.py`, matching its style.
2. Set `[project].version = "1.3"` in `pyproject.toml`.
3. Confirm Buildozer still extracts the version from `main.py`; leave that
   mechanism and package identity unchanged.
4. Add MkDocs to **dev**, not runtime or a new docs group:

```bash
# Repository root; resolves a compatible release and records an exact pin
uv add --group dev --bounds exact mkdocs
uv lock --check
uv sync --locked --group dev
uv pip check
uv run --locked --group dev mkdocs --version
```

Inspect the selected version and the full `pyproject.toml`/`uv.lock` diff.
No broad `--upgrade`; preserve current runtime, pytest and Android host pins.
If `uv add` did not refresh changed project metadata, run `uv lock`, then repeat
the lock check. Never hand-edit `uv.lock`.

Re-export the committed runtime requirements with the established command:

```bash
uv export --locked --no-dev --format requirements-txt --output-file requirements.txt
```

Review any export changes. MkDocs and its dev-only closure must not enter runtime
requirements. Shared runtime dependencies are legitimate. Keep generated hashes
and headers; do not manually trim the export.

### Gate

Source and project versions are 1.3, locked dev sync and pip check pass, MkDocs
runs, and runtime pins/export remain runtime-only. Record the selected MkDocs
version and any actual export diff. No APK has been rebuilt by these commands.

## Checkpoint 3 — Relocate planning records and the provisioning tool

1. Inventory every file currently in `docs/assistant/` with dedicated file tools.
2. Reconcile modernization completion before archiving: inspect its final
   validation entries, commit `06d9862`, and final trackers. Correct stale final
   headers/trackers based on evidence; preserve chronological commands, failures,
   versions and observations. Add a completion summary with actual date,
   implementation commits, delivered work, limitations/deferred work, and this
   follow-up. Do not treat a commit title alone as proof of every gate.
   Move its Markdown files together to
   `planning/archive/2026-10-mdclassics-modernization/`, retaining filenames.
   If required completion evidence is missing, keep modernization under
   `planning/active/mdclassics-modernization/` and record the blocker.
   Move this initiative's two files to
   `planning/active/mdclassics-documentation-v1.3/plan.md` and `runbook.md`.
   Update mutual links for the renamed files. Classify any other assistant
   documents by their owning initiative rather than blindly archiving them.
3. Move `mdclassic_games_install_android_tools.py` to `tools/`.
4. Update the provisioning script's usage docstring to:

```bash
uv run --locked --group android python tools/mdclassic_games_install_android_tools.py
```

5. Add a relocation note to the moved records explaining that historically
   recorded `docs/assistant/` paths describe the locations used at the time.
   Update active future commands/path instructions and Markdown links. Preserve
   historical Files changed lists, actual commands, dates, versions and results.
6. Same-directory plan links normally survive; inspect links that traverse to
   public documents or source files and adjust them.
7. Search for remaining `docs/assistant` and `assistant/` references. Classify
   retained matches as historical, not uncorrected runnable instructions.
8. Update companion-plan prose about its initial location with the relocation
   status. Continue tracker/log updates in this file's new path.
9. Create `planning/README.md` with a status/location index and conventions:
   one folder per initiative; active plans in `active/`; completed and reviewed
   initiatives archived together as `archive/YYYY-MM-<initiative>/` using the
   actual completion date. Clearly label Cancelled/Superseded initiatives.
   Require an outcome summary, final commit references or pending commit status,
   delivered work, limitations and follow-up links before archival.
   Explain archived instructions are historical; current operations are in
   `DEVELOPMENT.md`. Keep this initiative active until completion and review.

### Verification

```bash
# Help parses arguments and exits without provisioning tools
uv run --locked --group android python tools/mdclassic_games_install_android_tools.py --help
git diff --check
git diff --stat
```

Do not run provisioning itself just to verify a file relocation. Confirm all
source files are accounted for, script logic is unchanged, and `docs/assistant/`
has no remaining project files. Do not rewrite historical modernization scope
restrictions to authorize the new work retroactively.
Check the planning index, completion summaries, evidence-backed statuses, and
cross-links between the archive, active initiative and public documents.

## Checkpoint 4 — README and developer guide

### README content

Rewrite `README.md` as a concise MDClassics entry point:
- Description, an existing screenshot, and seven included games.
- uv installation link, Python 3.11, Kivy 2.3.1/KivyMD 2.0.0 baseline.
- Explain authoritative metadata/lock and app working directory.
- Complete desktop quick start:

```bash
# Repository root
uv sync --locked
cd source/MDclassic_games
uv run --locked python main.py
```

- Link player help, `DEVELOPMENT.md`, and the app changelog.
- Brief standalone-app origins, contribution information, license/asset credits.
- No Android setup/build/install instructions.

Preserve the distinction between the MIT code license and third-party asset
restrictions. Do not silently relicense resources or invent rights.

### Developer guide content

Create `DEVELOPMENT.md`. Each command block must state its working directory.
Include all of the following:

1. Python/uv/native prerequisites and locked sync/checks. Explain runtime/dev/
   android groups and why a later uv command without `--group android` can remove
   Android host packages from the environment. Show retained-group commands when
   needed.
2. Dependency maintenance: exact targeted changes, lock regeneration, runtime
   export command, and separate Android spec pins/cross-compiled recipe graph.
3. Test commands from repository root:

```bash
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
uv run --locked --group dev pytest
xvfb-run -a uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration
```

   Read existing tests/fixtures and `.github/workflows/mdclassic-games-tests.yml`
   before describing isolation, regression-test placement, display/GL/audio,
   CI prerequisites or logs. Unit tests are display-independent; full suite
   includes GUI. Dummy audio in CI does not verify audible device output.
4. Android instructions transferred from public getting-started content and
   validated runbooks: OS prerequisites, reviewed provisioning tool, interactive
   licenses, host versus embedded Python, actual SDK/JDK/NDK paths and versions,
   package ID, API/ABI requirements, and preserved settings.
5. Android build commands with **working directory `source/MDclassic_games`**:

```bash
uv run --locked --group android buildozer -v android debug
uv run --locked --group android buildozer android deploy run
uv run --locked --group android buildozer android logcat
```

   Explain `bin/` output and debug-only packaging, historical `releases/` versus
   new local APKs, selection of the exact device/artifact, and full logcat for
   native crashes. Link detailed clean-build/device evidence at its new GitHub
   location. Do not document unsupported signed-release publishing as validated.
6. Release checklist: Unreleased entries, version/date approval, `main.py` and
   project metadata, lock refresh, tests, APK build/manifest version inspection,
   device smoke checks, changelog copy, player-doc updates, review, then requested
   commit/tag/publication. Buildozer gets version from `main.py`.
7. Documentation ownership table and complete documentation workflow:

```bash
# Repository root
cp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
uv run --locked --group dev mkdocs serve
uv run --locked --group dev mkdocs build --strict
uv run --locked --group dev mkdocs gh-deploy
```

   Explain serve is long-running, build is local, deployment pushes `gh-pages`,
   and Pages must serve that branch's root. Run deployment from the checkout
   containing the intended sources. Source commits and site deployment are
   separate operations. No new workflow or synchronization code.
8. A changes-to-documents checklist: desktop setup changes update README and
   website setup together; controls/settings changes update player help; build/
   test changes update the guide; releases update and copy the changelog.
   Generated `site/` is not source and should not be edited/committed.
9. An **AI-assisted changes** section requiring a plan and detailed runbook
   before any AI-assisted implementation:
   - Store both under `planning/active/<initiative>/` and obtain user review and
     approval before implementation. Inspection and planning may happen first.
   - Plans define objectives, scope, constraints, acceptance criteria and review
     gates. Runbooks define bounded checkpoints, relevant files, commands,
     verification steps, progress and evidence logs.
   - Execute checkpoints in order and stop at review gates; revise the documents
     and review scope changes before implementing them.
   - Record the final outcome and archive the whole initiative after completion
     and review. Link to `planning/README.md` for lifecycle conventions.
   Include this reusable prompt:

   > Inspect the relevant project files and develop a plan and checkpoint-based
   > runbook for this change. Do not begin implementation. Include scope,
   > acceptance criteria, verification steps, and review gates. Store both
   > documents under `planning/active/<initiative>/` and present them for review.

### Gate

Read both completed documents end to end. Validate referenced files, commands,
providers and directories against actual configuration. Do not put relative
outside-`docs` links into website pages; use absolute GitHub URLs there.

## Checkpoint 5 — Reconcile public help and changelog

1. Update `docs/index.md` for combined MDClassics and seven games.
2. Update `docs/getting-started.md`: correct desktop uv and isolated pip setup,
   Python baseline, prerequisites and working directory. For pip, install root
   requirements in a Python 3.11 venv, then change into the app folder before
   `python main.py`. Move Android developer procedures to `DEVELOPMENT.md` and
   replace them with a link to that guide.
3. Update `docs/about.md` consistently with README license/credits/background.
4. Audit `docs/games/classic_games.md` against current navigation, controls and
   settings. Fix the outdated future Help/About description and current version
   reference to 1.3. Preserve game heading text that supplies Help anchors.
5. Read app Help URLs in drawer and game modules. Keep their paths and fragments
   valid; do not change application URLs to accommodate an unnecessary site move.
6. Copy the authoritative approved changelog:

```bash
cp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
```

7. Update root `CHANGELOG.md` links. Keep historical standalone changelogs.
8. Keep the existing website pages/nav entries; change `mkdocs.yml` only where
   needed for accurate naming/navigation. Assistant records must no longer be
   included in the site's sources. No new MkDocs plugin is required.

### Checks

```bash
cmp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
uv run --locked --group dev mkdocs build --strict
git diff --check
```

Inspect generated HTML using file tools for the expected `/games/classic_games/`
page and each fragment from the app's Help constants. Check internal pages,
images and links. Confirm Pages settings with read-only GitHub tooling if
available; otherwise report them as unverified, with the exact settings for the
user to check. Never change settings or run `gh-deploy` in this checkpoint.

If strict build fails, record the first warning/error and distinguish new
breakage from existing standalone-page issues. Fix relevant broken links. Do not
remove pages or relax strict checking merely to claim a pass; report unrelated
remaining blockers clearly.

## Checkpoint 6 — Final verification and review handoff

Run from repository root:

```bash
uv lock --check
uv pip check
uv run --locked --group dev pytest tests/mdclassic_games/unit
uv run --locked --group dev pytest
git diff --check
git status --short --untracked-files=all
git diff --stat
```

Use a real working display/GL or documented Xvfb environment for the full suite.
If Android tooling needs to remain installed, include `--group android` in uv
commands. Record actual counts and configuration isolation. Once these checks
pass, do not repeat them without further relevant changes.

Review all diffs and new files, verifying:
- Both source/metadata versions are 1.3 and spec extraction still works.
- Full historical changelog is preserved and website copy is byte-identical.
- README has no Android instructions, guide has all agreed developer procedures.
- MkDocs is dev-only; runtime/Android pins and package identity are preserved.
- Plans/tool moved completely, active links work, historical paths are explained.
- Modernization archive status is evidence-backed; planning index and completion
  summaries are accurate. This initiative remains active pending final review.
- Developer guide requires approved plans/runbooks before AI implementation and
  explains checkpoint execution, scope revisions and eventual archival.
- No accidental `main.ini`, assets, standalone code, generated site, SDK files,
  keys, caches or APK modifications are present.
- No docs deployment workflow was added or existing test workflow altered.

### v1.3 artifact status

The task prepares source/version metadata; it does not automatically authorize
publishing or installing an APK. If the user requests a v1.3 build and the
toolchain is available, build from the app directory using the documented
command, inspect the exact resulting manifest (package, versionName and
versionCode), and record path/hash/input state. Do not assume the filename proves
the embedded version or that a previous v1.2 device pass validates a new artifact.

If no v1.3 APK is built/inspected, state **version metadata updated; v1.3 APK
build/inspection pending**. Device install/tests, signed release packaging,
release uploads and website publishing are independently recorded as run or
not run. Do not invent a release date, artifact or device validation.

### Handoff gate

Update the tracker with actual completed/blocked states and give a concise final
summary: document paths, approved changelog/version, relocation destinations,
tests/site checks, Pages configuration status, and remaining build/publish work.
Stop for user review. Do not commit, tag, push or deploy without request.

### Post-review archival

After final user review and all required gates pass, record this initiative's
completion date, delivered work, final implementation commits (or pending commit
status), remaining optional build/publish work and follow-ups. Move its whole
folder to `planning/archive/YYYY-MM-mdclassics-documentation-v1.3/` using the
actual completion month, update the planning index and all external references,
and check links/whitespace. Pending optional publication is recorded separately;
failed or missing required implementation checks keep the initiative active.
Do not report the archival step as executed before review has occurred.

## Execution log

Append one entry per checkpoint; preserve failures and corrections:

```text
Date / checkpoint:
Status: in progress | awaiting approval | passed | blocked
Input revision and pre-existing changes:
User approval/date (if applicable):
Files changed:
Commands and working directories:
Observed results / counts / log locations:
Blocked or not-run checks:
Decisions:
Next exact action:
```

```text
Date / checkpoint: 2026-10-12 / Checkpoint 1 — Audit and changelog draft
Status: awaiting approval
Input revision and pre-existing changes: HEAD 2584603; clean tree on entry (no pre-existing changes)
User approval/date (if applicable): pending; release date not yet agreed (draft uses YYYY-MM-DD)
Files changed: source/MDclassic_games/CHANGELOG.md; this runbook (tracker + log)
Commands and working directories:
  - repository root: git status --short; git log --oneline -30
  - repository root: git diff --check; git diff --stat -- source/MDclassic_games/CHANGELOG.md
Observed results / counts / log locations:
  - git status --short clean before edits; git diff --check clean; diff adds 153 lines, removes 3.
  - Full v1.2..v0.1 history preserved verbatim from docs/changelogs/classic_games_changelog.md.
  - Blanket "each version has an apk" claim revised to "Published versions up to v1.2 ...".
  - Added empty Unreleased heading and drafted v1.3 (date placeholder YYYY-MM-DD).
  - Verified v1.3 claims against git log and validation record: Python 3.11/Kivy 2.3.1/KivyMD 2.0.0
    (pyproject.toml, validation master summary), uv lockfile + generated requirements.txt,
    Android arm64/toolchain (buildozer.spec), audio + system-bar fix (7227e15),
    15 puzzle fix (92a185f), Snake phantom-swipe fix (5153649), 112-test suite + CI.
  - Documentation bullet retained as planned work (true only once this release's docs work completes).
Blocked or not-run checks: checkpoint 2+ not started by design; no version bump, no dependency change,
  no file relocation, no website copy yet.
Decisions: Keep app changelog heading "# Classic games changelog" so the later `cp` to the website stays
  byte-identical and preserves the published page title.
Next exact action: wait for explicit user approval of the exact v1.3 entry and an agreed release date,
  then execute checkpoint 2.
```

```text
Date / checkpoint: 2026-10-12 / Checkpoint 2 — Version bump and MkDocs dev dependency
Status: passed
Input revision and pre-existing changes: HEAD 2584603; working tree carried checkpoint 1 changes
  (CHANGELOG.md, runbook) plus the approved changelog reflow
User approval/date (if applicable): changelog approved by user 2026-10-12; release date NOT provided
  (v1.3 entry still dated YYYY-MM-DD)
Files changed: source/MDclassic_games/main.py (__version__ = '1.3'); pyproject.toml (project.version "1.3",
  dev group + "mkdocs==1.6.1"); uv.lock (MkDocs closure); this runbook (tracker + log).
  requirements.txt re-exported but byte-identical (no diff) since MkDocs is dev-only.
Commands and working directories:
  - repository root: uv add --group dev --bounds exact mkdocs
  - repository root: uv lock --check; uv sync --locked --group dev; uv pip check
  - repository root: uv run --locked --group dev mkdocs --version
  - repository root: uv export --locked --no-dev --format requirements-txt --output-file requirements.txt
  - repository root: regex/tomllib version checks (no GUI import)
Observed results / counts / log locations:
  - Selected MkDocs version: 1.6.1 (resolved, exact pin recorded in pyproject dev group).
  - uv lock --check: "Resolved 57 packages" (lock consistent); uv sync --locked --group dev: 36 packages checked.
  - uv pip check: "All installed packages are compatible".
  - mkdocs --version: "mkdocs, version 1.6.1 ... Python 3.11".
  - Runtime export: no mkdocs entries; runtime pins unchanged, requirements.txt has no diff.
  - Spec extraction: version.regex against main.py yields 1.3; pyproject project.version = 1.3.
  - No broad --upgrade; runtime/pytest/android pins preserved.
Blocked or not-run checks: no APK built/rebuilt (not part of this checkpoint). Release date still pending.
Decisions: MkDocs added to dev (not runtime, not a new group) as required. Do not hand-edit uv.lock.
Next exact action: proceed to checkpoint 3 on user instruction; ask user to confirm the v1.3 release date
  so the changelog placeholder can be finalized before the website copy in checkpoint 5.
```

```text
Date / checkpoint: 2026-10-12 / Checkpoint 3 — Planning lifecycle and relocation
Status: passed
Input revision and pre-existing changes: HEAD 2584603; working tree carried checkpoints 1-2 changes
User approval/date (if applicable): continuation instructed by user; release date still not provided
Files changed:
  - Moved (git mv, filenames retained) docs/assistant/mdclassic_games_upgrade_plan.md,
    mdclassic_games_phase1_uv_plan.md, mdclassic_games_phase2_desktop_plan.md,
    mdclassic_games_phase3_android_plan.md, mdclassic_games_phase4_device_plan.md,
    mdclassic_games_phase5_handoff_plan.md, mdclassic_games_validation.md
    -> planning/archive/2026-10-mdclassics-modernization/
  - Moved docs/assistant/mdclassic_games_documentation_release_plan.md -> planning/active/mdclassics-documentation-v1.3/plan.md
  - Moved docs/assistant/mdclassic_games_documentation_release_runbook.md -> planning/active/mdclassics-documentation-v1.3/runbook.md
  - Moved docs/assistant/mdclassic_games_install_android_tools.py -> tools/mdclassic_games_install_android_tools.py
  - New planning/README.md
  - Edits: relocation notes in all 7 archived files; completion summary + checked final
    gate checklists in the archive; mutual plan<->runbook links and current paths updated;
    tool usage docstring updated to tools/.
Commands and working directories:
  - repository root: git mv ... (three moves); git status --short
  - repository root: uv run --locked --group android python tools/mdclassic_games_install_android_tools.py --help
  - repository root: git diff --check; git diff --stat
Observed results / counts / log locations:
  - docs/assistant/ left empty; all 10 tracked assistant files relocated.
  - Modernization completion verified against validation record, master plan header and
    git log (Phase 4 final artifact 8bc32723…, 112/112 desktop, CI run 38151771331);
    headers were already reconciled in ddca0a1, final gate checklists now checked.
  - planning/README.md documents the lifecycle and indexes both initiatives.
Blocked or not-run checks: provisioning NOT run (only --help) by design; no commit/tag/push.
Decisions: Archive folder uses actual completion month 2026-10; this initiative stays active
  until final review. Historical docs/assistant paths preserved with relocation notes.
Next exact action: proceed to checkpoint 4 (README + DEVELOPMENT.md) on user instruction;
  release date still needed before the checkpoint 5 website copy.
```

```text
Date / checkpoint: 2026-10-12 / Checkpoint 4 — README and developer guide
Status: passed
Input revision and pre-existing changes: HEAD 2584603; working tree carried checkpoints 1-3 changes
User approval/date (if applicable): continuation instructed by user; release date still not provided
Files changed:
  - README.md rewritten: overview, menu screenshot (docs/img/MD/MD_menu.jpg), seven games,
    uv/Python 3.11/Kivy 2.3.1/KivyMD 2.0.0 baseline, authoritative pyproject/uv.lock note,
    desktop quick start with working directory, links to player help / DEVELOPMENT.md / app
    changelog, background, contribution, license + asset credits. No Android setup/build/install.
  - New DEVELOPMENT.md: environment/groups, dependency maintenance + runtime export + spec pins,
    test commands and CI description, Android host setup + licenses + toolchain table, build/
    deploy/logcat, release checklist, documentation ownership + MkDocs workflow, document-sync
    checklist, AI-assisted changes section + reusable prompt.
Commands and working directories:
  - repository root: git diff --check; file-existence checks for every referenced path
Observed results / counts / log locations:
  - All referenced files exist (screenshot, LICENSE, CHANGELOGs, workflow, tool, planning/README).
  - README Android references are link-only (no setup/build instructions), per plan.
  - Validation-record pointers use absolute GitHub URLs.
Blocked or not-run checks: no MkDocs build here (checkpoint 5); no APK build; release date pending.
Decisions: Keep README concise and desktop-only; all Android procedures consolidated in DEVELOPMENT.md.
Next exact action: proceed to checkpoint 5 (website reconciliation + changelog copy) on user
  instruction; the v1.3 release date is still required before the copy.
```

```text
Date / checkpoint: 2026-10-13 / Checkpoint 4 follow-up — user review questions + release date
Status: passed
Input revision and pre-existing changes: working tree carried checkpoints 1-4 changes
User approval/date (if applicable): user confirmed the v1.3 release date = 2026-10-12 and raised
  four DEVELOPMENT.md clarity questions; answers applied
Files changed:
  - source/MDclassic_games/CHANGELOG.md: v1.3 heading date finalized YYYY-MM-DD -> 2026-10-12
  - DEVELOPMENT.md: (1) chapter 1 "basic checks" explained (what each uv command verifies);
    (2) chapter 3 explains xvfb-run is the Xvfb wrapper (not pytest) and how to run the whole
    suite (plain pytest, or xvfb-run -a pytest headless); (3) new "Installing on a phone"
    subsection describing buildozer deploy run and explicit adb install/launch; (4) new
    ".buildozer/ folder" subsection stating it is the build cache and must be kept, not deleted
  - this runbook (tracker rows 1-2 date, log)
Commands and working directories:
  - repository root: git diff --check; git status --short
Observed results / counts / log locations:
  - git diff --check clean. Corrected the earlier use of `uv run ... adb` (adb is a native
    platform-tools binary, not a Python package) to plain `adb` with a PATH note.
Decisions: v1.3 approved date is 2026-10-12; the changelog date is no longer a placeholder.
  Keep .buildozer/ and bin/ (generated, git-ignored) across builds.
Next exact action: proceed to checkpoint 5 (website reconciliation + changelog copy) on user
  instruction; the approved date 2026-10-12 is now available for the copy.
```

```text
Date / checkpoint: 2026-10-13 / Checkpoint 5 — Website reconciliation and changelog copy
Status: passed
Input revision and pre-existing changes: working tree carried checkpoints 1-4 changes plus the
  checkpoint 4 follow-up, and the later user-requested removal of the xvfb-run command/paragraph
  from DEVELOPMENT.md (only the CI description of a virtual display remains)
User approval/date (if applicable): user instructed continuation to checkpoint 5 on 2026-10-13;
  release date confirmed 2026-10-12
Files changed:
  - docs/index.md: rewritten to describe the combined MDClassics app, list the seven games as
    links to the combined-help anchors, and link the combined help + getting-started.
  - docs/getting-started.md: restructured desktop setup (uv path with app working directory;
    pip path in a Python 3.11 venv then change into the app folder); removed the Android host
    setup/build procedures and replaced them with an absolute link to DEVELOPMENT.md plus a
    pointer to the releases/ folder; added a Kivy native-dependency pointer.
  - docs/about.md: added a Background section consistent with README; reworded the license to
    match README (MIT code vs non-commercial assets); listed third-party sources and noted
    per-game Credits sections.
  - docs/games/classic_games.md: version reference 1.2 -> 1.3; side-menu list now includes
    Help and About; removed the outdated "(to be added in future versions)" about/help block.
    Preserved all seven game headings that supply the app's Help anchors.
  - docs/changelogs/classic_games_changelog.md: copied literally from the app changelog.
  - CHANGELOG.md: rewritten to point to the combined-app changelog (repo + website) and keep
    the historical standalone changelogs pointer.
  - mkdocs.yml: unchanged (nav/pages kept; no assistant records remain under docs/).
  - this runbook (tracker + log).
Commands and working directories:
  - repository root: uv run --locked --group dev mkdocs build --strict (baseline before edits,
    and again after edits)
  - repository root: cp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
  - repository root: cmp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
  - repository root: rg checks for anchors in site/games/classic_games/index.html and rendered
    links in site/index.html and site/about/index.html
  - repository root: gh api repos/osso73/classic_games/pages (to read Pages settings)
Observed results / counts / log locations:
  - Baseline mkdocs build --strict: exit 0. Post-edit build --strict: exit 0 (no warnings/errors).
  - cmp byte-identical for the changelog copy.
  - All seven Help anchor ids present in the built page: game-of-pong, game-of-ahorcado-hanged,
    game-of-memory, game-of-15-puzzle, game-of-2048, game-of-buscaminas-minesweeper, game-of-snake.
  - Built index.html links all seven fragments and both combined pages; about.html links the
    changelog page.
  - git diff --check clean.
Blocked or not-run checks: GitHub Pages settings could NOT be read: `gh` is not installed on the
  host (command not found). No gh-deploy and no settings change performed (by design).
  App Help URLs were not modified; the drawer's fragment-less help URL and the seven game-module
  fragments were verified against the built page.
Decisions: Keep existing site nav/pages; do not move the site or change app URLs. Leave the
  standalone snake page's "version 1.4" text as-is (it refers to the standalone snake release,
  not the combined app). No mkdocs.yml edits were necessary.
Pages configuration for the user to verify manually (unverified here):
  - Repository Settings -> Pages: source = "Deploy from a branch", branch = gh-pages, folder = / (root).
  - The published help base URL must remain https://osso73.github.io/classic_games/.
Next exact action: proceed to checkpoint 6 (final verification + handoff) on user instruction;
  no commit/tag/push/deploy without an explicit request.
```

```text
Date / checkpoint: 2026-10-13 / Checkpoint 6 — Final verification and review handoff
Status: passed (awaiting final user review)
Input revision and pre-existing changes: working tree carried checkpoints 1-5 changes
User approval/date (if applicable): user instructed continuation to checkpoint 6 on 2026-10-13
Files changed:
  - tests/mdclassic_games/unit/test_resources.py: the Android identity test hard-coded the
    expected extracted version as "1.2"; changed it to derive the expected value from
    pyproject.toml [project].version so the check verifies spec extraction against the canonical
    project metadata and does not break on future version bumps. This was the cause of the only
    failing check (the version bump in checkpoint 2 had not updated the test).
  - this runbook (tracker + log).
Commands and working directories:
  - repository root: uv lock --check; uv pip check
  - repository root: uv run --locked --group dev pytest tests/mdclassic_games/unit -q
  - repository root: uv run --locked --group dev pytest -q   (full suite; DISPLAY=:1 available)
  - repository root: git diff --check; git status --short --untracked-files=all; git diff --stat
  - repository root: verification greps (main.py __version__, pyproject diff, requirements.txt,
    buildozer.spec / app URL constants, .github workflows)
Observed results / counts / log locations:
  - uv lock --check: "Resolved 57 packages" (exit 0). uv pip check: "All installed packages are
    compatible" (51 packages).
  - Unit suite after fix: 47 passed (exit 0). Before fix: 1 failed, 46 passed
    (test_android_identity_and_appearance_are_preserved: extracted "1.3" != hard-coded "1.2").
  - Full suite: 112 passed in 29.58s (exit 0), run on display :1 (no xvfb needed).
  - Configuration isolation: source/MDclassic_games/main.ini unchanged; no untracked files;
    site/ ignored; no APK/SDK/cache additions.
  - main.py __version__ = '1.3'; pyproject [project].version = "1.3" (only other pyproject
    change is the dev-group mkdocs==1.6.1 pin). requirements.txt unchanged; buildozer.spec,
    app URL constants, drawer and game screens untouched; .github workflows untouched.
  - Spec extraction now verified jointly with project metadata by the updated unit test.
Blocked or not-run checks: v1.3 APK not built or inspected (no Android build requested/attempted
  in this initiative) -> record "version metadata updated; v1.3 APK build/inspection pending".
  Device install/tests, signed release packaging, release uploads and website publishing were not
  run. GitHub Pages settings remain unverified (`gh` unavailable). No commit/tag/push/gh-deploy.
Decisions: Fix the stale version test by deriving the expected value from pyproject.toml instead
  of hard-coding, so releases need no test edit. Do not repeat the passing checks unless inputs
  change. Leave the working tree uncommitted; initiative stays active pending final review.
Next exact action: stop for user review. After approval, optionally run the post-review archival
  step (record completion, move this folder to planning/archive/2026-10-mdclassics-documentation-v1.3/,
  update index/references). Commit/tag/push/deploy and any APK build only on explicit request.
```

Prior to checkpoint 1 no checkpoints had been executed. Checkpoints 1 (approved),
2 (passed), 3 (passed), 4 (passed), 5 (passed) and 6 (passed, awaiting final
review) are complete. The v1.3 release date is confirmed as 2026-10-12. Next
action: final user review; then optional post-review archival (no commit, tag,
push, deploy or APK build without an explicit request).
