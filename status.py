#!/usr/bin/env python3

from os import popen
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from inky.inky_ac073tc1a import Inky

# get network status
ip = popen('ifconfig wlan0 | grep "inet " | cat').readline().strip()
ssid = popen('iwconfig wlan0 | grep "ESSID:" | cat').readline().strip('wlan0').strip()
quality = popen('iwconfig wlan0 | grep "Link Quality" | cat').readline().strip('wlan0').strip()

# create image instance
image = Image.new('RGB', (800, 480))
draw = ImageDraw.Draw(image)

# headline
draw.text(
    xy = [18, 16],
    text = 'Inky Status',
    fill = 'white',
    font = ImageFont.truetype(f'{Path(__file__).parent}/assets/fonts/Oswald-Medium.ttf', 36),
)

# status
draw.multiline_text(
    xy = [18, 84],
    text = f'{ip}\n{ssid}\n{quality}',
    fill = 'white',
    font = ImageFont.truetype(f'{Path(__file__).parent}/assets/fonts/Oswald-Medium.ttf', 20),
    spacing = 12,
)

# show status on inky
display = Inky()
display.set_image(image, saturation=0)
display.show()
