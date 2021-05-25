#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:05:25 2021

@author: osso73
"""

# std libraries
import os
from random import choice

# non-std libraries
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  StringProperty

# my app imports
from ahorcado.general import replace_letter
import ahorcado.constants as AHORCADO


Builder.load_string(
    r"""

<PalabraLetras>:
    size_hint_y: None
    padding: 5
    canvas:
        Color:
            rgba: 0, 0.5, 0, 1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        text: root.actual
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        halign: 'left'
        valign: 'middle'
        font_name: 'ahorcado/fonts/lt-robotomono-bold'

""")

class PalabraLetras(BoxLayout):
    '''
    This is the area of the screen that shows the word to be found.
    
    Attributes
    ----------
    actual : string
        this is the word showing the letters found and not found
    palabra : string
        this is the word that needs to be found
    '''
    actual = StringProperty(' ')
    palabra = ' '
    
    
    def reset_palabra(self):
        '''
        Reset self.actual to all letters as '-'
        '''
        self.actual = '-'*len(self.palabra)
        
    def buscar_palabra(self):
        '''
        Find a new word. First load a word from the file, and then reset 
        self.actual to show all '-'.

        '''
        self.palabra = self.cargar_palabra()
        self.reset_palabra()
    
    def cargar_palabra(self):
        '''
        Find a word in form a file, an return it.

        Returns
        -------
        string
            Word chosen
        ''' 
        fullname = os.path.join(os.path.dirname(__file__), AHORCADO.FICHERO_PALABRAS)
        with open(fullname, 'rt') as f:
            lista = [ line.rstrip('\n') for line in f ]
        
        return choice(lista)
    
    def anadir_letra(self, letra):
        '''
        Add a correct letter to the self.actual string. Find all appearences
        of the letter in self.palabra, and replace the character '-' by 
        the letter.

        Parameters
        ----------
        letra : string (char)
            Letter to be added
        '''
        pos = 0
        pos = self.palabra.find(letra)
        while pos != -1:
            self.actual = replace_letter(
                self.actual, pos, letra)
            pos = self.palabra.find(letra, pos+1)
