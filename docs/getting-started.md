## Running the games

In order to run these games you need to install [kivy](https://kivy.org/#home) library. Full instructions on how to do that can be found in [Kivy documentation--Installation](https://kivy.org/doc/stable/gettingstarted/installation.html).

Once kivy library is installed, you can execute each of the games by going into their folder, and running:

```
python main.py
```

If you want to run them in your mobile phone, you will need to use `buildozer` to compile for android. The detailed instructions are here: [Packaging your application](https://kivy.org/doc/stable/guide/packaging.html). Inside each game folder I have the `game.spec` file that I use to compile it for android. You can adjust the parameters there.
