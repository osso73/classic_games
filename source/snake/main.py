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

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    BooleanProperty
)

import os
from time import time
from random import shuffle
import random
from functools import partial


SIZE = 100
SPEED = 0.2
MINIMUM_SWIPE = 50
IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images



class MainScreen(Widget):
    '''
    This class organizes the main screen.
    '''
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.snake = []
        Clock.schedule_once(self.start_game)
        Clock.schedule_interval(self.update, SPEED)
        

    def update(self, *args):
        if not self.active:
            return
        
        # save position of parts
        old_positions = []
        for part in self.snake:
            old_positions.append(list(part.pos))
        
        
        # move head
        head = self.snake[0]
        head.x += self.move_x
        head.y += self.move_y
       
        # check collision
        if self.collision():
            self.game_over()

        # move body
        for i, part in enumerate(self.snake):
            if i == 0:
                continue
            part.pos = old_positions[i-1]
        
        # check if food is found
        if head.pos == self.food.pos:        
            new_part = SnakePart()
            new_part.pos = old_positions[-1]
            self.snake.append(new_part)
            self.add_widget(new_part)
            self.food.spawn(self.snake)
        
            
        
    def collision(self):
        # collision with body
        head = self.snake[0]
        for part in self.snake[1:]:
            # if head.collide_widget(part):
            if head.pos == part.pos:
                return True
        
        # collision with borders
        if (head.top > self.height or head.y < 0 or 
            head.x < 0 or head.right > self.width):
            
            return True
        
        return False
        
        
        
    def game_over(self):
        self.snake = []
        self.active = False
        
        # remove snake
        parts = [p for p in self.children if isinstance(p, (SnakePart, Food))]
        for p in parts:
            self.remove_widget(p)
        
        self.start_game()
        
    
    def start_game(self, *args):
        w, h = self.size
        w = int(w / SIZE)
        h = int(h / SIZE)
        
        # create snake
        p = [int(w/2)*SIZE, int(h/2)*SIZE]
        head = SnakePart(pos=p)
        head.image = 'images/head_right.png'
        self.add_widget(head)
        self.snake.append(head)
        
        # create food
        self.food = Food(*Window.size)
        self.add_widget(self.food)
        self.food.spawn(self.snake)
        
        # reset parameters
        self.move_x = SIZE
        self.move_y = 0
        self.active = True
        
        
    
    def change_direction(self, direct, *args):
        # if position not multiple of SIZE, re-schedule the function
        head = self.snake[0]
        if head.x % SIZE != 0 or head.y % SIZE != 0:
            Clock.schedule_once(partial(self.change_direction, direct))
        else:
            if direct is 'LEFT' and self.move_x == 0:
                self.move_x = -SIZE
                self.move_y = 0
                head.image = 'images/head_left.png'
            elif direct is 'RIGHT' and self.move_x == 0:
                self.move_x = SIZE
                self.move_y = 0
                head.image = 'images/head_right.png'
            elif direct is 'UP' and self.move_y == 0:
                self.move_x = 0
                self.move_y = SIZE
                head.image = 'images/head_up.png'
            elif direct is 'DOWN' and self.move_y == 0:
                self.move_x = 0
                self.move_y = -SIZE
                head.image = 'images/head_down.png'

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

        

class Food(Widget):
    image = StringProperty()
    size = SIZE, SIZE
    
    def __init__(self, w, h, *args, **kwargs):
        super(Food, self).__init__(*args, **kwargs)
        self.w = int(w / SIZE) - 1
        self.h = int(h / SIZE) - 1
        self.images = os.listdir(os.path.join(IMAGES, 'food'))
        
    
    def spawn(self, snake):
        p = self._get_pos()
        positions = [part.pos for part in snake]
        while p in positions:
            p = self._get_pos()
        
        self.pos = p
        self.image = os.path.join(IMAGES, 'food', random.choice(self.images))
    
    def _get_pos(self):
        return [random.randint(0, self.w)*SIZE,
                random.randint(0, self.h)*SIZE]
 

class SnakePart(Widget):
    image = StringProperty()
    size = SIZE, SIZE


class SnakeApp(App):    
    def build(self):
        self.icon = os.path.join(IMAGES, 'icon.png')
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    # Window.size = (375, 800)
    SnakeApp().run()

