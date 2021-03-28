# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). For the version numbers, I just use a simple 2-digit, for major and minor changes. Each version has its corresponding apk under the folder `releases`.


## v1.1 - 2021-03-28

### Changed
- Changed graphic of head
- Menu buttons updated, and now using scale-independent pixels (#49)
- Improved the way the screen size is defined, and centered within the available space (#45)
- Score label moved
- Snake starts with 3 parts, instead of only head
- Increased base speed of the snake
- App icon changed

### Added
- Implemented speed button, as per iss. #37
- Implemented size button, as per iss. #50
- Added help button
- Snake opens mouth when close to the food (#47)

### Fixed
- Several internal fixes, improving the detection of collisions and end of screen


## v1.0 - 2021-03-21

### Changed
- Increased size of snake and food, as per iss. #36

### Added
- Spash screen, as per iss. #41
- Snake opens mouth before eating (iss. #47)
- Sounds for start, eat, game over and close app (iss. #39)
- Score tracking (iss #35)
- Added end of game message and sound (iss. #42)
- Menu at the top, with options for start game, end application (iss. #37)

### Fixed
- Food to check window limits at the start of a game, so it spawns correctly inside the window (iss. #43)
- Check collision with top and right have been fixed


## 0.1 - 2021-03-19

### Added:
- Initial version of the game.
- Basic functionality of snake game
- Image for the head of snake, and food
