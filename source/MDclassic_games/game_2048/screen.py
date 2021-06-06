# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:21:28 2021

@author: oriol
"""


# std libraries


# non-std libraries
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

# my app imports
from game_2048.board import Board


Builder.load_string(
    r"""

#:set ICONS 'game_2048/images/icons/'

<Screen2048>:
    name: '2048'
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.primary_light
        on_size: board.initialize_grid()
    
        MDToolbar:
            title: '2048'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.my_drawer.set_state("open")]]
            right_action_items: [["play-circle-outline", board.start_game], ["backup-restore", board.back_button], ["volume-off", board.mute_button]]
            
        BoxLayout:
            orientation: 'horizontal'
            padding: 20, 20
            spacing: 20
            size_hint_y: 0.5
            MDChip:
                text: str(board.win_score)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                icon: ''
                on_release: board.change_win_score()
            MDLabel:
                text: 'Score: {:,}'.format(board.score)
                halign: "center"
                font_style: 'H4'

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

<NewButton>
    font_size: 120
    size: self.texture_size
    texture_size: self.size
    padding: 20, 20
    
""")


class Screen2048(MDScreen):
    pass


class ButtonJoystick(Button):
    icon = StringProperty()


class NewButton(Button):
    pass
