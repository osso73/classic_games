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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image

from kivymd.app import MDApp

# my app imports
import game_15puzzle.constants as FIFTEEN




Builder.load_string(
    r"""

<Muestra>:
    cols: self.tamano
    spacing: '3dp'
    size_hint: None, None
    size: self.ventana, self.ventana

<FichaMuestra>:
    source: f'game_15puzzle/images/temas/{self.tema}/{self.tamano}/{self.name}.jpg'

""")


class Muestra(GridLayout):
    '''
    Control the bottom part of screen, showing the complete picture, so it 
    can be used as a reference. The picture is divided in tiles as well, to
    show the image of each tile.
    
    Use a GridLa
    Attributes
    ----------
    tema : StringProperty
        This controls what picture to show.
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5
    ventana : float
        Width and height of the widget. Determined from parent's size.        
    '''
    tema = StringProperty()
    tamano = NumericProperty()
    ventana = NumericProperty(100)
    
    def __init__(self, **kwargs):
        super(Muestra, self).__init__(**kwargs)
        app = MDApp.get_running_app()
        self.tema = app.config.get('fifteen', 'theme')        
        self.tamano = int(app.config.get('fifteen', 'level')) + 2
        Clock.schedule_once(self.load_tema)
    
    def initialize_grid(self, *args):
        '''
        Establish the width and height of the widget, based on parent's size
        '''
        self.ventana = min(self.parent.height, self.parent.width)
        

    def load_tema(self, *args):
        '''
        Load a new picture to be used, and divides it into the tiles as 
        defined by self.tamano. Load all tiles.
        '''
        self.clear_widgets()
        self.cols = self.tamano
        for n in list(range(1, self.tamano**2 + 1)):
            self.add_widget(FichaMuestra(name=str(n), tema=self.tema, 
                                         tamano=str(self.tamano)))


    def cambiar_tema(self, new_theme=None):
        '''
        Change the theme, used to load the picture. This is not changing the 
        picture, just the name. The picture is changed bymethod 
        load_tema().

        '''
        fullname = FIFTEEN.TEMAS
        themes = os.listdir(fullname)

        if new_theme:
            if new_theme in themes:
                self.tema = new_theme
            else:
                raise ValueError(f"Theme {new_theme} does not exist")
        
        else:
            ind = themes.index(self.tema)
            new_ind = (ind + 1) % len(themes)
            app = MDApp.get_running_app()
            self.tema = themes[new_ind]
            app.config.set('fifteen', 'theme', self.tema)
            app.config.write()
    
    def cambiar_tamano(self, new_level=None):
        '''
        Change the size of the board, cycling between 3x3, 4x4 and 5x5. 
        This is stored in variable self.tamano.
        '''
        if new_level:
            if not isinstance(new_level, int) or not (1 <= new_level <= 3):
                raise ValueError(f'Level value {new_level} is incorrect.')
                        
        else:
            level = self.tamano - 2
            new_level = level % 3 + 1
            app = MDApp.get_running_app()
            app.config.set('fifteen', 'level', new_level)
            app.config.write()
            
        self.tamano = new_level + 2
    
    def on_tema(self, *args):
        self.load_tema()
    
    def on_tamano(self, *args):
        self.load_tema()
                            

                    
class FichaMuestra(Image):
    name = StringProperty()
    tema = StringProperty()
    tamano = StringProperty()
