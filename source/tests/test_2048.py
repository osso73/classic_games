#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 20:44:48 2020

@author: osso73
"""

from twenty_fortyeight import main

class TestTile():        
    def test_calc_position(self):
        obj = main.Tile()
        obj.position = [2, 3]
        obj.tamano = 10
        pos = obj.calc_position()
        assert pos == (20+main.SPACING, 30+main.SPACING)
    
    def test_on_position(self):
        assert True
    
    def text_on_value(self):
        assert True


class TestBoard():        
    def test_attributes(self):
        obj = main.Board()
        assert obj.ventana == 0
        assert obj.win_score == 2048
        assert obj.score == 0
        assert obj.active_game == False
        assert obj.last_move == []
        assert obj._moving == False
        assert obj._moved_tile == False

    def test_change_win_score(self):
        obj = main.Board()
        obj.change_win_score()
        assert obj.win_score == 256
        obj.change_win_score()
        assert obj.win_score == 512
        obj.change_win_score()
        assert obj.win_score == 1024
    
    def test_start_game(self):
        obj = main.Board()
        obj.start_game()
        assert obj.score == 0
        assert len(obj.children) == 16
        
        non_empty = 0
        for tile in obj.children:
            if tile.value != 0:
                non_empty += 1
        assert non_empty == 2


