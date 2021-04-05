#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15, 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy import metrics

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    BooleanProperty
)

import os
import random
import webbrowser
from time import sleep

from levels import Level


SPEED = 0.25
GRID_SIZES = [11, 15, 19, 23]
SPEED_FACTORS = [0.5, 0.8, 1, 1.5, 2, 3]
MINIMUM_SWIPE = 50
IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images
HELP_URL = 'https://osso73.github.io/classic_games/games/snake/'


class MainScreen(BoxLayout):
    level_progress_bar = NumericProperty(0)

    def help(self):
        webbrowser.open(HELP_URL)


class GameBoard(Widget):
    '''
    This is the board of the game, where all logic occurs. It creates
    as a grid, with n x m squares, where the snake and the food will
    be located. It controls the movement of the snake, checking if there
    is any collision, and when food is eaten, spawning a new food. Keeps
    track of the score.
    
    Attributes
    ----------
    score : NumericProperty
        Score of the game (+1 for every food)
    size_pixels : NumericProperty
        Each square of the grid has size_pixels x size_pixels pixels.
    size_grid : ListProperty
        This is a 2-values list with the number of squares of the grid, in
        the form of [n, m]. So in fact the number of squares are n+1 x m+1.
    size_snake : NumericProperty
        This defines the number of squares that exist in the shortest window
        side. So the higher the number, the smaller will be the squares, and
        therefore the snake and food. It cycles through a number of
        pre-defined values: GRID_SIZES
    wall : list
        Contains all the widgets that form the wall, of type Wall
    snake_parts : list
        Contains all the widgets that form the snake: one SnakeHead, the
        rest SnakePart
    speed_factor : NumericProperty
        This defines the speed of the snake. This factor divides the
        interval between updates, so the higher the value the higher the
        speed of the snake.
    move_x : int
        Defines the move of the snake: value that the position x is 
        incremented/decremented at each step. The unit is the square of the 
        grid, not the pixels. Can be 1, -1 or 0.
    move_y : int
        Defines the move of the snake: value that the position y is 
        incremented/decremented at each step. The unit is the square of the 
        grid, not the pixels. Can be 1, -1 or 0.
    active : boolean
        If True, the update function will move the snake; if False, it will
        do nothing. This is set to False when the game finishes, and set
        to active when a new game starts.
    pause : boolean
        When True, the game will pause (i.e. the update function will not
        update). Set to False by default. This is triggered by button in 
        toolbar.
    mute : boolean
        If True, the sounds will not play; otherwise, they will play. Set
        to False by default. This is triggered by button in toolbar.
    level : Level class
        Object that keeps record of the current level, and has all properties
        associated to the level: wall, maximum score, level score.
    num_level : NumericProperty
        Current level. This can be set by menu buttons, or automatically at 
        the end of the level, moving to next level.
    '''

    score = NumericProperty(0)
    size_pixels = NumericProperty(0)
    size_grid = ListProperty()
    size_snake = NumericProperty(GRID_SIZES[0])
    snake_parts = ListProperty([])
    speed_factor = NumericProperty(1)
    mute = BooleanProperty(False)
    pause = BooleanProperty(False)
    num_level = NumericProperty(1)


    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.wall = []
        self.active = False
        self.sounds = self.load_sounds()
        self.event = Clock.schedule_interval(self.update, SPEED/self.speed_factor)


    def button_size(self):
        '''
        Cycle self.size_snake through a set of pre-defined sizes (GRID_SIZES).
        Show an informative message of the new speed, and to restart
        the game to take into account.
        
        This is called when button "size" is pressed.

        Returns
        -------
        None.

        '''
        sizes = GRID_SIZES
        idx = sizes.index(self.size_snake)
        idx = (idx + 1) % len(sizes)
        self.size_snake = sizes[idx]
        msg = f'Size set to {self.size_snake}\nRestart the game to take it into effect'
        p = PopupWin(title='Size change', content=PopupMsg(text=msg))

        p.open()
        self.set_size()



    def button_speed(self):
        '''
        Cycle self.speed_factor through a set of pre-defined sizes 
        (SPEED_FACTORS).
        
        This is called when button "speed" is pressed.

        Returns
        -------
        None.

        '''
        speeds = SPEED_FACTORS
        idx = speeds.index(self.speed_factor)
        idx = (idx + 1) % len(speeds)
        self.speed_factor = speeds[idx]
        self.event.cancel()
        self.event = Clock.schedule_interval(self.update, SPEED/self.speed_factor)


    def set_size(self):
        '''
        Define the size of the GameBoard widget. Based on the size of the
        grid, self.size_snake, it calculates the number of pixels of each 
        square of the grid, and stores it in self.size_pixels.

        Returns
        -------
        None.

        '''
        factor = 0.95
        side = factor * min(*self.parent.size)
        self.size_pixels = int(side / self.size_snake)
        w = int(factor*self.parent.width / self.size_pixels)
        h = int(factor*self.parent.height / self.size_pixels)
        self.size = (w*self.size_pixels, h*self.size_pixels)
        self.size_grid = w-1, h-1
        self.active = False



    def start_game(self):
        '''
        Start a new game. Reset the values (score, move, etc.), remove the
        previous snake and food, and recreate a new snake and food. Finally
        set the game to active, which will start moving the snake.

        Returns
        -------
        None.

        '''
        self.play('start')
        self.score = 0
        self.num_level = 1
        self.level = Level(self.size_grid, self.num_level)
        self.new_level()


    def new_level(self):
        '''
        Start a new game. Reset the values (score, move, etc.), remove the
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
        positions = self.level.get_walls()
        
        for p in positions:
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = p
            self.wall.append(brick)


    def create_snake(self):
        head = SnakeHead()
        self.add_widget(head)
        head.pos_nm = self.level.get_start_position()
        self.snake_parts.append(head)
        for _ in range(2):
            new_part = SnakePart()
            self.add_widget(new_part)
            new_part.pos_nm = head.pos_nm
            self.snake_parts.append(new_part)
            

    def clear_screen(self):
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
            self.score += 1
            self.play('eat')
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
            
    
    def on_snake_parts(self, *args):
        '''
        When the snake_parts changes (i.e. a new part is added), it flags the
        last part as a tail, and all others as non-tail.

        Parameters
        ----------
        *args : ?
            Arguments passed by the event. Not used.

        Returns
        -------
        None.

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

        Returns
        -------
        None.

        '''
        if self.score == 0:
            return
        
        # self.level.level_curr_score += 1
        self.level.inc_score(+1)
        app = App.get_running_app()
        app.root.level_progress_bar = self.level.level_pct
        if self.level.level_pct >= 1:
            if self.num_level == 12:
                self.game_over(win=True)
            else:
                self.change_level()
    
    
    def change_level(self):
        self.play('next_level')
        self.active = False
        msg = 'Reached end of level\nMoving to next level.'
        p = PopupWin(title='End of level', content=PopupMsg(text=msg))
        p.bind(on_dismiss=self.start_next_level)
        p.open()
    
    def start_next_level(self, *args):
        self.level.set_level(self.level.num_level+1)
        self.num_level = self.level.num_level
        app = App.get_running_app()
        app.root.level_progress_bar = self.level.level_pct
        self.new_level()
        
            
    
    def collision(self):
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
        self.active = False
        if win:
            self.play('win')
            msg = 'Congratulations!\nYOU WIN!!!'
            p = PopupWin(title='End', content=PopupMsg(text=msg))
            p.open()

        else:
            self.snake_parts[0].crashed = True
            self.play('game_over')


    def change_direction(self, direct, *args):
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
        if abs(dif_x) > MINIMUM_SWIPE or abs(dif_y) > MINIMUM_SWIPE:
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

    def load_sounds(self):
        '''
        Load all sounds of the game, and put them into the dictionary.

        Returns
        -------
        sound : dict
            The dictionary of sounds that have been loaded
        '''
        sound = dict()
        folder = os.path.join(os.path.dirname(__file__),'audio')
        for s in ['bye', 'eat', 'start', 'next_level', 'game_over', 'win']:
            sound[s] = SoundLoader.load(os.path.join(folder, f'{s}.ogg'))

        return sound


    def play(self, sound):
        '''
        Play a sound from the dictionary of sounds.

        Parameters
        ----------
        sound : string
            Key of the dictionary corresponding to the sound to be played.

        Raises
        ------
        Exception
            If string passed is not in the dictionary.
        '''
        if self.mute:
            return
        
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")


    def bye(self):
        '''
        Play a sound before closing the app, and wait a delay so the sound
        can be heard (Trump saying 'thank you very much')
        '''
        self.play('bye')
        sleep(1.5)


class GridElement(Widget):
    n = NumericProperty()
    m = NumericProperty()
    pos_nm = ListProperty()
    grid = ListProperty()

    def __init__(self, *args, **kwargs):
        super(GridElement, self).__init__(*args, **kwargs)


    def set_position(self):
        self.x = self.parent.x + self.n * self.width
        self.y = self.parent.y + self.m * self.height

    def on_n(self, *args):
        self.n = int(self.n)
        self.pos_nm = [self.n, self.m]

    def on_m(self, *args):
        self.m = int(self.m)
        self.pos_nm = [self.n, self.m]

    def on_pos_nm(self, *args):
        self.n, self.m = self.pos_nm
        self.set_position()




class Food(GridElement):
    image = StringProperty()

    def __init__(self, *args, **kwargs):
        super(Food, self).__init__(*args, **kwargs)
        self.images = os.listdir(os.path.join(IMAGES, 'food'))


    def spawn(self, snake):
        p = self._get_pos()
        positions = [ part.pos_nm for part in snake ]
        while p in positions:
            p = self._get_pos()

        self.pos_nm = p
        self.image = os.path.join(IMAGES, 'food', random.choice(self.images))


    def _get_pos(self):
        return [random.choice(range(self.grid[0]+1)),
                random.choice(range(self.grid[1]+1))]


class Wall(GridElement):
    pass


class SnakePart(GridElement):
    image = StringProperty('')
    is_tail = BooleanProperty()
    direction = StringProperty('RIGHT')
    
    def __init__(self, *args, **kwargs):
        super(SnakePart, self).__init__(*args, **kwargs)
        self.tail_image = dict()
        self.tail_image['LEFT'] = os.path.join(IMAGES, 'snake', 'tail_left.png')
        self.tail_image['RIGHT'] = os.path.join(IMAGES, 'snake', 'tail_right.png')
        self.tail_image['UP'] = os.path.join(IMAGES, 'snake', 'tail_up.png')
        self.tail_image['DOWN'] = os.path.join(IMAGES, 'snake', 'tail_down.png')
    
    
    def on_is_tail(self, *args):
        if self.is_tail:
            self.image = self.tail_image[self.direction]
        else:
            self.image = ''
        
    def on_direction(self, *args):
        if self.is_tail:
            self.image = self.tail_image[self.direction]
        else:
            self.image = ''



class SnakeHead(GridElement):
    image = StringProperty()
    direction = StringProperty()
    mouth_open = BooleanProperty(False)
    crashed = BooleanProperty(False)
    colour = ListProperty()


    def __init__(self, *args, **kwargs):
        super(SnakeHead, self).__init__(*args, **kwargs)
        self.counter = 0
        self.head_images = dict()
        self.head_images['LEFT'] = dict()
        self.head_images['LEFT'][True] = os.path.join(IMAGES, 'snake', 'open_left.png')
        self.head_images['LEFT'][False] = os.path.join(IMAGES, 'snake', 'head_left.png')

        self.head_images['RIGHT'] = dict()
        self.head_images['RIGHT'][True] = os.path.join(IMAGES, 'snake', 'open_right.png')
        self.head_images['RIGHT'][False] = os.path.join(IMAGES, 'snake', 'head_right.png')

        self.head_images['UP'] = dict()
        self.head_images['UP'][True] = os.path.join(IMAGES, 'snake', 'open_up.png')
        self.head_images['UP'][False] = os.path.join(IMAGES, 'snake', 'head_up.png')

        self.head_images['DOWN'] = dict()
        self.head_images['DOWN'][True] = os.path.join(IMAGES, 'snake', 'open_down.png')
        self.head_images['DOWN'][False] = os.path.join(IMAGES, 'snake', 'head_down.png')
        self.list_colours = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1],
                             [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], 
                             [1, 1, 1, 1]]


    def on_direction(self, *args):
        self.change_image()

    def on_mouth_open(self, *args):
        self.change_image()

    def open_mouth(self, food):
        radius = self.width
        if abs(food.x - self.x) <= radius and abs(food.y - self.y) <= radius:
            self.mouth_open = True
        else:
            self.mouth_open = False

    def change_image(self):
        self.image = self.head_images[self.direction][self.mouth_open]
    
    def on_crashed(self, *args):
        self.event = Clock.schedule_interval(self.change_colour, 0.2)
    
    def change_colour(self, *args):
        idx = self.list_colours.index(self.colour)
        idx = (idx +1) % len(self.list_colours)
        self.colour = self.list_colours[idx]
        self.counter += 1
        if self.counter == 10:
            return False


class MenuButton(Button):
    pass

class MenuButtonImage(Button):
    image = ListProperty(['',''])

class MenuLabel(Label):
    pass

class PopupMsg(Label):
    pass

class PopupWin(Popup):
    def on_content(self, *args):
        '''Trigger change of size when the contents changes. Schedule
        a call to give enough time to calculate size of the content.
        '''
        Clock.schedule_once(self.change_size)

    def change_size(self, *args):
        '''Set the size of the window based on the text of the content'''
        x, y = self.content.size
        self.size = x + metrics.sp(30), y + metrics.sp(100)
        


class SnakeApp(App):
    def build(self):
        self.icon = os.path.join(IMAGES, 'icon.png')
        main = MainScreen()
        return main


if __name__ == '__main__':
    SnakeApp().run()
