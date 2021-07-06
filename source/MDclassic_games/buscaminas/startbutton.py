#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 10:02:48 2021

@author: oriol
"""


# std libraries
import os


# non-std libraries
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty


# my app imports
import buscaminas.constants as MINES



Builder.load_string(
    r"""

<StartButton>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Ellipse:
            size: self.height, self.height
            pos: self.x + self.width / 2 - self.height / 2 , self.y
            source: self.button_face

""")



class StartButton(Label):
    '''
    The button to start the game. This class controls the image to use, and
    the action.
    
    Attributes
    ----------
    button_face: StringProperty
        Name of the image to be shown
    '''
    button_face = StringProperty()

    
    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)
        self.change_face('standard')


    def on_touch_down(self, touch):
        '''
        Change the face of button when it's pressed.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.change_face('press')
            return True

    
    def on_touch_up(self, touch):
        '''
        Trigger the start of the game, and change back the button face.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.change_face('standard')
            self.parent.parent.parent.ids.field.start_game()
            return True


    def change_face(self, face):
        '''
        Change the face of the button that is shown.

        Parameters
        ----------
        face : string
            Can be one of the 4 options: 'lost', 'press', 'standard', 'won'.

        '''
        if face not in ['lost', 'press', 'standard', 'won']:
            raise ValueError("Face incorrect")
        
        filename = f'{face}.png'
        self.button_face = os.path.join(MINES.IMAGES, filename)

