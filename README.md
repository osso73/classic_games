# classic_games
A series of classic games in Kivy

This is a little project to develop some simple games in kivy, so I get to know the language and build some apps for mobile. I started building each game separately using kivy only, and afterwards I've created a wrapper using [KivyMD](https://github.com/kivymd/KivyMD) library, and brought all games todgether, using the look and feel from KivyMD.

The list of games to be developed is inspired in project [GameStore](https://github.com/neo-mashiro/GameStore), and other ideas I collect from Internet or my own experience. These are the games that I have developed for now:

- [x] pong
- [x] ahorcado
- [x] memory
- [x] 15 puzzle
- [x] 2048
- [x] buscaminas
- [x] snake

Other potential games that may come later:
- [ ] asteroids
- [ ] pacman


## Usage

In order to run these games you need to install [kivy](https://kivy.org/#home) library. Check here: [Getting started--Installation](https://kivy.org/doc/stable/gettingstarted/installation.html) for instructions how to install it.

Then you can execute each of the games by going into their folder, and running:

```
python main.py
```

The game based on KivyMD is under folder MDclassic_games.

If you want to run them in your mobile phone, you will need to use `buildozer` to compile for android. The detailed instructions are here: [Packaging your application](https://kivy.org/doc/stable/guide/packaging.html). Inside each game folder I have the `buildozer.spec` file that I use to compile it for android. You can adjust the parameters from there to your liking.

Alternatively, you can download the .apk image of the games and install it directly on your phone. The images are under folder [releases](https://github.com/osso73/classic_games/tree/main/releases).

You can find information about how to play these games in this page: https://osso73.github.io/classic_games/.


## Contribution

I started this project to practice with kivy, and also to build some games for my daughter. So I'm not expecting to have a collaboration on this project. Having said that, feel free to open issues to improve the games, or improve the code. If you would like to contribute, drop me a mail.


## License

This project is under MIT license. But commercial use is not allowed, as I am using some images that cannot be used for commercial purposes. Only use it commercially if you change the images by license-free material.

I am using resources from the following sites:

- [Perfect Icons](http://www.perfect-icons.com/index.htm)
- [Free Sound](https://freesound.org/)
- [GoodFon.com](https://www.goodfon.com/)

More information about the assets used in each of the games can be found in the [documentation](https://osso73.github.io/classic_games/) page, under the _Credits_ section in each game.
