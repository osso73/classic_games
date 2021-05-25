#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:29:44 2021

@author: osso73
"""

# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  StringProperty

# my app imports
from ahorcado.general import replace_letter


Builder.load_string(
    r"""

<LetrasFalladas>:
    orientation: 'vertical'
    size_hint_x: None
    padding: 0.1 * self.width, 0
    canvas:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        text: root.fallo[0]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[1]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[2]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[3]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[4]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[5]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[6]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[7]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[8]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'
    Label:
        text: root.fallo[9]
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        font_name: 'ahorcado/fonts/lt-robotomono-bold'

""")

class LetrasFalladas(BoxLayout):
    '''
    Area with the list of wrong letters. It shows initially only spaces (_),
    and as errors are made they are added to the shown string (self.fallo).
    
    Attributes
    ----------
    fallo : string
        String showing the wrong letters.
    '''
    fallo = StringProperty('_'*10)
    
    
    def reset_letras(self):
        '''
        Reset status to start a new game.
        '''
        self.fallo = '_'*10
    
    
    def anadir_letra(self, letra, fallos):
        '''
        Adds a letter to the list of wrong letters, in the position fallo

        Parameters
        ----------
        letra : string
            Letter to add
        fallos : int
            Number of errors. Determines the position of the letter.

        '''
        self.fallo = replace_letter(self.fallo, fallos-1, letra)

