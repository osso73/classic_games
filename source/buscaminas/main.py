#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:22:18 2020

@author: osso73
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    BooleanProperty
)

import os
from time import time
from random import shuffle


IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images
DOUBLE_TAP = 0.3  # seconds to wait to evaluat if double-tap is clicked

class Field(GridLayout):
    '''
    This is the field where all mines are distributed.
    
    Attributes
    ----------
    columnas : NumericProperty
        Number of columns of the field
    mines : NumericProperty
        Number of mines
    '''
    columnas = NumericProperty(9)
    mines = NumericProperty(0)
    time = NumericProperty(0)
    game_active = False
    
    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)
        self._start_time = 0
        Clock.schedule_interval(self.tick, 0.1)
        
    def start_game(self):
        '''
        Start a new game: reset score and timer, rebuild the field.
        '''
        self.mines = 10
        self.clear_widgets()
        self.distribute_mines()
        self.find_adjacent_mines()
        self.game_active = True
        self._start_time = time()

    def tick(self, *args):
        '''
        Update timer. This function is called every 0.1s
        '''
        if self.game_active:
            self.time = int(time() - self._start_time)
                
    def distribute_mines(self):
        '''
        Create a field with mines distributed randomly. The number of mines 
        is defined by mines attribute.
        '''
        areas = [9]*self.mines + [0]*(self.columnas**2 - self.mines)
        shuffle(areas)
        
        n=0
        for i in range(self.columnas):
            for j in range(self.columnas):
                self.add_widget(Area(posicion=[j, i], value=areas[n]))
                n += 1
    
    def find_adjacent_mines(self):
        '''
        For each area, find the number of adjacent mines, and establish it
        as its value. 
        '''
        for area in self.children:
            if area.value != 9:  # skip if area is a bomb
                neighbours = self.find_neighbours(area.posicion)
                for n in neighbours:
                    if n.value == 9:
                        area.value += 1
    
    def find_neighbours(self, p):
        '''
        Given a position p, return a list with all neighbour areas.

        Parameters
        ----------
        p : list
            Coordinates of the position of the tile in the Field.

        Returns
        -------
        ret : list
            List of tiles that are neighbours to tile in position p.

        '''
        ret = list()
        for child in self.children:
            if child.posicion != list(p):
                i, j = child.posicion
                if (p[0]-1 <= i <= p[0]+1) and (p[1]-1 <= j <= p[1]+1):
                    ret.append(child)
        
        return ret
    
    def check_uncover(self, area):
        '''
        Check if the game has finished, or the last uncovered has 0 adjacent 
        mines. If any of these sitations is true, trigger actions.
        
        This method is triggered every time an area is uncovered.

        Parameters
        ----------
        area : Area
            Area where the last action has taken place.

        '''
        if area.value == 9:
            # game lost
            self.game_lost()
        if not area.value:
            # 0 adjacent mines
            self.no_adjacent_mines(area)
        
        if self.all_discovered():
            # game won
            self.game_won()
    
    
    def all_discovered(self):
        '''
        Check if all mines have been flagged, and all non-mines uncovered.

        Returns
        -------
        Boolean.
            True if all mines are flagged and non-mines uncovered. False 
            otherwise

        '''
        uncovered = [ a for a in self.children if (a.value != 9 and 
                                                   not a.uncovered) ]
        bombs_without_flag = [ a for a in self.children if (a.value == 9 and 
                                                            not a.flag) ]

        if not len(uncovered) and not len(bombs_without_flag):
            return True
        else:
            return False
        
        
    def game_lost(self):
        '''
        When game is lost, show all mines and change the face of button.
        '''
        self.game_active = False
        self.parent.ids.start_button.change_face('lost')
        for area in self.children:
            if area.flag and area.value != 9:
                area.set_show(name='wrong')
            elif area.value == 9 and not area.flag:
                area.uncovered = True
    
    def game_won(self):
        '''
        When game is won, a popup is shown.
        '''
        self.game_active = False
        self.parent.ids.start_button.change_face('won')
    
    def no_adjacent_mines(self, area):
        '''
        Uncover all adjacent areas.
        
        Parameters
        ----------
        area : Area
            Area which has a value of 0
        '''
        neighbours = self.find_neighbours(area.posicion)
        for neighbour in neighbours:
            neighbour.uncover()
    
    def open_adjacent(self, area):
        '''
        If area has the same number of flagged neighbours as mines, uncover 
        all the other adjacent areas.
        
        This method is triggered when clicking on an uncovered aera.

        Parameters
        ----------
        area : Area
            Area around which we need to open the uncovered areas.

        '''
        if 0 < area.value < 9:
            neighbours = self.find_neighbours(area.posicion)
            flagged = [n for n in neighbours if n.flag]
            if len(flagged) == area.value:
                not_flagged = [n for n in neighbours if not n.flag]
                for tile in not_flagged:
                    tile.uncover()



