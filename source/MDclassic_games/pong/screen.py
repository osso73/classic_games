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
from pong.pongboard import PongBoard



URL_HELP = 'https://osso73.github.io/classic_games/games/classic_games/#game-of-pong'


Builder.load_string(
    r"""

<ScreenPong>:
    name: 'pong'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDTopAppBar:
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'menu'
                    on_release: app.root.ids.my_drawer.set_state('open')

            MDTopAppBarTitle:
                text: 'Pong'

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'play-circle-outline'
                    on_release: pong.start_game()
                MDActionTopAppBarButton:
                    icon: 'pause'
                    on_release: pong.pause_button()
                MDActionTopAppBarButton:
                    icon: 'help-circle-outline'
                    on_release: root.help_button(self)
            
        PongBoard:
            id: pong
        

""")


class ScreenPong(MDScreen):
    '''
    This class organizes the screen in different sections: menu, and game.
    It controls the config settings.

    '''        
    
    def config_change(self, config, section, key, value):
        if key == 'speed':
            val = int(value)
            if val < 0:
                val = abs(val)
                config.set('Pong', 'speed', val)
            self.ids.pong.initial_vel = val

        elif key == 'max-speed':
            val = int(value)
            if val < 0:
                val = abs(val)
                config.set('Pong', 'max-speed', val)
            self.ids.pong.ids.pong_ball.max_vel = val

        elif key == 'skin':
            self.ids.pong.change_skin(value)

        config.write()


    def help_button(self, button):
        webbrowser.open(URL_HELP)
