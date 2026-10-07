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
from memory.mat import Mat


URL_HELP = 'https://osso73.github.io/classic_games/games/classic_games/#game-of-memory'


Builder.load_string(
    r"""

<ScreenMemory>:
    name: 'memory'
    
    BoxLayout:
        orientation: 'vertical'
    
        MDTopAppBar:
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'menu'
                    on_release: app.root.ids.my_drawer.set_state('open')

            MDTopAppBarTitle:
                text: 'Memory'

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'play-circle-outline'
                    on_release: mat_area.start_game()
                MDActionTopAppBarButton:
                    icon: 'volume-high'
                    on_release: mat_area.mute_button(self)
                MDActionTopAppBarButton:
                    icon: 'help-circle-outline'
                    on_release: root.help_button(self)
            
        MDBoxLayout:
            orientation: 'horizontal'
            padding: '10dp'
            size_hint_y: None
            height: score.texture_size[1] + dp(10)*2
            md_bg_color: app.theme_cls.primaryColor
            
            BoxLayout:
                orientation: 'horizontal'
                spacing: '10dp'

                MDChip:
                    on_release: mat_area.change_theme()
                    MDChipText:
                        text: mat_area.current_theme
                MDChip:
                    on_release: mat_area.change_level()
                    MDChipText:
                        text: str(mat_area.num_pairs)

            MDLabel:
                id: score
                text: 'Moves: ' + str(mat_area.moves)
                halign: "center"
                font_style: 'Headline'
                role: 'large'
        
        Mat:
            id: mat_area

""")


class ScreenMemory(MDScreen):
    '''
    This is the main screen, to organize the menu and the mat area. Almost
    no logic here, as everything is happening on the Mat class. Only
    handles the settings changes for memory.
    
    '''  
    def config_change(self, config, section, key, value):
        if key == 'theme':
            self.ids.mat_area.current_theme = value

        elif key == 'level':
            num = int(value)
            if num < 2:
                num = 2
            elif num > 20:
                num = 20
            config.set('Memory', 'level', num)
            self.ids.mat_area.num_pairs = num

        config.write()


    def help_button(self, button):
        webbrowser.open(URL_HELP)
