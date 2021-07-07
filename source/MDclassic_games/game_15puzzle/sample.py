#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:59:45 2021

@author: osso73
"""

# std libraries
import os

# non-std libraries
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image

from kivymd.app import MDApp

# my app imports
import game_15puzzle.constants as FIFTEEN


Builder.load_string(
    r"""

<Sample>:
    cols: self.board_size
    spacing: '3dp'
    size_hint: None, None
    size: self.window_size, self.window_size

<CardSample>:
    source: f'game_15puzzle/images/themes/{self.theme}/{self.board_size}/{self.name}.jpg'
    allow_stretch: True

""")


class Sample(MDGridLayout):
    '''
    Control the bottom part of screen, showing the complete picture, so it 
    can be used as a reference. The picture is divided in tiles as well, to
    show the image of each tile.
    
    Use a GridLayout
    
    Attributes
    ----------
    theme : StringProperty
        This controls what picture to show.
    board_size : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5
    window_size : float
        Width and height of the widget. Determined from parent's size.  
        
    '''
    theme = StringProperty()
    board_size = NumericProperty()
    window_size = NumericProperty(100)
    
    def __init__(self, **kwargs):
        super(Sample, self).__init__(**kwargs)
        app = MDApp.get_running_app()
        self.theme = app.config.get('fifteen', 'theme')        
        self.board_size = int(app.config.get('fifteen', 'level')) + 2
        Clock.schedule_once(self.load_theme)
    
    def initialize_grid(self, *args):
        '''
        Establish the width and height of the widget, based on parent's size
        '''
        self.window_size = min(self.parent.height, self.parent.width)
        

    def load_theme(self, *args):
        '''
        Load a new picture to be used, and divides it into the tiles as 
        defined by self.board_size. Load all tiles.
        '''
        self.clear_widgets()
        self.cols = self.board_size
        for n in list(range(1, self.board_size**2 + 1)):
            self.add_widget(CardSample(name=str(n), theme=self.theme, 
                                         board_size=str(self.board_size)))


    def change_theme(self, new_theme=None):
        '''
        Change the theme, used to load the picture. This is not changing the 
        picture, just the name. The picture is changed by method 
        load_theme().

        '''
        fullname = FIFTEEN.THEMES
        themes = os.listdir(fullname)

        if new_theme:
            if new_theme in themes:
                self.theme = new_theme
            else:
                raise ValueError(f"Theme {new_theme} does not exist")
        
        else:
            ind = themes.index(self.theme)
            new_ind = (ind + 1) % len(themes)
            app = MDApp.get_running_app()
            self.theme = themes[new_ind]
            app.config.set('fifteen', 'theme', self.theme)
            app.config.write()
    
    def change_size(self, new_level=None):
        '''
        Change the size of the board, cycling between 3x3, 4x4 and 5x5. 
        This is stored in variable self.board_size.
        '''
        if new_level:
            if not isinstance(new_level, int) or not (1 <= new_level <= 3):
                raise ValueError(f'Level value {new_level} is incorrect.')
                        
        else:
            level = self.board_size - 2
            new_level = level % 3 + 1
            app = MDApp.get_running_app()
            app.config.set('fifteen', 'level', new_level)
            app.config.write()
            
        self.board_size = new_level + 2
    
    def on_theme(self, *args):
        self.load_theme()
    
    def on_board_size(self, *args):
        self.load_theme()
                            

                    
class CardSample(Image):
    name = StringProperty()
    theme = StringProperty()
    board_size = StringProperty()
