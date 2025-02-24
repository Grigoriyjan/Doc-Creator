from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial-Thick', "app\data\\fonts\G_ari_bd.TTF"))
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def drawPDF(c, data):
    if data['type'] < 3 : 
        c.setFont(data['font'], data['font-size'])
    
    if data['type'] == 1:
        c.drawString(data['x'], data['y'], data['val'])
    elif data['type'] == 2:
        str_arr = data['arr'][data['val']]
        str_arr = str_arr.split('~')
        str_arr.reverse()
        for index, str in enumerate(str_arr):
            c.drawString(data['x'], data['y'] + index * data['gap'], str)
    elif data['type'] == 3:
        c.drawImage(data['val'], data['x'], data['y'],mask="auto")
    elif data['type'] == 4:
        if data['place'] == False:
            return
        sign =  data['arr'][data['val']] if data['val'] <= 1 else data['arr'][0]
        c.drawImage(sign['path'], data['x'], data['y'], sign['width'], sign['heigth'], mask="auto")
    elif data['type'] == 5:
        c.drawImage(data['val'], data['x'], data['y'])
        