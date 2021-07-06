#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries
from random import choice
import webbrowser


# non-std libraries
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.app import App

from kivymd.uix.screen import MDScreen

# my app imports
from ahorcado.drawing import Drawing
from ahorcado.letters import FailedLetters
from ahorcado.word import Word
from ahorcado.keyboard import Keyboard
from popup import PopupButton
import ahorcado.constants as AHORCADO


Builder.load_string(
    r"""

<ScreenAhorcado>:
    name: 'ahorcado'

    drawing: drawing_area
    errors: failed_letters_area
    target_word: word_area
    keyboard: keyboard_area


    id: main
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Ahorcado'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", root.start_game], ["help", root.give_hint], ["volume-high", root.mute_button], ["help-circle-outline", root.help_button]]

        BoxLayout:
            orientation: 'horizontal'
            Drawing:
                id: drawing_area

            FailedLetters:
                id: failed_letters_area
                width: root.width * 1 / 6


        Word:
            id: word_area
            height: root.height / 10

        Keyboard:
            id: keyboard_area
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
    num_errors : int
        Number of failed tries
    drawing : ObjectProperty
        Object with the drawing
    errors : ObjectProperty
        Object of the failed letters
    target_word : ObjectProperty
        Object of the word to find
    keyboard : ObjectProperty
        Object of the keyboard
    keyboard_skin : string
        Name of the skin to be used for keyboard
    active : boolean
        Defines whether the game is active or not
    allow_hint : boolean
        Variable to track if a hint is available or not. Only one hint
        per game is allowed.

    '''
    num_errors = NumericProperty(0)
    drawing = ObjectProperty(None)
    errors = ObjectProperty(None)
    target_word = ObjectProperty(None)
    keyboard = ObjectProperty(None)
    keyboard_skin = StringProperty('teclado1')
    active = False
    allow_hint = BooleanProperty(True)
    mute = BooleanProperty(False)


    def start_game(self, *args):
        '''
        Start the game: find a new word, and reset all variables.
        '''
        self.target_word.find_word()
        self.reset_game()


    def reset_game(self):
        '''
        Reset all the variables to start the game.
        '''
        self.num_errors = 0
        self.good_letters = ''
        self.failed_letters = ''
        self.active = True
        self.allow_hint = True
        self.errors.reset_letters()
        self.drawing.reset_drawing()
        self.target_word.reset_word()
        self.keyboard.reset_keyboard()


    def end_game(self, win):
        '''
        Launch a popup a the end of the game.

        Parameters
        ----------
        win : boolean
            Indicates if the game is won or not. Popup text is
            adjusted depending on this.
        '''
        if win:
            msg = 'You in!!\nCONGRATULATIONS!!'
            self.play('win')
        else:
            msg = "I'm sorry,'\nyou've been HANGED..."
            self.play('lose')

        PopupButton(title='End', msg=msg)
        self.target_word.current = self.target_word.word
        self.active =  False


    def check_letter(self, letter):
        '''
        Check if the letter is in the word or not. If it is, show
        the letter in its place, and add to the self.good_letters;
        if it is not, increase the self.num_errors and add the letter
        to the self.failed_letters.

        Parameters
        ----------
        letter : string (1-char)
            Letter to be evaluated.

        '''
        if not self.active:
            return

        # if the character is not valid, or was previously selected, do nothing
        if letter not in AHORCADO.VALID_CHARACTERS or \
            letter in self.failed_letters + self.good_letters:
            return

        # if the letter is correct, it will be shown
        if letter in self.target_word.word:
            self.target_word.add_letter(letter)
            self.good_letters += letter
            if self.target_word.current == self.target_word.word:
                self.end_game(win=True)

        # if not correct, it is added to the list of errors
        else:
            self.num_errors += 1
            self.failed_letters += letter
            self.errors.add_letter(
                letter, self.num_errors)
            self.drawing.add_piece(self.num_errors)

            if self.num_errors >= 10:
                self.end_game(win=False)


    def mute_button(self, button):
        '''Toogle mute. Action triggered by toolbar button.'''
        self.mute = not self.mute       
        button.icon = 'volume-off' if self.mute else 'volume-high'


    def give_hint(self, *args):
        '''
        Give a hint: show one of the letters. Only if this is
        the first time hint is requested.
        '''
        if self.active:
            if self.allow_hint:
                letter = choice(self.target_word.word)
                while letter in self.target_word.current:
                    letter = choice(self.target_word.word)

                self.keyboard.push_key(letter)
                self.allow_hint = False
            else:
                PopupButton(title='Aviso',
                                    msg='You cannot get more hints!')


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

        app = App.get_running_app()
        app.play(sound)


    def config_change(self, config, section, key, value):
        '''
        When configuration changes (e.g. skin of the keyboard, or the hanged
        man), trigger the change on the objects.

        Parameters
        ----------
        config : ConfigParser
            Configuration object. To write the configuration.
        section : string
            Section of the configuration. Should always be 'ahorcado'.
        key : string
            Key that has changed.
        value : string
            New value of the key, after the change.

        '''
        if key == 'keyboard':
            self.keyboard.change_keyboard(value)

        elif key == 'man':
            self.drawing.change_man(value[-1])


        config.write()

    
    def help_button(self, button):
        '''Open web-browser with the help page for the game'''
        webbrowser.open(AHORCADO.URL_HELP)
