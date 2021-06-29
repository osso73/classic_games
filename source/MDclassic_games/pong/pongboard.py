#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 18:43:21 2021

@author: oriol
"""


# std libraries
from functools import partial


# non-std libraries
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget   
from kivy.app import App

# my app imports
from pong.elements import PongBall, PongPaddle
from popup import PopupButton



Builder.load_string(
    r"""

<PongBoard>:
    ball: pong_ball
    player1: player_left
    player2: player_right

    canvas:
        Color:
            rgba: 0,0,0,1  # black
            
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: 1,1,1,1  # white
        Rectangle:
            pos: self.center_x - dp(5), 0
            size: dp(10), self.height
            
    Label:
        font_size: '50sp'
        center_x: root.width / 4
        center_y: root.height * 3 / 4
        text: str(root.player1.score)
        
    Label:
        font_size: '50sp'  
        center_x: root.width * 3 / 4
        center_y: root.height * 3 / 4
        text: str(root.player2.score)

    PongBall:
        id: pong_ball
        center: self.parent.center
    
    PongPaddle:
        id: player_left
        x: '50dp'
        center_y: root.center_y
        
    PongPaddle:
        id: player_right
        x: root.width - self.width - dp(50)
        center_y: root.center_y

""")



class PongBoard(Widget):
    '''
    This is the board of the game, containing all the objects (ball, paddles)
    and the logic to make the game work.

    Attributes
    ----------
    ball : ObjectProperty
        This is the object ball, that is defined as a separate class
    player1, player 2 : ObjectProperty
        These are the paddles for each player. PongPaddle is defined as a
        separate class, and these are two instances of the class
    active : boolean
        Defines if the game is active or has finished. Controls the movement
        of the ball.
    initial_vel : int
        Defines the speed when the ball starts. This speed can be changed from
        the menu of the app.
        
    '''
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    active = BooleanProperty(False)
    initial_vel = NumericProperty()

    
    def __init__(self, *args, **kwargs):
        '''
        Trigger the clock event every 60th of sec.
        '''
        super(PongBoard, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1.0/60.0)
        app = App.get_running_app()
        self.initial_vel = app.config.get('Pong', 'speed')
        skin = app.config.get('Pong', 'skin')
        Clock.schedule_once(partial(self.change_skin, skin))

    
    def serve_ball(self, vel=0):
        '''
        Start the point: start the ball from the center, and sets the velocity.
        '''
        vel = (self.initial_vel, 0) if vel==0 else (vel, 0)
        self.ball.center = self.center
        self.ball.velocity = vel
    
    
    def on_touch_move(self, touch):
        '''
        Move the player based on the touch on the screen.
        '''
        if touch.y < self.top:
            if touch.x < self.width / 3:
                self.player1.center_y = touch.y
            if touch.x > self.width - self.width / 3:
                self.player2.center_y = touch.y

    
    def start_game(self, *args):
        '''
        Start the game: reset scores, and serve the ball
        '''
        self.active = True
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()

        
    def update(self, *args, **kwargs):
        '''
        This is the function that runs 60 times per second. It moves the ball,
        checks the bouncing from walls or paddles and adjust velocity. Also
        checks the score and if it's end of game.
        '''
        if not self.active:
            return
        
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=self.initial_vel)
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=-self.initial_vel)
        
        if max(self.player1.score, self.player2.score) >= 5:
            self.end_game()

    
    def end_game(self):
        '''
        Show popup to indicate who wins, and reset active flag to False.
        '''
        self.active = False
        num = 1 if self.player1.score >= 5 else 2
        
        PopupButton(title='Final', msg=f'El jugador {num} gana!!')


    def pause_button(self, button):
        self.active = not self.active
        button.icon = 'pause' if self.active else 'play'


    def change_skin(self, skin, *args):
        '''
        Change the skin: it sets the skin provided to the ball, 
        and each player.
        '''        
        self.ball.update_skin(skin)
        self.player1.update_skin(skin)
        self.player2.update_skin(skin)
    