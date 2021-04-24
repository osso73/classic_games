# Snake

These instructions are for version 1.4. You can find [here](../changelogs/snake_changelog.md) a changelog explaining the changes introduced in each version.

## Rules of the game

Very classic game, exists in most of the platforms, one of the first games ever built on a phone (old Nokia phones). There are many variants of the game.

In here, the player controls a snake that goes on the screen. There is a piece of food at a random location of the screen. When the snake eats the food, it grows the length, and a new piece of food appears (note that each type of food will have slightly different effects). The player has to avoid that the snake hits a wall or its own body: this will kill the snake. Reaching the end of the screen will not kill the snake, it will just pop up at the opposite end.

The game has different levels, each of them has a certain amount of walls that the snake has to avoid. Once you reach a partial score of the level (which depends on the grid size), you move to the next level.

Swipe on the screen to change the direction of the snake. The snake can turn 90 degrees in any direction.

The screen can be either portrait or landscape. If the screen changes, you should start a new game to take the dimensions into account.


## Main screen

This is the main screen of the game.

![screenshot](../img/snake_screen.jpg)

It is divided in three areas:

- _top row_: it shows a toolbar with some buttons that will allow you different functions, described in section [Buttons in toolbar](#buttons-in-toolbar).

- _results row_: display the score and the current level, with a progress bar on the level. When the progress bar reaches 100%, you move to the next level.

- _playing ground_: this is where the snake will run. Here you can see as well the current score of the game, which is the number of fruits you have eaten.


## Types of food

Latest version has introduced different types of food. There are 3  types with different behaviour:

| Type      | Behaviour                                                                                       | Examples                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Fruit     | Adds one snake part, and 2 points to the score. This is the healthy food!                       | ![][apple] ![][apple2] ![][bananas] ![][cherry] ![][kiwi] ![][strawberry] ![][watermelon] |
| Fast-food | Increases the speed of the snake by 50% for a while, adds 2 snake parts, and one point of score | ![][fries] ![][hamburger] ![][pizza]                                                      |
| Sweet     | adds 3 parts of the snake, one point of score.                                                  | ![][cake] ![][flan] ![][ice]                                                                |

Fruit is what you get most often. But watch out when eating other food, as you will suffer the consequences!

## Buttons in toolbar

The buttons give you access to the following functions:

  - **Start**: to start a new game. It will reset the score, and remove the snake and food. It will create a new snake with the head only, and spawn a new food.

  - ![][b_mute_on]/![][b_mute_off]: mute the sounds of the game. Another click will unmmute.

  - ![][b_pause]/![][b_play]: this button will pause the game. Another click will continue the game where it was.

  - ![][b_settings]: open the Settings panel, to configure the options of the game. See the section [Settings](#settings) for details

  - ![][b_help]: open a webpage with the instructions on how to play the game (this manual you are reading).

  - ![][b_exit]: exit the app.

## Settings

All settings are grouped under a settings panel, as shown in this screenshot, and can be accessed through the :

![Settings](../img/snake/settings_screen.jpg "Settings")

  - **Size**: to change the size of the head and food. They can be larger or smaller. You can select from a number of pre-defined sizes: 11, 15, 19, 23. This is the number of squares that has the shortest side of the window. So the higher the number, the smaller the square will be, and hence the smaller the snake parts and food.

  - **Speed**: to change the speed of the snake. You can select from a number of pre-defined speed factors: 0.5, 0.8, 1, 1.5, 2, 3. The game starts with a factor of 1 by default. The factor will be dividing the interval between updates of the game. Therefore, the higher the factor the smaller is the interval between updates, producing a higher speed.

  - **Play story**: this flag allows you to select the game mode: True to play in story mode, or False to play only one level. Story mode will start at the level selected below, and single-level will play the selected level endless.

  - **Start level**: You can select the level to start your story, from 1 to 12. If the game mode is single-level, this will be the level you play; if the game mode is story, you will start at this level.

The settings are saved, so next time you start the game it will maintain the same settings defined.

## Credits

For the icons in the menubar I'm using [Material Design icons](https://material.io/resources/icons).

I found the snake head in [here](https://www.iconfinder.com/icons/3015218/dangerous_animal_reptile_serpent_head_snake_face_viper_icon). And the images for food are from [Perfect Icons](http://www.perfect-icons.com/index.htm) website. These images cannot be used for commercial purposes, otherwise they are free for personal use.

The sounds I found on [Free Sound](https://freesound.org/), and some of them I had found over Internet. I'm not aware of any copyright or limitation to use these.


[b_mute_on]: ../img/snake/btn_mute_on.png "Mute on"
[b_mute_off]: ../img/snake/btn_mute_on.png "Mute off"
[b_pause]: ../img/snake/btn_pause.png "Pause"
[b_play]: ../img/snake/btn_play.png "Play"
[b_settings]: ../img/snake/btn_settings.png "Settings"
[b_help]: ../img/snake/btn_help.png "Help"
[b_exit]: ../img/snake/btn_power.png "Exit"

[apple]: ../img/snake/fruit-apple.png "Apple"
[apple2]: ../img/snake/fruit-apple2.png "Apple"
[bananas]: ../img/snake/fruit-bananas.png "Bananas"
[cherry]: ../img/snake/fruit-cherry.png "Cherry"
[kiwi]: ../img/snake/fruit-kiwi.png "Kiwi"
[strawberry]: ../img/snake/fruit-strawberry.png "Strawberry"
[watermelon]: ../img/snake/fruit-watermelon.png "Watermelon"

[fries]: ../img/snake/junk-french-fries.png "French fries"
[hamburger]: ../img/snake/junk-hamburger.png "Hamburger"
[pizza]: ../img/snake/junk-pizza.png "Pizza"

[cake]: ../img/snake/sweet-cake.png "Cake"
[flan]: ../img/snake/sweet-flan.png "Flan"
[ice]: ../img/snake/sweet-icecream.png "Ice cream"
