#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:50:49 2020

cut_images.py: will search for all images in the current folder (.jpg and
.png) and for each of them will create a theme: it creates a folder with
the same name as image, moves the image to the folder, and it creates
3 subfolders named 3, 4, 5 with the cropped image for each of the sizes.

Note: image is expected to be square. The program resizes it to (512, 512),
so if not square it will be distorted.

@author: oriol
"""


import sys, os, shutil
from PIL import Image



def cut_image(image, sizes):
    """
    Cut the image provided in different sizes. Size means the image is 
    cropped in size x size squares.

    Parameters
    ----------
    image : Image
        Image object with the image to be cut
    sizes : list of integers
        the different sizes that the image needs to be cut into.

    Returns
    -------
    None.

    """
    image = image.resize((512, 512))
    for num in sizes:
        cut_size(image, num)


def cut_size(image, num):
    """
    Cut the image in sub-images, and save them into a folder named num.

    Parameters
    ----------
    image : Image
        Image object with the image to be cut
    num : int
        number of images to be created (i.e. it creates num x num images)

    Returns
    -------
    None.

    """
    w, h = image.size
    x_side = w / num
    y_side = h / num
    os.makedirs(str(num))
    for i in range(num):
        for j in range(num):
            box = (i*x_side, j*y_side, (i+1)*x_side, (j+1)*y_side)
            name = i + j * num + 1
            cropped = image.crop(box)
            filename = os.path.join(str(num), str(name)+'.jpg')
            cropped.save(filename)

def main():
    image_list = os.listdir()
    for image in image_list:
        name, ext = os.path.splitext(image)
        if ext in ['.jpg', '.png']:
            os.makedirs(name)
            shutil.move(image, os.path.join(name, image))
            os.chdir(name)
            im = Image.open(image)
            cut_image(im, [3, 4, 5])
            os.chdir('..')

if __name__ == '__main__':
    main()
