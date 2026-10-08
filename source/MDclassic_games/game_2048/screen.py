# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries
import webbrowser


# non-std libraries
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import (
    MDActionTopAppBarButton,
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDTopAppBarTitle,
    MDTopAppBarTrailingButtonContainer,
)

# my app imports
from game_2048.board import Board
import game_2048.constants as G2048


Builder.load_string(
    r"""

#:set ICONS 'game_2048/images/icons/'

<Screen2048>:
    name: '2048'
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.primaryColor
        on_size: board.initialize_grid()
    
        MDTopAppBar:
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'menu'
                    on_release: app.root.ids.my_drawer.set_state('open')

            MDTopAppBarTitle:
                text: '2048'

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: 'play-circle-outline'
                    on_release: board.start_game()
                MDActionTopAppBarButton:
                    icon: 'backup-restore'
                    on_release: board.back_button()
                MDActionTopAppBarButton:
                    icon: 'volume-high'
                    on_release: board.mute_button(self)
                MDActionTopAppBarButton:
                    icon: 'help-circle-outline'
                    on_release: root.help_button(self)
            
        BoxLayout:
            orientation: 'horizontal'
            padding: 20, 20
            spacing: 20
            size_hint_y: 0.5
            MDChip:
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                on_release: board.change_win_score()
                MDChipText:
                    text: str(board.win_score)
            MDLabel:
                text: 'Score: {:,}'.format(board.score)
                halign: "center"
                font_style: 'Headline'
                role: 'small'

        Board:
            id: board

        BoxLayout:       
            Label:
                canvas:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                        source: 'game_2048/images/logo.jpg'
            GridLayout:
                cols: 3
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label
                ButtonJoystick:
                    text: '^'
                    icon: ICONS + 'up.png'
                    on_release: board.move('up')
                Label
                ButtonJoystick:
                    text: '<'
                    icon: ICONS + 'left.png'
                    on_release: board.move('left')
                ButtonJoystick:
                    text: 'O'
                    icon: ICONS + 'joystic.png'
                ButtonJoystick:
                    text: '>'
                    icon: ICONS + 'right.png'
                    on_release: board.move('right')
                Label
                ButtonJoystick:
                    text: 'v'
                    icon: ICONS + 'down.png'
                    on_release: board.move('down')
                Label

<ButtonJoystick>
    canvas:
        Color:
            rgba: 0,1,0,1
        Rectangle:
            pos: self.pos
            size: self.size
            source: self.icon
    
""")


class Screen2048(MDScreen):
    '''
    This is the main screen, to organize the menu and the board area. Almost
    no logic here, as everything is happening on the Board class. Only
    handles the help button.
    
    '''  
    def help_button(self, button):
        '''Open web-browser with the help page of the game'''
        
        webbrowser.open(G2048.URL_HELP)


class ButtonJoystick(Button):
    icon = StringProperty()

