#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 22:09:24 2021

@author: oriol
"""


# std libraries
import webbrowser


# non-std libraries
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.button import MDButton, MDButtonText

# my app imports



Builder.load_file('drawer.kv')


class MyDrawer(MDNavigationDrawer):
    screen = StringProperty('menu')

    def open_help(self):
        webbrowser.open('https://osso73.github.io/classic_games/games/classic_games/')
    
    def about(self, *args):
        
        def close_msg(button):
            about.dismiss()
                
        version = App.get_running_app().version
        msg = f"""
Classic games version {version}.

Program written by osso73.

You can find more information on github: 
https://github.com/osso73/classic_games
        """
        
        about = MDDialog(
            MDDialogHeadlineText(text='About'),
            MDDialogSupportingText(text=msg),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text='CLOSE'),
                    style='text',
                    on_release=close_msg,
                ),
                spacing='8dp',
            ),
        )
        
        about.open()
 
