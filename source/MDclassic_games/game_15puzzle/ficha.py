#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:43:35 2021

@author: osso73
"""


# std libraries


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

<Ficha>:
    canvas.before:
        Color:
            rgba: [1,1,1,1] if self.name else [0,0,0,0] 
        Rectangle:
            size: self.size
            pos: self.pos
            source: root.filename

""")

class Ficha(Label):
    '''
    Contains the properties and logic of the tiles and their movement.
    
    Attributes
    ----------    
    name : StringProperty
        Name of the tile, a number between 1 and the size of board -1. It can
        be '' as well, for the empty tile.
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5.
    lado : NumericProperty
        Length of the side, in pixels. Tiles are square.
    posicion : ListProperty
        Position in the board, starting from (0,0) at top-left, to (n,n) 
        bottom-right, n being the size of the board.
    filename : StringProperty
        Filename of the image to be shown.
    '''
    
    name = StringProperty()
    tamano = NumericProperty()
    lado = NumericProperty()
    posicion = ListProperty()
    filename = StringProperty()
    
    def __init__(self, **kwargs):
        super(Ficha, self).__init__(**kwargs)
        self.pos = self.calcular_posicion()
        app = MDApp.get_running_app()
        tema = app.root.ids.fifteen.ids.muestra.tema
        tamano = app.root.ids.fifteen.ids.muestra.tamano
        if self.name:
            self.filename = f'game_15puzzle/images/temas/{tema}/{tamano}/{self.name}.jpg'
        else:
            self.filename = f'game_15puzzle/images/temas/{tema}/{tamano}/{tamano**2}.jpg'

    
    def calcular_posicion(self):
        '''
        Calculate the position on the canvas, in pixels, based on the posicion 
        attribute of the tile

        Returns
        -------
        tuple
            Coordinates (x, y ) of the position on the canvas.
        '''
        return (self.posicion[0]*self.lado + FIFTEEN.SPACING/2, 
                (self.tamano-1-self.posicion[1])*self.lado + FIFTEEN.SPACING/2)

    
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
            ex, ey = empty.posicion
            px, py = self.posicion
            if (ex==px and ey==py+1) or (ex==px and ey==py-1) or\
                (ey==py and ex==px+1) or (ey==py and ex==px-1):
                    empty.posicion, self.posicion = self.posicion, empty.posicion
                    self.parent.parent.parent.play('move2')
                    self.parent.movimientos += 1
            self.parent.end_of_game()
    

    def on_posicion(self, *args):
        '''
        When posicion changes, initiate the Animation of the move to the new
        position.
        '''
        anim = Animation(pos=self.calcular_posicion(), duration=FIFTEEN.MOVE_DURATION)
        anim.start(self)