class Area(Label):
    '''
    This class refers to each of the tiles in the field.

    Attributes
    ----------
    value : NumericProperty
        Value of the area. Usually a number showing the mines adjacent to this
        tile. A value of -1 means there is a bomb in the area.
    posicion : ListProperty
        Coordinates (i, j) of the tile in the field.
    show : StringProperty
        Name of the image that is shown by the tile
    uncovered : BooleanProperty
        If the tile has been uncovered or not. This defines what image is 
        shown.
    flag : BooleanProperty
        If the tile has a flag or not.

    '''
    value = NumericProperty(0)
    posicion = ListProperty()
    show = StringProperty()
    uncovered = BooleanProperty(False)
    flag = BooleanProperty(False)
    _current_touch = None
    
    def __init__(self, **kwargs):
        super(Area, self).__init__(**kwargs)
        self.set_show()
    
    def set_show(self, name=None):
        '''
        Evaluate the different flags (flag, uncovered) and define what image
        should be shown on the tile.
        '''
        
        if name:
            file = f'{name}.jpg'
        else:
            if self.uncovered:
                file = f'{self.value}.jpg'
            else:
                if self.flag:
                    file = 'bandera.jpg'
                else:
                    file = 'covered.jpg'
        
        self.show = os.path.join(IMAGES, file)
    
    def on_uncovered(self, *args):
        '''
        Any change on the flag triggers the re-evaluation of the flags to 
        show the appropriate image on the tile.
        '''
        self.set_show()
        self.parent.check_uncover(self)
    
    def on_flag(self, *args):
        '''
        Any change on the flag triggers the re-evaluation of the flags to 
        show the appropriate image on the tile.
        '''
        self.set_show()
        change = -1 if self.flag else 1
        self.parent.mines += change
        if self.parent.all_discovered():
            self.parent.game_won()
    
    def switch_flag(self, *args):
        '''
        Switch the flag boolean, and decrease mines counter.
        '''
        self.flag = not self.flag
        
    def uncover(self, *args):
        '''
        Uncover mine, if not uncovered. And check if end of game or 0 bombs, 
        to uncover other adjacent areas.
        '''
        if not self.uncovered and not self.flag:
            self.uncovered = True
        
                
    def on_touch_down(self, touch):
        '''
        Depending on the value of the flag button, trigger the switch_flag() 
        or uncover() methods.
        '''
        if self.collide_point(*touch.pos) and self.parent.game_active:
            if self.uncovered:
                self.parent.open_adjacent(self)
            elif hasattr(touch, 'button') and touch.button == 'right':
                self.switch_flag()
            elif self.parent.parent.ids.flag_button.option == 'bandera':
                self.switch_flag()
            elif self.parent.parent.ids.flag_button.option == 'covered':
                self.uncover()

class StartButton(Label):
    '''
    The button to start the game. This class controls the image to use, and
    the action.
    
    Attributes
    ----------
    button_face: StringProperty
        Name of the image to be shown
    '''
    button_face = StringProperty()
    
    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)
        self.change_face('standard')
    
    def on_touch_down(self, touch):
        '''
        Change the face of button when it's pressed.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.change_face('press')
            return True
    
    def on_touch_up(self, touch):
        '''
        Trigger the start of the game, and change back the button face.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.change_face('standard')
            self.parent.parent.ids.field.start_game()
            return True
    
    def change_face(self, face):
        '''
        Change the face of the button that is shown.

        Parameters
        ----------
        face : string
            Can be one of the 4 options: 'lost', 'press', 'standard', 'won'.

        '''
        if face not in ['lost', 'press', 'standard', 'won']:
            raise ValueError("Face incorrect")
        
        filename = f'{face}.png'
        self.button_face = os.path.join(os.path.dirname(__file__), 
                                        'images', filename)

        
class MenuButton(Label):
    '''
    To control behaviour of flag button in the menu.
    
    Attributes
    ----------
    button_face: StringProperty
        Name of the image to be shown
    option: StringProperty
        Option selected. Can be any of the following: 'bandera', 'covered'
    '''
    button_face = StringProperty()
    option = StringProperty()
    options = ListProperty()
        
    def on_option(self, *args):
        '''
        When option changes, generate the name of the image to be shown.
        '''
        filename = f'{self.option}.jpg'
        self.button_face = os.path.join(os.path.dirname(__file__), 
                                        'images', filename)

    def on_touch_down(self, touch):
        '''
        Change the face of button when it's pressed.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.button_face = os.path.join(os.path.dirname(__file__), 
                                            'images', 'hover.jpg')
            return True

    def on_touch_up(self, touch):
        '''
        Trigger the change of option.

        Parameters
        ----------
        touch : touch event
            Has the coordinates of the touch.

        Returns
        -------
        bool
            True, in case the touch point was within the widget.

        '''
        if self.collide_point(*touch.pos):
            self.change_option()
            return True
    
    def change_option(self):
        '''
        Change the option selected, cycling through the options available: 
        'bandera', 'covered'
        '''
        ind = self.options.index(self.option)
        ind = (ind+ 1) % len(self.options)
        self.option = self.options[ind]


class Indicator(Label):
    '''
    For the indicators of mines and time.
    '''
    pass

class MainScreen(BoxLayout):
    '''
    This class organizes the main screen, with the menu on top, and the field
    below.
    '''
    pass


class BuscaminasApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (375, 800)
    BuscaminasApp().run()

