#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 21:26:32 2021

@author: oriol
"""


# std libraries


# non-std libraries
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

# my app imports



Builder.load_string(
    r"""

<Carta>:
    on_release: self.click()
    canvas:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: root.pos
            size: root.size
            source: root.show

""")


class Carta(Button):
    '''
    This class defines the behaviour of each card: the image that is in the 
    front and the back, and its status (shown or not shown). The card is 
    modeled as a button with an image, which can be the back of the card or
    the front. Action occurs when button is clicked.
    
    Attributes
    ----------
    back : StringProperty
        Filename of the image that appears as back of the card.
    image : StringProperty
        Filename of the image that is in the front of the card.
    show : StringProperty
        Filename of the image that is shown at each moment. It is one of the
        two: image or show.
    shown : BooleanProperty
        Whether the card is turned up or down. False == turned down.
    
    '''
    back = StringProperty()
    image = StringProperty()
    show = StringProperty()
    shown = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Carta, self).__init__(**kwargs)
        self.show = self.back

    def click(self):
        '''
        When button is clicked, trigger the function to turn the card.
        '''
        if not self.shown:
            self.turn()
            self.parent.play('turn')
            Clock.schedule_once(self.add_card_to_current)
            
    def add_card_to_current(self, *args):
        '''
        Add card to Tapete.current_cards list.
        '''
        self.parent.current_cards.append(self)
        
    def turn(self):
        '''
        Turn the card. If the card is shown, turns it back; if not, 
        turn it up.
        '''
        if self.shown:
            self.show = self.back
        else:
            self.show = self.image
        self.shown = not self.shown
        
