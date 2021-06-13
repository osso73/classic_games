#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries
from random import choice

# non-std libraries
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.core.audio import SoundLoader

from kivymd.uix.screen import MDScreen

# my app imports
from ahorcado.dibujo import Dibujo
from ahorcado.letras import LetrasFalladas
from ahorcado.palabra import PalabraLetras
from ahorcado.teclado import Teclado
from ahorcado.popup import PopupButtonAhorcado
import ahorcado.constants as AHORCADO


Builder.load_string(
    r"""

<ScreenAhorcado>:
    name: 'ahorcado'

    obj_dibujo: pantalla_dibujo
    obj_letras_falladas: pantalla_letras_falladas
    obj_palabra: pantalla_palabra
    obj_teclado: pantalla_teclado


    id: main
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Ahorcado'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", root.iniciar_juego], ["help", root.dar_pista], ["volume-high", root.mute_button]]

        BoxLayout:
            orientation: 'horizontal'
            Dibujo:
                id: pantalla_dibujo

            LetrasFalladas:
                id: pantalla_letras_falladas
                width: root.width * 1 / 6


        PalabraLetras:
            id: pantalla_palabra
            height: root.height / 10

        Teclado:
            id: pantalla_teclado
            height: root.height / 10 * 2

""")

class ScreenAhorcado(MDScreen):
    '''
    This class organizes the screen in different sections, with menu on top,
    the middle section with the picture and failed letters, the word to
    search, and the keyboard.

    It contains most of the logic of starting/ending game, evaluate letter...

    Attributes
    ----------
    fallos : int
        Number of failed tries
    obj_dibujo : ObjectProperty
        Object with the drawing
    obj_letras_falladas : ObjectProperty
        Object of the failed letters
    obj_palabra : ObjectProperty
        Object of the word to find
    obj_teclado : ObjectProperty
        Object of the keyboard
    teclado : string
        Name of the skin to be used for keyboard
    active : boolean
        Defines whether the game is active or not
    sounds : dictionary
        Contains all the sounds of the game (except the key)
    pista : boolean
        Variable to track if a hint is available or not. Only one hint
        per game is allowed.

    '''
    fallos = NumericProperty(0)
    obj_dibujo = ObjectProperty(None)
    obj_letras_falladas = ObjectProperty(None)
    obj_palabra = ObjectProperty(None)
    obj_teclado = ObjectProperty(None)
    teclado = StringProperty('teclado1')
    active = False
    sounds = dict()
    pista = BooleanProperty(True)
    mute = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ScreenAhorcado, self).__init__(**kwargs)
        self.sounds['win'] = SoundLoader.load('ahorcado/audio/game-over-win.ogg')
        self.sounds['lose'] = SoundLoader.load('ahorcado/audio/game-over-lost.ogg')

    def iniciar_juego(self, *args):
        '''
        Start the game: find a new word, and reset all variables.
        '''
        self.obj_palabra.buscar_palabra()
        self.reset_juego()

    def reset_juego(self):
        '''
        Reset all the variables to start the game.
        '''
        self.fallos = 0
        self.letras_acertadas = ''
        self.letras_falladas = ''
        self.active = True
        self.pista = True
        self.obj_letras_falladas.reset_letras()
        self.obj_dibujo.reset_dibujo()
        self.obj_palabra.reset_palabra()
        self.obj_teclado.reset_teclado()

    def final(self, win):
        '''
        Launch a popup a the end of the game.

        Parameters
        ----------
        win : boolean
            Indicates if the game is won or not. Popup text is
            adjusted depending on this.
        '''
        if win:
            msg = '¡¡Has ganado!!\n¡¡ENHORABUENA!!'
            # self.sound['win'].play()
            self.play('win')
        else:
            msg = 'Lo siento,\nte han colgado...'
            # self.sound['lose'].play()
            self.play('lose')

        p = PopupButtonAhorcado(title='Final', msg=msg)
        self.obj_palabra.actual = self.obj_palabra.palabra



    def evaluar_letra(self, letra):
        '''
        Check if the letter is in the word or not. If it is, show
        the letter in its place, and add to the self.letras_acertadas;
        if it is not, increase the self.fallos and add the letter
        to the self.letras_falladas.

        Parameters
        ----------
        letra : string (1-char)
            Letter to be evaluated.

        '''
        if not self.active:
            return

        # si no es un carácter válido, o ya ha salido, no hace nada
        if letra not in AHORCADO.CARACTERES_VALIDOS or \
            letra in self.letras_falladas + self.letras_acertadas:
            return

        # si letra es correcta, se muestra
        if letra in self.obj_palabra.palabra:
            self.obj_palabra.anadir_letra(letra)
            self.letras_acertadas += letra
            if self.obj_palabra.actual == self.obj_palabra.palabra:
                self.final(win=True)

        # si la letra no es correcta, se añade a la lista de fallos
        else:
            self.fallos += 1
            self.letras_falladas += letra
            self.obj_letras_falladas.anadir_letra(
                letra, self.fallos)
            self.obj_dibujo.anadir_dibujo(self.fallos)

            if self.fallos >= 10:
                self.final(win=False)


    def mute_button(self, button):
        '''Toogle mute. Action triggered by toolbar button.'''
        self.mute = not self.mute       
        button.icon = 'volume-off' if self.mute else 'volume-high'


    def dar_pista(self, *args):
        '''
        Give a hint: show one of the letters. Only if this is
        the first time hint is requested.
        '''
        if self.active:
            if self.pista:
                letra = choice(self.obj_palabra.palabra)
                while letra in self.obj_palabra.actual:
                    letra = choice(self.obj_palabra.palabra)

                self.obj_teclado.pulsar_tecla(letra)
                self.pista = False
            else:
                PopupButtonAhorcado(title='Aviso',
                                    msg='¡No puedes pedir más pistas!')




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

        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")


    def config_change(self, config, section, key, value):
        if key == 'keyboard':
            self.obj_teclado.cambiar_teclado(value)

        elif key == 'man':
            self.obj_dibujo.cambiar_hombre(value[-1])


        config.write()
