#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:09:31 2021

@author: osso73
"""

# std libraries
import os


# non-std libraries
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import  StringProperty, BooleanProperty

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout


# my app imports
import ahorcado.constants as AHORCADO



Builder.load_string(
    r"""

<Keyboard>:
    skin: app.config.get('Ahorcado', 'keyboard')
    size_hint_y: None
    rows: 3
    padding: '5dp'
    spacing: '5dp'
    md_bg_color: 0, 0, 0, 1

<Key>:
    on_press: if not self.disabled: self.parent.parent.parent.play('key')
    on_release: self.push()
    canvas:
        Color:
            rgba: [1, 1, 1, 0.2] if self.disabled else COLOUR_IMAGE
        Rectangle:
            size: root.size
            pos: root.pos
            # source: 'ahorcado/images/'+root.skin+'/' + root.filename + '.png'
            source: root.skin

""")

class Keyboard(MDGridLayout):
    '''
    The keyboard area, showing all the keys. It controls when keys are
    pressed, and the skin to use for keyboard.

    '''
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.create_keys()
        app = MDApp.get_running_app()
        skin = app.config.get('Ahorcado', 'keyboard')
        self.change_keyboard(skin)


    def create_keys(self):
        '''
        Create all keys for the keyboard
        '''
        for letter in AHORCADO.VALID_CHARACTERS:
            name = letter if letter != 'Ñ' else 'N2'
            self.add_widget(Key(letter=letter, filename=name))


    def change_keyboard(self, keyboard_skin):
        '''
        Change the skin of the keyboard. Skins are a string formed by word
        keyboard plus a number, from 1 to 6.
        
        '''

        # self.skin = keyboard_skin
        path_skin = os.path.join(os.path.dirname(__file__), 'images', keyboard_skin)

        for key in self.children:
            key.skin = os.path.join(path_skin, key.filename+'.png')


    def reset_keyboard(self):
        '''Reset all keys, putting their disabled attribute to False.'''
        
        for key in self.children:
            key.disabled = False


    def push_key(self, letter):
        '''
        Triggers a pulsation of a key (used for the hint)

        Parameters
        ----------
        letter : string (char)
            Key to be pulsed
            
        '''
        for key in self.children:
            if key.letter == letter:
                self.parent.parent.play('key')
                key.push()


class Key(Button):
    '''
    Logic for each of the keys of the keyboard.

    Attributes
    ----------
    letter : string (char)
        This is the letter that corresponds to the key
    skin : string
        skin to be used
    filename : string
        filename of the key to be loaded. It's the same as letter, except for
        letter ñ, that uses the filename n2 to avoid issues with os.
    disabled : boolean
        Defines whether the key is disabled or not. Used to dim the image of
        the key.

    '''
    letter = StringProperty()
    skin = StringProperty()
    filename = StringProperty()
    disabled = BooleanProperty(False)

    def push(self):
        '''
        Trigger the check_letter method, and disable the letter, so it shows
        dimmer on the screen.

        '''
        app = MDApp.get_running_app()
        app.sm.get_screen('ahorcado').check_letter(self.letter)
        self.disabled = True

