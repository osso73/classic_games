#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15, 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy import metrics

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    BooleanProperty
)

import os
import random
import webbrowser
from functools import partial
from time import sleep


SPEED = 0.3
GRID_SIZES = [9, 15, 21, 27]
SPEED_FACTORS = [0.5, 0.8, 1, 1.5, 2, 3]
MINIMUM_SWIPE = 50
IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images
HELP_URL = 'https://osso73.github.io/classic_games/games/snake/'


class MainScreen(BoxLayout):
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
    '''

    score = NumericProperty(0)
    size_pixels = NumericProperty(0)
    size_grid = ListProperty()
    size_snake = NumericProperty(9)
    speed_factor = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.snake_parts = []
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
        factor = 0.90
        side = factor * min(*self.parent.size)
        self.size_pixels = int(side / self.size_snake)
        w = int(factor*self.parent.width / self.size_pixels)
        h = int(factor*self.parent.height / self.size_pixels)
        self.size = (w*self.size_pixels, h*self.size_pixels)
        self.size_grid = w-1, h-1


    def start_game(self):
        '''
        Start a new game. Reset the values (score, move, etc.), remove the
        previous snake and food, and recreate a new snake and food. Finally
        set the game to active, which will start moving the snake.

        Returns
        -------
        None.

        '''
        # reset parameters
        self.snake_parts = []
        self.wall = []
        self.move_x = 0
        self.move_y = 0
        self.score = 0
        self.set_size()

        # remove previous snake & food
        instances = (SnakeHead, SnakePart, Food, Wall)
        parts = [p for p in self.children if isinstance(p, instances)]
        for p in parts:
            self.remove_widget(p)

        # build wall
        self.build_wall()

        # create snake
        head = SnakeHead()
        self.add_widget(head)
        n_ini, m_ini = self.size_grid
        head.pos_nm = n_ini / 2, m_ini / 2
        self.snake_parts.append(head)
        for _ in range(2):
            new_part = SnakePart()
            self.add_widget(new_part)
            new_part.pos_nm = head.pos_nm
            self.snake_parts.append(new_part)
            

        # create food
        self.food = Food()
        self.add_widget(self.food)
        self.food.spawn(self.snake_parts + self.wall)

        # activate game
        self.play('start')
        self.active = True
        self.change_direction('RIGHT')
    
    
    def build_wall(self):
        # around the screen
        n_max, m_max = self.size_grid
        n_list = [n for n in range(n_max+1)]
        m_list = [m for m in range(m_max+1)]
        
        if n_max < m_max:
            idx = int((n_max + 1) / 3)
            n_list = n_list[:idx] + n_list[-idx:]
            idx = int((m_max + 1) / 6)
            m_list = m_list[:idx] + m_list[2*idx:-2*idx] + m_list[-idx:]
        else:
            idx = int((m_max + 1) / 3)
            m_list = m_list[:idx] + m_list[-idx:]
            idx = int((n_max + 1) / 6)
            n_list = n_list[:idx] + n_list[2*idx:-2*idx] + n_list[-idx:]
            
        for i in n_list:
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = i, 0
            self.wall.append(brick)
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = i, m_max
            self.wall.append(brick)
        
        for j in m_list:
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = 0, j
            self.wall.append(brick)
            brick = Wall()
            self.add_widget(brick)
            brick.pos_nm = n_max, j
            self.wall.append(brick)
            
            
        
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
        if not self.active:
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


    def game_over(self):
        self.active = False
        self.play('end_game')
        msg = 'Sorry, snake crashed!'
        p = PopupWin(title='End', content=PopupMsg(text=msg))
        p.open()


    def change_direction(self, direct, *args):
        if not self.active:
            return
        head = self.snake_parts[0]
        if direct is 'LEFT' and self.move_x == 0:
            self.move_x = -1
            self.move_y = 0
            head.direction = direct
        elif direct is 'RIGHT' and self.move_x == 0:
            self.move_x = 1
            self.move_y = 0
            head.direction = direct
        elif direct is 'UP' and self.move_y == 0:
            self.move_x = 0
            self.move_y = 1
            head.direction = direct
        elif direct is 'DOWN' and self.move_y == 0:
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
        for s in ['bye', 'eat', 'start', 'end_game']:
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
    pass


class SnakeHead(GridElement):
    image = StringProperty()
    direction = StringProperty()
    mouth_open = BooleanProperty(False)


    def __init__(self, *args, **kwargs):
        super(SnakeHead, self).__init__(*args, **kwargs)
        self.head_images = dict()
        self.head_images['LEFT'] = dict()
        self.head_images['LEFT'][True] = os.path.join(IMAGES, 'head', 'open_left.png')
        self.head_images['LEFT'][False] = os.path.join(IMAGES, 'head', 'head_left.png')

        self.head_images['RIGHT'] = dict()
        self.head_images['RIGHT'][True] = os.path.join(IMAGES, 'head', 'open_right.png')
        self.head_images['RIGHT'][False] = os.path.join(IMAGES, 'head', 'head_right.png')

        self.head_images['UP'] = dict()
        self.head_images['UP'][True] = os.path.join(IMAGES, 'head', 'open_up.png')
        self.head_images['UP'][False] = os.path.join(IMAGES, 'head', 'head_up.png')

        self.head_images['DOWN'] = dict()
        self.head_images['DOWN'][True] = os.path.join(IMAGES, 'head', 'open_down.png')
        self.head_images['DOWN'][False] = os.path.join(IMAGES, 'head', 'head_down.png')


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


class MenuButton(Button):
    pass

class MenuButtonSmall(Button):
    pass

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
    # Window.size = (1080, 2340)
    # Window.size = (375, 800)
    SnakeApp().run()
