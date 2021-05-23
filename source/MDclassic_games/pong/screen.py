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
            
        MDLabel:
            text: 'Not yet implemented'
            font_style: 'H3'
            pos_hint: { 'center_x': 0.5, 'center_y': 0.5 }
            halign: 'center'

""")

class ScreenPong(MDScreen):
    pass
