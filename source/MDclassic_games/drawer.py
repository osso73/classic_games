#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 22:09:24 2021

@author: oriol
"""


# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.uix.navigationdrawer import MDNavigationDrawer

# my app imports

Builder.load_file('drawer.kv')


class MyDrawer(MDNavigationDrawer):
    pass
    

