#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:08:56 2020

@author: osso73
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from random import sample
from time import sleep
import os


TEMAS = os.path.join('images', 'temas')


#######################################################################
class Tapete(GridLayout):
    columnas = NumericProperty(2)
    current_cards = ListProperty()
    movimientos = NumericProperty(0)
    
        
    def load_images(self, app):
        p = os.path.join(TEMAS, app.root.tema_actual) 
        ims = os.listdir(p)
        ims = [os.path.join(p,im) for im in ims if im.startswith('image')]
        back = os.path.join(p,'back.jpg')
        return ims, back
        
    def start_game(self):
        self.clear_widgets()
        
        app = App.get_running_app()
        num = app.root.tamano
        app.root.play('start')
        self.imagenes, back = self.load_images(app)
        self.movimientos = 0
        
        imagenes = sample(self.imagenes, num)
        imagenes = sample(imagenes*2, num*2)
        
        self.set_columns(num)     
        for im in imagenes:
            self.add_widget(Carta(image=im, back=back))
    
    def set_columns(self, num):
        if num < 5:
            self.columnas = 2
        elif num < 10:
            self.columnas = 3
        elif num < 16:
            self.columnas = 4
        else:
            self.columnas = 5
        
    def on_current_cards(self, *args, **kwargs):
        if len(self.current_cards) == 2:
            self.movimientos += 1
            if self.current_cards[0].image != self.current_cards[1].image:
                sleep(2)
                self.current_cards.pop().turn()
                self.current_cards.pop().turn()
            else:
                self.current_cards.pop()
                self.current_cards.pop()
                app = App.get_running_app()
                app.root.play('ok')
                self.check_end()
    
    def check_end(self):
        for carta in self.children:
            if not carta.shown:
                return
        
        app = App.get_running_app()
        app.root.play('end_game')
        p = Popup(title='Final', size_hint=(0.75, 0.15),
                  content=PopupMsg(text='!Muy bien!\nHas encontrado todas las parejas'))
        p.open()

        
#######################################################################
class Carta(Button):    
    back = StringProperty()
    image = StringProperty()
    show = StringProperty()
    shown = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Carta, self).__init__(**kwargs)
        self.show = self.back

    def click(self):
        if not self.shown:
            self.turn()
            app = App.get_running_app()
            app.root.play('turn')
            Clock.schedule_once(self.add_card_to_current)
            
    def add_card_to_current(self, *args):
        app = App.get_running_app()
        app.root.ids.obj_tapete.current_cards.append(self)
        
    def turn(self):
        if self.shown:
            self.show = self.back
        else:
            self.show = self.image
        self.shown = not self.shown
        

#######################################################################
class MainScreen(BoxLayout):
    tamano = NumericProperty(6)
    tema_actual = StringProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.lista_temas = os.listdir(TEMAS)
        self.cambiar_tema()
        self.sounds = self.load_sounds()
        
    def cambiar_tema(self):
        if not self.tema_actual:
            self.tema_actual = self.lista_temas[0]
        else:
            ind = self.lista_temas.index(self.tema_actual)
            new_ind = ind+1 if ind<len(self.lista_temas)-1 else 0
            self.tema_actual = self.lista_temas[new_ind]
    
    def load_sounds(self):
        sound = dict()
        sound['bye'] = SoundLoader.load('audio/bye.ogg')
        # sound['ambience'] = SoundLoader.load('audio/ambience.ogg')
        sound['ok'] = SoundLoader.load('audio/ok.ogg')
        sound['start'] = SoundLoader.load('audio/start.ogg')
        sound['turn'] = SoundLoader.load('audio/turn.ogg')
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



class PopupMsg(Label):
    pass

class MenuButton(Button):
    pass

class MenuButtonSmall(Button):
    pass

class MenuLabel(Label):
    pass



class MemoryApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (500, 1000)
    MemoryApp().run()
