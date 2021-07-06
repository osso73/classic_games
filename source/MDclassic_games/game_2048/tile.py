#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 20:34:19 2021

@author: oriol
"""


# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import  NumericProperty, ListProperty
from kivy.animation import Animation

# my app imports
import game_2048.constants as G2048



Builder.load_string(
    r"""

#:set TILES 'game_2048/images/tiles/'
#:set SPACING 20

<Tile>:
    pos: self.calc_position()
    size_hint: None, None
    size: self.size_pizels - SPACING, self.size_pizels - SPACING
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
            source: TILES + str(self.value)+'.png'

""")

class Tile(Label):
    '''
    Represents one of the tiles in the board.

    Attributes
    ----------
    value : int
        The number shown on the tile. For each value, a different image is
        shown, showing the value and a colour.
    position: list (i, j)
        Position of the tile in the grid. i, j can have values from 0 to 3
    size_pizels: int
        Size of the tile, in pixels. Needed to calculate position of tile in 
        screen
    merged: boolean
        Has this tile been merged? This is put to False when move start, and 
        becomes True in case of merging, to avoid a second merge in the 
        same move
    
    '''
    value = NumericProperty(0)
    position = ListProperty()
    size_pizels = NumericProperty()
    merged = False
    _previous = 0
    
    def calc_position(self):
        '''
        calculate position of Tile in screen, based on attribute self.position

        Returns
        -------
        (x, y) : tuple
            Coordinates in screen
        '''
        return (self.position[0]*(self.size_pizels) + G2048.SPACING, 
                (self.position[1])*(self.size_pizels) + G2048.SPACING)
    
    def on_position(self, *args):
        '''
        When position changes, trigger an animation to move to the new
        position on screen, and play sound of moving Tile.
        '''
        if self.value:  # don't move empty tiles (e.g. self.value=0)
            anim = Animation(pos=self.calc_position(), duration=G2048.MOVE_TILE)
            anim.start(self)
            self.parent.play('move')

    
    def on_value(self, tile, value):
        '''
        When value attribute changes, trigger animation: if previous value
        is 0, animation to spawn a new Tile; if not, animation of merge.

        Use self._previous to store the previous value.
        '''
        x, y = self.size
        if self._previous != 0:
            anim = Animation(size=(1.1*x, 1.1*y), duration=0.05) + \
                Animation(size=(x, y), duration=0.05)
            anim.start(self)
            self.merged = True
            self.parent.score += value
        else:
            m,n = self.pos
            self.size = [0, 0]
            self.pos = [m+self.size_pizels/2, n+self.size_pizels/2]
            anim = Animation(size=(x, y), pos=(m, n), duration=0.1)
        anim.start(self)
        self._previous = self.value
