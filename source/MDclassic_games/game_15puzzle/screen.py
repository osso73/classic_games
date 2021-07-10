# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""

# std libraries
import os
import webbrowser

# non-std libraries
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

# my app imports
from game_15puzzle.puzzle import Puzzle
from game_15puzzle.sample import Sample
import game_15puzzle.constants as FIFTEEN


Builder.load_string(
    r"""

<Screen15Puzzle>:
    name: 'fifteen'
    
    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        md_bg_color: app.theme_cls.primary_light
        on_size: puzzle.initialize_grid()
    
        MDToolbar:
            title: '15 Puzzle'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", puzzle.start_game], ["volume-high", root.mute_button], ["help-circle-outline", root.help_button]]
            
        MDLabel:
            id: score
            text: 'Moves: ' + str(puzzle.moves)
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]


        Puzzle:
            id: puzzle
        
        BoxLayout:
            orientation: 'horizontal'
            on_size: sample.initialize_grid()
        
            FloatLayout:
                MDChip:
                    text: 'Theme'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.66}
                    on_release: sample.change_theme()
                    icon: ''

                MDChip:
                    text: 'Level: ' + str(sample.board_size - 2)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.33}
                    on_release: sample.change_size()
                    icon: ''
                    
            Sample:
                id: sample

""")

class Screen15Puzzle(MDScreen):    
    '''
    This class organizes the mainscreen in the different areas: menu at the 
    top, the main board in the middle, additional buttons in the middel, and 
    the reference picture at the bottom.
    '''
    mute = False
    
    
    def play(self, sound):
        '''
        Play a sound from the dictionary of sounds. Call to the main app.play. 

        Parameters
        ----------
        sound : string
            Key of the dictionary corresponding to the sound to be played.

        '''
        if self.mute:
            return
        
        app = MDApp.get_running_app()
        app.play(sound)



    def mute_button(self, button):
        '''Toogle the mute on/off. Called from menu bar button.'''
        
        self.mute = not self.mute
        button.icon = 'volume-off' if self.mute else 'volume-high'
        
        
    def config_change(self, config, section, key, value):
        '''
        

        Parameters
        ----------
        config : TYPE
            DESCRIPTION.
        section : TYPE
            DESCRIPTION.
        key : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        if key == 'level':
            # change level
            level = int(value)
            self.ids.sample.change_size(level)

        elif key == 'theme':
            self.ids.sample.change_theme(value)

        config.write()


    def help_button(self, button):
        webbrowser.open(FIFTEEN.URL_HELP)
