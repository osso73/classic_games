# Buscaminas changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). For the version numbers, I just use a simple 2-digit, for major and minor changes. Each version has its corresponding apk under the folder `releases`.


## 1.1 - 2021-01-10

### Added:
- Sounds at the end of game, if winning or losing (iss. #34).

### Changed:
- Increased the number of mines from 99 to 125 in expert mode (level 3), as per iss. #32.


## 1.0 - 2021-01-07

Polish of interface and app behaviour, and adding some enhancements.


### Added:
- Added app icon and splash screen, as per iss. #31
- Control when game is finished, as per iss. #30
- Timer counting seconds, as per iss. #25
- Enable different sizes of the board (3 levels of difficutly), as per iss. #24
- Uncover areas when clicking a number, as per iss. #29

### Changed:
- Change top-bar indicators and button, as per iss. #26
- Changed final behaviour, as per iss. #27
- Control of uncover/flag action through a button, instead of double-tapping, as per iss. #23


## 0.1 - 2021-01-03

Initial version of the game. It has basic functionality to play a game, no options for different sizes, no sounds, etc. Interface to be improved.

### Added:
- Initial version of minesweeper (buscaminas)
- 9x9 board, 10 mines
- Basic button to start the game
- Click to discover the mine, double-tap or right-click to add a flag.
- Auto-clear tiles with no adjacent mines
- Detect end of game, either by uncovering areas and flagging all mines (game won), or by uncovering a bomb (game lost)
- Basic pop-up to undicate game won or game lost
