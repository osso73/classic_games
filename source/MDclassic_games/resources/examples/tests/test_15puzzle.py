#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 19:35:26 2020

@author: osso73
"""

import os
import pytest
from random import shuffle

from game_15puzzle import main


class TestPuzzle():
    @pytest.mark.parametrize("size, result", [
        ((140, 300), 140), ((140, 320), 140), 
        ((260, 300), 260), ((260, 330), 260), 
        ((200, 360), 200), ((240, 360), 240), 
        ((200, 210), 200), ((240, 210), 210),
        ((200, 260), 200), ((320, 240), 240),
        ])
    def test_initialize_grid(self, size, result):
        parent = main.BoxLayout()
        parent.size = size
        obj = main.Puzzle()
        parent.add_widget(obj)
        obj.initialize_grid()
        assert obj.ventana == result
    
    @pytest.mark.skip
    def test_start_game(self):
        '''cannot be tested'''
        pass
    
    class Ficha(main.Label):
        '''
        Class to replace main.Ficha, so it can be used for testing
        '''
        name = main.StringProperty()
        posicion = main.ListProperty()

    def test_find_empty_ok(self):
        obj = main.Puzzle()
        title = list(range(1, 16)) + ['']
        shuffle(title)
        for i in range(16):
            obj.add_widget(self.Ficha(name=str(title[i])))
        
        empty_tile = obj.find_empty()
        assert empty_tile.name == ''
    
    def test_find_empty_error(self):
        obj = main.Puzzle()
        title = list(range(16))
        shuffle(title)
        for i in range(16):
            obj.add_widget(self.Ficha(name=str(title[i])))
        
        empty_tile = obj.find_empty()
        assert empty_tile == False
    
    @pytest.mark.parametrize("tamano", [3, 4, 5])
    def test_check_win_win(self, tamano):
        obj = main.Puzzle()
        obj.tamano = tamano
        title = list(range(1, tamano**2)) + ['']
        n = 0
        for i in range(tamano):
            for j in range(tamano):
                obj.add_widget(self.Ficha(name=str(title[n]),
                                          posicion=[j, i]))
                n += 1
        assert  obj.check_win() == True
        
    @pytest.mark.parametrize("tamano", [3, 4, 5])
    def test_check_win_not(self, tamano):
        obj = main.Puzzle()
        obj.tamano = tamano
        title = list(range(tamano**2-1, 0, -1)) + ['']
        n = 0
        for i in range(tamano):
            for j in range(tamano):
                obj.add_widget(self.Ficha(name=str(title[n]),
                                          posicion=[j, i]))
                n += 1
        assert  obj.check_win() == False
    
    @pytest.mark.skip
    def test_end_of_game(self):
        '''cannot be tested'''
        pass
    
    @pytest.mark.parametrize("game, result", [
        ([1, 8, 2, 
          '', 4, 3, 
          7, 6, 5], True),
        (['1', '8', '2', 
           '', '4', '3', 
          '7', '6', '5'], True),
        ([13,  2, 10,  3, 
           1, 12,  8,  4,
           5, '',  9,  6,
          15, 14, 11, 7], True),
        (['13',  '2', '10',  '3',
           '1', '12',  '8',  '4',
           '5',   '',  '9',  '6',
          '15', '14', '11',  '7'], True),
        ([ 6, 13,  7, 10,
           8,  9, 11, '',
          15,  2, 12,  5,
          14,  3,  1,  4], True),
        ])
    def test_is_solvable_true(self, game, result):
        obj = main.Puzzle()
        assert obj.is_solvable(game) == result

    @pytest.mark.parametrize("game, result", [
        ([ 3,  9,  1, 15,
          14, 11,  4,  6,
          13, '', 10, 12,
           2,  7,  8,  5], False),
        ])
    def test_is_solvable_false(self, game, result):
        obj = main.Puzzle()
        assert obj.is_solvable(game) == result

    @pytest.mark.parametrize("game, error", [
        ([1, 8, 2, 
          0, 4, 3, 
          7, 6, 5], ValueError),
        (['1', '8', '2', 
           '0', '4', '3', 
          '7', '6', '5'], ValueError),
        ([ 3,  5,  6, 10,
           2, 11,  7,  1,
           4, '',  8,  9], Exception),
        ])
    def test_is_solvable_error(self, game, error):
        obj = main.Puzzle()
        with pytest.raises(error):
            obj.is_solvable(game)


class TestMuestra():
    @pytest.fixture
    def muestra_with_parent(self):
        def _method(size=(300,200)):
            parent = main.BoxLayout()
            parent.size = size
            obj = main.Muestra()
            parent.add_widget(obj)
            return obj
        
        return _method
    
    @pytest.mark.parametrize("size, result", [
        ((140, 300), 140), ((140, 320), 140), 
        ((260, 300), 260), ((260, 330), 260), 
        ((200, 360), 200), ((240, 360), 240), 
        ((200, 210), 200), ((240, 210), 210),
        ((200, 260), 200), ((320, 240), 240),
        ])
    def test_initialize_grid(self, muestra_with_parent, size, result):
        obj = muestra_with_parent(size)
        obj.initialize_grid()
        assert obj.ventana == result
    
    def test_load_tema(self, muestra_with_parent):
        obj = muestra_with_parent()
        for n in range(3):
            tam = n+3
            obj.tamano = tam
            obj.load_tema()
            assert obj.cols == tam
            assert len(obj.children) == tam**2
            children_names = set()
            for child in obj.children:
                assert type(child) == main.FichaMuestra
                children_names.add(child.name)
            
            assert children_names == {str(c) for c in range(1, tam**2+1)}
        
    
    def test_cambiar_tema(self, muestra_with_parent):
        obj = muestra_with_parent()
        dir_temas = os.path.join('game_15puzzle', main.TEMAS)
        temas = os.listdir(dir_temas)
        i = temas.index('numeros')
        temas = temas[i:] + temas[:i]
        for _ in [1, 2]:
            for t in temas:
                assert obj.tema == t
                obj.cambiar_tema()
    
    def test_cambiar_tamano(self, muestra_with_parent):
        obj = muestra_with_parent()
        tamanos = [3, 4, 5]
        for _ in [1, 2]:
            for t in tamanos:
                assert obj.tamano == t
                obj.cambiar_tamano()

@pytest.mark.skip
class TestFicha():
    '''cannot be tested, as __init__ contains app statement'''
    pass


class TestMainScreen():
    @pytest.fixture
    def sound_list(self):
        return {'bye', 'ok', 'start', 'move', 'end_game'}
    
    def test_initialisation(self, sound_list):
        obj = main.MainScreen()
        assert sound_list == set(obj.sounds)
    
    def test_load_sounds(self, sound_list):
        obj = main.MainScreen()
        assert set(obj.load_sounds()) == sound_list
        