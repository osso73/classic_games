# classic_games
A series of classic games in Kivy

This is a little project to develop some simple games in kivy, so I get to know the language and build some apps for mobile. I build each game separately, and later will build an interface to bring them all together, using [KivyMD](https://github.com/kivymd/KivyMD) library.

The list of games to be developed is inspired in project [GameStore](https://github.com/neo-mashiro/GameStore), and other ideas I collect from Internet or my own experience. These are the games that I plan for now:

- [x] pong
- [x] ahorcado
- [x] memory
- [ ] 2048
- [ ] 15 puzzle
- [ ] asteroids
- [ ] buscaminas
- [ ] snake
- [ ] pacman(?)

The ones ticked are already developed standalone. This is work in progress.

## Running the games

In order to run these games you need to install [kivy](https://kivy.org/#home) library. Check here: [Getting started--Installation](https://kivy.org/doc/stable/gettingstarted/installation.html) for instructions how to install it.

Then you can execute each of the games by going into their folder, and running:

```
python main.py
```

If you want to run them in your mobile phone, you will need to use `buildozer` to compile for android. The detailed instructions are here: [Packaging your application](https://kivy.org/doc/stable/guide/packaging.html). Inside each game folder I have the `game.spec` file that I use to compile it for android. You can adjust the parameters there.


## License

This project is under MIT license. But commercial use is not allowed, as I am using some images that cannot be used for commercial purposes. Only use it commercially if you change the images by license-free material.

I am using resources from the following sites:

- [Perfect Icons](http://www.perfect-icons.com/index.htm)
- [Free Sound](https://freesound.org/)
- [GoodFon.com](https://www.goodfon.com/)