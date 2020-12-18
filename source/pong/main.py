#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 18:36:11 2020

@author: osso73
"""

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import (
    NumericProperty, ReferenceListProperty, 
    ObjectProperty, BooleanProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import math
import os


class MainScreen(BoxLayout):
    skin = StringProperty('original')
        
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.skin_list = ['original'] + sorted(os.listdir('skins'))
        

    def change_skin(self, game):
        ind = self.skin_list.index(self.skin)
        ind = (ind + 1) % len(self.skin_list)
        self.skin = self.skin_list[ind]
        game.ball.update_skin(self.skin)
        game.player1.update_skin(self.skin)
        game.player2.update_skin(self.skin)


class GameBoard(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    active = BooleanProperty(False)
    initial_vel = NumericProperty(10)
    
    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1.0/60.0)
    
    def serve_ball(self, vel=0):
        vel = (self.initial_vel, 0) if vel==0 else (vel, 0)
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def on_touch_move(self, touch):
        if touch.y < self.top:
            if touch.x < self.width / 3:
                self.player1.center_y = touch.y
            if touch.x > self.width - self.width / 3:
                self.player2.center_y = touch.y
    
    def start_game(self):
        self.player1.score = 0
        self.player2.score = 0
        self.active = True
        self.serve_ball()
        
    def update(self, *args, **kwargs):
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
        self.active = False
        num = 1 if self.player1.score >= 5 else 2
        
        p = Popup(title='Final', size_hint=(None, None), size=(800, 300),
                  content=Label(text=f'El jugador {num} gana!!', 
                                font_size = 64))
        p.open()


class PongPaddle(Widget):
    score = NumericProperty(0)
    source = StringProperty()

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            abs_vel = math.sqrt(vx**2 + vy**2)
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = Vector(bounced.x, bounced.y + 5*offset)
            norm = math.sqrt(vel.x**2 + vel.y**2)
            ball.velocity = vel / norm * abs_vel * 1.1
    
    def update_skin(self, skin_name):
        self.source = 'skins/' + skin_name + '/paddle.gif'


class PongBall(Widget):
    source = StringProperty()

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def update_skin(self, skin_name):
        self.source = 'skins/' + skin_name + '/ball.gif'


class PongApp(App):
    def build(self):
        main = MainScreen()
        return main


if __name__ == '__main__':
    PongApp().run()
