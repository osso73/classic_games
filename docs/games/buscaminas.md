# Buscaminas (Minesweeper)

## Rules of the game

There is a field of mines. The field is divided in areas, each area can contain a mine or not. If no mines, it will show a number indicating the number of mines adjacent to the area. You have to use this information to discover where the mines are hiding. Your objective is to discover all mines, and uncover all areas without a mine.

Flag the areas where you think the mines are, with double click or right-click. You can flag and unflag the area as many times as you want; but when you uncover the area, it remains uncovered.

In the initial version, the minefield is always 9x9 size, with 10 mines. No option yet to change size or number of mines.


## Main screen

This is the main screen of the game.

![screenshot](../img/buscaminas_screen.jpg)

It is divided in two areas:

- _top row_: has some indicators, and the button to start a new game. Left indicator is the number of mines left (i.e. each flag will you put decrease this number). The right indicator is the amount of seconds used.

- _playing ground_: this is the minefield. In the initial version, this is always 9x9 size, with 10 mines.



## Other resources

Under folder `resources` I have a file with a diagram to know the position of the areas, and to help design the screen distribution.

## Credits

I've used the images of this game from the original windows version. I've taken them from this website: https://minesweeper.us
