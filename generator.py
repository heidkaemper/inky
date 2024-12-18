#!/usr/bin/env python3

from dotenv import load_dotenv
from PIL import Image, ImageOps, ImageFont, ImageDraw
from openai import OpenAI
from pathlib import Path
from requests import get
from os import getenv
from random import choice

class Generator:
    def __init__(self):
        load_dotenv()

        self.openai_client = OpenAI(
            api_key = getenv('OPENAI_API_KEY')
        )

    def generate(self):
        chat_response = self.openai_client.chat.completions.create(
            messages=[{
                'role': 'user',
                'content': self._get_phrase_prompt(),
            }],
            model='gpt-4o-mini',
        )

        self.phrase = chat_response.choices[0].message.content

        image_response = self.openai_client.images.generate(
            model='dall-e-3',
            prompt=self._get_image_prompt(),
            size='1792x1024',
            quality='standard',
            response_format='url',
        )

        image = Image.open(get(image_response.data[0].url, stream=True).raw)
        image = self._resize_image(image)
        image = self._draw_phrase(image)

        return image

    def _get_phrase_prompt(self):
        options = \
        [
            'which special holiday or curious event is today? if there are several answers, try to choose the funniest one and then only give that one. the answer should be between 15 and 90 characters long.',
            'describe a scene with at least two characters. the description should be between 15 and 90 characters long.',
            'generate a fun fact that is between 15 and 90 characters long.',
        ]

        return choice(options)

    def _get_image_prompt(self):
        return f'create a humorous picture without text based on the phrase „{self.phrase}“. white background, pop art style and in landscape format.'

    def _resize_image(self, image):
        return ImageOps.pad(
            image=image,
            size=[800, 480],
            color='white',
            centering=[0.5, 0],
        )

    def _draw_phrase(self, image):
        font = ImageFont.truetype(f'{Path(__file__).parent}/assets/fonts/Oswald-Medium.ttf', 16)

        draw = ImageDraw.Draw(image)

        # at white rectangle at the bottom as text background
        draw.rectangle(xy=[0, 454, 800, 480], fill='white')
        draw.line(xy=[0, 454, 800, 454], fill='black')

        # calculate phrase width
        textlength = draw.textlength(text=self.phrase.upper(), font=font)

        # write phrase
        draw.text(
            xy=[(800 - textlength) / 2, 454],
            text=self.phrase.upper(),
            fill='black',
            font=font,
        )

        return image
