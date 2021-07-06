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
from kivy.properties import  StringProperty

from kivymd.uix.boxlayout import MDBoxLayout


# my app imports
from ahorcado.general import replace_letter
import ahorcado.constants as AHORCADO


Builder.load_string(
    r"""

<Word>:
    size_hint_y: None
    padding: 5
    md_bg_color: 0, 0.5, 0, 1
    
    Label:
        text: root.current
        font_size: 120
        texture_size: self.size
        size: self.texture_size
        halign: 'left'
        valign: 'middle'
        font_name: 'ahorcado/fonts/lt-robotomono-bold'

""")

class Word(MDBoxLayout):
    '''
    This is the area of the screen that shows the word to be found.
    
    Attributes
    ----------
    current : string
        this is the word showing the letters found and not found
    word : string
        this is the word that needs to be found
    '''
    current = StringProperty(' ')
    word = ' '
    
    
    def reset_word(self):
        '''
        Reset self.current to all letters as '-'
        '''
        self.current = '-'*len(self.word)

        
    def find_word(self):
        '''
        Find a new word. First load a word from the file, and then reset 
        self.current to show all '-'.

        '''
        self.word = self.load_word()
        self.reset_word()
    

    def load_word(self):
        '''
        Find a word in form a file, an return it.

        Returns
        -------
        string
            Word chosen
        ''' 
        fullname = os.path.join(os.path.dirname(__file__), AHORCADO.WORDS_FILE)
        with open(fullname, 'rt') as f:
            words_list = [ line.rstrip('\n') for line in f ]
        
        return choice(words_list)

    
    def add_letter(self, letter):
        '''
        Add a correct letter to the self.current string. Find all appearences
        of the letter in self.word, and replace the character '-' by 
        the letter.

        Parameters
        ----------
        letter : string (char)
            Letter to be added
        '''
        pos = 0
        pos = self.word.find(letter)
        while pos != -1:
            self.current = replace_letter(
                self.current, pos, letter)
            pos = self.word.find(letter, pos+1)
