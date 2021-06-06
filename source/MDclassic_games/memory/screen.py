# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries


# non-std libraries
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


# my app imports
from memory.tapete import Tapete



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
            right_action_items: [["play-circle-outline", obj_tapete.start_game], ["volume-off", obj_tapete.mute_button]]
            
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
                    text: obj_tapete.tema_actual
                    valign: 'center'
                    icon: ''
                    on_release: obj_tapete.cambiar_tema()
                MDChip:
                    text: str(obj_tapete.tamano)
                    icon: ''
                    on_release: obj_tapete.change_level()

            MDLabel:
                id: score
                text: 'Moves: ' + str(obj_tapete.movimientos)
                halign: "center"
                font_style: 'H4'
        
        Tapete:
            id: obj_tapete

""")

class ScreenMemory(MDScreen):
    def config_change(self, config, section, key, value):
        if key == 'theme':
            self.ids.obj_tapete.tema_actual = value

        elif key == 'level':
            num = int(value)
            if num < 2:
                num = 2
            elif num > 20:
                num = 20
            config.set('Memory', 'level', num)
            self.ids.obj_tapete.tamano = num

        config.write()

