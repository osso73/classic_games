# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). For the version numbers, I just use a simple 2-digit, for major and minor changes. Each version has its corresponding apk under the folder `releases`.


## Unreleased

Initial version of the game. It has basic functionality to play a game, no options for different sizes, no sounds, etc. Interface to be improved.

### Added:
- Initial version of minesweeper (buscaminas)
- 9x9 board, 10 mines
- Basic button to start the game
- Click to discover the mine, double-tap or right-click to add a flag.
- Auto-clear tiles with no adjacent mines
- Detect end of game, either by uncovering areas and flagging all mines (game won), or by uncovering a bomb (game lost)
- Basic pop-up to undicate game won or game lost
