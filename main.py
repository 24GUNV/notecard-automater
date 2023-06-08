import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import csv

NOTE_HEIGHT = 400
NOTE_WIDTH = 400
NOTES_PER_PAGE = 8

# font = ImageFont.truetype('FreeMono.ttf', 65)

with open('messages.csv') as csvFile:
    data = list(csv.DictReader(csvFile, delimiter=","))
    
    x = 0
    y = 0

    pageCount = 0

    for i in range(0, len(data)):
        if (i % 4 == 0 and i != 0):
            y += NOTE_HEIGHT
            x = 0

        # Saves the image and starts a new page
        if (i) % 8 == 0:
            x = 0
            y = 0
            pageCount += 1

            if (i != 0):
                page.save(f"output/page{pageCount}.jpg")

            page = PIL.Image.new(mode="RGB", size=(int(NOTES_PER_PAGE * NOTE_WIDTH / 2), int(NOTES_PER_PAGE * NOTE_HEIGHT / 4)), color=(255, 255, 255))
    
        img = Image.open('note-card-template-resized.png')
        
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        # Add Text to an image
        I1.text((14, 56), f"Sender: {data[i]['Sender']}", fill=(0, 0, 0))
        I1.text((14, 73), f"Reciever: {data[i]['Reciever']}", fill=(0, 0, 0))
        I1.text((14, 90), f"Message: {data[i]['Message']}", fill=(0, 0, 0))
        
        # Display edited image
        # img.show()
        
        page.paste(img, (x, y))
        
        x += NOTE_WIDTH
        
    
    else:
        page.save(f"output/page{pageCount}.jpg")
