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
    