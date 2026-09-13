# MDclassic_games Phase 1 runbook — Adopt uv

Reviewed: 2026-09-13. Status: **not executed**.

Read [the master plan](mdclassic_games_upgrade_plan.md) first. This runbook creates the desktop environment only. Phase 2 in the revised master plan handles application compatibility; Phase 3 handles Android. Environment installation success and application startup success are separate results.

## Allowed changes

- Add root `pyproject.toml`, `.python-version`, and generated `uv.lock`.
- Include an exact pytest pin in the root `dev` dependency group; test files, pytest discovery configuration, and CI are implemented in master-plan Phase 2D.
- Add a root-only `.python-version` exception to `.gitignore`.
- Add provisional MD-app instructions to `README.md` and `docs/getting-started.md`.
- Create/update `docs/assistant/mdclassic_games_validation.md` using the master-plan template.

Do not edit application source/KV, `buildozer.spec`, assets, `main.ini`, standalone games, or `requirements.txt` in this phase. The master plan specifies a functional requirements export in Phase 5; there is no optional comment-only replacement.

## 1. Preflight and dependency decision

Run from repository root:

```bash
git status --short
uv --version
```

Record existing changes. If uv is unavailable, install it following <https://docs.astral.sh/uv/getting-started/installation/> and record the version used. Do not assume the previous plan's observed uv or system-Python versions still apply.

Use Python `>=3.11,<3.12` with `.python-version` set to `3.11`. This selects a minor version; it does **not** pin a patch release. Record the actual provisioned Python patch. The lockfile pins Python packages, not the interpreter, OS libraries, or Android SDK.

Use `kivy==2.3.1` and `kivymd==1.2.0` as the initial API baseline. These are candidate compatibility targets, not a “latest release” claim. Verify package availability and Python requirements through the resolver. Do not fall back to KivyMD master or 2.x.

Retain Pillow and materialyoucolor as explicit supporting dependencies for the selected KivyMD stack, but **select exact available versions through uv** as described below. The old plan's `pillow==12.2.0` / `materialyoucolor==3.0.2` were not validated in this review and should not be copied on faith. Record their package metadata/dependency relationship; if metadata proves one is unused by this runtime, document that evidence before omitting it and adapt the inventory check accordingly. Android recipe compatibility is separately checked in Phase 3.

## 2. Add the project files

Create root `pyproject.toml` initially with:

```toml
[project]
name = "classic-games"
version = "1.2"
description = "Classic games built with Kivy/KivyMD"
requires-python = ">=3.11,<3.12"
dependencies = [
    "kivy==2.3.1",
    "kivymd==1.2.0",
]

[tool.uv]
package = false
```

`version = "1.2"` reflects the current `main.py` version; it is not a release bump. `package = false` is intentional: the app is launched as a script with sibling imports and assets. Do not add a build backend, package-discovery configuration, console entry point, or move files into `src/`.

Create root `.python-version` containing:

```text
3.11
```

Immediately after the existing `.python-version` ignore rule, add `!/.python-version`. Preserve ignore behavior for selectors elsewhere. `.venv` is already ignored. Do not ignore `uv.lock` or force-add the selector as a workaround.

## 3. Resolve, pin, and sync

Run from repository root, one command at a time:

```bash
uv python install 3.11
uv add --bounds exact pillow materialyoucolor
uv add --group dev --bounds exact pytest
uv lock --check
uv sync --locked --group dev
uv pip check
```

The first `uv add` command resolves available supporting releases compatible with Python 3.11 and core pins, writes exact requirements to `pyproject.toml`, generates `uv.lock`, and normally syncs. The second adds pytest under `[dependency-groups].dev`, not `[project].dependencies`. Review the actual diff: the **final** project must contain exact versions for all direct runtime dependencies and pytest. Never edit `uv.lock` manually.

If resolution or installation fails:

1. Record failing package, selected version, platform, and first meaningful error.
2. For network/index failures, fix or report the environment; do not churn versions.
3. For an unsupported package version, inspect release metadata and select a supported stable version explicitly, using `uv add "package==verified-version"` with the actual value. Record the reason and rerun checks.
4. If Kivy/KivyMD core pins cannot be installed on the supported host with Python 3.11, report a blocked dependency decision rather than silently changing the framework major or interpreter minor version.

