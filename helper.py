import PIL
from PIL import Image

im = Image.open("templates/high qual.png")
im = im.resize((1328, 885))
im.save(f"templates/christmas card resized.png")