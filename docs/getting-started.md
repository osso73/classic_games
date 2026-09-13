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

Observed status: the environment is ready, but UI compatibility migration is pending because the pinned KivyMD 1.2.0 distribution failed to load a required `label.kv` resource. Android has not yet been validated.

If you want to run them in your mobile phone, you will need to use `buildozer` to compile for android. The detailed instructions are here: [Packaging your application](https://kivy.org/doc/stable/guide/packaging.html). Inside each game folder I have the `game.spec` file that I use to compile it for android. You can adjust the parameters there.

In the folder `releases` you can find apk files to be installed on your android mobile phone.