Do not run broad `uv lock --upgrade` or add build/test tools to runtime dependencies to make unrelated commands pass. Verify pytest installation with `uv run --locked --group dev pytest --version` and record its version. Do not run test discovery in Phase 1: scoped collection and the new suite are established in Phase 2D, and a zero-test run is not a passing suite.

## 4. Verify environment without importing the GUI

Run from repository root:

```bash
uv run --locked python --version
uv run --locked python -c "import sys; from importlib.metadata import version; assert sys.version_info[:2] == (3, 11); print(sys.executable); print({p: version(p) for p in ('kivy', 'kivymd', 'pillow', 'materialyoucolor')})"
```

Expected: Python 3.11.x, the project environment's interpreter, and installed versions matching the final direct pins. This metadata check does not require a graphical display and does not claim the application works.

Verify version-control handling:

```bash
git status --short --untracked-files=all
git check-ignore .venv
git check-ignore .python-version uv.lock
```

Expected: `.venv` is ignored; `.python-version` and `uv.lock` are not. The final `git check-ignore` returning exit code 1 with no output is the expected “not ignored” result. Confirm there are no environment contents in the proposed changes.

## 5. Attempt startup from the correct working directory

Use working directory **`source/MDclassic_games`**:

```bash
uv run --locked python main.py
```

uv discovers the root project through parent directories. Do not use `uv run python source/MDclassic_games/main.py` from repository root: `menu.py` and `drawer.py` load bare KV filenames, and settings/images/fonts also use relative paths. Do not use `--project` alone as a substitute for setting the working directory.

Before launching, preserve existing `main.ini` content. Do not change settings during this phase; inspect the diff afterward for automatic config writes and restore only test-generated changes.

Classify and record the result:

| Result | Action / status |
| --- | --- |
| Menu renders and window closes normally | Record startup PASS. Full game validation still belongs to Phase 2. |
| Removed/changed KivyMD import, widget, or property | Record relevant traceback and implicated file/symbol as Phase 2 input. Do not migrate code here. |
| KV/asset not found | First verify working directory and file presence. Do not misclassify as KivyMD migration or add dependencies. |
| No display, GL provider, or audio device/provider | Record environment blocker and exact error. Do not claim GUI validation passed or suppress providers/exceptions to get a green result. |
| Other Python/runtime error | Record it without guessing the cause; investigate minimally and hand it to Phase 2 if application-related. |

A closed window after an exception or timeout is not successful startup. Keep logs outside tracked source and link their location in the validation record.

## 6. Add provisional documentation

In `README.md` and `docs/getting-started.md`, add an explicitly labeled combined **MDclassic_games** setup section. Preserve standalone-game instructions.

Show root setup separately from app launch:

```bash
# Repository root
uv sync --locked
```

```bash
# Working directory: source/MDclassic_games
uv run --locked python main.py
```

Explain that the reader must change into the stated app directory before the second command. Link uv installation instructions, state Python 3.11, identify `pyproject.toml` / `uv.lock` as authoritative, and include the **observed** status: environment ready, UI migration pending if it failed, Android not yet validated. Do not advertise an untested startup/build command as working. Leave root `requirements.txt` intact until the master plan's final export step.

## 7. Phase 1 completion and handoff

Run `git diff --check` and review tracked diffs **and new files** (ordinary `git diff` does not show untracked file contents). Verify that only allowed files changed.

Complete Phase 1 only when:

- [ ] Root metadata, Python selector, ignore exception, and generated lockfile are present.
- [ ] All direct runtime dependencies have exact, available pins; actual versions and uv/Python patch are recorded.
- [ ] pytest is pinned in the `dev` group and its version command passes; no test tool was added to runtime requirements.
- [ ] `uv lock --check`, `uv sync --locked --group dev`, and `uv pip check` pass.
- [ ] Metadata verification confirms the project interpreter is Python 3.11.
- [ ] Startup was attempted and honestly classified, or explicitly NOT RUN with an environmental blocker.
- [ ] MD-app docs use the app-directory launch contract and accurately label partial status.
- [ ] No app, Android spec, requirements, assets, user config, or standalone-game changes occurred.

Handoff to **Phase 2 — Desktop compatibility** with the first application traceback and remaining checks. A completed environment phase with blocked GUI validation does not mean the app is runnable. Do not start Android build work until the master plan's desktop gate passes.
