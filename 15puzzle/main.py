#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 19:00:00 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from time import sleep
from random import shuffle
import os
import math


SPACING = 10
MOVE_DURATION = 0.1
TEMAS = 'images/temas'

class Puzzle(RelativeLayout):
    ventana = NumericProperty(100)
    empty = ObjectProperty()
    movimientos = NumericProperty(0)
    tamano = NumericProperty()
    
    def __init__(self, **kwargs):
        super(Puzzle, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_grid)
    
    def initialize_grid(self, *args):
        self.ventana = min(self.parent.height, self.parent.width)
    
    def start_game(self):
        self.parent.play('start')
        self.clear_widgets()
        self.tamano = 2 + self.parent.nivel
        self.movimientos = 0

        lado = int(self.ventana / self.tamano)
        title = list(range(1, self.tamano**2))+['']
        shuffle(title)
        while not self.solvable(title):
            shuffle(title)
        n = 0
        for i in range(self.tamano):
            for j in range(self.tamano):
                self.add_widget(Ficha(name=str(title[n]), lado=lado, 
                                      tamano=self.tamano,
                                      size=(lado-SPACING, lado-SPACING),
                                      size_hint=(None, None), posicion=(j, i)))
                n += 1

    def find_empty(self):
        for child in self.children:
            if not child.name:
                return child       
        raise Exception('Empty square not found!')

    def check_win(self):
        for child in self.children:
            if not child.name:
                continue
            if int(child.name) != child.posicion[0] + child.posicion[1] * self.tamano + 1:
                return False        
        return True
    
    def solvable(self, game):
        lado = math.sqrt(len(game))
        if int(lado) != lado:
            raise Exception('Game sequence not an exact square.')
        
        lado = int(lado)
        seq = [int(n) for n in game if n]
        inversions = 0
        for n in seq:
            for m in seq:
                if seq.index(n) < seq.index(m) and n > m:
                    inversions += 1
        
        if lado % 2:
            if inversions % 2:
                return False
            else:
                return True
        else:
            blank = game.index('')
            row_blank = lado - blank // lado
            if row_blank % 2:
                if not inversions % 2:
                    return True
                else:
                    return False
            else:
                if inversions % 2:
                    return True
                else:
                    return False
            
"""
If N is even, puzzle instance is solvable if 

    the blank is on an even row counting from the bottom 
    (second-last, fourth-last, etc.) and number of inversions is odd.
    
    the blank is on an odd row counting from the bottom (last, third-last, 
    fifth-last, etc.) and number of inversions is even.

"""            
                
                
                
        
        

class PopupMsg(Label):
    pass

class Ficha(Label):
    name = StringProperty()
    tamano = NumericProperty()
    lado = NumericProperty()
    posicion = ListProperty()
    
    def __init__(self, **kwargs):
        super(Ficha, self).__init__(**kwargs)
        self.pos = self.calcular_posicion()
    
    def calcular_posicion(self):
        return (self.posicion[0]*self.lado + SPACING/2, 
                (self.tamano-1-self.posicion[1])*self.lado + SPACING/2)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.move()
    
    def move(self):
        empty = self.parent.find_empty()
        ex, ey = empty.posicion
        px, py = self.posicion
        if (ex==px and ey==py+1) or (ex==px and ey==py-1) or\
            (ey==py and ex==px+1) or (ey==py and ex==px-1):
                empty.posicion, self.posicion = self.posicion, empty.posicion
                self.parent.parent.play('move')
                self.parent.movimientos += 1
        
        
        if self.parent.check_win():
            self.parent.parent.play('end_game')
            p = Popup(title='Final', size_hint=(0.80, 0.20),
                  content=PopupMsg(text='!Muy bien!\nTodas las piezas están correctas.'))
            p.open()

    
    def on_posicion(self, *args):
        anim = Animation(pos=self.calcular_posicion(), duration=MOVE_DURATION)
        anim.start(self)

                    


class MenuButton(Button):
    pass

class MenuButtonSmall(Button):
    pass

class MenuLabel(Label):
    pass

class PopupMsg(Label):
    pass


class MainScreen(BoxLayout):
    nivel = NumericProperty(1)
    tema = StringProperty('numeros')
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.sounds = self.load_sounds()

    def load_sounds(self):
        sound = dict()
        sound['bye'] = SoundLoader.load('audio/bye.ogg')
        sound['ok'] = SoundLoader.load('audio/ok.ogg')
        sound['start'] = SoundLoader.load('audio/start.ogg')
        sound['move'] = SoundLoader.load('audio/move.ogg')
        sound['end_game'] = SoundLoader.load('audio/end_game.ogg')
        
        return sound
    
    def play(self, sound):
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")

    def bye(self):
        self.play('bye')
        sleep(1.5)
    
    def cambiar_tema(self):
        temas = os.listdir(TEMAS)
        ind = temas.index(self.tema)
        new_ind = (ind + 1) % len(temas)
        self.tema = temas[new_ind]
        




class PuzzleApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (500, 1000)
    PuzzleApp().run()

