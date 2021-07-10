# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries
import webbrowser


# non-std libraries
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


# my app imports
from memory.mat import Mat


URL_HELP = 'https://osso73.github.io/classic_games/games/classic_games/#game-of-memory'


Builder.load_string(
    r"""

<ScreenMemory>:
    name: 'memory'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDToolbar:
            title: 'Memory'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", mat_area.start_game], ["volume-high", mat_area.mute_button], ["help-circle-outline", root.help_button]]
            
        MDBoxLayout:
            orientation: 'horizontal'
            padding: '10dp'
            size_hint_y: None
            height: score.texture_size[1] + dp(10)*2
            md_bg_color: app.theme_cls.primary_light
            
            BoxLayout:
                orientation: 'horizontal'
                spacing: '10dp'

                MDChip:
                    text: mat_area.current_theme
                    valign: 'center'
                    icon: ''
                    on_release: mat_area.change_theme()
                MDChip:
                    text: str(mat_area.num_pairs)
                    icon: ''
                    on_release: mat_area.change_level()

            MDLabel:
                id: score
                text: 'Moves: ' + str(mat_area.moves)
                halign: "center"
                font_style: 'H4'
        
        Mat:
            id: mat_area

""")


class ScreenMemory(MDScreen):
    '''
    This is the main screen, to organize the menu and the mat area. Almost
    no logic here, as everything is happening on the Mat class. Only
    handles the settings changes for memory.
    
    '''  
    def config_change(self, config, section, key, value):
        if key == 'theme':
            self.ids.mat_area.tema_actual = value

        elif key == 'level':
            num = int(value)
            if num < 2:
                num = 2
            elif num > 20:
                num = 20
            config.set('Memory', 'level', num)
            self.ids.mat_area.num_pairs = num

        config.write()


    def help_button(self, button):
        webbrowser.open(URL_HELP)
