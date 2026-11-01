# MDClassics documentation consolidation and v1.3 plan

Created: 2026-10-11. Status: **planned; implementation has not started**.

This records the user's agreed follow-up to the modernization work. Execute using
the [detailed runbook](runbook.md).
These two documents were initially stored in `docs/assistant/` at the user's request and
were relocated to `planning/active/mdclassics-documentation-v1.3/` as `plan.md` and
`runbook.md` during implementation (checkpoint 3). Historical references to
`docs/assistant/` in the moved records describe the locations used at the time.

## Objective

Provide clear, current documentation for the combined app in
`source/MDclassic_games`, preserve its MkDocs help website, and prepare version
**1.3** because version 1.2 was already published.

The website is served through GitHub Pages and is used by the application's Help
buttons. Its existing pages must be updated, not removed as a consolidation shortcut.

## Agreed document ownership

| Location | Purpose |
| --- | --- |
| `README.md` | MDClassics overview, screenshot, seven games, desktop prerequisites/setup/launch, links to player help, development and changelog, background, license and credits |
| `DEVELOPMENT.md` | Environment/dependency maintenance, tests, Android provisioning/build/install/debug, version/release checklist, documentation preview/build/publish procedures, mandatory AI planning/runbook workflow |
| `source/MDclassic_games/CHANGELOG.md` | Authoritative combined-app release history, including v1.3 and an Unreleased section for subsequent work |
| `docs/index.md` | Website introduction and navigation, focused on the combined app |
| `docs/getting-started.md` | Current desktop getting-started instructions; developer-only Android procedures link to the guide on GitHub |
| `docs/about.md` | Project background, license and asset credits |
| `docs/games/classic_games.md` | Current combined-app navigation, rules, controls and settings; preserve Help URL anchors |
| `docs/changelogs/classic_games_changelog.md` | Literal copy of the authoritative app changelog, maintained with `cp` |
| `CHANGELOG.md` | Links to the combined-app changelog and historical standalone release histories |
| `planning/README.md` | Planning conventions and index of active and archived initiatives |
| `planning/active/mdclassics-documentation-v1.3/` | This initiative's plan and runbook, renamed to `plan.md` and `runbook.md` |
| `planning/archive/2026-10-mdclassics-modernization/` | Completed modernization plans, runbooks and validation evidence, retaining historical filenames |
| `tools/mdclassic_games_install_android_tools.py` | Relocated Android provisioning tool |

README must contain **no Android setup, build or installation instructions**.
Android developer instructions belong in `DEVELOPMENT.md`. The standalone apps
may be mentioned as historical background; their code and documentation are not
the focus of this task.

## Dependency and publishing decisions

- Add an exact, available Python-3.11-compatible MkDocs pin to the existing `dev`
  dependency group in `pyproject.toml`; regenerate `uv.lock` through uv.
- `pyproject.toml` and `uv.lock` remain authoritative. Runtime
  `requirements.txt` remains a generated runtime-only export.
- No new GitHub workflow is needed. Preserve the existing unit/GUI test workflow.
- Documentation publishing is manual: edit sources, copy the app changelog,
  preview/check the site, then run `mkdocs gh-deploy` when publishing is requested.
- `mkdocs serve` previews locally; `mkdocs build` produces local `site/`;
  `mkdocs gh-deploy` builds and pushes the website to `gh-pages`.
- Markdown edits or a push to the source branch alone do not publish the site.
- Verify GitHub Pages is configured for the root of `gh-pages`; a local/remote
  branch exists, but branch existence alone does not establish Pages settings.
- Generated `site/` stays ignored. Do not commit it to the source branch.
- Copy the changelog directly; do not create a synchronization application,
  plugin, workflow, or source-inclusion mechanism.

## v1.3 and changelog review gate

1. Preserve the full release history currently in
   `docs/changelogs/classic_games_changelog.md` and put it into the app changelog.
