# MDClassics documentation and v1.3 execution runbook

Created: 2026-10-11. Status: **not executed**.

Read the [scope and decisions](mdclassic_games_documentation_release_plan.md)
before executing. This runbook is intended for a smaller model using bounded,
explicit checkpoints. It implements the follow-up documentation/release task,
not the earlier modernization phases.

## Progress tracker

| Checkpoint | Status | Evidence / next action |
| --- | --- | --- |
| 1 — Audit and changelog draft | Pending | Start here; user must approve the changelog before checkpoint 2 |
| 2 — Version and MkDocs | Pending | Requires checkpoint 1 approval |
| 3 — Planning lifecycle and relocation | Pending | Reconcile/archive modernization; move this plan/runbook to active initiative |
| 4 — README and developer guide | Pending | Include mandatory AI planning/runbook workflow |
| 5 — Website reconciliation | Pending | Keep existing Help routes/anchors |
| 6 — Verification and handoff | Pending | No deployment or commit without request |

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
  `docs/assistant/mdclassic_games_validation.md` and commits for the release fixes.

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

No checkpoints have been executed. Next action: checkpoint 1, changelog draft
and mandatory user review.
