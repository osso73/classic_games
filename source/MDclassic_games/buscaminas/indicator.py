#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 09:59:07 2021

@author: oriol
"""


# std libraries


# non-std libraries
from kivy.lang import Builder
from kivy.uix.label import Label

# my app imports



Builder.load_string(
    r"""

<Indicator>:
    bold: True
    color: 1,0,0,1
    font_size: '200sp'
    padding: '10dp', '10dp'
    size: self.texture_size
    texture_size: self.size
    font_name: 'buscaminas/fonts/digital-7 (mono)'
    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos            

""")



class Indicator(Label):
    '''
    For the indicators of mines and time.
    '''
    pass