2. Draft the v1.3 entry and show the user its exact content and diff.
3. **Stop for explicit changelog approval.** Approval of this plan is not approval
   of the final changelog. Before this gate, do not bump versions, relocate files,
   change dependencies, or implement the other documentation changes.
4. After approval, change `__version__` in `source/MDclassic_games/main.py` and
   `[project].version` in `pyproject.toml` to `1.3`; refresh lockfile metadata.
5. Buildozer reads the app version from `main.py` using `version.regex` and
   `version.filename`. Do not introduce an independent hard-coded spec version.
6. Update current player documentation version references and copy the approved
   changelog to the website.
7. Existing v1.2 release APKs, dates, hashes and validation results remain
   historical v1.2 records. Do not relabel an old APK as v1.3.

Use a release date agreed with the user. An undetermined date is a draft
placeholder, not a factual release date. The initial proposed entry is:

```markdown
## v1.3 - YYYY-MM-DD

Internal modernization of the combined app, with compatibility updates
and a few fixes for current Android devices. The same seven games remain
available.

### Changed
- Updated to Python 3.11, Kivy 2.3.1, and KivyMD 2.0.0, adapting the
  application to the updated framework APIs.
- Introduced a reproducible uv development environment with locked
  dependencies and generated pip requirements.
- Updated the Android build configuration and toolchain, including
  arm64 support.
- Reorganized and updated project documentation, development instructions,
  and the MkDocs help website.

### Added
- Automated unit and GUI regression tests for the combined app.
- Continuous integration checks for the test suite.

### Fixed
- Android audio initialization and layout around system bars.
- The 15 puzzle reference picture covering controls in portrait orientation.
- Snake reacting to a phantom swipe when returning through the navigation
  drawer.
```

Verify these claims against actual commits and validation records when drafting.
The documentation bullet describes planned work and is only true of the final
release once that work is complete. Most changes are internal, but the visible
Android fixes must not be omitted. Do not claim new games or unsupported platforms.

## Planning lifecycle and relocation policy

Keep one folder per initiative, containing its plan, runbooks and evidence.
Active initiatives live in `planning/active/`. After completion and review, move
the entire initiative to `planning/archive/YYYY-MM-<initiative>/`, using its
actual completion year/month. Cancelled or superseded initiatives also belong
in the archive, clearly labelled **Cancelled** or **Superseded**, not Completed.

Create `planning/README.md` explaining these conventions and indexing each
initiative with its status and location. No archiving automation is needed.

During relocation:

1. Reconcile the previous modernization plan's final headers and trackers against
   Git history and validation evidence. Commit `06d9862` reports Phase 5 complete,
   while some headers still say in progress; verify the evidence before updating.
2. Add a completion summary with actual completion date, implementation commit
   references, delivered work, known limitations/deferred work, and a link to this
   follow-up. Preserve chronological evidence and failures.
3. Archive the completed modernization Markdown files together under
   `planning/archive/2026-10-mdclassics-modernization/`, retaining filenames.
   If completion cannot be established, keep the initiative active and record the
   blocker instead of labelling it completed.
4. Move this plan and runbook to
   `planning/active/mdclassics-documentation-v1.3/plan.md` and `runbook.md`, updating
   their mutual links for the new names. Classify any additional assistant files
   by their owning initiative rather than blindly archiving them.
5. Move the provisioning script to `tools/` because it remains an active developer
   tool. Move all remaining assistant material out of public `docs/`.

- Preserve historical evidence, failure entries, original versions and commands.
- Add relocation notes explaining old recorded paths rather than mass-replacing
  historical execution records.
- Update active links, future execution instructions, and runnable provisioning
  commands to the new paths. Update the script's usage docstring.
- Keep relative cross-links between relocated plans working.
- Link to developer/planning material from published pages using absolute GitHub
  URLs, not relative links outside the MkDocs source directory.
- Preserve `/games/classic_games/` and its existing game section anchors.
- Old modernization plans describe the earlier scope, including preserving v1.2;
  this new plan authorizes the follow-up version bump. Do not rewrite the earlier
  plan as though it originally authorized v1.3.

