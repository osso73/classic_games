#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:41:49 2021

@author: oriol
"""

# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy import metrics

# my app imports


Builder.load_string(
    r"""

<PopupButton>:
    size_hint: None, None
    auto_dismiss: False
    BoxLayout:
        orientation: 'vertical'
        
        Label:
            text: root.msg
            padding: sp(20), sp(20)
            font_size: '20sp'
            size_hint: None, None
            size: self.texture_size
        Button:
            text: 'Ok'
            font_size: '20sp'
            padding: sp(20), sp(10)
            size_hint: None, None
            size: self.texture_size
            on_release: root.dismiss()
            pos_hint: {'center_x': 0.5}

""")



class PopupButton(Popup):
    msg = StringProperty()

    def __init__(self, **kwargs):
        super(PopupButton, self).__init__(**kwargs)
        Clock.schedule_once(self.open)
        Clock.schedule_once(self.set_size)

    def calculate_size(self):
        width = height = 0
        for child in self.content.children:
            x, y = child.size
            width = max(width, x)
            height += y
        width += metrics.sp(50)
        height += metrics.sp(60)

        return width, height

    def set_size(self, *args):
        self.size = self.calculate_size()

