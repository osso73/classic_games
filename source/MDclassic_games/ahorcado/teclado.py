#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:09:31 2021

@author: osso73
"""

# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import  StringProperty, BooleanProperty

from kivymd.app import MDApp

# my app imports



Builder.load_string(
    r"""

<Teclado>:
    skin: app.config.get('Ahorcado', 'keyboard')
    size_hint_y: None
    rows: 3
    padding: '5dp'
    spacing: '5dp'
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            size: root.size
            pos: root.pos

<Tecla>:
    on_press: if not self.disabled: self.play()
    on_release: self.pulsar()
    skin: app.config.get('Ahorcado', 'keyboard')
    canvas:
        Color:
            rgba: [1, 1, 1, 0.2] if self.disabled else COLOUR_IMAGE
        Rectangle:
            size: root.size
            pos: root.pos
            source: 'ahorcado/images/'+root.skin+'/' + root.filename + '.png'

""")

class Teclado(GridLayout):
    '''
    The keyboard area, showing all the keys. It controls when keys are
    pressed, and the skin to use for keyboard.

    Attributes
    ----------
    skin : string
        Skin to be used.
    '''
    # skin = 'teclado1'

    def __init__(self, **kwargs):
        super(Teclado, self).__init__(**kwargs)
        self.crear_teclas()

    def crear_teclas(self):
        '''
        Create all keys for the keyboard
        '''
        for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
            name = letra if letra != 'Ñ' else 'N2'
            self.add_widget(Tecla(letra=letra, filename=name))

    def cambiar_teclado(self, teclado):
        '''
        Change the skin of the keyboard. Skins are a string formed by word
        teclado plus a number, from 1 to 6.
        '''

        self.skin = teclado

        for tecla in self.children:
            tecla.skin = self.skin

    def reset_teclado(self):
        '''
        Reset all keys, putting their disabled attribute to False.
        '''
        for tecla in self.children:
            tecla.disabled = False

    def pulsar_tecla(self, letra):
        '''
        Triggers a pulsation of a key (used for the hint)

        Parameters
        ----------
        letra : string (char)
            Key to be pulsed
        '''
        for tecla in self.children:
            if tecla.letra == letra:
                tecla.play()
                tecla.pulsar()


class Tecla(Button):
    '''
    Logic for each of the keys of the keyboard.

    Attributes
    ----------
    letra : string (char)
        This is the letter that corresponds to the key
    skin : string
        skin to be used
    filename : string
        filename of the key to be loaded. It's the same as letra, except for
        letter ñ, that uses the filename n2 to avoid issues with os.
    disabled : boolean
        Defines whether the key is disabled or not. Used to dim the image of
        the key.

    '''
    letra = StringProperty()
    skin = StringProperty()
    filename = StringProperty()
    disabled = BooleanProperty(False)

    def pulsar(self):
        '''
        Trigger the evaluar_letra method, and disable the letter, so it shows
        dimmer on the screen.

        '''
        app = MDApp.get_running_app()
        app.root.ids.ahorcado.evaluar_letra(self.letra)
        self.disabled = True

    def play(self):
        app = MDApp.get_running_app()
        if app.root.ids.ahorcado.mute:
            return

        app.play('tecla')
