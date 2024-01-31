from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch


def generate_pdf(filename: str, catalog: dict):
    canvas = Canvas(filename, pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))
    xcenter = 4 * inch
    annotation = "Аннотация: " + catalog['annotation']
    count_strings = len(annotation) / 40
    canvas.setFont('FreeSansBold', 14)
    canvas.setFillColorCMYK(100, 0, 73, 1)
    canvas.drawCentredString(xcenter, 610, f"Входящий ДСП документ")
    canvas.setFont('FreeSans', 14)
    canvas.drawCentredString(xcenter, 580, f"Номер и дата: {catalog['date_number']}")
    if count_strings > 1:
        first = -60
        last = 0
        y_draw_string = 565
        for i in range(1, int(count_strings) + 2):
            first += 60
            last += 60
            y_draw_string -= 15
            canvas.drawCentredString(xcenter, y_draw_string, annotation[first:last])
    else:
        canvas.drawCentredString(xcenter, 530, annotation)
    #
    if int(catalog['page_cnt']) > 1:
        for i in range(1, int(catalog['page_cnt'])):
            canvas.showPage()
            canvas.drawString(150, 100, '')
    canvas.showPage()
    canvas.save()




    """
    canvas = Canvas(filename, pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    canvas.setFont('FreeSans', 16)
    canvas.drawString(150, 460, f"Входящий ДСП документ")
    canvas.drawString(150, 430, f"Аннотация: {catalog['annotation']}")
    canvas.drawString(150, 400, f"Дата и номер: {catalog['date_number']}")
    canvas.drawString(150, 490, f"ТЕСТ ТЕСТ ТЕСТ")
    print(f'{catalog["page_cnt"]}00')
    if int(catalog['page_cnt']) > 1:
        for i in range(1, int(catalog['page_cnt'])):
            canvas.showPage()
            canvas.drawString(150, 100, '')
    canvas.showPage()
    canvas.save()
    """