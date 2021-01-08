from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "files/Skillbox ticket.jpg"
FONT_PATH = "files/Roboto-Regular.ttf"
FONT_SIZE = 20

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (330, 230)
EMAIL_OFFSET = (330, 270)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)

    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file
