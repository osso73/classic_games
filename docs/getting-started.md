## Running the games

In order to run these games you need to install [kivy](https://kivy.org/#home) library. Full instructions on how to do that can be found in [Kivy documentation--Installation](https://kivy.org/doc/stable/gettingstarted/installation.html).

Once kivy library is installed, you can execute each of the games by going into their folder, and running:

```
python main.py
```

### MDclassic_games setup (provisional)

The combined KivyMD app uses [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.11. Its root `pyproject.toml` and `uv.lock` are authoritative; the existing `requirements.txt` remains in place until the final migration phase.

From the repository root, create the locked environment:

```
uv sync --locked
```

Then change into `source/MDclassic_games` before running the app. The app requires that working directory for relative KV and asset paths:

```
# Working directory: source/MDclassic_games
uv run --locked python main.py
```

Observed status: desktop compatibility and acceptance passed with Kivy 2.3.1 and KivyMD 2.0.0. All 80 desktop tests and the focused visual recheck pass with the common Pillow 11.3.0 / pycairo 1.28.0 supporting pins. Android host setup is validated, including installed zip and accepted SDK licenses; spec/packaging work is next. APK builds and Android runtime support remain unvalidated. See the [validation record](assistant/mdclassic_games_validation.md).

#### MDclassic_games Android host setup (Phase 3, provisional)

The following setup has been exercised on Manjaro Linux x86_64. EndeavourOS is also Arch-based, but has not been tested yet. Python packages belong to the repository's `.venv`; Java and Android tools are installed under `~/.local/share/classic-games-android`. No shell profile or system-default Java change is needed.

For a fresh Arch-based host, install the OS prerequisites with `pacman` (this step requires administrator privileges):

```bash
sudo pacman -S --needed base-devel git zip unzip cmake gettext pkgconf cairo openssl libffi zlib lld
```

On the recorded host, all listed prerequisites are present; the user installed the previously missing `zip` utility with `sudo pacman -S --needed zip`. Cairo headers and pkg-config are also needed to build the locked desktop pycairo package. The pinned upstream Buildozer/p4a installation references and observed package versions are in the validation record.

From repository root:

```bash
uv python install 3.11
uv sync --locked --group android
uv pip check
uv run --locked --group android buildozer --version
uv run --locked --group android python docs/assistant/mdclassic_games_install_android_tools.py
```

The provisioning script uses exact reviewed archive URLs and checksums for Temurin JDK 17.0.20.1+1, SDK command-line tools 19.0 (build 13114758), platform-tools 37.0.1, build-tools 36.0.0, Android API 36 revision 2 and NDK r28c (28.2.13676358). It preserves existing directories unless they carry its matching installation record, retains downloaded archives for reuse, and accepts no licenses automatically. Re-running it reuses the installed tools. It requires Linux x86_64, Python 3.11 and `unzip`.

Review and accept the SDK licenses interactively using this command, which selects Java 17 for this process only:

```bash
env JAVA_HOME="$HOME/.local/share/classic-games-android/jdk-17.0.20.1+1" \
    PATH="$HOME/.local/share/classic-games-android/jdk-17.0.20.1+1/bin:$PATH" \
    "$HOME/.local/share/classic-games-android/sdk/tools/bin/sdkmanager" \
    --sdk_root="$HOME/.local/share/classic-games-android/sdk" --licenses
```

To inspect the installed SDK, repeat that command with `--list_installed` instead of `--licenses`. Buildozer 1.6.0 expects the legacy `sdk/tools/bin/sdkmanager` location; the provisioning script creates a small launcher pointing to the canonical `sdk/cmdline-tools/19.0/bin/sdkmanager`, without duplicating SDK package metadata.

The project's `android` dependency group pins host build tools; `uv.lock` does not lock OS packages, Java, SDK/NDK binaries or p4a's cross-compiled Python environment. The APK's selected Python 3.11.14 is separate from the host interpreter. The next spec checkpoint will use the immutable p4a revision, explicit APIs/NDK, isolated SDK paths and disabled SDK auto-updates. Building is still gated by that spec/resource review.

For regression checks with the Android host group retained in `.venv`, run from repository root:

```bash
uv run --locked --group dev --group android pytest
```

After reinstalling the OS, restore the repository including committed metadata, recreate `.venv` with the locked sync above, and rerun the provisioning script. Preserve local app settings separately if wanted. Check graphics/audio providers and rerun desktop tests on the new OS; the clean Android build and device checks remain separate acceptance gates.

If you want to run them in your mobile phone, you will need to use `buildozer` to compile for android. The detailed instructions are here: [Packaging your application](https://kivy.org/doc/stable/guide/packaging.html). Inside each game folder I have the `game.spec` file that I use to compile it for android. You can adjust the parameters there.

In the folder `releases` you can find apk files to be installed on your android mobile phone.
