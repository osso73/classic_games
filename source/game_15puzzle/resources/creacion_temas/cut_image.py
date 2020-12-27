#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:50:49 2020

@author: oriol
"""

import sys, os, shutil
from PIL import Image



if len(sys.argv) < 2:
    print("Debes entrar un nombre de imagen a trocear.")
    print('Inténtalo otra vez.')
    exit(0)

im = Image.open(sys.argv[1])
im = im.resize((512, 512))
w, h = im.size

for num in [3,4,5]:
    os.makedirs(str(num))
    x_side = w / num
    y_side = h / num
    for i in range(num):
        for j in range(num):
            box = (i*x_side, j*y_side, (i+1)*x_side, (j+1)*y_side)
            name = i + j * num + 1
            cropped = im.crop(box)
            filename = os.path.join(str(num), str(name)+'.jpg')
            cropped.save(filename)
