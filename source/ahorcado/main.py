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
import os

FICHERO_PALABRAS = 'lista_palabras.txt'
CARACTERES_VALIDOS = 'abcdefghijoklmnñoprstuvwxyz\
ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'


def replace_letter(string, pos, letter):
    '''
    Replace the character in string in position pos, by letter.

    Attributes
    ----------
    string : string
        String of characters containing the text to be replaced
    pos : int
        Position to be replaced
    letter : string (1 character)
        Character that replaces the previous
    
    Returns
    -------
    string:
        the new string with the character replaced
    '''
    if pos > len(string):
        raise IndexError(f"pos > len(string) --> {pos} > {len(string)}")

    if len(letter) != 1:
        raise Exception("letter has to be a single character")
    
    return string[:pos] + letter + string[pos+1:]


class MainScreen(BoxLayout):
    '''
    This class organizes the screen in different sections, with menu on top,
    the middle section with the picture and failed letters, the word to 
    search, and the keyboard.

    It contains most of the logic of starting/ending game, evaluate letter...

    Attributes
    ----------
    fallos : int
        Number of failed tries
    obj_dibujo : ObjectProperty
        Object with the drawing
    obj_letras_falladas : ObjectProperty
        Object of the failed letters
    obj_palabra : ObjectProperty
        Object of the word to find
    obj_teclado : ObjectProperty
        Object of the keyboard
    teclado : string
        Name of the skin to be used for keyboard
    active : boolean
        Defines whether the game is active or not
    sound : dictionary
        Contains all the sounds of the game
    pista : boolean
        Variable to track if a hint is available or not. Only one hint
        per game is allowed.

    '''
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
        '''
        Start the game: find a new word, and reset all variables.
        '''
        self.obj_palabra.buscar_palabra()
        self.reset_juego()
    
    def reset_juego(self):
        '''
        Reset all the variables to start the game.
        '''
        self.fallos = 0
        self.letras_acertadas = ''
        self.letras_falladas = ''
        self.active = True
        self.pista = True
        self.obj_letras_falladas.reset_letras()
        self.obj_dibujo.reset_dibujo()
        self.obj_palabra.reset_palabra()
        self.obj_teclado.reset_teclado()

    def final(self, win):
        '''
        Launch a popup a the end of the game.

        Parameters
        ----------
        win : boolean
            Indicates if the game is won or not. Popup text is
            adjusted depending on this.
        '''
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
        '''
        Check if the letter is in the word or not. If it is, show
        the letter in its place, and add to the self.letras_acertadas; 
        if it is not, increase the self.fallos and add the letter
        to the self.letras_falladas.

        Parameters
        ----------
        letra : string (1-char)
            Letter to be evaluated.

        '''
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
        '''
        Play final sound, before exiting the app
        '''
        self.sound['bye'].play()
        sleep(1.5)


    def dar_pista(self):
        '''
        Give a hint: show one of the letters. Only if this is
        the first time hint is requested.
        '''
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
    skin = NumericProperty(1)
    
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
    
    def cambiar_hombre(self):
        '''
        Change the skin used for the man (2 options possible).
        '''
        self.skin = self.skin % 2 + 1
        


class LetrasFalladas(BoxLayout):
    '''
    Area with the list of wrong letters. It shows initially only spaces (_),
    and as errors are made they are added to the shown string (self.fallo).
    
    Attributes
    ----------
    fallo : string
        String showing the wrong letters.
    '''
    fallo = StringProperty('_'*10)
    
    
    def reset_letras(self):
        '''
        Reset status to start a new game.
        '''
        self.fallo = '_'*10
    
    
    def anadir_letra(self, letra, fallos):
        '''
        Adds a letter to the list of wrong letters, in the position fallo

        Parameters
        ----------
        letra : string
            Letter to add
        fallos : int
            Number of errors. Determines the position of the letter.

        '''
        self.fallo = replace_letter(self.fallo, fallos-1, letra)



