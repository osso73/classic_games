#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 18:47:36 2021

@author: oriol
"""


# std libraries
import math
import os


# non-std libraries
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


# my app imports



Builder.load_string(
    r"""

<PongBall>:
    size: '40dp', '40dp'
    canvas:
        Ellipse:
            source: self.source
            pos: self.pos
            size: self.size


<PongPaddle>:
    size: '20dp', '75dp'
    canvas:
        Rectangle:
            source: self.source
            pos:self.pos
            size:self.size

""")



class PongPaddle(Widget):
    '''
    This class defines the properties and intelligence of the paddle. The
    game has two paddles, one for each player.

    Attributes
    ----------
    score : int
        Holds the score of the player
    source : string
        The name of the skin to be used

    '''
    score = NumericProperty(0)
    source = StringProperty()

    def bounce_ball(self, ball):
        '''

        '''
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            abs_vel = math.sqrt(vx**2 + vy**2)
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = Vector(bounced.x, bounced.y + 5*offset)
            norm = math.sqrt(vel.x**2 + vel.y**2)
            ball.velocity = vel / norm * abs_vel * 1.1
    
    def update_skin(self, skin_name):
        self.source = os.path.join(os.path.dirname(__file__), 
                                   'images', skin_name, 'paddle.gif')


class PongBall(Widget):
    '''
    This class controls the ball.

    Attributes
    ----------
    source : string
        The name of the skin to be used

    velocity_x, velocity_y : int
        Velocity of the ball on x and y axis

    velocity = ReferenceListProperty(velocity_x, velocity_y)
        Referencelist property so we can use ball.velocity as
        a shorthand, just like e.g. w.pos for w.x and w.y

    '''
    source = StringProperty()
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        '''
        ``move`` function will move the ball one step. This
        will be called in equal intervals to animate the ball
        '''
        self.pos = Vector(*self.velocity) + self.pos

    def update_skin(self, skin_name):
        '''
        Change the skin used
        '''
        self.source = os.path.join(os.path.dirname(__file__), 
                                   'images', skin_name, 'ball.gif')

