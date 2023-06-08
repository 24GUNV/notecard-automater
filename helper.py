import PIL
from PIL import Image

im = Image.open("note-card-template.jpg")
im = im.resize((400, 400))
im.save(f"note-card-template-resized.png")