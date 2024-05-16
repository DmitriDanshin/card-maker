from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def create_card(c, x, y, title, image_path, description):
    card_width, card_height = 58 * mm, 88 * mm
    padding = 5 * mm
    title_height = 10 * mm
    image_height = (card_height - title_height - padding - padding) / 2

    c.rect(x, y, card_width, card_height)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + padding, y + card_height - padding - 12, title)

    c.line(
        x + padding,
        y + card_height - padding - 14,
        x + card_width - padding,
        y + card_height - padding - 14,
    )

    try:
        image = Image.open(image_path)
        image_width, image_height_original = image.size
        aspect = image_width / image_height_original
        image_draw_height = image_height
        image_draw_width = image_draw_height * aspect
        if image_draw_width > card_width - 2 * padding:
            image_draw_width = card_width - 2 * padding
        c.drawImage(
            ImageReader(image),
            x + (card_width - image_draw_width) / 2,
            y + card_height - padding - title_height - image_draw_height,
            image_draw_width,
            image_draw_height,
        )
    except Exception as e:
        print(f"Error loading image: {e}")

    text_y_position = y + padding
    text_x_position = x + padding
    text_width = card_width - 2 * padding
    text_height = image_height - padding

    styles = getSampleStyleSheet()
    description_style = styles["BodyText"]
    description_style.fontSize = 10
    description_style.leading = 12
    description_style.alignment = 0

    description_paragraph = Paragraph(description, description_style)
    description_height = description_paragraph.wrap(text_width, text_height)[1]

    while description_height > text_height and description_style.fontSize > 6:
        description_style.fontSize -= 1
        description_style.leading -= 1
        description_paragraph = Paragraph(description, description_style)
        description_height = description_paragraph.wrap(text_width, text_height)[1]

    description_paragraph.drawOn(c, text_x_position, text_y_position)


def create_pdf(cards, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    card_width, card_height = 58 * mm, 88 * mm
    spacing = 10 * mm

    cards_per_row = 3
    cards_per_column = 3
    cards_per_page = cards_per_row * cards_per_column

    x_start = (page_width - (cards_per_row * (card_width + spacing) - spacing)) / 2
    y_start = (page_height - (cards_per_column * (card_height + spacing) - spacing)) / 2

    for i, card in enumerate(cards):
        row = (i % cards_per_page) // cards_per_row
        col = (i % cards_per_page) % cards_per_row
        x = x_start + col * (card_width + spacing)
        y = y_start + row * (card_height + spacing)
        create_card(c, x, y, card["title"], card["image_path"], card["description"])

        if (i + 1) % cards_per_page == 0:
            c.showPage()

    if len(cards) % cards_per_page != 0:
        c.showPage()

    c.save()


# cards = [
#     {
#         "title": "Card 1",
#         "image_path": r"C:\Users\Dmitri\Downloads\week7_1100.jpg",
#         "description": "Description of card 1",
#     },
# ]

cards = []

create_pdf(cards, "cards.pdf")
