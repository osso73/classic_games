#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 10:28:53 2021

@author: oriol
"""


# std libraries
import os


# non-std libraries
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty


# my app imports
import buscaminas.constants as MINES



Builder.load_string(
    r"""

<Area>:
    canvas:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
            source: self.show

""")



class Area(Label):
    '''
    This class refers to each of the tiles in the field.

    Attributes
    ----------
    value : NumericProperty
        Value of the area. Usually a number showing the mines adjacent to this
        tile. A value of -1 means there is a bomb in the area.
    location : ListProperty
        Coordinates (i, j) of the tile in the field.
    show : StringProperty
        Name of the image that is shown by the tile
    uncovered : BooleanProperty
        If the tile has been uncovered or not. This defines what image is 
        shown.
    flag : BooleanProperty
        If the tile has a flag or not.

    '''
    value = NumericProperty(0)
    location = ListProperty()
    show = StringProperty()
    uncovered = BooleanProperty(False)
    flag = BooleanProperty(False)
    _current_touch = None

    
    def __init__(self, **kwargs):
        super(Area, self).__init__(**kwargs)
        self.set_show()

    
    def set_show(self, name=None):
        '''
        Evaluate the different flags (flag, uncovered) and define what image
        should be shown on the tile.
        '''
        
        if name:
            file = f'{name}.jpg'
        else:
            if self.uncovered:
                file = f'{self.value}.jpg'
            else:
                if self.flag:
                    file = 'flag.jpg'
                else:
                    file = 'covered.jpg'
        
        self.show = os.path.join(MINES.IMAGES, file)
    

    def on_uncovered(self, *args):
        '''
        Any change on the flag triggers the re-evaluation of the flags to 
        show the appropriate image on the tile.
        '''
        self.set_show()
        self.parent.check_uncover(self)
    

    def on_flag(self, *args):
        '''
        Any change on the flag triggers the re-evaluation of the flags to 
        show the appropriate image on the tile.
        '''
        self.set_show()
        change = -1 if self.flag else 1
        self.parent.mines += change
        if self.parent.all_discovered():
            self.parent.game_won()
    

    def switch_flag(self, *args):
        '''
        Switch the flag boolean, and decrease mines counter.
        '''
        self.flag = not self.flag
        

    def uncover(self, *args):
        '''
        Uncover mine, if not uncovered. And check if end of game or 0 bombs, 
        to uncover other adjacent areas.
        '''
        if not self.uncovered and not self.flag:
            self.uncovered = True
        
                
    def on_touch_down(self, touch):
        '''
        Depending on the value of the flag button, trigger the switch_flag() 
        or uncover() methods.
        '''
        if self.collide_point(*touch.pos) and self.parent.game_active:
            if self.uncovered:
                self.parent.open_adjacent(self)
            elif hasattr(touch, 'button') and touch.button == 'right':
                self.switch_flag()
            elif self.parent.mode == 'flag':
                self.switch_flag()
            elif self.parent.mode == 'covered':
                self.uncover()
