#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 20:01:28 2021

@author: oriol
"""

# std libraries
import os


# non-std libraries
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App


# my app imports
import snake.constants as SNAKE
from snake.levels import Level
from snake.grid_elements import Food, Wall, SnakePart, SnakeHead
from popup import PopupButton


Builder.load_string(
    r"""

<GameBoard>:
    canvas.before:
        Color:
            rgba: 250/255, 248/255, 239/255, 1
        Rectangle:
            pos: self.pos
            size: self.size

""")


class GameBoard(Widget):
    '''
    This is the board of the game, where all logic occurs. It creates
    as a grid, with n x m squares, where the snake and the food will
    be located. It controls the movement of the snake, checking if there
    is any collision, and when food is eaten, spawning a new food. Keeps
    track of the score.

    Attributes
    ----------
    active : boolean
        If True, the update function will move the snake; if False, it will
        do nothing. This is set to False when the game finishes, and set
        to active when a new game starts.
    level : Level class
        Object that keeps record of the current level, and has all properties
        associated to the level: wall, maximum score, level score.
    move_x : int
        Defines the move of the snake: value that the position x is
        incremented/decremented at each step. The unit is the square of the
        grid, not the pixels. Can be 1, -1 or 0.
    move_y : int
        Defines the move of the snake: value that the position y is
        incremented/decremented at each step. The unit is the square of the
        grid, not the pixels. Can be 1, -1 or 0.
    mute : boolean
        If True, the sounds will not play; otherwise, they will play. Set
        to False by default. This is triggered by button in toolbar.
    num_level : NumericProperty
        Current level. This can be set by menu buttons, or automatically at
        the end of the level, moving to next level.
    pause : boolean
        When True, the game will pause (i.e. the update function will not
        update). Set to False by default. This is triggered by button in
        toolbar.
    score : NumericProperty
        Score of the game (+1 for every food)
    size_grid : ListProperty
        This is a 2-values list with the number of squares of the grid, in
        the form of [n, m]. So in fact the number of squares are n+1 x m+1.
    size_pixels : NumericProperty
        Each square of the grid has size_pixels x size_pixels pixels.
    size_snake : NumericProperty
        This defines the number of squares that exist in the shortest window
        side. So the higher the number, the smaller will be the squares, and
        therefore the snake and food. It cycles through a number of
        pre-defined values: GRID_SIZES
    snake_parts : list
        Contains all the widgets that form the snake: one SnakeHead, the
        rest SnakePart
    speed : NumericProperty
        The actual speed of the snake, defined as the interval between
        updates. The result of the base speed, divided by the speed_factor
        and by the food speed.
    speed_factor : NumericProperty
        This defines the speed of the snake. This factor divides the
        interval between updates, so the higher the value the higher the
        speed of the snake.
    story : boolean
        Define if the game mode is story (True) or single-level (False)
    wall : list
        Contains all the widgets that form the wall, of type Wall
    level_progress_bar : NumericProperty
        Used to show the progress inside one level. This is updated according
        to the level.score.
    '''

    score = NumericProperty(0)
    size_pixels = NumericProperty(0)
    size_grid = ListProperty()
    size_snake = NumericProperty()
    snake_parts = ListProperty([])
    speed_factor = NumericProperty()
    speed = NumericProperty(0.0)
    mute = BooleanProperty(False)
    pause = BooleanProperty(False)
    num_level = NumericProperty(1)
    level_progress_bar = NumericProperty(0)


    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.wall = []
        self.active = False
        self.size_hint = None, None
        app = App.get_running_app()
        self.story = bool(int(app.config.get('Snake', 'mode')))
        self.size_snake = int(app.config.get('Snake', 'size'))
        self.speed_factor = float(app.config.get('Snake', 'speed'))
        self.speed = SNAKE.SPEED/self.speed_factor


    def on_speed(self, *args):
        # first time event does not need to be cancelled
        if hasattr(self, 'event'):
            self.event.cancel()

        self.event = Clock.schedule_interval(self.update, self.speed)
        
    
    def pause_button(self, button):
        '''Toogle pause state of the game. Action triggered by toolbar button.'''
        self.pause = not self.pause
        button.icon = 'play' if self.pause else 'pause'


    def mute_button(self, button):
        '''Toogle mute. Action triggered by toolbar button.'''
        self.mute = not self.mute
        button.icon = 'volume-off' if self.mute else 'volume-high'


    def set_size(self):
        '''
        Define the size of the GameBoard widget. Based on the size of the
        grid, self.size_snake, it calculates the number of pixels of each
        square of the grid, and stores it in self.size_pixels.

        '''
        factor = 0.95
        w_pixels, h_pixels = self.parent.size
        w_pixels_reduced = factor * w_pixels
        h_pixels_reduced = factor * h_pixels
        

        if w_pixels_reduced < h_pixels_reduced:
            self.size_pixels = int(w_pixels_reduced / self.size_snake)
            if self.size_pixels == 0:
                self.size_pixels = 1
            w_grid = self.size_snake
            h_grid = int(h_pixels_reduced / self.size_pixels)
        else:
            self.size_pixels = int(h_pixels_reduced / self.size_snake)
            if self.size_pixels == 0:
                self.size_pixels = 1
            h_grid = self.size_snake
            w_grid = int(w_pixels_reduced / self.size_pixels)

        self.size = w_grid*self.size_pixels, h_grid*self.size_pixels
        self.size_grid = w_grid-1, h_grid-1
        self.active = False



    def start_game(self, *args):
        '''
        Start a new game. Reset the values (score, move, etc.), remove the
        previous snake and food, and recreate a new snake and food. Finally
        set the game to active, which will start moving the snake.

        Returns
        -------
        None.

        '''
        self.play('start-mario')
        self.score = 0
        self.level_progress_bar = 0.0
        app = App.get_running_app()
        self.num_level = int(app.config.get('Snake', 'level_start'))
        self.level = Level(self.size_grid, self.num_level)
        self.new_level()


    def new_level(self):
        '''
        Start a new level. Reset the values (score, move, etc.), remove the
        previous snake and food, and recreate a new snake and food. Finally
        set the game to active, which will start moving the snake.

        Returns
        -------
        None.

        '''
        # reset parameters & clear screen
        self.clear_screen()

        # build wall
        self.build_wall()

        # create snake
        self.create_snake()

        # create food
        self.food = Food()
        self.add_widget(self.food)
        self.food.spawn(self.snake_parts + self.wall)

        # activate game
        self.active = True
        self.change_direction(self.level.get_start_direction())


    def build_wall(self):
        '''
        Build a wall based on the positions defined as walls for the current
        level. For each position, create a brick, give it the right position,
        and add it to the wall list, so it can be tested for collisions.

        '''
        positions = self.level.get_walls()

        for p in positions:
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = p
            self.wall.append(brick)


    def create_snake(self):
        '''
        Create the snake at the beginning of the level. It creates a snake with
        a head, and a number of body parts defined by INITIAL_SNAKE_LENGTH.
        All parts are added at the same position; when the snake starts moving
        the parts will be fall in its correct position.
        
        '''
        head = SnakeHead()
        self.add_widget(head)
        head.pos_nm = self.level.get_start_position()
        self.snake_parts.append(head)
        for _ in range(SNAKE.INITIAL_SNAKE_LENGTH-1):
            new_part = SnakePart()
            self.add_widget(new_part)
            new_part.pos_nm = head.pos_nm
            self.snake_parts.append(new_part)


    def clear_screen(self):
        '''
        Remove all elements of the grid and screen, initialise all variables

        '''
        if len(self.snake_parts) > 0 and hasattr(self.snake_parts[0], 'event'):
            self.snake_parts[0].event.cancel()
        self.snake_parts = []
        self.wall = []
        self.move_x = 0
        self.move_y = 0
        self.set_size()

        # remove previous snake & food & wall
        instances = (SnakeHead, SnakePart, Food, Wall)
        parts = [p for p in self.children if isinstance(p, instances)]
        for p in parts:
            self.remove_widget(p)


    def update(self, *args):
        '''
        Make the move of the snake. This callback is called periodically to
        update the position of the snake, and check if there is a collision
        or it has eaten food.

        Parameters
        ----------
        *args : ?
            Arguments passed by the Clock.schedule function. Not used.

        Returns
        -------
        None.

        '''
        if not self.active or self.pause:
            return

        # save position of parts
        old_positions = []
        for part in self.snake_parts:
            old_positions.append(part.pos_nm)

        # move head
        head = self.snake_parts[0]
        head.n += self.move_x
        head.m += self.move_y
        head.open_mouth(self.food)

        # move body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.pos_nm = old_positions[i-1]

        # borders
        if head.n < 0:
            head.n = self.size_grid[0]
        if head.n > self.size_grid[0]:
            head.n = 0
        if head.m < 0:
            head.m = self.size_grid[1]
        if head.m > self.size_grid[1]:
            head.m = 0

        # check collision
        if self.collision():
            self.game_over()

        # check if food is found
        if head.pos_nm == self.food.pos_nm:
            self.play('eat')
            self.score += self.food.current['score']
            if self.food.current['speed'] > 1:
                self.food.speed_counter += SNAKE.FOOD_SPEED_TIME

            self.speed_food = self.food.current['speed']
            for _ in range(self.food.current['length']):
                new_part = SnakePart()
                self.add_widget(new_part)
                new_part.pos_nm = old_positions[-1]
                self.snake_parts.append(new_part)
            self.food.spawn(self.snake_parts + self.wall)
            head.mouth_open = False

        # change direction of tail based on previous part
        n_prev, m_prev = self.snake_parts[-2].pos_nm
        n_last, m_last = self.snake_parts[-1].pos_nm
        if n_last != n_prev:
            if n_last == n_prev-1 or n_last > n_prev+1:
                direction = 'RIGHT'
            else:
                direction = 'LEFT'
        else:
            if m_last == m_prev-1 or m_last > m_prev+1:
                direction = 'UP'
            else:
                direction = 'DOWN'
        self.snake_parts[-1].direction = direction

        # adjust speed, and speed countdown
        if self.food.speed_counter == 0:
            self.speed = SNAKE.SPEED/self.speed_factor
        else:
            self.speed = SNAKE.SPEED/self.speed_factor/SNAKE.FOOD_SPEED
            self.food.speed_counter -= 1


    def on_snake_parts(self, *args):
        '''
        When the snake_parts changes (i.e. a new part is added), it flags the
        last part as a tail, and all others as non-tail.

        Parameters
        ----------
        *args : ?
            Arguments passed by the event. Not used.

        '''
        # if only head, return
        if len(self.snake_parts) < 2:
            return

        # remove tail flag from all parts
        for p in self.snake_parts[1:]:
            p.is_tail = False


        # change flag
        self.snake_parts[-1].is_tail = True


    def on_score(self, parent, value):
        '''
        When score changes, ensure score is added to the partial level score,
        update the level progress bar and check if end-of level is reached.

        Parameters
        ----------
        parent : object
            Argument passed by the event. Not used.
        value : number
            Argument passed by the event. The value that has changed, i.e.
            the new score.

        '''
        if self.score == 0:
            return

        if self.story:
            self.level.inc_score(self.food.current['score'])
            self.level_progress_bar = self.level.level_pct
            if self.level.level_pct >= 1:
                if self.num_level == 12:
                    self.game_over(win=True)
                else:
                    self.change_level()


    def change_level(self):
        '''
        Actions at the end of the level: play sound, and show a pop-up.
        Then trigger the method start_next_level.

        '''
        self.play('next_level')
        self.active = False
        msg = 'Reached end of level\nMoving to next level.'
        p = PopupButton(title='End of level', msg=msg)
        p.bind(on_dismiss=self.start_next_level)


    def start_next_level(self, *args):
        '''
        Actions to start a new level: increase level count and reset progress
        bar. Then trigger the new_level method.

        Parameters
        ----------
        *args : ?
            Arguments from popup call. Not used

        '''
        self.level.set_level(self.level.num_level+1)
        self.num_level = self.level.num_level
        self.level_progress_bar = self.level.level_pct
        self.new_level()



    def collision(self):
        '''
        Check if the head of the snake has hit a wall or the body of the 
        snake. This is checked at every move of the snake.

        Returns
        -------
        bool
            True if there is a collision; False otherwise.

        '''
        # collision with body
        head = self.snake_parts[0]
        for element in self.snake_parts[1:]:
            if head.pos_nm == element.pos_nm:
                self.remove_widget(head)
                self.add_widget(head)
                return True

        # collision with wall
        for element in self.wall:
            if head.pos_nm == element.pos_nm:
                return True

        return False


    def game_over(self, win=False):
        '''
        Finish the game by playing a sound and showing a popup. 

        Parameters
        ----------
        win : bool, optional
            To define if the end of the game is for a win or a lose. Based on
            that the different sound and popup are shown. The default is False.

        '''
        self.active = False
        if win:
            self.play('win')
            msg = 'Congratulations!\nYOU WIN!!!'
            PopupButton(title='End', msg=msg)
        else:
            self.snake_parts[0].crashed = True
            self.play('game_over')


    def change_direction(self, direct):
        '''
        Change the direction of the snake, based on the argument direct. This
        method includes the logic to decide if it has to change direction
        or not, and setting the variables corresponding to new direction.

        Parameters
        ----------
        direct : string
            Can be one of ['UP', 'DOWN', 'LEFT', 'RIGHT']. This is the new
            direction.

        '''
        if not self.active:
            return
        head = self.snake_parts[0]
        if direct == 'LEFT' and self.move_x == 0:
            self.move_x = -1
            self.move_y = 0
            head.direction = direct
        elif direct =='RIGHT' and self.move_x == 0:
            self.move_x = 1
            self.move_y = 0
            head.direction = direct
        elif direct == 'UP' and self.move_y == 0:
            self.move_x = 0
            self.move_y = 1
            head.direction = direct
        elif direct == 'DOWN' and self.move_y == 0:
            self.move_x = 0
            self.move_y = -1
            head.direction = direct


    def on_touch_down(self, touch):
        '''
        When touch down, store the value of (x, y) in attributes swipe_x
        and swipe_y. These will be used by method on_touch_up.

        Parameters
        ----------
        touch : touch event
            contains the coordinates of the touch.
        '''
        self.swipe_x = touch.x
        self.swipe_y = touch.y


    def on_touch_up(self, touch):
        '''
        When touch up, compare coordinates with swipe_x, swipe_y to find
        the direction of the move, and trigger the move() method.

        Parameters
        ----------
        touch : touch event
            contains the coordinates of the touch.

        Returns
        -------
        direction : string
            Direction of the move.

        '''
        dif_x = self.swipe_x - touch.x
        dif_y = self.swipe_y - touch.y
        if abs(dif_x) > SNAKE.MINIMUM_SWIPE or abs(dif_y) > SNAKE.MINIMUM_SWIPE:
            if abs(dif_x) > abs(dif_y):
                if dif_x > 0:
                    direction = 'LEFT'
                else:
                    direction = 'RIGHT'
            else:
                if dif_y > 0:
                    direction = 'DOWN'
                else:
                    direction = 'UP'
            self.change_direction(direction)

            return direction


    def play(self, sound):
        '''
        Trigger play method from the main app, if not muted.

        Parameters
        ----------
        sound : string
            Key of the dictionary corresponding to the sound to be played.

        '''
        if not self.mute:
            app = App.get_running_app()
            app.play(sound)
