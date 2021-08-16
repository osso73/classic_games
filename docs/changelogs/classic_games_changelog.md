# Classic games changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). For the version numbers, I just use a simple 2-digit, for major and minor changes. I add a letter in the case I create a new version fixing only bugs.

Each version has its corresponding apk under the folder `releases`.


## v1.2 -  2021-08-01

A couple of bug fixes that were left.


### Fixed
- Hint button in ahorcado didn't work, made the app crash. Now this is fixed (iss. #83)
- Help button in Snake didn't work, made the app crash. Now this is fixed (iss. #84)
- Change settings before loading the game makes the app crash (iss. #85)


## v1.1 - 2021-07-11

Some bug fixes, and recoding of the games to a single app.


### Fixed
- Sample picture for 15puzzle was too separated (iss. #70). Now fixed.
- Games are only loaded when clicked, instead of all loaded at the start (iss. #74)


### Added
- Help button for each of the games, pointing to the game instructions (iss. #78)
- Limit the maximum speed of the ball in game pong (iss. #79)
- Audio message when clicking on exit


### Changed
- Icon and splash screen
- Order of the games in the main menu, side menu and settings, to be aligned with the order they were created.
- Level progress bar: changed to an MD widget, more aligned with theme.


### Removed
- Removed some themes from pong, 15 puzzle, memory (iss. #77)



## v1.0 - 2021-06-13

Initial versión of the game, with all the individual games integrated and basic navigation functionality.


### Added
- Spash screen, as per iss. #71.
- Options in main menu for help, and about, as per iss. #69.


### Changed
- Made buttons on toolbar dynamic, e.g. changed the icon when clicked, as per iss. #68.
- Changed order of the menu, to reflect the order in which programs were written.
- Changed drawer menu, adding title, and scroll only for games, as per iss. #72.

### Fixed
- Hint button in ahorcado, if clicked when game is not happening, it hanged the game. Now this is fixed, as per iss. #75.


## v0.7 - 2021-06-12

### Added
- Game of Buscaminas implemented.
- Added mute button for Buscaminas
- Buttons in toolbar change icon.



## v0.6 - 2021-06-12

### Added
- Game of Pong implemented. Still using some elements from kivy.
- Added settings for Pong


## v0.5 - 2021-06-06

### Added
- Game of Memory implemented. Still using some elements from kivy.
- Added settings for Memory
- Added mute button for Memory


## v0.4 - 2021-06-04

### Added
- Game of 2048 implemented. Still using some elements from kivy.
- Added mute button for 2048


## v0.3 - 2021-05-29

### Added:
- Game of 15 puzzle implemented. Still using many elements from kivy.
- Added mute buton for 15 puzzle.
- Settings for 15 puzzle.


## v0.2 - 2021-05-26

### Changed
- Appearance: order of the menu to show snake, ahorcado first, and settings panels.

### Added:
- Game of ahorcado implemented. Still using many elements from kivy.
- Added mute buton for ahorcado.
- Settings for ahorcado.


## v0.1 - 2021-05-23

Initial version of the app. It includes the main menu with the navigation and the snake game with the settings. All the other games are not yet implemented.

### Added:
- Initial version of the menu and navigation.
- Game of snake implemented. Still using many elements from kivy.
