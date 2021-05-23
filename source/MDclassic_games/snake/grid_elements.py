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
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
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
    size_pixels: app.root.ids.snake.ids.game.size_pixels
    grid: app.root.ids.snake.ids.game.size_grid
    size: self.size_pixels, self.size_pixels


<SnakePart>:
    canvas.before:
        Color:
            rgba: COLOUR_IMAGE if self.image else COLOUR_SNAKE
        Rectangle:
            source: self.image
            pos: self.pos
            size: self.size

<SnakeHead>:
    colour: COLOUR_IMAGE
    canvas.before:
        Color:
            rgba: self.colour
        Rectangle:
            source: self.image
            pos: self.pos
            size: self.size

<Food>:
    canvas.before:
        Color:
            rgba: COLOUR_IMAGE
        Rectangle:
            source: self.image
            pos: self.pos
            size: self.size


<Wall>:
    canvas.before:
        Color:
            rgba: COLOUR_IMAGE
        Rectangle:
            source: 'snake/images/wall.jpg'
            pos: self.pos
            size: self.size

""")




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
        self.images = os.listdir(os.path.join(SNAKE.IMAGES, 'food'))
        self.food_parameters = {
            'fruit': {'speed': 1, 'score': 3, 'length': 1},
            'junk':  {'speed': SNAKE.FOOD_SPEED, 'score': 1, 'length': 2},
            'sweet': {'speed': 1, 'score': 1, 'length': 3},
            }
        self.current = self.food_parameters['fruit']
        self.speed_counter = 0


    def spawn(self, snake):
        p = self._get_pos()
        positions = [ part.pos_nm for part in snake ]
        while p in positions:
            p = self._get_pos()

        self.pos_nm = p
        self.image = os.path.join(SNAKE.IMAGES, 'food', random.choice(self.images))

    def _get_pos(self):
        return [random.choice(range(self.grid[0]+1)),
                random.choice(range(self.grid[1]+1))]

    def on_image(self, *args):
        name = os.path.basename(self.image)
        food_type = name.split('-')[0]
        self.current = self.food_parameters[food_type]


class Wall(GridElement):
    pass


class SnakePart(GridElement):
    image = StringProperty('')
    is_tail = BooleanProperty()
    direction = StringProperty('RIGHT')

    def __init__(self, *args, **kwargs):
        super(SnakePart, self).__init__(*args, **kwargs)
        self.tail_image = dict()
        self.tail_image['LEFT'] = os.path.join(SNAKE.IMAGES, 'snake', 'tail_left.png')
        self.tail_image['RIGHT'] = os.path.join(SNAKE.IMAGES, 'snake', 'tail_right.png')
        self.tail_image['UP'] = os.path.join(SNAKE.IMAGES, 'snake', 'tail_up.png')
        self.tail_image['DOWN'] = os.path.join(SNAKE.IMAGES, 'snake', 'tail_down.png')


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
        self.original_size = self.size
        self.head_images = dict()
        self.head_images['LEFT'] = dict()
        self.head_images['LEFT'][True] = os.path.join(SNAKE.IMAGES, 'snake', 'open_left.png')
        self.head_images['LEFT'][False] = os.path.join(SNAKE.IMAGES, 'snake', 'head_left.png')

        self.head_images['RIGHT'] = dict()
        self.head_images['RIGHT'][True] = os.path.join(SNAKE.IMAGES, 'snake', 'open_right.png')
        self.head_images['RIGHT'][False] = os.path.join(SNAKE.IMAGES, 'snake', 'head_right.png')

        self.head_images['UP'] = dict()
        self.head_images['UP'][True] = os.path.join(SNAKE.IMAGES, 'snake', 'open_up.png')
        self.head_images['UP'][False] = os.path.join(SNAKE.IMAGES, 'snake', 'head_up.png')

        self.head_images['DOWN'] = dict()
        self.head_images['DOWN'][True] = os.path.join(SNAKE.IMAGES, 'snake', 'open_down.png')
        self.head_images['DOWN'][False] = os.path.join(SNAKE.IMAGES, 'snake', 'head_down.png')
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
