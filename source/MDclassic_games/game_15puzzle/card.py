#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:43:35 2021

@author: osso73
"""


# std libraries
import os

# non-std libraries
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.animation import Animation

from kivymd.app import MDApp

# my app imports
import game_15puzzle.constants as FIFTEEN



Builder.load_string(
    r"""

<Card15>:
    canvas.before:
        Color:
            rgba: [1,1,1,1] if self.name else [0,0,0,0] 
        Rectangle:
            size: self.size
            pos: self.pos
            source: root.filename

""")


class Card15(Label):
    '''
    Contains the properties and logic of the tiles and their movement.
    
    Attributes
    ----------    
    name : StringProperty
        Name of the tile, a number between 1 and the size of board -1. It can
        be '' as well, for the empty tile.
    board_size : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5.
    card_size : NumericProperty
        Length of the side, in pixels. Tiles are square.
    position : ListProperty
        Position in the board, starting from (0,0) at top-left, to (n,n) 
        bottom-right, n being the size of the board.
    filename : StringProperty
        Filename of the image to be shown.
    '''
    
    name = StringProperty()
    board_size = NumericProperty()
    card_size = NumericProperty()
    position = ListProperty()
    filename = StringProperty()
    
    def __init__(self, **kwargs):
        super(Card15, self).__init__(**kwargs)
        self.pos = self.calculate_position()
        app = MDApp.get_running_app()
        theme = app.sm.get_screen('fifteen').ids.sample.theme
        board_size = app.sm.get_screen('fifteen').ids.sample.board_size
        image = self.name if self.name else str(board_size**2)        
        self.filename = os.path.join(FIFTEEN.THEMES, theme, str(board_size), image+'.jpg')

    
    def calculate_position(self):
        '''
        Calculate the position on the canvas, in pixels, based on the position 
        attribute of the tile

        Returns
        -------
        tuple
            Coordinates (x, y ) of the position on the canvas.
        '''
        return (self.position[0]*self.card_size + FIFTEEN.SPACING/2, 
                (self.board_size-1-self.position[1])*self.card_size + FIFTEEN.SPACING/2)

    
    def on_touch_down(self, touch):
        '''
        When tile is touched, it initiates the move to the empty space.

        Parameters
        ----------
        touch : touch event
            Position of the touch in screen.
        '''
        if self.collide_point(*touch.pos):
            self.move()

    
    def move(self):
        '''
        Move the tile if it is adjacent to empty space.
        '''
        empty = self.parent.find_empty()
        if empty:
            ex, ey = empty.position
            px, py = self.position
            if (ex==px and ey==py+1) or (ex==px and ey==py-1) or\
                (ey==py and ex==px+1) or (ey==py and ex==px-1):
                    empty.position, self.position = self.position, empty.position
                    self.parent.parent.parent.play('move2')
                    self.parent.moves += 1
            self.parent.end_of_game()
    

    def on_position(self, *args):
        '''
        When position changes, initiate the Animation of the move to the new
        position.
        '''
        anim = Animation(pos=self.calculate_position(), duration=FIFTEEN.MOVE_DURATION)
        anim.start(self)
