# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries


# non-std libraries
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivymd.uix.screen import MDScreen

# my app imports
from snake.gameboard import GameBoard
import snake.constants as SNAKE


Builder.load_string(
    r"""

<ScreenSnake>:
    name: 'snake'
    
    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        md_bg_color: app.theme_cls.primary_light
    
        MDToolbar:
            title: 'Snake'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", game.start_game], ["pause", game.pause_button], ["volume-high", game.mute_button]]
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: score.texture_size[1]
            
            MDLabel:
                id: score
                text: 'Score: ' + str(game.score)
                font_style: 'H5'
                halign: 'center'

            MDLabel:
                text: 'Level: ' + str(game.num_level)
                font_style: 'H5'
                halign: 'center'
                canvas.before:
                    Color:
                        rgba: app.theme_cls.bg_normal
                    Rectangle:
                        size: self.width * root.level_progress_bar, self.height
                        pos: self.pos
        
        GridLayout:
            cols: 3
            on_size: game.set_size()
    
            Label:
            Label:
            Label:
    
            Label:
            GameBoard:
                id: game
            Label:
    
            Label:
            Label:
            Label:

""")

class ScreenSnake(MDScreen):
    '''
    This is the main screen, to organize the menu and the board area. Almost
    no logic here, as everything is happening on the GameBoard class. Only
    handles the settings changes for snake.
    
    Attributes
    ----------
    level_progress_bar : NumericProperty
        Used to show the progress inside one level. This is updated according
        to the level.score.
    '''
    
    level_progress_bar = NumericProperty(0)
    
    def config_change(self, config, section, key, value):
        if key == 'speed':
            self.ids.game.speed_factor = float(value)

        elif key == 'size':
            self.ids.game.size_snake = int(value)
            self.ids.game.set_size()

        elif key == 'mode':
            self.ids.game.story = bool(int(value))

        elif key == 'level_start':
            num = int(value)
            if num < 1:
                num = 1
            elif num > 12:
                num = 12
            config.set('Snake', 'level_start', num)

        config.write()
