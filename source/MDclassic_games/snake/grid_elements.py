#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 21:11:44 2021

@author: oriol
"""

# std libraries
import os
import random

# non-std libraries
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder

# my app imports
import snake.constants as SNAKE


Builder.load_string(
    r"""

#:set COLOUR_IMAGE [1, 1, 1, 1]
#:set COLOUR_SNAKE [140/255, 198/255, 62/255, 1]

<GridElement>:
    size_pixels: app.sm.get_screen('snake').ids.game.size_pixels
    grid: app.sm.get_screen('snake').ids.game.size_grid
    size: self.size_pixels, self.size_pixels
    colour: COLOUR_IMAGE
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.rotation[self.direction]
            origin: self.center
        Color:
            rgba: self.colour if self.image else COLOUR_SNAKE
        Rectangle:
            source: self.image
            pos: self.pos
            size: self.size
    canvas.after:
        PopMatrix

""")




class GridElement(Widget):
    '''
    This class defines the mechanisms to translate the position of an element
    in the grid to the position on the screen in pixels. All elements (head,
    body parts, food) inherit from this class.
    
    Attributes
    ----------
    active : boolean
        If True, the update function will move the snake; if False, it will
        do nothing. This is set to False when the game finishes, and set
        to active when a new game starts.
    n, m : NumericProperty
        Coordinates in the grid.
    pos_nm : ListProperty
        The two coordinates n and m in a list of 2.
    grid: ListProperty
        Size of the grid. Inherits from parent.
    image : StringProperty
        name of the image to be shown. It can be the tail, or none.
    direction : StringProperty
        Direction of the tail. Can be one of ['LEFT', 'RIGHT', 'UP', 'DOWN'].
    rotation : DictProperty
        Contains the angle of rotation of tail image for each direction.
    colour: ListProperty
        Colour (in rgba) of the element. Used when crashing to change colours
        of the head.

    '''
    n = NumericProperty()
    m = NumericProperty()
    pos_nm = ListProperty()
    grid = ListProperty()
    image = StringProperty('')
    direction = StringProperty('RIGHT')
    rotation = DictProperty({'RIGHT': 0, 'UP': 90, 'LEFT': 180, 'DOWN': 270})
    colour = ListProperty()


    def set_position(self):
        '''Set the position on the screen, based on n,m coordinates'''
        self.x = self.parent.x + self.n * self.width
        self.y = self.parent.y + self.m * self.height


    def on_n(self, *args):
        '''When n changes, update pos_nm'''
        self.n = int(self.n)
        self.pos_nm = [self.n, self.m]


    def on_m(self, *args):
        '''When m changes, update pos_nm'''
        self.m = int(self.m)
        self.pos_nm = [self.n, self.m]


    def on_pos_nm(self, *args):
        '''
        When pos_nm changes, trigger set_position (e.g. update position 
        on screen
        
        '''
        self.n, self.m = self.pos_nm
        self.set_position()


class Food(GridElement):
    '''
    This class to define the food, and its behaviour. It inherits from the
    GridElement, so it can be positioned on the grid by giving grid coordinates
    
    Attributes:
    -----------
    images : list
        Contains all the different images available on the image folder.
    current : dict
        Dictionary of the parameters of the current food. These are: 
            speed: what increase of speed when eaten
            score: how many points it adds when eaten
            length: what length is added to the snake when eaten
    speed_counter: int
        Counter of the number of moves used with high speed. Used to limit the
        amount of time the snake goes to a higher speed.
        
    '''

    def __init__(self, *args, **kwargs):
        super(Food, self).__init__(*args, **kwargs)
        self.images = os.listdir(os.path.join(SNAKE.IMAGES, 'food'))
        self.current = SNAKE.FOOD_PARAMETERS['fruit']
        self.speed_counter = 0


    def spawn(self, snake):
        '''
        Generate a new random food on a random position on the grid 
        (except on a wall or on the snake)
        
        '''
        p = self._get_pos()
        positions = [ part.pos_nm for part in snake ]
        while p in positions:
            p = self._get_pos()

        self.pos_nm = p
        self.image = os.path.join(SNAKE.IMAGES, 'food', random.choice(self.images))


    def _get_pos(self):
        '''Return a random position within the grid'''
        
        return [random.choice(range(self.grid[0]+1)),
                random.choice(range(self.grid[1]+1))]


    def on_image(self, *args):
        '''When image changes, update the food parameters.'''
        
        name = os.path.basename(self.image)
        food_type = name.split('-')[0]
        self.current = SNAKE.FOOD_PARAMETERS[food_type]


class Wall(GridElement):
    '''Defines the wall element, used to load the image. No actions.'''

    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.image = os.path.join(SNAKE.IMAGES, 'wall.jpg')


class SnakePart(GridElement):
    '''
    Defines the snake part, i.e. any part except the head (separate class).
    Each snake part can be defined as tail, in which case will show the tail
    image, or normal, which shows no image, just the green colour.
    
    Attributes:
    -----------
    is_tail : BooleanProperty
        True if the part is the tail. False otherwise.
        
    '''
    is_tail = BooleanProperty()


    def on_is_tail(self, *args):
        '''When is_tail changes its state, change the image accordingly'''
        
        if self.is_tail:
            self.image = os.path.join(SNAKE.IMAGES, 'snake', 'tail.png')
        else:
            self.image = ''
        


class SnakeHead(GridElement):
    '''
    Defines the head of the snake, with methods to open/close mouth, and
    change direction..
    
    Attributes:
    -----------
    list_colours : list
        List of colours to be shown when crashing. It iterates through this
        list.
    mouth_open : BooleanProperty
        True if the mouth should be open; False otherwise. Mouth is open if
        close to the food.
    crashed : BooleanProperty
        True when the snake has collisioned; False otherwise. When True, it 
        triggers the changes in colour.
        
    '''
    mouth_open = BooleanProperty(False)
    crashed = BooleanProperty(False)


    def __init__(self, *args, **kwargs):
        super(SnakeHead, self).__init__(*args, **kwargs)
        self.original_size = self.size
        self.image = os.path.join(SNAKE.IMAGES, 'snake', 'head.png')
        self.list_colours = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1],
                             [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1],
                             [1, 1, 1, 1]]


    def on_mouth_open(self, *args):
        '''When mouth_opn changes its state, change the image of the head'''

        name = 'open' if self.mouth_open else 'head'
        self.image = os.path.join(SNAKE.IMAGES, 'snake', name+'.png')


    def open_mouth(self, food):
        '''
        Check if mouth should be open or not, by measuring distance to the 
        food, and set the variable mouth_open
        
        '''        
        radius = self.width
        if abs(food.x - self.x) <= radius and abs(food.y - self.y) <= radius:
            self.mouth_open = True
        else:
            self.mouth_open = False


    def on_crashed(self, *args):
        '''When crashed is True, trigger the sequence of changing colours'''
        
        self.event = Clock.schedule_interval(self.change_colour, 0.2)


    def change_colour(self, *args):
        '''Change colour of the snake. It goes through the list_colours'''

        idx = self.list_colours.index(self.colour)
        idx = (idx +1) % len(self.list_colours)
        self.colour = self.list_colours[idx]
