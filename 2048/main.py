#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:50:53 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from time import sleep
from random import choice
from functools import partial

SPACING = 20
TILES = 'images/tiles/'
MOVE_DURATION = 0.1


class Tile(Label):
    value = NumericProperty(0)
    position = ListProperty()
    tamano = NumericProperty()
    
    def calc_position(self):
        return (self.position[0]*(self.tamano) + SPACING/2, 
                (self.position[1])*(self.tamano) + SPACING/2)
    
    def on_position(self, *args):
        if self.value:  # don't move empty tiles (e.g. self.value=0)
            anim = Animation(pos=self.calc_position(), duration=MOVE_DURATION)
            anim.start(self)
            

    
class Board(RelativeLayout):
    ventana = NumericProperty()
    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_grid)
    
    def initialize_grid(self, *args):
        self.ventana = min(self.parent.height, self.parent.width)
        
    def start_game(self):
        self.clear_widgets()
        tamano = self.ventana / 4
        for i in range(4):
            for j in range(4):
                self.add_widget(Tile(position=(i, j), tamano=tamano))        
        self.add_tile()

    def add_tile(self, *args):
        new_tile = choice(self.get_empty_tiles())
        new_tile.value = choice([2, 2, 2, 4, 4])
        
    def get_empty_tiles(self):
        return [child for child in self.children if not child.value]


    def get_full_tiles(self, row=-1, col=-1):
        full_tiles = [child for child in self.children if child.value]
        if row != -1:
            full_tiles = [t for t in full_tiles if t.position[0] == row]
        elif col != -1:
            full_tiles = [t for t in full_tiles if t.position[1] == col]
        
        return full_tiles
    
    def move(self, direction):
        if direction == 'right':
            for row in range(2, -1, -1):  # [2, 1, 0]
                tiles = self.get_full_tiles(row=row)
                print('moving line right:', tiles)
                self.move_row_line(direction, tiles)
        elif direction == 'left':
            for row in range(1, 4, +1):  # [1, 2, 3]
                tiles = self.get_full_tiles(row=row)
                print('moving line left:', tiles)
                self.move_row_line(direction, tiles)
        elif direction == 'up':
            for col in range(2, -1, -1):  # [2, 1, 0]
                tiles = self.get_full_tiles(col=col)
                print('moving line up:', tiles)
                self.move_row_line(direction, tiles)
        else:
            for col in range(1, 4, +1):  # [1, 2, 3]
                tiles = self.get_full_tiles(col=col)
                print('moving line down:', tiles)
                self.move_row_line(direction, tiles)
        Clock.schedule_once(self.add_tile, MOVE_DURATION)
    
    def move_row_line(self, direction, row_line):
        for tile in row_line:
            print(f'moving tile {direction}: {tile}')
            self.move_tile(direction, tile)
    
    def move_tile(self, direction, tile):
        old_position = tile.position
        final_position = self.check_final(direction, old_position, tile.value)
        if final_position != old_position:
            print(f'old position: {old_position} -- new position: {final_position}')
            self.add_widget(Tile(position=old_position, tamano=tile.tamano))        
            self.remove_tile(tile)
            self.add_widget(tile)  # to ensure it in on top
            tile_to_remove = self.get_tile(final_position)
            tile.position = final_position
            tile.value += tile_to_remove.value
            Clock.schedule_once(partial(self.remove_tile, tile_to_remove), 
                                MOVE_DURATION)
    
    def remove_tile(self, tile, *args):
        self.remove_widget(tile)
        
    def check_final(self, direction, position, value):
        x, y = position
        if direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        elif direction == 'up':
            y += 1
        else:
            y -= 1
        if (x not in range(4)) or (y not in range(4)):
            return position
        new_position = [x, y]
        new_tile = self.get_tile(new_position)
        if not new_tile:
            raise Exception("tile not found!!")
        if new_tile.value:
            if new_tile.value == value:
                return new_position
            else:
                return position
        return self.check_final(direction, new_position, value)
        
    def get_tile(self, position):
        for child in self.children:
            if child.position == position:
                return child

class ButtonJoystick(Button):
    icon = StringProperty()

class MainScreen(BoxLayout):
    pass

class PuzzleApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (375, 800)
    PuzzleApp().run()

