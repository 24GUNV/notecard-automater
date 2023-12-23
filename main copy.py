import textwrap
from PIL import Image, ImageDraw, ImageFont
import csv
import emoji
import codecs

NOTE_HEIGHT = 2214
NOTE_WIDTH = 3322
NOTES_PER_PAGE = 8

max_line_width = 1616
line_spacing = 200

# Holiday font
holiday_font_path = 'fonts/HolidayFree.ttf'
holiday_font_size = 100
holiday_font = ImageFont.truetype(holiday_font_path, holiday_font_size)

emoji_font = ImageFont.truetype('fonts/Apple Color Emoji.ttc', 100)

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
    # for char in text:
    #     if char in emoji.UNICODE_EMOJI:
    #         unicode_char = convert_emoji_to_unicode(char)
    #         print(unicode_char)
    #         draw.text((x, y), unicode_char, font=emoji_font, fill=(0, 0, 0))
    #         x += font_size  # Adjust spacing for emojis
    #     else:
    draw.text((x, y), text, font=emoji_font, fill=(0, 0, 0))
    x += holiday_font.getsize(text)[0]/2

# Iterate through CSV data
for i, row in enumerate(data):
    if (i % 4 == 0 and i != 0):
        y += NOTE_HEIGHT
        x = 0

    # Save the image and start a new page
    if i % 8 == 0:
        x = 0
        y = 0

        if i != 0:
            pageCount += 1
            page.save(f"output/page{pageCount}.jpg")
            print(pageCount)

        page = Image.new(mode="RGB", size=(int(NOTES_PER_PAGE * NOTE_WIDTH / 2), int(NOTES_PER_PAGE * NOTE_HEIGHT / 4)), color=(255, 255, 255))

    img = Image.open('templates/high qual.png')

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Add Text to an image
    I1.text((2000, 1248), f"{row['Name of Sender:']}", fill=(0, 0, 0), font=holiday_font)
    I1.text((2116, 1698), f"{row['Recipient Name:']}", fill=(0, 0, 0), font=holiday_font)

    message = row['Note:']

    # Iterate through words and draw text on canvas
    # Initialize variables to keep track of the current position
    current_x = 607
    current_y = 597

    for line in textwrap.wrap(message, width=17):
        # Draw each character separately to handle emojis
        draw_text_with_emoji(I1, line, current_x, current_y, emoji_font, emoji_font=emoji_font)
        current_y += holiday_font_size  # Adjust spacing for emojis

    page.paste(img, (x, y))
    x += NOTE_WIDTH

else:
    pageCount += 1
    page.save(f"output/page{pageCount}.jpg")
    print(pageCount)
