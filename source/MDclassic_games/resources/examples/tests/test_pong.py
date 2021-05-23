#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 20:44:48 2020

@author: osso73
"""

import pytest
from collections import namedtuple

from pong import main

Point = namedtuple('Point', 'x y')

class TestMainScreen():
    def test_initialisation(self):
        obj = main.MainScreen()
        skins = ['original', 'baseball', 'basket', 'billar', 'futbol', 
                 'golf', 'jupiter', 'saturno', 'skin1', 'skin2', 
                 'tenis', 'urano']
        
        assert obj.skin == 'original'
        assert obj.skin_list == skins

    def test_change_skin(self):
        obj = main.MainScreen()
        game = main.GameBoard()
        skins = ['baseball', 'basket', 'billar', 'futbol', 
                 'golf', 'jupiter', 'saturno', 'skin1', 'skin2', 
                 'tenis', 'urano']
        
        for skin in skins:
            try:
                obj.change_skin(game)
            except AttributeError:
                pass
            assert obj.skin == skin

class TestGameBoard():
    def test_serve_ball(self):
        '''cannot be tested'''
        assert True
    
    def test_on_touch_move(self):
        '''cannot be tested'''
        assert True

    def test_start_game(self):
        obj = main.GameBoard()
        obj.active = False
        try:
            obj.start_game()
        except AttributeError:
            pass
        assert obj.active == True
        
    def test_update(self):
        '''cannot be tested'''
        assert True

    def test_end_game(self):
        obj = main.GameBoard()
        obj.active = True
        try:
            obj.end_game()
        except AttributeError:
            pass
        assert obj.active == False

'''the rest of classes cannot be tested'''
