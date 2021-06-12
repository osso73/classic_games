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
from buscaminas.indicator import Indicator
from buscaminas.startbutton import StartButton
from buscaminas.field import Field



Builder.load_string(
    r"""

<ScreenBuscaminas>:
    name: 'buscaminas'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDToolbar:
            id: toolbar
            title: 'Buscaminas'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", field.start_game], ['bomb', field.entry_mode], ['numeric-1-box', field.set_level], ['volume-high', field.mute_button]]
            

        BoxLayout:
            id: menu
            orientation: 'horizontal'
            size_hint_y: None
            height: toolbar.height
            padding: '10dp'
            spacing: '5dp'
            canvas:
                Color:
                    rgba: 0.7, 0.7, 0.7, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    
            Indicator:
                text: '{:03}'.format(field.mines)
    
            Label:
    
            StartButton:
                id: start_button
            
            Label:                
                    
            Indicator:
                text: '{:03}'.format(field.time)
        
        Field:
            id: field
        
        Label:
            canvas:
                Color:
                    rgba: 0.8, 0.8, 0.8, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
    
""")

class ScreenBuscaminas(MDScreen):
    pass
