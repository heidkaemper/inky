#!/usr/bin/env python3

from PIL import Image
from pathlib import Path
from glob import glob
from random import choice
from inky.inky_ac073tc1a import Inky

def show_comic():
    # get all available comics
    files = glob(f'{Path(__file__).parent}/assets/images/comics/*.webp')

    # pick random file
    file_path =choice(files)

    # load image
    image = Image.open(file_path)

    # show image on inky
    display = Inky()
    display.set_image(image, saturation=0)
    display.show()
