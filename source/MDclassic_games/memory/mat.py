#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 20:49:34 2021

@author: oriol
"""


# std libraries
import os
from random import sample
from time import sleep


# non-std libraries
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.app import MDApp

# my app imports
from memory.card import CardMemory
from popup import PopupButton



THEMES = os.path.join(os.path.dirname(__file__), 'images', 'themes')


Builder.load_string(
    r"""

<Mat>:
    cols: self.columns
    md_bg_color: app.theme_cls.primary_light
    padding: '5dp'
    spacing: '5dp'

""")


class Mat(MDGridLayout):
    '''
    Main area of the game, where the tiles are distributed. This class has 
    the logic to turn tiles, shuffle, etc. The tiles are distributed in a 
    GridLayout.
    
    Attributes
    ----------
    columns : NumericProperty
        Number of columns of the GridLayout. 
    current_cards : ListProperty
        Cards that are turned up, but not yet matched. This list can have 0, 1
        or 2 cards max.
    moves : NumericProperty
        Count the number of moves that have been made. It is the score.
    images : list
        List of filenames of the images.
    current_theme : StringProperty
        Current theme to be used.
    num_pairs : NumericProperty
        Number of pairs to be discovered.
    mute : boolean
        If True, the sounds will not play; otherwise, they will play. Set
        to False by default. This is triggered by button in toolbar.
        
    '''
    columns = NumericProperty(2)
    current_cards = ListProperty()
    moves = NumericProperty(0)
    current_theme = StringProperty()
    num_pairs = NumericProperty()
    mute = BooleanProperty(False)
    

    def __init__(self, **kwargs):
        '''
        Create the list of themes based on the folders available, load the
        sounds to memory so they can be played without delay.
        '''
        super(Mat, self).__init__(**kwargs)
        self.theme_list = os.listdir(THEMES)
        self.change_theme()
        
        app = MDApp.get_running_app()
        self.current_theme = app.config.get('Memory', 'theme')
        self.num_pairs = int(app.config.get('Memory', 'level'))

        
    def change_theme(self):
        '''
        Switch to the following theme of the theme_list.
        '''
        if not self.current_theme:
            self.current_theme = self.theme_list[0]
        else:
            ind = self.theme_list.index(self.current_theme)
            new_ind = ind+1 if ind<len(self.theme_list)-1 else 0
            self.current_theme = self.theme_list[new_ind]
    
    
    def change_level(self):
        '''
        Switch to the following size. Available sizes range from 2 to 20.
        '''
        self.num_pairs = self.num_pairs + 1 if self.num_pairs < 20 else 2

    

    def play(self, sound):
        '''
        Trigger play method from the main app, if not muted.

        Parameters
        ----------
        sound : string
            Key of the dictionary corresponding to the sound to be played.

        '''
        if not self.mute:
            app = MDApp.get_running_app()
            app.play(sound)


    def load_images(self):
        '''
        Load images of current theme, and return them.

        Parameters
        ----------
        app : App
            Instance of the running app.

        Returns
        -------
        ims : list
            List of filenames of the images. These are the images of the 
            current theme.
        back : string
            Filename of the image shown in the back of the cards.

        '''
        p = os.path.join(THEMES, self.current_theme) 
        ims = os.listdir(p)
        ims = [os.path.join(p,im) for im in ims if im.startswith('image')]
        back = os.path.join(p,'back.jpg')
        return ims, back


    def start_game(self, *args):
        '''
        Start the game: reset score to 0, load images according to currently
        selected theme and size, and create the tiles.
        '''
        self.clear_widgets()
        
        self.play('start')
        self.images, back = self.load_images()
        self.moves = 0
        
        # take only a number of images of the total, duplicate and shuffle
        images = sample(self.images, self.num_pairs)
        images = sample(images*2, self.num_pairs*2)
        
        self.set_columns(self.num_pairs)     
        for im in images:
            self.add_widget(CardMemory(image=im, back=back))
    
    
    def set_columns(self, num):
        '''
        Define the columns of the widget, how the tiles will be distributed
        based on the number of tiles. The thresholds are determined by trial
        and error, based on the shape factor of a mobile phone.

        Parameters
        ----------
        num : int
            Total number of pairs of images to be distributed.
        '''
        if num < 5:
            self.columns = 2
        elif num < 10:
            self.columns = 3
        elif num < 16:
            self.columns = 4
        else:
            self.columns = 5
        
        
    def on_current_cards(self, *args, **kwargs):
        '''
        When the list of current cards changes, check if the length of the
        list is 2; if so, check if the pair match, in which case the cards
        are left with the image; if no match, turn the cards down again.
        '''
        if len(self.current_cards) == 2:
            self.moves += 1
            if self.current_cards[0].image != self.current_cards[1].image:
                sleep(2)  # wait 2 seconds before turning back cards
                self.current_cards.pop().turn()
                self.current_cards.pop().turn()
            else:
                self.current_cards.pop()
                self.current_cards.pop()
                self.play('ok')
                self.check_end()  # check if the game is finished
    
    
    def check_end(self):
        '''
        Check if the game is finished: all cards are up.
        '''
        for carta in self.children:
            if not carta.shown:
                return
        
        self.play('win-short')
        PopupButton(title='End', msg='Well done!\nYou found all pairs')


    def mute_button(self, button):
        '''Toogle mute. Action triggered by toolbar button.'''
        self.mute = not self.mute
        button.icon = 'volume-off' if self.mute else 'volume-high'
        


