import re

import json
import subprocess
import datetime
from docHistory import drawPastDocs
from num2words import num2words
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from createPdf import drawPDF

mothArr = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']

date = {
    'currDay': str(datetime.date.today().day),
    'currMoth': int(datetime.date.today().month),
    'currYear': str(datetime.date.today().year)
}

kp_title = [
    {'title':'ИП Алапаев А.А.', 'chief':'Алапаев Адилет'},
    {'title':'ОсОО "Эмин и Ко"', 'chief':'Умуш Аскар'},
]

sign_arr = [
    {
        'width':120,
        'heigth':120,
        'path':'app\data\image\sign_1.png'
    },
    {
        'width':150,
        'heigth':100,
        'path':'app\data\image\sign_2.png'
    }]

def load_json_file(path):
    with open(path,'r', encoding="utf-8") as file:
        return json.load(file)

def convert_number_to_words(number):
    try:
        words = num2words(number, lang='ru')
        words = words.capitalize()
        return words
    except ValueError:
        return "Неверный ввод. Пожалуйста, введите действительное число."

def open_pdf(file_path):
    try:
        subprocess.run(file_path, shell=True, timeout=10)
    except subprocess.TimeoutExpired:
        print('Процесс не завершился в течение указанного времени.')

def name_pdf(data,docName, docType):
    indexPull = [
        [1, 2, 4],
        [0, 1]
    ]
    string = docName
    string += kp_title[data[0]]['title']
    for i in indexPull[docType]:
        string += f'_{data[i]}'
    string = re.sub(r'[/\\"!@#$%^&*|+=,.:;?<>-«»\n]', "", string)
    string = string.replace(" ", "_")
    return '\ ' + string + '.pdf'

def save_doc(data, docType):
    storage = load_json_file('app\data\JSON\docHistory.json')
    common = {"date":date, "docType":docType}
    data.extend([len(storage['docs']), common])
    storage['docs'].append(data)
    with open("app\data\JSON\docHistory.json", "w") as file:
        json.dump(storage, file, indent=4)
        
def create_element(font_size, font, x, y, val, element_type, **kwargs):
    element = {'font-size': font_size, 'font': font, 'x': x, 'y': y, 'val': val, 'type': element_type}
    element.update(kwargs)
    return element

def fillData(data, docType, main_window):
    props = load_json_file('app\data\JSON\props.json')['props']
    save_doc(data, docType)
    local_data = []
    
    date_str = f'Счет на оплату №{data[1]} от {date["currDay"]} {mothArr[date["currMoth"] - 1]} {date["currYear"]}г.'
    
    if docType == 0:
        local_data.extend([
            create_element(13, 'Arial-Thick', 60, 760, date_str, 1),
            create_element(13, 'Arial', 60, 538, 'Покупатель ', 1),
            create_element(13, 'Arial', 60, 563, 'Склад ', 1),
            create_element(13, 'Arial', 60, 580, 'Поставщик ', 1),
            create_element(13, 'Arial-Thick', 150, 580, data[0], 2, arr=props, gap=18),
            create_element(13, 'Arial-Thick', 150, 538, data[2], 1),
            create_element(13, 'Arial', 80, 170, f'Всего наименованний {data[4]}, на сумму {data[3]} сом', 1),
            create_element(13, 'Arial', 80, 150, f'{convert_number_to_words(data[3])} сом', 1),
            create_element(None, None, 60, 750, 'app\data\image\payCheckImages\Image_001.png', 3),
            create_element(None, None, 190, 65, 'app\data\image\payCheckImages\Image_003.png', 3),
            create_element(13, 'Arial-Thick', 80, 70, 'Руководитель', 1),
            create_element(13, 'Arial-Thick', 430, 70, 'Бухгалтер', 1),
            create_element(None, None, 170, 0, data[0], 4, arr=sign_arr, place=data[5])
        ])
        
    elif docType == 1:
        local_data.extend([
            create_element(None, None, 100, 720, 'app\data\image\kpImages\emin.png', 3, width=140, height=55),
            create_element(15, 'Arial-Thick', 365, 775, getTitle(data[0], 'title'), 1),
            create_element(10, 'Arial', 350, 700, 0, 2, arr=[' г. Бишкек ул. Логвиненко 24/1~ ИНН 02207201510155~ https://emin.kg~ emin.ko@mail.ru~Тел: 0777 555 899, 0312 900 897 '], gap=15),
            create_element(None, None, 85, 670, 'app\data\image\kpImages\Image_003.png', 3),
            create_element(11, 'Arial', 85, 655, f' «{date["currDay"]}» {date["currMoth"]}. {date["currYear"]} г.', 1),
            create_element(11, 'Arial', 85, 635, f'Исходящий документ №{data[1]}', 1),
            create_element(15, 'Arial-Thick', 220, 590, 'Коммерческое предложение', 1),
            create_element(11, 'Arial', 120, 560, f'{getTitle(data[0], "title")} выражает Вам свое уважение и предлагает рассмотреть Наше', 1),
            create_element(11, 'Arial', 85, 540, f'предложение по реализации {data[2]}:', 1),
            create_element(11, 'Arial', 120, 200, f'Итого настоящего коммерческого предложения составило: {data[3]}', 1),
            create_element(11, 'Arial', 85, 180, f'({convert_number_to_words(data[3])}) сом', 1),
            create_element(11, 'Arial', 90, 70, 'С уважением,', 1),
            create_element(11, 'Arial', 90, 55, getTitle(data[0], "chief"), 1),
            create_element(None, None, 200, 0, data[0], 4, arr=sign_arr, place=data[4])
        ])
    
    drawPastDocs(main_window)
    return local_data

def getTitle(i, which):
    return kp_title[i][which]

def preparePdf(data, docName, docType,path, main_window):
    path = path + name_pdf(data, docName, docType) 
    c = canvas.Canvas(path, pagesize=A4)
    data = fillData(data, docType, main_window)
    for item in data:
        drawPDF(c, item)
    
    c.save()    
    c.showPage()
    open_pdf(path)
    

    