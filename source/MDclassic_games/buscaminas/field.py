#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 10:09:16 2021

@author: oriol
"""


# std libraries
import os
from time import time
from random import shuffle

# non-std libraries
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

# my app imports
import buscaminas.constants as MINAS
from buscaminas.area import Area



Builder.load_string(
    r"""

<Field>:
    canvas:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Rectangle:
            size: self.size
            pos: self.pos
    size_hint: None, None
    size: self.parent.width, self.parent.width
    cols: self.columnas

""")



class Field(GridLayout):
    '''
    This is the field where all mines are distributed.
    
    Attributes
    ----------
    columnas : NumericProperty
        Number of columns of the field
    filas : NumericProperty
        Number of rows of the field
    mines : NumericProperty
        Number of mines
    time : NumericProperty
        Number of seconds since the start of the game
    game_active : boolean
        Determines if the game is ongoing or not. When True, the clicks 
        trigger actions; if False, nothing happens until the start button is
        clicked again.
    sounds : dictionary
        Dictionary with all the sounds of the game.
    '''
    columnas = NumericProperty(9)
    filas = NumericProperty(9)
    mines = NumericProperty(0)
    time = NumericProperty(0)
    game_active = False
    level = 1
    mode = 'covered'
    mute = False
    
    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)
        self._start_time = 0
        Clock.schedule_interval(self.tick, 0.1)
        self.sounds = self.load_sounds()
        
    def load_sounds(self):
        '''
        Load all sounds of the game, and put them into the dictionary.

        Returns
        -------
        sound : dict
            The dictionary of sounds that have been loaded

        '''
        sound = dict()
        folder = os.path.join(os.path.dirname(__file__),'sounds')
        for s in ['lose', 'win']:
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
        if self.mute:
            return
        
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")

    def start_game(self, *args):
        '''
        Start a new game: reset score and timer, rebuild the field.
        '''
        self.parent.parent.ids.start_button.change_face('standard')
        ventana_width = self.parent.width
        ventana_height = (self.parent.height - 
                          self.parent.parent.ids.toolbar.height -
                          self.parent.parent.ids.menu.height) / 2
        self.mines = MINAS.LEVELS[self.level]['mines']
        self.columnas = MINAS.LEVELS[self.level]['columnas']
        self.filas = MINAS.LEVELS[self.level]['filas']
        self.size = (ventana_width * MINAS.LEVELS[self.level]['window'][0], 
                     ventana_height * MINAS.LEVELS[self.level]['window'][1])
            
        self.clear_widgets()
        self.distribute_mines()
        self.find_adjacent_mines()
        self.game_active = True
        self._start_time = time()


    def tick(self, *args):
        '''
        Update timer. This function is called every 0.1s
        '''
        if self.game_active:
            self.time = int(time() - self._start_time)
              
            
    def distribute_mines(self):
        '''
        Create a field with mines distributed randomly. The number of mines 
        is defined by mines attribute.
        '''
        areas = [9]*self.mines + [0]*(self.columnas*self.filas - self.mines)
        shuffle(areas)
        
        n=0
        for i in range(self.filas):
            for j in range(self.columnas):
                self.add_widget(Area(posicion=[j, i], value=areas[n]))
                n += 1
    
    def find_adjacent_mines(self):
        '''
        For each area, find the number of adjacent mines, and establish it
        as its value. 
        '''
        for area in self.children:
            if area.value != 9:  # skip if area is a bomb
                neighbours = self.find_neighbours(area.posicion)
                for n in neighbours:
                    if n.value == 9:
                        area.value += 1
    
    def find_neighbours(self, p):
        '''
        Given a position p, return a list with all neighbour areas.

        Parameters
        ----------
        p : list
            Coordinates of the position of the tile in the Field.

        Returns
        -------
        ret : list
            List of tiles that are neighbours to tile in position p.

        '''
        ret = list()
        for child in self.children:
            if child.posicion != list(p):
                i, j = child.posicion
                if (p[0]-1 <= i <= p[0]+1) and (p[1]-1 <= j <= p[1]+1):
                    ret.append(child)
        
        return ret
    
    def check_uncover(self, area):
        '''
        Check if the game has finished, or the last uncovered has 0 adjacent 
        mines. If any of these sitations is true, trigger actions.
        
        This method is triggered every time an area is uncovered.

        Parameters
        ----------
        area : Area
            Area where the last action has taken place.

        '''
        if area.value == 9:
            # game lost
            self.game_lost()
        if not area.value:
            # 0 adjacent mines
            self.no_adjacent_mines(area)
        
        if self.all_discovered():
            # game won
            self.game_won()
    
    
    def all_discovered(self):
        '''
        Check if all mines have been flagged, and all non-mines uncovered.

        Returns
        -------
        Boolean.
            True if all mines are flagged and non-mines uncovered. False 
            otherwise

        '''
        uncovered = [ a for a in self.children if (a.value != 9 and 
                                                   not a.uncovered) ]
        bombs_without_flag = [ a for a in self.children if (a.value == 9 and 
                                                            not a.flag) ]

        if not len(uncovered) and not len(bombs_without_flag):
            return True
        else:
            return False
        
        
    def game_lost(self):
        '''
        When game is lost, show all mines and change the face of button.
        '''
        self.game_active = False
        self.parent.parent.ids.start_button.change_face('lost')
        self.play('lose')
        for area in self.children:
            if area.flag and area.value != 9:
                area.set_show(name='wrong')
            elif area.value == 9 and not area.flag:
                area.uncovered = True
    
    def game_won(self):
        '''
        When game is won, a popup is shown.
        '''
        self.game_active = False
        self.parent.parent.ids.start_button.change_face('won')
        self.play('win')
    
    def no_adjacent_mines(self, area):
        '''
        Uncover all adjacent areas.
        
        Parameters
        ----------
        area : Area
            Area which has a value of 0
        '''
        neighbours = self.find_neighbours(area.posicion)
        for neighbour in neighbours:
            neighbour.uncover()
    
    def open_adjacent(self, area):
        '''
        If area has the same number of flagged neighbours as mines, uncover 
        all the other adjacent areas.
        
        This method is triggered when clicking on an uncovered aera.

        Parameters
        ----------
        area : Area
            Area around which we need to open the uncovered areas.

        '''
        if 0 < area.value < 9:
            neighbours = self.find_neighbours(area.posicion)
            flagged = [n for n in neighbours if n.flag]
            if len(flagged) == area.value:
                not_flagged = [n for n in neighbours if not n.flag]
                for tile in not_flagged:
                    tile.uncover()

    def entry_mode(self, button):
        if self.mode == 'bandera':
            self.mode = 'covered'
            button.icon = 'bomb'
        else:
            self.mode = 'bandera'
            button.icon  = 'flag'
        
    def set_level(self, button):
        self.level = self.level % 3 + 1
        button.icon = f'numeric-{self.level}-box'
        
    def mute_button(self, button):
        '''Toogle mute flag'''
        self.mute = not self.mute
        if self.mute:
            button.icon = 'volume-off'
        else:
            button.icon = 'volume-high'
        # self.parent.parent.ids.toolbar.icon_mute = 'volume-on'