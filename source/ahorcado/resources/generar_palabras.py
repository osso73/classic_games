#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:45:41 2020

generar_palabras: genera una lista de palabras únicas a partir de un 
fichero de texto (libro, etc.). Lo almacena en un fichero, con una
palabra en cada línea. Este fichero será utilizado por el programa
principal para buscar palabras.

@author: osso73
"""

INPUT_FILE = 'spanish_book.txt'
OUTPUT_FILE = 'lista_palabras.txt'
PUNCTUATION = '\'",.-!?¿¡()[]'
ACCENTS = {
    'À': 'A',
    'È': 'E',
    'Ì': 'I',
    'Ò': 'O',
    'Ù': 'U',
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U',
    'Ï': 'I',
    'Ü': 'U',    
    }


def remove_accent(string):
    s = string
    for char, new_char in ACCENTS.items():
        if char in s:
            s = s.replace(char, new_char)
    return s


def remove_punctuation(word):
    w = word
    for char in PUNCTUATION:
        w = w.strip(char)
    return w


palabras = set()

with open(INPUT_FILE, 'rt', encoding='utf-8') as f:
    for line in f:
        words = line.rstrip('\n').upper().split()
        for w in words:
            w = remove_accent(w)
            w = remove_punctuation(w)
            if w.isalpha() and len(w) > 3 and len(w) < 20:
                palabras.add(w)
            
with open(OUTPUT_FILE, 'wt', encoding='utf-8') as f:
    for w in palabras:
        f.write(w + '\n')