class PalabraLetras(BoxLayout):
    '''
    This is the area of the screen that shows the word to be found.
    
    Attributes
    ----------
    actual : string
        this is the word showing the letters found and not found
    palabra : string
        this is the word that needs to be found
    '''
    actual = StringProperty(' ')
    palabra = ' '
    
    
    def reset_palabra(self):
        '''
        Reset self.actual to all letters as '-'
        '''
        self.actual = '-'*len(self.palabra)
        
    def buscar_palabra(self):
        '''
        Find a new word. First load a word from the file, and then reset 
        self.actual to show all '-'.

        '''
        self.palabra = self.cargar_palabra()
        self.reset_palabra()
    
    def cargar_palabra(self):
        '''
        Find a word in form a file, an return it.

        Returns
        -------
        string
            Word chosen
        ''' 
        fullname = os.path.join(os.path.dirname(__file__), FICHERO_PALABRAS)
        with open(fullname, 'rt') as f:
            lista = [ line.rstrip('\n') for line in f ]
        
        return choice(lista)
    
    def anadir_letra(self, letra):
        '''
        Add a correct letter to the self.actual string. Find all appearences
        of the letter in self.palabra, and replace the character '-' by 
        the letter.

        Parameters
        ----------
        letra : string (char)
            Letter to be added
        '''
        pos = 0
        pos = self.palabra.find(letra)
        while pos != -1:
            self.actual = replace_letter(
                self.actual, pos, letra)
            pos = self.palabra.find(letra, pos+1)


class Menu(BoxLayout):
    '''
    This is the menu window at the top. All coding is in kv file
    '''
    pass


class Teclado(GridLayout): 
    '''
    The keyboard area, showing all the keys. It controls when keys are 
    pressed, and the skin to use for keyboard.
    
    Attributes
    ----------
    skin : string
        Skin to be used.
    '''
    skin = 'teclado1'
    
    def __init__(self, **kwargs):
        super(Teclado, self).__init__(**kwargs)
        self.crear_teclas()
    
    def crear_teclas(self):
        '''
        Create all keys for the keyboard
        '''
        for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
            name = letra if letra != 'Ñ' else 'N2'
            self.add_widget(Tecla(letra=letra, filename=name))

    def cambiar_teclado(self):
        '''
        Change the skin of the keyboard. Skins are a string formed by word 
        teclado plus a number, from 1 to 6.
        '''
        n = int(self.skin[-1])
        n = n % 6 + 1
        self.skin = self.skin[:-1] + str(n)
        
        for tecla in self.children:
            tecla.skin = self.skin
    
    def reset_teclado(self):
        '''
        Reset all keys, putting their disabled attribute to False.
        '''
        for tecla in self.children:
            tecla.disabled = False
    
    def pulsar_tecla(self, letra):
        '''
        Triggers a pulsation of a key.

        Parameters
        ----------
        letra : string (char)
            Key to be pulsed
        '''
        for tecla in self.children:
            if tecla.letra == letra:
                tecla.sound.play()
                tecla.pulsar()


class Tecla(Button):
    '''
    Logic for each of the keys of the keyboard.
    
    Attributes
    ----------
    letra : string (char)
        This is the letter that corresponds to the key
    sound : SoundLoader
        Sound to be played when key is pressed
    skin : string
        skin to be used
    filename : string
        filename of the key to be loaded. It's the same as letra, except for
        letter ñ, that uses the filename n2 to avoid issues with os.
    disabled : boolean
        Defines whether the key is disabled or not. Used to dim the image of
        the key.
    
    '''
    letra = StringProperty()
    sound = SoundLoader.load('audio/tecla.ogg')
    skin = StringProperty('teclado1')
    filename = StringProperty()
    disabled = BooleanProperty(False)
    
    def pulsar(self):
        '''
        Trigger the evaluar_letra method, and disable the letter, so it shows
        dimmer on the screen.

        '''
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


