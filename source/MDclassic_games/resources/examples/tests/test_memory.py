#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:44:27 2020

@author: osso73
"""

import os
import pytest

from memory import main


class TestTapete():
    def test_load_images(self):
        temas = os.listdir(main.TEMAS)
        class app():
            class root():
                tema_actual = ''
        
        obj = main.Tapete()
        for tema in temas:
            app.root.tema_actual = tema
            images, back = obj.load_images(app)
            assert len(images) >= 20
            assert back.endswith('back.jpg')
    
    @pytest.mark.skip
    def test_start_game(self):
        '''cannot be tested'''
        pass
    
    @pytest.mark.parametrize('num_pairs, columns', 
                             zip(list(range(4, 21)), 
                                 [2] + [3]*5 + [4]*6 + [5]*5))
    def test_set_columns(self, num_pairs, columns):
        obj = main.Tapete()
        obj.set_columns(num_pairs)
        assert obj.columnas == columns
    
    @pytest.mark.skip
    def test_on_current_cards(self):
        '''cannot be tested'''
        pass
    
    
    @pytest.fixture
    def tapete_with_cards(self):
        def _method(num):
            class Card(main.Label):
                shown = main.BooleanProperty(False)
            obj = main.Tapete()
            for _ in range(num):
                obj.add_widget(Card())
            
            return obj
        
        return _method
    
    @pytest.mark.parametrize('num', list(range(4, 21)))
    def test_check_end_false(self, tapete_with_cards, num):
        obj = tapete_with_cards(num)        
        obj.check_end()
        assert True
                
    @pytest.mark.parametrize('num', list(range(4, 21)))
    def test_check_end_true(self, tapete_with_cards, num):
        obj = tapete_with_cards(num)
        for card in obj.children:
            card.shown = True
        
        # if all cards are shown, an error is raised by the function
        # when trying to play the sound
        with pytest.raises(AttributeError):
            obj.check_end()
    

class TestCarta():
    @pytest.mark.skip
    def test_click(self):
        '''cannot be tested'''
        pass
    
    @pytest.mark.skip
    def test_add_card_to_current(self):
        '''cannot be tested'''
        pass
    
    def test_turn(self):
        obj = main.Carta()
        for _ in range(2):
            assert obj.shown == False
            assert obj.show == obj.back
            obj.turn()
            assert obj.shown == True
            assert obj.show == obj.image
            obj.turn()


class TestMainScreen():
    @pytest.fixture
    def sound_list(self):
        return {'bye', 'ok', 'start', 'turn', 'end_game'}
    
    @pytest.fixture
    def theme_list(self):
        return os.listdir(main.TEMAS)
    
    def test_initialisation_sounds(self, sound_list):
        obj = main.MainScreen()
        assert sound_list == set(obj.sounds)
    
    def test_initialisation_theme(self, theme_list):
        obj = main.MainScreen()
        assert set(theme_list) == set(obj.lista_temas)

    def test_load_sounds(self, sound_list):
        obj = main.MainScreen()
        assert set(obj.load_sounds()) == sound_list    
    
    def test_cambiar_tema(self, theme_list):
        obj = main.MainScreen()
        for _ in range(2):
            for tema in theme_list:
                assert obj.tema_actual == tema
                obj.cambiar_tema()

        