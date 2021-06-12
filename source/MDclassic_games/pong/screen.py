# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries
import os


# non-std libraries
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.screen import MDScreen


# my app imports
from pong.pongboard import PongBoard



Builder.load_string(
    r"""

<ScreenPong>:
    name: 'pong'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDToolbar:
            title: 'Pong'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", pong.start_game], ["pause", pong.pause_button]]
            
        PongBoard:
            id: pong
        

""")

class ScreenPong(MDScreen):
    '''
    This class organizes the screen in different sections: menu, and game.
    It controls the config settings.

    '''        
    
    def config_change(self, config, section, key, value):
        if key == 'speed':
            val = int(value)
            if val < 0:
                val = abs(val)
                config.set('Pong', 'speed', val)
            self.ids.pong.initial_vel = val

        elif key == 'skin':
            self.ids.pong.change_skin(value)

        config.write()
        