import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import csv
from textwrap import fill
from app import *

NOTE_HEIGHT = 400
NOTE_WIDTH = 400
NOTES_PER_PAGE = 8

root = tk.Tk()

# Provide the path to your image
image_path = "templates/note-card-template-resized.png"
app = ImageClickApp(root, image_path)

information = app.start_app()



max_line_width = information['Max Length per Line'][0]
line_spacing = information['2nd Message Line'][1] - information['1st Message Line'][1]

# Define fonts, text sizes, and text colors
font_path = 'fonts/FreeMono.ttf'
font_size_sender_receiver = 18
font_size_message = 14
text_color = (0, 0, 0)

sender_font = ImageFont.truetype(font_path, font_size_sender_receiver)
receiver_font = ImageFont.truetype(font_path, font_size_sender_receiver)
message_font = ImageFont.truetype(font_path, font_size_message)

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
        if i % 8 == 0:
            x = 0
            y = 0

            if i != 0:
                pageCount += 1
                page.save(f"output/page{pageCount}.jpg")

            page = PIL.Image.new(
                mode="RGB",
                size=(
                    int(NOTES_PER_PAGE * NOTE_WIDTH / 2),
                    int(NOTES_PER_PAGE * NOTE_HEIGHT / 4),
                ),
                color=(255, 255, 255),
            )

        img = Image.open('templates/note-card-template-resized.png')

        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        # Add Text to an image
        sender_text = f"Sender: {data[i]['Sender']}"
        receiver_text = f"Receiver: {data[i]['Receiver']}"
        message = data[i]['Message']

        # Calculate text bounding boxes
        sender_pos = information["Sender Line"]
        receiver_pos = information['Receiver Line']
        # sender_bbox = I1.textbbox(sender_pos, sender_text, font=sender_font)
        # receiver_bbox = I1.textbbox(receiver_pos, receiver_text, font=receiver_font)

        # Draw text on canvas
        I1.text(sender_pos, sender_text, fill=text_color, font=sender_font)
        I1.text(receiver_pos, receiver_text, fill=text_color, font=receiver_font)

        # Calculate bounding box for the message
        message_bbox = I1.textbbox(
            (14, 90),
            message,
            font=message_font,
        )        

        message_pos = information['1st Message Line']

        # Wrap and draw the message using textwrap
        wrapped_message = fill(message, width=max_line_width)
        I1.text(
            message_pos,
            wrapped_message,
            fill=text_color,
            font=message_font,
            spacing=line_spacing,
        )

        page.paste(img, (x, y))

        x += NOTE_WIDTH

    else:
        pageCount += 1
        page.save(f"output/page{pageCount}.jpg")
