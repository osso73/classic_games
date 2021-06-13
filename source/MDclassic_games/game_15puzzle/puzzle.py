#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 23:18:57 2021

@author: osso73
"""


# std libraries
from random import shuffle
import math

# non-std libraries
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
from kivy.animation import Animation

from kivymd.app import MDApp

# my app imports
import game_15puzzle.constants as FIFTEEN
from game_15puzzle.ficha import Ficha



Builder.load_string(
    r"""

<Puzzle>:
    size_hint: None, None
    size: self.ventana, self.ventana

""")

class Puzzle(RelativeLayout):
    '''
    This is the widget that holds the logic of the game. Tiles are organized
    through a RelativeLayout so that animation can be used when moving tiles.
    The Tiles are children to this widget, including the empty space.
    
    Attributes
    ----------
    ventana : NumericProperty
        Width and height of the widget. Determined from parent's size.        
    movimientos : NumericProperty
        Count the number of moves made (for the score).
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5
        
    '''
    ventana = NumericProperty(100)
    movimientos = NumericProperty(0)
    tamano = NumericProperty()
    
    def __init__(self, **kwargs):
        super(Puzzle, self).__init__(**kwargs)
        # launch initialize in the next iteration, once the main window is
        # defined, to ensure it has height and width
        Clock.schedule_once(self.initialize_grid)
    
    def initialize_grid(self, *args):
        '''
        Establish the width and height of the widget, based on parent's size
        '''
        self.ventana = min(self.parent.height, self.parent.width)
    
    def start_game(self, *args):
        '''
        Start a new game: play sound of start, build the tiles, reset score.
        '''
        self.parent.parent.play('start')
        self.clear_widgets()
        app = MDApp.get_running_app()
        self.tamano = app.root.ids.fifteen.ids.muestra.tamano
        self.movimientos = 0
        
        # create list of tiles. Each tile has a number, so its order can be
        # checked. A blank tile is added at the end
        lado = int(self.ventana / self.tamano)
        title = list(range(1, self.tamano**2)) + ['']
        shuffle(title)
        
        # ensure that the puzzle is solvable; if not shuffle again
        while not self.is_solvable(title):
            shuffle(title)
        
        # create tiles as widgets added to the Puzzle
        n = 0
        for i in range(self.tamano):
            for j in range(self.tamano):
                self.add_widget(Ficha(name=str(title[n]), lado=lado, 
                                      tamano=self.tamano,
                                      size=(lado-FIFTEEN.SPACING, 
                                            lado-FIFTEEN.SPACING),
                                      size_hint=(None, None), 
                                      posicion=(j, i)))
                n += 1
        # load theme
        self.parent.parent.ids.muestra.load_tema()

    def find_empty(self):
        '''
        Find the empty tile in the board.

        Returns
        -------
        Tile
            The tile that is empty. If no empty tile found, return False.

        '''
        for child in self.children:
            if not child.name:
                return child       
        return False

    def check_win(self):
        '''
        Check if game has finished: all tiles should be in order.

        Returns
        -------
        bool
            True if the game has finished, False if not.

        '''
        for child in self.children:
            if not child.name:
                continue
            if int(child.name) != (child.posicion[0] + 
                                   child.posicion[1] * self.tamano + 1):
                return False        
        return True
    
    def end_of_game(self):
        '''
        Check if the picture is complete. If so, convert empty tile to the 
        last piece of the puzzle, and show it with an animation
        '''
        if self.check_win():
            self.parent.parent.play('end_game')
            lado = int(self.ventana / self.tamano)
            for child in self.children:
                if not child.name:
                    child.name=str(self.tamano**2)
                    child.size=(0,0)
                
                # animation is applied to all tiles
                anim = Animation(size=(lado, lado), duration=0.5)
                anim.start(child)
                

    
    def is_solvable(self, game):
        '''
        Check if the game provided is solvable or not. Based on the algorithm
        explained here: 
        https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

        Parameters
        ----------
        game : list
            Values of the game in the order they are shown. The blank tile 
            should be represented by ''. The values can be int or 
            strings, they are converted to int.

        Raises
        ------
        Exception
            If the game is not square.
        ValueError
            If the blank piece not in the list. It has to be ''.

        Returns
        -------
        bool
            True if the game is solvable; False if not.

        '''
        lado = math.sqrt(len(game))
        if int(lado) != lado:
            raise Exception('Game sequence not an exact square.')
        
        if '' not in game:
            raise ValueError("Blank tile missing. Expected ''")
        
        lado = int(lado)
        seq = [int(n) for n in game if n]
        inversions = 0
        for n in seq:
            for m in seq:
                if seq.index(n) < seq.index(m) and n > m:
                    inversions += 1
        
        if lado % 2:
            if inversions % 2:
                return False
            else:
                return True
        else:
            blank = game.index('')
            row_blank = lado - blank // lado
            if row_blank % 2:
                if not inversions % 2:
                    return True
                else:
                    return False
            else:
                if inversions % 2:
                    return True
                else:
                    return False
                