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
from kivymd.uix.appbar import (
    MDActionTopAppBarButton,
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDTopAppBarTitle,
    MDTopAppBarTrailingButtonContainer,
)

# my app imports
from buscaminas.indicator import Indicator
from buscaminas.startbutton import StartButton
from buscaminas.field import Field
import buscaminas.constants as MINES


Builder.load_string(
    r"""

<ScreenBuscaminas>:
    name: 'buscaminas'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDTopAppBar:
            id: toolbar
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'menu'
                    on_release: app.root.ids.my_drawer.set_state('open')

            MDTopAppBarTitle:
                text: 'Buscaminas'

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'play-circle-outline'
                    on_release: field.start_game()
                MDActionTopAppBarButton:
                    icon: 'bomb'
                    on_release: field.entry_mode(self)
                MDActionTopAppBarButton:
                    icon: 'numeric-1-box'
                    on_release: field.set_level(self)
                MDActionTopAppBarButton:
                    icon: 'volume-high'
                    on_release: field.mute_button(self)
                MDActionTopAppBarButton:
                    icon: 'help-circle-outline'
                    on_release: root.help_button(self)
            

        MDBoxLayout:
            id: menu
            orientation: 'horizontal'
            size_hint_y: None
            height: toolbar.height
            padding: '10dp'
            spacing: '5dp'
            md_bg_color: 0.7, 0.7, 0.7, 1
                    
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
    def help_button(self, button):
        webbrowser.open(MINES.URL_HELP)

