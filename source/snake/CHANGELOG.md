# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). For the version numbers, I just use a simple 2-digit, for major and minor changes. Each version has its corresponding apk under the folder `releases`.

## Unreleased

### Changed
- Food now gives 3 points, instead of 2 (iss. #65).
- Speed up takes shorter than before: 20 moves instead of 30 (iss. #65).

### Fixed
- Now starting a game will reset the progress bar to 0, instead of keeping previous score (iss. #64)
- Take the starting speed and size from the settings previously saved (iss. #61).
- Avoid crashing if the _start_ button is pressed very fast after crashing (iss. #66).


## v1.4 - 2021-04-11

### Added
- Option to select starting level, as per iss. #57.
- Option to play story (e.g. one level after the other), or just one level endless, as per iss #58.

### Changed
- Different types of food, having different behaviours (iss. #46).
- All configuration options now set through a settings screen, instead of buttons.

### Fixed
- Fixed error when sizing the grid, in some specific window / grid configurations, as per iss. #60.
- Popup messages now have a button to close the message. This avoids accidental closing of the window, and moving to next level (iss. #59).


## v1.3 - 2021-04-06

### Added
- Tail: last part of the snake is a tail, instead of a regular part (iss. #56).
- Created 12 different levels (iss. #44). Now game move to the next level after a certain score.

### Changed
- End of game: instead of popup, now the colour of head will change to multiple colours, to indicate game over (iss. #55).
- Changed speed options to 11, 15, 19, 23, to have better visual on some levels.

### Fixed
- When change of size, the grid is not well aligned. Now the change of size button will stop the game, and change screen size. (iss. #52).


## v1.2 - 2021-04-01

### Added
- Walls around the edges of the screen (iss. #38).
- Menu buttons for pause and mute (iss. #51).

### Changed
- Snake doesn't die when hitting the end of screen: it pops out at the opposite end. Only hitting the wall or hitting the snake will kill the snake.
- Screen sizes adapted, to accomodate the wall.


## v1.1 - 2021-03-28

### Added
- Implemented speed button, as per iss. #37.
- Implemented size button, as per iss. #50.
- Added help button.
- Snake opens mouth when close to the food (#47).

### Changed
- Changed graphic of head.
- Menu buttons updated, and now using scale-independent pixels (#49).
- Improved the way the screen size is defined, and centered within the available space (#45).
- Score label moved.
- Snake starts with 3 parts, instead of only head.
- Increased base speed of the snake.
- App icon changed.

### Fixed
- Several internal fixes, improving the detection of collisions and end of screen.


## v1.0 - 2021-03-21

### Added
- Spash screen, as per iss. #41.
- Snake opens mouth before eating (iss. #47).
- Sounds for start, eat, game over and close app (iss. #39).
- Score tracking (iss #35).
- Added end of game message and sound (iss. #42).
- Menu at the top, with options for start game, end application (iss. #37).

### Changed
- Increased size of snake and food, as per iss. #36.

### Fixed
- Food to check window limits at the start of a game, so it spawns correctly inside the window (iss. #43).
- Check collision with top and right have been fixed.


## 0.1 - 2021-03-19

### Added:
- Initial version of the game.
- Basic functionality of snake game.
- Image for the head of snake, and food.
