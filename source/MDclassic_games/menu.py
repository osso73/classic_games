# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.imagelist import MDSmartTile

from kivymd.uix.screen import MDScreen

# my app imports


Builder.load_file('menu.kv')


class Menu(MDScreen):
    pass


class MyTile(MDSmartTile):
    txt = StringProperty()
    screen = StringProperty()
    source = StringProperty()
