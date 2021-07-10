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
from kivy.app import App


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
                        
            # offset to control how the ball deviates on the Y axis
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            
            # bouncing: calculate the new velocity
            bounced = Vector(-1 * vx, vy)
            vel = Vector(bounced.x, bounced.y + 5*offset)
            
            # increase increase speed with each bounce, and set the value
            ball.increase_velocity(vel)
            
    
    def update_skin(self, skin_name):
        '''
        Change the image of the paddle, according to the skin_name.

        Parameters
        ----------
        skin_name : str
            Name of the skin. Used as part of the foldername of the image.

        '''
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
    velocity: ReferenceListProperty
        Referencelist property so we can use ball.velocity as
        a shorthand, just like e.g. w.pos for w.x and w.y   
    max_velocity : int
        Defines the maximum speed that can be achieved by the ball. When 
        reached, the ball will not accelerate any more after bouncing.

    '''
    source = StringProperty()
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    max_velocity = 0

    
    def __init__(self, *args, **kwargs):
        '''Trigger the clock event every 60th of sec.'''
        
        super(PongBall, self).__init__(*args, **kwargs)
        app = App.get_running_app()
        self.max_vel = int(app.config.get('Pong', 'max-speed'))

    
    def move(self):
        '''
        Move the ball one step. This will be called in equal intervals to 
        animate the ball.
        
        '''
        self.pos = Vector(*self.velocity) + self.pos


    def update_skin(self, skin_name):
        '''Change the skin used'''
        
        self.source = os.path.join(os.path.dirname(__file__), 
                                   'images', skin_name, 'ball.gif')


    def increase_velocity(self, vel):
        '''
        Take the speed vel, and increase it if less than max-vel. Otherwise
        no increase. And set the value as the new speed for the ball
        (self.velocity).

        Parameters
        ----------
        vel : Vector
            Speed that needs to be increased. This is the resulting speed
            after bouncing.

        '''
        abs_vel = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        speedup = 1.1 if abs_vel < self.max_vel else 1
        self.velocity = vel * speedup
