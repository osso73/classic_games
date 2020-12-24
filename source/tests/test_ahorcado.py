#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 20:44:48 2020

@author: osso73
"""

import pytest
from collections import namedtuple

from ahorcado import main

Point = namedtuple('Point', 'x y')


@pytest.mark.parametrize("original, letter, position, check", [
    ('potato', '!', 2, 'po!ato'),
    ('orange', 'x', 4, 'oranxe'),
    ('Xmas', 'X', 1, 'XXas'),
    ('this is a test', '3', 10, 'this is a 3est')])
def test_replace_letter_ok(original, letter, position, check):
    final = main.replace_letter(original, position, letter)
    assert final == check

def test_replace_letter_error():
    original = 'potato'
    letter = '!'
    position = 18
    with pytest.raises(IndexError):
        main.replace_letter(original, position, letter)

    original = 'potato'
    letter = '!!'
    position = 2
    with pytest.raises(Exception):
        main.replace_letter(original, position, letter)


class TestMainScreen():
    def test_reset_juego(self):
        obj = main.MainScreen()
        obj.pista = False
        obj.letras_acertadas = 'test'
        obj.letras_falladas = 'check'
        assert obj.active == False
        
        try:
            obj.reset_juego()
        except:
            pass
        
        assert obj.active == True
        assert obj.pista == True
        assert obj.letras_acertadas == ''
        assert obj.letras_falladas == ''
    
    def test_final(self):
        '''cannot be tested'''
        pass
    
    @pytest.fixture
    def mainscreen(self):
        # initialize PalabraLetras
        palabra = main.PalabraLetras()
        palabra.cargar_palabra()
        
        # initialize LetrasFalladas
        letras_falladas = main.LetrasFalladas()

        # initialize dibujo
        dibujo = main.Dibujo()
        
        # initialize Mainscreen
        obj = main.MainScreen()
        obj.active = True
        obj.letras_acertadas = ''
        obj.letras_falladas = ''
        obj.fallos = 0
        obj.obj_palabra = palabra
        obj.obj_letras_falladas = letras_falladas
        obj.obj_dibujo = dibujo
        
        return obj

        
    def test_evaluar_letra_ok(self, mainscreen):
        obj = mainscreen
        
        letters_wrong = [c for c in main.CARACTERES_VALIDOS 
                         if c not in obj.obj_palabra.palabra]
        
        for n, c in enumerate(letters_wrong[:5]):
            obj.evaluar_letra(c)
            assert obj.letras_falladas[-1] == c
            assert obj.fallos == n+1
        

    def test_evaluar_letra_error(self, mainscreen):
        obj = mainscreen
                
        for n, c in enumerate(obj.obj_palabra.palabra[:-1]):
            obj.evaluar_letra(c)
            assert obj.letras_acertadas[-1] == c


class TestDibujo():
    def test_anadir_dibujo(self):
        obj = main.Dibujo()
        assert obj.status == 'D'*10
        for n in range(1, len(obj.status)+1):
            obj.anadir_dibujo(n)
            assert obj.status == 'A'*n + 'D'*(10-n)
    
    def test_reset_dibujo(self):
        obj = main.Dibujo()
        obj.status = 'test'
        obj.reset_dibujo()
        assert obj.status == 'D'*10
    
    def test_cambiar_hombre(self):
        obj = main.Dibujo()
        assert obj.skin == 1
        obj.cambiar_hombre()
        assert obj.skin == 2
        obj.cambiar_hombre()
        assert obj.skin == 1


class TestLetrasFalladas():
    def test_reset_letras(self):
        obj = main.LetrasFalladas()
        obj.fallo = 'test'
        obj.reset_letras()
        assert obj.fallo == '_'*10
    
    def test_anadir_letra(self):
        obj = main.LetrasFalladas()
        letters = 'IHAVENOCL'
        for n, c in enumerate(letters):
            obj.anadir_letra(c, n+1)
            assert obj.fallo == letters[:n+1] + '_'*(10-(n+1))
    
class TestPalabraLetras():
    def test_reset_palabra(self):
        obj = main.PalabraLetras()
        obj.actual = 'test'
        obj.palabra= '12345'
        obj.reset_palabra()
        assert obj.actual == '-'*5
        assert len(obj.palabra) == len(obj.actual)
        
    def test_buscar_palabra(self):
        obj = main.PalabraLetras()
        obj.actual = 'test'
        obj.palabra= '12345'
        obj.buscar_palabra()
        assert obj.palabra != '12345'
        assert obj.palabra.isalpha()
        assert obj.palabra.isupper()
        assert 3 < len(obj.palabra) < 20
        assert obj.actual == '-'*len(obj.palabra)
        assert len(obj.palabra) == len(obj.actual)
        
    def test_cargar_palabra(self):
        obj = main.PalabraLetras()
        p = obj.cargar_palabra()
        assert p.isalpha()
        assert p.isupper()
        assert 3 < len(p) < 20
        
    def test_anadir_letra(self):
        obj = main.PalabraLetras()
        obj.palabra = 'IMPOSSIBLE'
        obj.reset_palabra()
        letters = 'IMPOSBLE'
        
        obj.anadir_letra('I')
        assert obj.actual == 'I-----I---'
        obj.anadir_letra('M')
        assert obj.actual == 'IM----I---'
        obj.anadir_letra('B')
        assert obj.actual == 'IM----IB--'
        obj.anadir_letra('S')
        assert obj.actual == 'IM--SSIB--'
        obj.anadir_letra('E')
        assert obj.actual == 'IM--SSIB-E'
        obj.anadir_letra('L')
        assert obj.actual == 'IM--SSIBLE'
        obj.anadir_letra('P')
        assert obj.actual == 'IMP-SSIBLE'
        obj.anadir_letra('O')
        assert obj.actual == 'IMPOSSIBLE'
    
class TestTeclado():
    def test_crear_teclas(self):
        obj = main.Teclado()
        obj.crear_teclas()
        widgets = [child.letra for child in obj.children]
        letters = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        for l in letters:
            assert l in widgets
        
        for wid in widgets:
            assert wid in letters
    
    def test_cambiar_teclado(self):
        obj = main.Teclado()
        name = 'teclado'
        for _ in [1, 2]:
            for n in range(6):
                assert obj.skin == f'{name}{n+1}'
                obj.cambiar_teclado()
    
    def test_reset_teclado(self):
        obj = main.Teclado()
        for tecla in obj.children:
            tecla.disabled = True
        obj.reset_teclado()
        for tecla in obj.children:
            assert tecla.disabled == False
        
    def test_pulsar_tecla(self):
        '''cannot be tested'''
        pass


class TestTecla():
    def test_pulsar(self):
        '''cannot be tested'''
        pass

