# Running the games

The games are combined in a single KivyMD app, MDClassics, in the
`source/MDclassic_games` folder. It uses
[uv](https://docs.astral.sh/uv/getting-started/installation/) with Python 3.11.
The root `pyproject.toml` and `uv.lock` are the authoritative dependency
definitions; a runtime `requirements.txt` is generated from the lockfile
(excluding development and Android host tooling).

If Kivy's native dependencies are not already available on your system, follow
the [Kivy installation instructions](https://kivy.org/doc/stable/gettingstarted/installation.html)
for your platform first.

## Installing and running

### With uv

From the repository root, create the locked environment:

```bash
# Working directory: repository root
uv sync --locked
```

Then change into the app folder before running, because the app loads its KV files
and assets through relative paths:

```bash
# Working directory: source/MDclassic_games
uv run --locked python main.py
```

### With pip

From the repository root, create a Python 3.11 virtual environment and install the
generated requirements:

```bash
# Working directory: repository root
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then change into the app folder before running:

```bash
# Working directory: source/MDclassic_games
python main.py
```

Observed status: desktop compatibility and acceptance passed with Kivy 2.3.1 and
KivyMD 2.0.0, with the common Pillow 11.3.0 / pycairo 1.28.0 supporting pins. See
the [validation record](https://github.com/osso73/classic_games/blob/main/planning/archive/2026-10-mdclassics-modernization/mdclassic_games_validation.md)
for full details.

## Android

Android is a developer-only topic. Setting up the Android toolchain, building the
APK and installing it on a device are documented in the repository's
[development guide](https://github.com/osso73/classic_games/blob/main/DEVELOPMENT.md).

Ready-to-install APKs for published versions are kept in the
[`releases`](https://github.com/osso73/classic_games/tree/main/releases) folder of
the repository.
