#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:29:44 2021

@author: osso73
"""

# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import  StringProperty

from kivymd.uix.boxlayout import MDBoxLayout


# my app imports
from ahorcado.general import replace_letter


Builder.load_string(
    r"""

<FailedLetters>:
    orientation: 'vertical'
    size_hint_x: None
    padding: 0.1 * self.width, 0
    md_bg_color: 1, 0, 0, 1

    Letter:
        text: root.error_string[0]
    Letter:
        text: root.error_string[1]
    Letter:
        text: root.error_string[2]
    Letter:
        text: root.error_string[3]
    Letter:
        text: root.error_string[4]
    Letter:
        text: root.error_string[5]
    Letter:
        text: root.error_string[6]
    Letter:
        text: root.error_string[7]
    Letter:
        text: root.error_string[8]
    Letter:
        text: root.error_string[9]

<Letter>:
    font_size: 120
    texture_size: self.size
    size: self.texture_size
    font_name: 'ahorcado/fonts/lt-robotomono-bold'
    
""")

class FailedLetters(MDBoxLayout):
    '''
    Area with the list of wrong letters. It shows initially only spaces (_),
    and as errors are made they are added to the shown string (self.error_string).
    
    Attributes
    ----------
    error_string : string
        String showing the wrong letters.
    '''
    error_string = StringProperty('_'*10)
    
    
    def reset_letters(self):
        '''
        Reset status to start a new game.
        '''
        self.error_string = '_'*10
    
    
    def add_letter(self, letter, num_error):
        '''
        Adds a letter to the list of wrong letters, in the position num_error.

        Parameters
        ----------
        letter : string
            Letter to add
        num_error : int
            Number of errors. Determines the position of the letter.

        '''
        self.error_string = replace_letter(self.error_string, num_error-1, letter)


class Letter(Label):
    pass