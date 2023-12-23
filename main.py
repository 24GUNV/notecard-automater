import textwrap
from PIL import Image, ImageDraw, ImageFont
import csv
import emoji
import codecs
import string

NOTE_HEIGHT = 885
NOTE_WIDTH = 1328
NOTES_PER_PAGE = 6

max_line_width = 646
line_spacing = 80

# Holiday font
holiday_font_path = 'fonts/HolidayFree.ttf'
holiday_font_size = 40
holiday_font = ImageFont.truetype(holiday_font_path, holiday_font_size)

normal_font = ImageFont.truetype("fonts/Symbola.ttf", 40)
emoji_font = ImageFont.truetype('fonts/Apple Color Emoji.ttc', 40)

# Read CSV using the csv module
with open('Sales.csv', 'r', encoding='utf-8') as csvFile:
    csv_reader = csv.DictReader(csvFile, delimiter=",")
    data = list(csv_reader)

x = 0
y = 0
pageCount = 0

def convert_emoji_to_unicode(text):
    return ''.join(codecs.encode(char, 'unicode_escape').decode('utf-8') if char in emoji.UNICODE_EMOJI else char for char in text)

def draw_text_with_emoji(draw, text, x, y, font_size, emoji_font):
    for char in text:
        if char in [' ']:
            x += draw.textlength(char, font=emoji_font)/4
        elif char in string.printable:
            draw.text((x, y), char, font=normal_font, fill=(0, 0, 0))
            x += draw.textlength(char, font=normal_font)
        else:
            unicode_char = convert_emoji_to_unicode(char)
            draw.text((int(x), int(y)), unicode_char, font=emoji_font, embedded_color=True)
            x += draw.textlength(unicode_char, font=emoji_font) 

# Iterate through CSV data
for i, row in enumerate(data):
    if (i % 3 == 0 and i != 0):
        y += NOTE_HEIGHT
        x = 0

    # Save the image and start a new page
    if i % 6 == 0:
        x = 0
        y = 0

        if i != 0:
            pageCount += 1
            page.save(f"output/page{pageCount}.jpg")
            print(pageCount)

        page = Image.new(mode="RGB", size=(int(NOTES_PER_PAGE * NOTE_WIDTH / 2), int(NOTES_PER_PAGE * NOTE_HEIGHT / 3)), color=(255, 255, 255))

    img = Image.open('templates/christmas card resized.png')

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Add Text to an image
    if row['Anonymous?:'] == "Yes":
        I1.text((845, 670), f"Anonymous", fill=(0, 0, 0), font=holiday_font)
    else: 
        I1.text((845, 670), f"{row['Name of Sender:']}", fill=(0, 0, 0), font=holiday_font)

    I1.text((800, 490), f"{row['Recipient Name:']}", fill=(0, 0, 0), font=holiday_font)
    I1.text((1010, 580), f"{row['Recipient HR:']}", fill=(0, 0, 0), font=holiday_font)

    message = row['Note:']

    # Iterate through words and draw text on canvas
    # Initialize variables to keep track of the current position
    current_x = 240
    current_y = 230

    for line in textwrap.wrap(message, width=15):
        # Draw each character separately to handle emojis
        draw_text_with_emoji(I1, line, current_x, current_y, emoji_font, emoji_font=emoji_font)
        current_y += holiday_font_size  # Adjust spacing for emojis

    page.paste(img, (x, y))
    x += NOTE_WIDTH

else:
    pageCount += 1
    page.save(f"output/page{pageCount}.jpg")
    print(pageCount)
