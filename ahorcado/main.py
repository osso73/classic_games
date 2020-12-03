#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 7 18:58:11 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)
from random import choice
from time import sleep

FICHERO_PALABRAS = 'lista_palabras.txt'
CARACTERES_VALIDOS = 'abcdefghijoklmnñoprstuvwxyz\
ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'


def replace_letter(string, pos, letter):
    if pos > len(string):
        print(f"Error: pos > len(string) --> {pos} > {len(string)}")
        return None
    
    return string[:pos] + letter + string[pos+1:]


class MainScreen(BoxLayout):
    fallos = NumericProperty(0)
    obj_dibujo = ObjectProperty(None)
    obj_letras_falladas = ObjectProperty(None)
    obj_palabra = ObjectProperty(None)
    obj_teclado = ObjectProperty(None)
    teclado = StringProperty('teclado1')
    active = False
    sound = dict()
    pista = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.sound['bye'] = SoundLoader.load('audio/thanks.ogg')
        self.sound['win'] = SoundLoader.load('audio/game-over-win.ogg')
        self.sound['lose'] = SoundLoader.load('audio/game-over-lost.ogg')

    def iniciar_juego(self):
        self.obj_palabra.buscar_palabra()
        self.reset_juego()
    
    def reset_juego(self):
        self.fallos = 0
        self.letras_acertadas = ''
        self.letras_falladas = ''
        self.obj_letras_falladas.reset_letras()
        self.obj_dibujo.reset_dibujo()
        self.obj_palabra.reset_palabra()
        self.obj_teclado.reset_teclado()
        self.active = True
        self.pista = True

    def final(self, win):
        if win:
            msg = '¡¡Has ganado!!\n¡¡ENHORABUENA!!'
            self.sound['win'].play()
        else:
            msg = 'Lo siento,\nte han colgado...'
            self.sound['lose'].play()
        
        
        p = Popup(title='Final', size_hint=(0.75, 0.25),
                  content=PopupMsg(text=msg))
        p.open()
        self.obj_palabra.actual = self.obj_palabra.palabra
        

    
    def evaluar_letra(self, letra):   
        if not self.active:
            return
        
        # si no es un carácter válido, o ya ha salido, no hace nada
        if letra not in CARACTERES_VALIDOS or \
            letra in self.letras_falladas + self.letras_acertadas:
            return
        
        # si letra es correcta, se muestra
        if letra in self.obj_palabra.palabra:
            self.obj_palabra.anadir_letra(letra)
            self.letras_acertadas += letra
            if self.obj_palabra.actual == self.obj_palabra.palabra:
                self.final(win=True)
        
        # si la letra no es correcta, se añade a la lista de fallos
        else:
            self.fallos += 1
            self.letras_falladas += letra
            self.obj_letras_falladas.anadir_letra(
                letra, self.fallos)
            self.obj_dibujo.anadir_dibujo(self.fallos)
            
            if self.fallos >= 10:
                self.final(win=False)
    
    def thanks(self):
        self.sound['bye'].play()
        sleep(1.5)


    def dar_pista(self):
        if self.active:
            if self.pista:
                letra = choice(self.obj_palabra.palabra)
                while letra in self.obj_palabra.actual:
                    letra = choice(self.obj_palabra.palabra)
        
                self.obj_teclado.pulsar_tecla(letra)
                self.pista = False
            else:
                p = Popup(title='Aviso', size_hint=(0.75, 0.15),
                          content=PopupMsg(text='¡No puedes pedir más pistas!'))
                p.open()
            



class Dibujo(RelativeLayout):
    status = StringProperty('D'*10)
    skin = NumericProperty(1)
    
    def anadir_dibujo(self, fallos):
        self.status = replace_letter(self.status, fallos-1, 'A')
    
    def reset_dibujo(self):
        self.status = 'D'*10
    
    def cambiar_hombre(self):
        self.skin = self.skin % 2 + 1
        


class LetrasFalladas(BoxLayout):
    fallo = StringProperty('_'*10)
    
    
    def reset_letras(self):
        self.fallo = '_'*10
    
    
    def anadir_letra(self, letra, fallos):
        '''
        Añade una letra en la lista de letras falladas, en la posición
        num_fallo

        Parameters
        ----------
        letra : string
            letra a añadir
        num_fallo : int
            número de fallo. Es un número entre 1 y 10, indica el fallo

        Returns
        -------
        None.

        '''
        self.fallo = replace_letter(self.fallo, fallos-1, letra)



class PalabraLetras(BoxLayout):
    actual = StringProperty(' ')
    palabra = ' '
    
    
    def reset_palabra(self):
        self.actual = '-'*len(self.palabra)
        
    def buscar_palabra(self):
        self.palabra = self.cargar_palabra()
        self.reset_palabra()
    
    def cargar_palabra(self):
        '''
        Busca una palabra en un fichero, y la devuelve.

        Returns
        -------
        str
            Palabra escogida

        ''' 
        with open(FICHERO_PALABRAS, 'rt') as f:
            lista = [ line.rstrip('\n') for line in f ]
        
        return choice(lista)
    
    def anadir_letra(self, letra):
        pos = 0
        pos = self.palabra.find(letra)
        while pos != -1:
            self.actual = replace_letter(
                self.actual, pos, letra)
            pos = self.palabra.find(letra, pos+1)


class Menu(BoxLayout):
    pass


class Teclado(GridLayout): 
    skin = 'teclado1'
    
    def __init__(self, **kwargs):
        super(Teclado, self).__init__(**kwargs)
        self.crear_teclas()
    
    def crear_teclas(self):
        for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
            name = letra if letra != 'Ñ' else 'N2'
            self.add_widget(Tecla(letra=letra, filename=name))

    def cambiar_teclado(self):
        n = int(self.skin[-1])
        n = n % 6 + 1
        self.skin = self.skin[:-1] + str(n)
        
        for tecla in self.children:
            tecla.skin = self.skin
    
    def reset_teclado(self):
        for tecla in self.children:
            tecla.disabled = False
    
    def pulsar_tecla(self, letra):
        for tecla in self.children:
            if tecla.letra == letra:
                tecla.sound.play()
                tecla.pulsar()


class Tecla(Button):
    letra = StringProperty()
    sound = SoundLoader.load('audio/tecla.ogg')
    skin = StringProperty('teclado1')
    filename = StringProperty()
    
    def pulsar(self):
        app = App.get_running_app()
        app.root.evaluar_letra(self.letra)
        self.disabled = True

class PopupMsg(Label):
    pass


class AhorcadoApp(App):
    def build(self):
        self.icon = 'textures/icon.png'
        prog = MainScreen()
        return prog


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (540, 1170)
    AhorcadoApp().run()


