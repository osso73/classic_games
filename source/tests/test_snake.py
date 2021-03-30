#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:45:54 2020

@author: osso73
"""

import os
import pytest
import time

from snake import main


class TestMainScreen():
    pass


class TestGameBoard():
    
    def test_button_size(self):
        game = main.GameBoard()
        idx = main.GRID_SIZES.index(game.size_snake)
        
        for n in main.GRID_SIZES[idx:] + main.GRID_SIZES[:idx]:
            assert game.size_snake == n
            game.button_size()


    def test_button_speed(self):
        game = main.GameBoard()
        idx = main.SPEED_FACTORS.index(game.speed_factor)
        
        for n in main.SPEED_FACTORS[idx:] + main.SPEED_FACTORS[:idx]:
            assert game.speed_factor == n
            game.button_speed()
    
    
    @pytest.mark.parametrize('x, y, j', [
        (320, 240, 10), (820, 540, 25), (300, 300, 5)
        ])
    def test_set_size(self, x, y, j):
        parent = main.Widget()
        game = main.GameBoard()
        parent.add_widget(game)
        parent.size = x, y
        game.size_snake = j
        game.set_size()
        
        pix = int(0.9 * min(x,y) / j)
        n = int(0.9 * x / pix)
        m = int(0.9 * y / pix)
        
        # assert game.size_grid == [n-1, m-1]
        assert game.size_pixels == pix
        assert game.size == [n*pix, m*pix]
        
    
    @pytest.mark.skip
    def test_start_game_reset(self):
        '''
        cannot be tested because Food is defined with grid variable in 
        kv file
        '''
        parent = main.Widget()
        game = main.GameBoard()
        parent.add_widget(game)
        parent.size = 1920, 1080
        
        game.snake_parts = [3,6,8,1,5,3,2]
        game.score = 28
        game.start_game()
        assert game.score == 0
        assert len(game.snake_parts) == 4
        for part in game.snake_parts:
            assert isinstance(part, [SnakeHead, SnakePart])
        

    @pytest.mark.skip
    def test_start_game_erase(self):
        pass
    
    @pytest.mark.skip
    def test_start_game_new_snake(self):
        pass
    
    @pytest.mark.skip
    def test_start_game_activation(self):
        pass



