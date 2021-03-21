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
from functools import partial
from time import sleep


SIZE = 100
SPEED = 0.3
MINIMUM_SWIPE = 50
IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images


class MainScreen(BoxLayout):
    pass


class GameBoard(FloatLayout):
    
    '''
    This is the board of the game, where all logic occurs.
    '''
    
    score = NumericProperty(0)
    
    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.snake_parts = []
        self.active = False
        Clock.schedule_interval(self.update, SPEED)
        self.sounds = self.load_sounds()
        # Clock.schedule_once(self.start_game)

    def start_game(self, *args):
        # reset parameters
        self.snake_parts = []
        self.move_x = 0
        self.move_y = 0
        self.score = 0

        # remove previous snake & food
        instances = (SnakeHead, SnakePart, Food)
        parts = [p for p in self.children if isinstance(p, instances)]
        for p in parts:
            self.remove_widget(p)

        w, h = self.size
        print('window size:', w, h)
        w_int = int(w / SIZE)
        h_int = int(h / SIZE)
        
        # create snake
        p = [int(w_int/2)*SIZE, int(h_int/2)*SIZE]
        head = SnakeHead(pos=p)
        self.add_widget(head)
        self.snake_parts.append(head)

        # create food
        self.food = Food(w, h)
        self.food.spawn(self.snake_parts)
        self.add_widget(self.food)
        
        # activate game
        self.play('start')
        self.active = True
        self.change_direction('RIGHT')

    
    def update(self, *args):
        if not self.active:
            return
        
        # save position of parts
        old_positions = []
        for part in self.snake_parts:
            old_positions.append(list(part.pos))
        
        
        # move head
        head = self.snake_parts[0]
        head.x += self.move_x
        head.y += self.move_y
        head.open_mouth(self.food)
       
        # check collision
        if self.collision():
            self.game_over()

        # move body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.pos = old_positions[i-1]
        
        # check if food is found
        if head.pos == self.food.pos:        
            self.score += 1
            self.play('eat')
            new_part = SnakePart()
            new_part.pos = old_positions[-1]
            self.snake_parts.append(new_part)
            self.add_widget(new_part)
            self.food.spawn(self.snake_parts)
            head.mouth_open = False
            
        
    def collision(self):
        # collision with body
        head = self.snake_parts[0]
        for part in self.snake_parts[1:]:
            if head.pos == part.pos:
                return True

        # collision with borders
        if (head.y + SIZE > self.height or head.y < 0 or 
            head.x < 0 or head.x + SIZE > self.width):
            
            return True
        
        return False
        
                
    def game_over(self):
        self.active = False
        self.play('end_game')
        p = Popup(title='End', size_hint=(0.75, 0.3),
          content=PopupMsg(text='Sorry, snake crashed!'))
        p.open()

    
    def change_direction(self, direct, *args):
        # if position not multiple of SIZE, re-schedule the function
        head = self.snake_parts[0]
        if direct is 'LEFT' and self.move_x == 0:
            self.move_x = -SIZE
            self.move_y = 0
            head.direction = direct
        elif direct is 'RIGHT' and self.move_x == 0:
            self.move_x = SIZE
            self.move_y = 0
            head.direction = direct
        elif direct is 'UP' and self.move_y == 0:
            self.move_x = 0
            self.move_y = SIZE
            head.direction = direct
        elif direct is 'DOWN' and self.move_y == 0:
            self.move_x = 0
            self.move_y = -SIZE
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
        return [random.randint(0, self.w) * SIZE,
                random.randint(0, self.h) * SIZE]
 

class SnakePart(Widget):
    size = SIZE, SIZE


class SnakeHead(Widget):
    image = StringProperty()
    direction = StringProperty()
    mouth_open = BooleanProperty(False)
    size = SIZE, SIZE
    
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
        radius = SIZE
        if abs(food.x - self.x) <= radius and abs(food.y - self.y) <= radius:
            self.mouth_open = True
        else:
            self.mouth_open = False
    
    def change_image(self):
        self.image = self.head_images[self.direction][self.mouth_open]


class MenuButton(Button):
    pass


class MenuLabel(Label):
    pass

class PopupMsg(Label):
    pass


class SnakeApp(App):    
    def build(self):
        self.icon = os.path.join(IMAGES, 'icon.png')
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    # Window.size = (375, 800)
    SnakeApp().run()

