from dotenv import load_dotenv
from PIL import Image, ImageOps, ImageFont, ImageDraw
from openai import OpenAI
from pathlib import Path
from requests import get
from os import getenv

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
            quality='hd',
            response_format='url',
        )

        image = Image.open(get(image_response.data[0].url, stream=True).raw)
        image = self._resize_image(image)
        image = self._draw_phrase(image)

        return image

    def _get_phrase_prompt(self):
        return 'describe a scene in a short phrase, between 20 and 75 characters long, that could be the start of a joke. something like „a horse walks into a bar“. without quotes.'

    def _get_image_prompt(self):
        return f'create a humorous picture with at least two subjects based on the phrase „{self.phrase}“. white background, pop art style and in landscape format'

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
