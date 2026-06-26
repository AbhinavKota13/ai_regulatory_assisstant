import os
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

GENERATED_FOLDER = "generated"


def create_pdf(text):

    filename = f"{uuid.uuid4()}.pdf"

    path = os.path.join(GENERATED_FOLDER, filename)

    c = canvas.Canvas(path, pagesize=letter)

    width, height = letter

    y = height - 40

    for line in text.split("\n"):

        if y < 40:
            c.showPage()
            y = height - 40

        c.drawString(40, y, line[:95])

        y -= 15

    c.save()

    return path