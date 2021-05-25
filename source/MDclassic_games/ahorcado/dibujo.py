#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:23:00 2021

@author: osso73
"""


# std libraries

# non-std libraries
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import  StringProperty, NumericProperty

# my app imports
from ahorcado.general import replace_letter


Builder.load_string(
    r"""

#:set COLOUR_IMAGE [1,1,1,1]
#:set COLOUR_ACTIVE [0,0,1,1]
#:set COLOUR_DISABLED [0,0,1,0]

<Dibujo>:
    skin: int(app.config.get('Ahorcado', 'man')[-1])
    canvas:
        Color:
            rgba: COLOUR_IMAGE
        Rectangle:
            size: self.size
            pos: 0,0
            source: 'ahorcado/images/desierto.jpg'
        Color:
            rgba: COLOUR_IMAGE if self.status[0]=='A' else COLOUR_DISABLED
        Rectangle:
            size: 8 * self.width/10, 0.35 * self.height/10
            pos: 1 * self.width/10, 1 * self.height/10
            source: 'ahorcado/images/madera.jpg'
        Color:
            rgba: COLOUR_IMAGE if self.status[1]=='A' else COLOUR_DISABLED
        Rectangle:
            size: 0.5 * self.width/10, 8 * self.height/10
            pos: 2 * self.width/10, 1 * self.height/10
            source: 'ahorcado/images/madera.jpg'
        Color:
            rgba: COLOUR_IMAGE if self.status[2]=='A' else COLOUR_DISABLED
        Rectangle:
            size: 5 * self.width/10, 0.35 * self.height/10
            pos: 1 * self.width/10, 9 * self.height/10
            source: 'ahorcado/images/madera.jpg'
        Color:
            rgba: COLOUR_IMAGE if self.status[3]=='A' else COLOUR_DISABLED
        Rectangle:
            size: 0.5 * self.width/10, 1.35 * self.height/10
            pos: 6 * self.width/10, 8 * self.height/10
            source: 'ahorcado/images/cuerda.jpg'

        Color:
            rgba: COLOUR_IMAGE if (self.status[4]=='A' and self.skin==1) else COLOUR_DISABLED
        Ellipse:
            size: 1.5 * self.width/10, 1.5 * self.height/10
            pos: 5.5 * self.width/10, 7 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-cara.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[5]=='A' and self.skin==1) else COLOUR_DISABLED
        Rectangle:
            size: 2 * self.width/10, 2.5 * self.height/10
            pos: 5.25 * self.width/10, 4.5 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-tronco.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[6]=='A' and self.skin==1) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.5 * self.height/10
            pos: 6.8 * self.width/10, 4.3 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-brazo-derecho.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[7]=='A' and self.skin==1) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.5 * self.height/10
            pos: 4.6 * self.width/10, 4.3 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-brazo-izquierdo.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[8]=='A' and self.skin==1) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.5 * self.height/10
            pos: 5.26 * self.width/10, 2.15 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-pierna-izquierda.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[9]=='A' and self.skin==1) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.4 * self.height/10
            pos: 6.24 * self.width/10, 2.15 * self.height/10
            source: 'ahorcado/images/hombre/hombre1-pierna-derecha.png'

        Color:
            rgba: COLOUR_IMAGE if (self.status[4]=='A' and self.skin==2) else COLOUR_DISABLED
        Ellipse:
            size: 2 * self.width/10, 2 * self.height/10
            pos: 5.2 * self.width/10, 6.5 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-cara.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[5]=='A' and self.skin==2) else COLOUR_DISABLED
        Rectangle:
            size: 2 * self.width/10, 2.2 * self.height/10
            pos: 5.25 * self.width/10, 4.4 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-tronco.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[6]=='A' and self.skin==2) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.5 * self.height/10
            pos: 7.1 * self.width/10, 3.95 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-brazo-derecho.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[7]=='A' and self.skin==2) else COLOUR_DISABLED
        Rectangle:
            size: 1 * self.width/10, 2.5 * self.height/10
            pos: 4.4 * self.width/10, 3.95 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-brazo-izquierdo.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[8]=='A' and self.skin==2) else COLOUR_DISABLED
        Rectangle:
            size: 1.6 * self.width/10, 2.8 * self.height/10
            pos: 4.6 * self.width/10, 1.65 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-pierna-izquierda.png'
        Color:
            rgba: COLOUR_IMAGE if (self.status[9]=='A' and self.skin==2) else COLOUR_DISABLED
        Rectangle:
            size: 1.6 * self.width/10, 2.8 * self.height/10
            pos: 6.2 * self.width/10, 1.65 * self.height/10
            source: 'ahorcado/images/hombre/hombre2-pierna-derecha.png'

""")


class Dibujo(RelativeLayout):
    '''
    Area of the screen with the picture of the hangman. Most of the logic
    here is defined in .kv file.
    
    Attributes
    ----------
    status : string
        Used to define what parts of the drawing of hangman should be shown,
        and what parts should be invisible (A=Active, i.e. shown; D=Deactive
        i.e. not shown)
    skin : int
        Defines what skin to use for the men. Two options are possible, 1 and 2
    '''
    status = StringProperty('D'*10)
    skin = NumericProperty()
    
    def anadir_dibujo(self, fallos):
        '''
        Change self.status, so a new portion of the drawing is
        shown

        Parameters
        ----------
        fallos : int
            Number of errors
        '''
        self.status = replace_letter(self.status, fallos-1, 'A')
    
    def reset_dibujo(self):
        '''
        Reset status to everything de-activated, to start a
        new game.
        '''
        self.status = 'D'*10
    
    def cambiar_hombre(self, value):
        '''
        Change the skin used for the man (2 options possible).
        '''
        self.skin = int(value)
        
