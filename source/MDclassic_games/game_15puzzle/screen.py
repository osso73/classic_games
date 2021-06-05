# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""

# std libraries
import os

# non-std libraries
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

from kivymd.uix.screen import MDScreen

# my app imports
from game_15puzzle.puzzle import Puzzle
from game_15puzzle.muestra import Muestra


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
            right_action_items: [["play-circle-outline", puzzle.start_game], ["volume-off", root.mute_button]]
            
        MDLabel:
            id: score
            text: 'Moves: ' + str(puzzle.movimientos)
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]


        Puzzle:
            id: puzzle
        
        BoxLayout:
            orientation: 'horizontal'
            on_size: muestra.initialize_grid()
        
            FloatLayout:
                MDChip:
                    text: 'Theme'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.66}
                    on_release: muestra.cambiar_tema()
                    icon: ''

                MDChip:
                    text: 'Level: ' + str(muestra.tamano - 2)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.33}
                    on_release: muestra.cambiar_tamano()
                    icon: ''
                    
            Muestra:
                id: muestra

""")

class Screen15Puzzle(MDScreen):    
    '''
    This class organizes the mainscreen in the different areas: menu at the 
    top, the main board in the middle, additional buttons in the middel, and 
    the reference picture at the bottom.
    
    Attributes
    ----------
    sounds : dict
        Dictionary of sounds, containing all sounds to be played during the 
        game. Different functions will play them as needed.
    '''
    def __init__(self, **kwargs):
        '''
        It triggers loading of sounds to memory when the game is launched, so
        they can be played without delay.
        '''
        super(Screen15Puzzle, self).__init__(**kwargs)
        self.sounds = self.load_sounds()
        self.mute = False

    def load_sounds(self):
        '''
        Load all sounds of the game, and put them into the dictionary.

        Returns
        -------
        sound : dict
            The dictionary of sounds that have been loaded

        '''
        sound = dict()
        folder = os.path.join(os.path.dirname(__file__),'audio')
        for s in ['ok', 'start', 'move', 'end_game']:
            sound[s] = SoundLoader.load(os.path.join(folder, f'{s}.ogg'))
        
        return sound
    
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



    def mute_button(self, *args):
        '''Toogle the mute on/off. Called from menu bar button.'''
        self.mute = not self.mute
        
        
    def config_change(self, config, section, key, value):
        if key == 'level':
            # change level
            level = int(value)
            self.ids.muestra.cambiar_tamano(level)

        elif key == 'theme':
            self.ids.muestra.cambiar_tema(value)

        config.write()