Before archiving any initiative, record its outcome, completion date, final
implementation commit references (or explicitly pending commit status), delivered
work, limitations and follow-ups. Archived instructions are historical references;
current operating instructions belong in `DEVELOPMENT.md`.

Archive this documentation/v1.3 initiative only after the required work is
complete and reviewed. While awaiting final review or blocked on a required gate,
keep it active. On archival, repair external links and update the planning index.

## Required AI-assisted development instructions

Add an **AI-assisted changes** section to `DEVELOPMENT.md`. Before any AI-assisted
implementation, develop a plan and detailed runbook under
`planning/active/<initiative>/`, and obtain user review/approval of those documents.
Repository inspection and drafting the planning documents may happen beforehand;
approval is the boundary before implementation.

- The plan defines objectives, scope, constraints, acceptance criteria and review
  gates.
- The runbook defines bounded checkpoints, relevant files, commands, verification
  steps, and a progress/evidence log.
- Execute checkpoints in order, record actual outcomes, and stop at review gates.
- Update both documents when scope changes and review revised scope before
  implementing it.
- Record the outcome and archive the initiative after completion and review,
  following `planning/README.md`.

Include this reusable planning prompt in the developer guide:

> Inspect the relevant project files and develop a plan and checkpoint-based
> runbook for this change. Do not begin implementation. Include scope, acceptance
> criteria, verification steps, and review gates. Store both documents under
> `planning/active/<initiative>/` and present them for review.

## Execution sequence and gates

| Checkpoint | Work | Required gate |
| --- | --- | --- |
| 1 | Audit state and draft authoritative v1.3 changelog | Exact changelog presented; stop for user approval |
| 2 | Approved version bump and MkDocs dev dependency | Versions agree, locked sync/check pass, runtime export excludes MkDocs |
| 3 | Reconcile/archive modernization, relocate active plan/tool, create planning index | Evidence-backed statuses, contents preserved, new links/commands work, historical paths explained |
| 4 | Rewrite README and create developer guide | Complete desktop/development/release/docs procedures and AI planning workflow with correct working directories |
| 5 | Reconcile website and copy changelog | Existing help pages/anchors preserved, copies identical, MkDocs build checked |
| 6 | Final verification and review handoff | Reviewed diff, meaningful test evidence, accurate v1.3 artifact status |

Checkpoint 1 is the mandatory user review boundary. Later checkpoints may proceed
after approval, recording their evidence as they complete. Commits, pushes,
website deployment, release uploads and tags require an explicit user request.

## Verification and completion

- Review current application controls/settings and documentation, not only old
  runbook summaries. Some older modernization headers are stale; consult actual
  validation evidence and Git history before stating completion or test counts.
- Check lockfile consistency, dependency sync and pip consistency.
- Check the version declared in source/metadata without importing the GUI.
- Verify the literal changelog copy and the MkDocs build, internal links and all
  Help URL anchors. Explain any pre-existing strict-build warning before changing
  unrelated content; do not suppress warnings to manufacture a pass.
- Run appropriate existing unit and GUI/full-suite checks for the metadata/dev
  environment change. No new tests are required solely for prose or file moves.
- Distinguish code version **1.3** from a newly built/inspected **1.3 APK**. Build
  and inspect the latter if requested/available; if not run, report it as pending.
  Installation on a device and publication are separate activities, never implied
  by changing a version string.
- Preserve tracked `main.ini`, assets, standalone apps, historical release APKs,
  dependency runtime pins, and Android package ID `org.games.clasicgames`.
- Final summary identifies changed documents, new planning/tool locations,
  checks actually run, blockers, and publishing/build steps still pending.
- Verify the developer guide requires approved plans/runbooks before AI-assisted
  implementation, and that the planning index/statuses match actual progress.
- After completion and final review, archive this initiative and update all
  affected links; do not archive incomplete work as completed.
