from dotenv import load_dotenv
from PIL import Image, ImageOps, ImageFont, ImageDraw
from openai import OpenAI
from requests import get
from os import getenv

class Generator:
    def __init__(self):
        load_dotenv()

        self.openai_client = OpenAI(
            api_key = getenv('OPENAI_API_KEY')
        )

    def generate(self, phrase):
        self.phrase = phrase

        response = self.openai_client.images.generate(
            model='dall-e-3',
            prompt=self._get_prompt(),
            size='1792x1024',
            quality='standard',
            response_format='url',
        )

        image = Image.open(get(response.data[0].url, stream=True).raw)
        image = self._resize_image(image)
        image = self._draw_phrase(image)

        return image

    def _get_prompt(self):
        return f'create a humorous picture without text based on the phrase „{self.phrase}“. white background, in popart style. only use the following hex color codes to create the image: #000000 #ffffff #00ff00 #0000ff #ff0000 #ffff00 #ff8c00';

    def _resize_image(self, image):
        return ImageOps.pad(
            image=image,
            size=[800, 480],
            color='white',
            centering=[0.5, 0],
        )

    def _draw_phrase(self, image):
        font = ImageFont.truetype('assets/fonts/Oswald-Medium.ttf', 16)

        draw = ImageDraw.Draw(image)

        # at white rectangle at the bottom as text background
        draw.rectangle(
            xy=[0, 454, 800, 480],
            fill='white',
        )

        # calculate phrase width
        textlength = draw.textlength(
            text=self.phrase.upper(),
            font=font,
        )

        # write phrase
        draw.text(
            xy=[(800 - textlength) / 2, 454],
            text=self.phrase.upper(),
            fill='black',
            font=font,
        )

        return image
