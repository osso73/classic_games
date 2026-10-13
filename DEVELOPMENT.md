# Development guide

How to set up, test, package, document and release the MDClassics combined app
(`source/MDclassic_games`). Player-facing instructions are in the
[Getting started](docs/getting-started.md) page and on the
[help website](https://osso73.github.io/classic_games/).

Every command block below states its working directory. Unless a different
directory is noted, run commands from the repository root.

## 1. Environment and prerequisites

The project uses [uv](https://docs.astral.sh/uv/getting-started/installation/)
with Python 3.11. The root `pyproject.toml` and `uv.lock` are authoritative; never
hand-edit `uv.lock`.

Dependency groups:

- **Runtime** (`[project].dependencies`): the app's Python packages, pinned
  exactly (Kivy 2.3.1, KivyMD 2.0.0, Pillow 11.3.0, pycairo 1.28.0,
  materialyoucolor 3.0.4).
- **`dev`**: test and documentation tooling (pytest, MkDocs). This is uv's
  default group.
- **`android`**: host-side Android build tooling (Buildozer and its host
  dependencies). It is not installed by default.

`uv run`/`uv sync` without `--group android` syncs only the default groups and
therefore **removes** the Android host packages from `.venv`. When you need both
sets of tools in the same environment, name both groups explicitly:

```bash
# Working directory: repository root
uv sync --locked --group dev --group android
```

Native prerequisites:

- Linux desktop: Kivy's SDL2/GL runtime plus Cairo headers/pkg-config to build the
  locked `pycairo` wheel (`sudo pacman -S --needed base-devel pkgconf cairo` on
  Arch-based hosts).
- Android host: see section 4.

After changing environment or dependency files, run these three checks:

```bash
# Working directory: repository root
uv lock --check     # fails if uv.lock is out of sync with pyproject.toml
uv sync --locked    # installs the locked dev environment into .venv (never re-locks)
uv pip check        # verifies the installed packages have compatible dependencies
```

`uv sync --locked` is the normal way to (re)create or update `.venv`; use it
whenever the environment looks wrong. `uv lock --check` and `uv pip check` are
read-only verification steps you can run at any time.

## 2. Dependency maintenance

Change dependencies in `pyproject.toml` only through targeted commands, with
exact bounds, and let uv regenerate the lockfile:

```bash
# Working directory: repository root
uv add --bounds exact <package>            # runtime dependency
uv add --group dev --bounds exact <package>       # development tool
uv add --group android --bounds exact <package>   # Android host tool
uv lock
uv lock --check
uv pip check
```

Do not run a broad `uv upgrade`; preserve the existing runtime, pytest and Android
host pins. Regenerate the committed runtime export after any runtime dependency
change:

```bash
# Working directory: repository root
uv export --locked --no-dev --format requirements-txt --output-file requirements.txt
```

Review the export diff. It must stay runtime-only (no `dev` or `android` packages,
no MkDocs). Keep the generated file and hashes; do not trim it by hand.

The Android APK is **not** built from `pyproject.toml`. Its Python and native
dependency pins live separately:

- `source/MDclassic_games/buildozer.spec` `requirements` lists the cross-compiled
  Python packages and p4a recipes (Python/hostpython 3.11.14, Kivy, KivyMD,
  Pillow, pycairo, materialyoucolor and pure-Python transitives).
- The same spec pins the p4a release (`p4a.branch = v2026.05.09`) and immutable
  commit (`p4a.commit = 58d21141f17c889bf8585f5665921d72028f8831`).
- The desktop `android` uv group only provides the host build tools; it does not
  define the APK's contents.

Keep runtime pins consistent between `pyproject.toml` and the spec where they
overlap, and re-run the tests after a shared dependency change.

## 3. Tests

The suite lives in `tests/mdclassic_games/`. Unit tests are display-independent;
integration tests use real Kivy widgets and a GUI, and are marked `gui`. Shared
fixtures isolate user configuration so tests do not write to the tracked
`source/MDclassic_games/main.ini` or depend on execution order.

```bash
# Working directory: repository root
uv run --locked --group dev pytest tests/mdclassic_games/unit            # unit tests only (no display needed)
uv run --locked --group dev pytest -m gui tests/mdclassic_games/integration  # GUI tests only
uv run --locked --group dev pytest                                       # everything (unit + GUI)
```

Run all tests with `uv run --locked --group dev pytest`; it collects unit and GUI
tests and needs a real display and OpenGL context. Add a regression test alongside
each fix, in the matching game's integration module or in the unit tests when the
behavior needs no display. Do not hard-code an expected total test count anywhere
in the project; read the actual result from the run.

Continuous integration runs the same suite in
[`.github/workflows/mdclassic-games-tests.yml`](.github/workflows/mdclassic-games-tests.yml):
a `unit` job for the display-independent tests and a `gui` job that supplies a
virtual display, software Mesa GL and `SDL_AUDIODRIVER=dummy`. Dummy audio lets
OGGs decode in CI but does **not** prove audible output; verify sound on a real
desktop or device.

## 4. Android host setup

The recorded setup targets a Linux x86_64 host and installs everything under
`~/.local/share/classic-games-android`; no shell profile or system Java change is
needed. On an Arch-based host:

```bash
# Working directory: repository root
sudo pacman -S --needed base-devel git zip unzip cmake gettext pkgconf cairo openssl libffi zlib lld
uv python install 3.11
uv sync --locked --group android
uv pip check
uv run --locked --group android buildozer --version
uv run --locked --group android python tools/mdclassic_games_install_android_tools.py
```

The provisioning tool downloads exact, checksummed archives and is safe to re-run:
it preserves existing directories that carry its matching installation record and
reuses downloaded archives. It only provisions archives; it does not accept
licenses or change system defaults. Accept the SDK licenses interactively (this
selects Java 17 for the process only):

```bash
# Working directory: repository root
env JAVA_HOME="$HOME/.local/share/classic-games-android/jdk-17.0.20.1+1" \
    PATH="$HOME/.local/share/classic-games-android/jdk-17.0.20.1+1/bin:$PATH" \
    "$HOME/.local/share/classic-games-android/sdk/tools/bin/sdkmanager" \
    --sdk_root="$HOME/.local/share/classic-games-android/sdk" --licenses
```

Installed toolchain (as recorded and pinned in `buildozer.spec`):

| Component | Version | Path / setting |
| --- | --- | --- |
| Temurin JDK | 17.0.20.1+1 | `~/.local/share/classic-games-android/jdk-17.0.20.1+1` |
| SDK command-line tools | 19.0 | `~/.local/share/classic-games-android/sdk/cmdline-tools/19.0` |
| Platform-tools | 37.0.1 | `~/.local/share/classic-games-android/sdk/platform-tools` |
| Build-tools | 36.0.0 | `~/.local/share/classic-games-android/sdk/build-tools/36.0.0` |
| Android platform | API 36 (rev 2) | `~/.local/share/classic-games-android/sdk/platforms/android-36` |
| NDK | r28c (28.2.13676358) | `~/.local/share/classic-games-android/android-ndk-r28c` |

Buildozer 1.6.0 expects the legacy `sdk/tools/bin/sdkmanager` path and p4a's API
check runs `sdk/tools/bin/avdmanager`; the provisioning tool creates small
launchers for both that point at the canonical `cmdline-tools/19.0/bin` binaries.

App identity and Android settings are preserved in `buildozer.spec`: package
`org.games.clasicgames`, title "Classic games", `arm64-v8a` only, target API 36,
minimum/NDK API 24, debug packaging. The APK embeds its own Python 3.11.14, which
is separate from the host interpreter. `uv.lock` does not lock the OS packages,
JDK, SDK/NDK binaries or p4a's cross-compiled environment.

## 5. Android build, deploy and debug

Run Buildozer from the app directory, not the repository root.

The Gradle APK build must run under the provisioned Temurin JDK 17. On a rolling
Arch-based host the default Java is newer (for example Java 26) than Gradle
8.14.3 supports, so the build aborts with `Unsupported class file major version
70` right after the sources are packaged. Put the provisioned JDK on `JAVA_HOME`
and `PATH` for the build — either exported once per shell (shown here) or inline
with `env`, as in section 4:

```bash
# Working directory: source/MDclassic_games
export JAVA_HOME="$HOME/.local/share/classic-games-android/jdk-17.0.20.1+1"
export PATH="$JAVA_HOME/bin:$PATH"

uv run --locked --group android buildozer -v android debug   # build the debug APK
uv run --locked --group android buildozer android deploy run # install to device and launch
uv run --locked --group android buildozer android logcat     # filtered app logs
```

Only the commands that run the Gradle APK build (`android debug`, and `android
release` if it were supported) need this environment. `android deploy`/`run`
installs and launches an APK already produced by `android debug`, and `android
logcat` only streams device logs; neither invokes Gradle, so a plain `uv run
--locked --group android buildozer ...` is enough for them once the APK exists in
`bin/`.

The debug APK is written to `source/MDclassic_games/bin/`. `buildozer -v android
debug` produces a debug-signed APK for local testing only. Signed release/AAB
packaging and publication are **not** documented here as validated; do not present
them as supported without new evidence.

Buildozer reads the app version from `main.py` using `version.regex` /
`version.filename`; do not add an independent hard-coded version to the spec.

### Installing on a phone

`buildozer android deploy run` does the install for you: it pushes the APK from a
previous `android debug` build, installs it over `adb` on a single connected
device and starts the app (it does not run the Gradle build itself).
It requires exactly one device, USB debugging enabled, and `adb` available (the
provisioned `platform-tools` provide it). Check the device is seen first:

```bash
# Working directory: source/MDclassic_games
adb devices
```

`adb` is the platform-tools binary provisioned under
`~/.local/share/classic-games-android/sdk/platform-tools`. Add that directory to
your `PATH` once if `adb` is not found.

If more than one device is connected, build and install explicitly with `adb`
rather than `buildozer deploy run`:

```bash
# Working directory: source/MDclassic_games
uv run --locked --group android buildozer -v android debug
adb devices                                              # note the serial of your phone
adb -s <serial> install -r bin/clasicgames-<version>-arm64-v8a-debug.apk
adb -s <serial> shell am start -n org.games.clasicgames/org.kivy.android.PythonActivity
```

Use `-r` to replace an existing install while keeping its data; drop `-r` for a
clean install, or `adb -s <serial> uninstall org.games.clasicgames` first. For a
crash, take a full unfiltered capture instead of the spec's filtered logcat,
because `android.logcat_filters` (`*:S python:D`) can hide native crashes:

```bash
# Working directory: source/MDclassic_games
adb logcat
```

The folder `releases/` holds historical APKs from older versions; a new local
build in `bin/` is not a published release.

### About the `.buildozer/` folder

`source/MDclassic_games/.buildozer/` is Buildozer's build cache: the
python-for-android checkout, the Android project tree and compiled recipe
outputs. **Keep it — do not delete it after a build.** Reusing it makes the next
build much faster. It is generated output and is ignored by git, so it is never
committed and does not need cleaning. Delete it only when you deliberately want a
clean rebuild (for example after changing the toolchain), knowing that the next
build will re-download and recompile everything from scratch. The same applies to
`bin/`: it is generated and ignored, but you normally keep it.

Detailed clean-build and device-validation evidence (artifact hashes, manifest
inspection, tested devices) is recorded in the
[modernization validation record](https://github.com/osso73/classic_games/blob/main/planning/archive/2026-10-mdclassics-modernization/mdclassic_games_validation.md).

## 6. Release checklist

1. Add the change under the `Unreleased` heading of
   `source/MDclassic_games/CHANGELOG.md`; when releasing, convert it into a dated
   version heading (Keep a Changelog format).
2. Get the version and release date agreed before publishing.
3. Bump `__version__` in `source/MDclassic_games/main.py` and `[project].version`
   in `pyproject.toml` to the same value.
4. Refresh the lockfile metadata (`uv lock`, then `uv lock --check`) and confirm
   `uv pip check`.
5. Run the unit and full test suites (section 3) on the final inputs.
6. Build the debug APK (section 5) and inspect the resulting manifest
   (`package`, `versionName`, `versionCode`) with `aapt dump badging`.
7. Smoke-test on a device: install the exact artifact, launch, exercise the
   affected games, and take a full logcat capture.
8. Copy the approved changelog to the website and update player-doc version
   references (section 7).
9. Review the complete diff. Commit, tag, publish, upload releases and run
   `mkdocs gh-deploy` **only on an explicit request**; changing a version string
   does not authorise any of these.

## 7. Documentation

Documentation ownership:

| File | Purpose |
| --- | --- |
| `README.md` | Project overview, screenshot, games, desktop quick start, links, license |
| `DEVELOPMENT.md` | This guide: environment, tests, Android, release, docs, AI workflow |
| `source/MDclassic_games/CHANGELOG.md` | Authoritative combined-app release history |
| `docs/index.md` | Website introduction and navigation |
| `docs/getting-started.md` | Player desktop setup |
| `docs/about.md` | Background, license and asset credits |
| `docs/games/classic_games.md` | Player help: navigation, rules, controls, settings |
| `docs/changelogs/classic_games_changelog.md` | Literal copy of the app changelog |
| `CHANGELOG.md` | Links to the combined-app and historical standalone changelogs |
| `planning/README.md` | Planning lifecycle conventions and initiative index |

The website is built with MkDocs from `mkdocs.yml` and `docs/`. The authoritative
changelog is copied literally to the website; there is no synchronization script,
plugin or workflow:

```bash
# Working directory: repository root
cp source/MDclassic_games/CHANGELOG.md docs/changelogs/classic_games_changelog.md
uv run --locked --group dev mkdocs serve
uv run --locked --group dev mkdocs build --strict
uv run --locked --group dev mkdocs gh-deploy
```

- `mkdocs serve` starts a long-running local preview.
- `mkdocs build --strict` builds into the ignored `site/` directory; fix the first
  reported warning/error rather than suppressing it. `site/` is generated output;
  never edit or commit it.
- `mkdocs gh-deploy` builds and force-pushes to the `gh-pages` branch. GitHub
  Pages must serve the **root of `gh-pages`**. Run it from the checkout that
  contains the intended sources. Committing source and deploying the site are
  separate operations; a source push does not publish the site.
- Link to developer/planning material from published pages with absolute GitHub
  URLs, never with relative paths that leave the MkDocs `docs/` tree.

Generated `site/` stays ignored; do not commit it.

## 8. Keeping documents in sync

When a change lands, update the affected documents together:

- Desktop setup change → `README.md` and `docs/getting-started.md`.
- Controls or settings change → `docs/games/classic_games.md` (preserve the game
  heading anchors used by the app's Help URLs).
- Build or test change → this guide.
- Release → `source/MDclassic_games/CHANGELOG.md`, then `cp` it to the website.

## 9. AI-assisted changes

Any AI-assisted implementation must be preceded by an approved plan and a
checkpoint-based runbook:

- Store both documents under `planning/active/<initiative>/` and present them for
  user review and approval **before** implementation. Repository inspection and
  drafting the planning documents may happen first; approval is the boundary.
- The plan defines objectives, scope, constraints, acceptance criteria and review
  gates. The runbook defines bounded checkpoints, relevant files, commands,
  verification steps, and progress/evidence logs.
- Execute the checkpoints in order, record actual outcomes, and stop at each
  review gate. Revise both documents when scope changes and get the revised scope
  reviewed before implementing it.
- After completion and review, record the outcome and archive the whole
  initiative. Lifecycle conventions are in [`planning/README.md`](planning/README.md);
  archived runbooks are historical references while current operating
  instructions live here.

Reusable planning prompt:

> Inspect the relevant project files and develop a plan and checkpoint-based
> runbook for this change. Do not begin implementation. Include scope, acceptance
> criteria, verification steps, and review gates. Store both documents under
> `planning/active/<initiative>/` and present them for review.
