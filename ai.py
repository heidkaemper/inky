#!/usr/bin/env python3

from os import path
from PIL import Image
from pathlib import Path
from datetime import date
from generator import Generator
from inky.inky_ac073tc1a import Inky

def show_ai():
    file_path = f'{Path(__file__).parent}/storage/{date.today()}.webp'

    # check if we have to generate a new image
    if not path.exists(file_path):
        try:
            image = Generator().generate()
            image.save(file_path, 'WEBP')
        except:
            print('Could not generate a new image')

    # use fallback image if needed
    if not path.exists(file_path):
        file_path = f'{Path(__file__).parent}/assets/images/fallback.png'

    # load image
    image = Image.open(file_path)

    # show image on inky
    display = Inky()
    display.set_image(image)
    display.show()
