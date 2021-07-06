#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 10:09:16 2021

@author: oriol
"""


# std libraries
from time import time
from random import shuffle


# non-std libraries
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.app import App

# my app imports
import buscaminas.constants as MINES
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
    cols: self.cols

""")



class Field(GridLayout):
    '''
    This is the field where all mines are distributed.
    
    Attributes
    ----------
    cols : NumericProperty
        Number of columns of the field
    rows : NumericProperty
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
    cols = NumericProperty(9)
    rows = NumericProperty(9)
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
        
        app = App.get_running_app()
        app.play(sound)


    def start_game(self, *args):
        '''
        Start a new game: reset score and timer, rebuild the field.
        '''
        self.parent.parent.ids.start_button.change_face('standard')
        window_width = self.parent.width
        window_height = (self.parent.height - 
                          self.parent.parent.ids.toolbar.height -
                          self.parent.parent.ids.menu.height) / 2
        self.mines = MINES.LEVELS[self.level]['mines']
        self.cols = MINES.LEVELS[self.level]['cols']
        self.rows = MINES.LEVELS[self.level]['rows']
        self.size = (window_width * MINES.LEVELS[self.level]['window'][0], 
                     window_height * MINES.LEVELS[self.level]['window'][1])
            
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
        areas = [9]*self.mines + [0]*(self.cols*self.rows - self.mines)
        shuffle(areas)
        
        n=0
        for i in range(self.rows):
            for j in range(self.cols):
                self.add_widget(Area(location=[j, i], value=areas[n]))
                n += 1

    
    def find_adjacent_mines(self):
        '''
        For each area, find the number of adjacent mines, and establish it
        as its value. 
        '''
        for area in self.children:
            if area.value != 9:  # skip if area is a bomb
                neighbours = self.find_neighbours(area.location)
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
            if child.location != list(p):
                i, j = child.location
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
        self.play('lose-explode')
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
        self.play('win-Ateam')

    
    def no_adjacent_mines(self, area):
        '''
        Uncover all adjacent areas.
        
        Parameters
        ----------
        area : Area
            Area which has a value of 0
        '''
        neighbours = self.find_neighbours(area.location)
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
            neighbours = self.find_neighbours(area.location)
            flagged = [n for n in neighbours if n.flag]
            if len(flagged) == area.value:
                not_flagged = [n for n in neighbours if not n.flag]
                for tile in not_flagged:
                    tile.uncover()


    def entry_mode(self, button):
        '''
        Switch entry mode, between flag or covered. This defines what happens
        when cliked: either puts a flag, or uncovers the area. This method
        is triggered when clicking the button on the toolbar.

        Parameters
        ----------
        button : MDButton
            Button that has been clicked. Used to change the icon on it.

        '''
        if self.mode == 'flag':
            self.mode = 'covered'
            button.icon = 'bomb'
        else:
            self.mode = 'flag'
            button.icon  = 'flag'

        
    def set_level(self, button):
        '''
        Switch level (1, 2 or 3). This method is triggered when clicking the 
        button on the toolbar.

        Parameters
        ----------
        button : MDButton
            Button that has been clicked. Used to change the icon on it.

        '''
        self.level = self.level % 3 + 1
        button.icon = f'numeric-{self.level}-box'

        
    def mute_button(self, button):
        '''
        Switch mute flag. This method is triggered when clicking the 
        button on the toolbar.

        Parameters
        ----------
        button : MDButton
            Button that has been clicked. Used to change the icon on it.

        '''
        self.mute = not self.mute
        if self.mute:
            button.icon = 'volume-off'
        else:
            button.icon = 'volume-high'
