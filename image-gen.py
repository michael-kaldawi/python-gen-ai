from time import sleep
import sys
import random
from io import BytesIO
import os
from openai import OpenAI
import webbrowser
import requests
from PIL import Image

SECRET_KEY = "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"

client = OpenAI(api_key=SECRET_KEY)

prompt_descriptor = ""

# """In a vast desert landscape, there is a cube. It is clear, glass, 5ft by 5ft, and a little smaller than a person. There is a ladder, made of light colored wood leaned up against the cube on the side and it reaches the top of the cube. There is a white horse with brown patches and it's standing next to the cube not moving. There are desert flowers - they are pink with spikey leaves and they are growing out of the sand. They are next to the horse - the horse is in between the flowers and the cube. A storm is not directly over the desert but is approaching it. it has big rain clouds and is blowing closer to the cube, horse, and flowers.
# """ # ADD .format(<scene>, <cube>, etc.)

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt_descriptor,
  size="1024x1024",
  quality="standard",
  n=1
)
image_url = response.data[0].url

webbrowser.open(image_url)

image = requests.get(image_url).content

f = open(str("img-" + random.randrange(1,10000000) + ".png"), 'wb')
f.write(image)
f.close()