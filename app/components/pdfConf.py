import re

import json
from num2words import num2words
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import subprocess
from createPdf import drawPDF

mothArr = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']

date = {
    'currDay': str(datetime.date.today().day),
    'currMoth': mothArr[int(datetime.date.today().month) - 1],
    'currYear': str(datetime.date.today().year)
}

kp_title = [
    {'title':'ИП Алапаев А.А.', 'chief':'Алапаев Адилет'},
    {'title':'ОсОО "Эмин и Ко"', 'chief':'Умуш Аскар'},
    {'title':'ИП Алапаев Оптима', 'chief':'Алапаев Адилет'},
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
    print(storage)
    data.extend([len(storage['docs']), date])
    storage['docs'].append(data)
    with open("app\data\JSON\docHistory.json", "w") as file:
        json.dump(storage, file, indent=4)
def fillData(data, docType):
    local_data = None 
    
    props = load_json_file('app\data\JSON\props.json')['props']
    save_doc(data, docType)
    if docType == 0:
        local_data = [
            {'font-size':13, 'font':'Arial-Thick', 'x':60, 'y':760, 'val':f'Счет на оплату №{data[1]} от {date["currDay"]} {date["currMoth"]} {date["currYear"]}г.', 'type': 1},
            {'font-size':13, 'font':'Arial', 'x':60, 'y':538, 'val':'Покупатель ', 'type':1},
            {'font-size':13, 'font':'Arial', 'x':60, 'y':563, 'val':'Склад ', 'type':1},
            {'font-size':13, 'font':'Arial', 'x':60, 'y':580, 'val':'Поставщик ', 'type':1},
            {'font-size':13, 'font':'Arial-Thick', 'x':150, 'y':580, 'val':data[0], 'type':2, 'arr':props, 'gap':18},
            {'font-size':13, 'font':'Arial-Thick', 'x':150, 'y':538, 'val':data[2], 'type':1},
            {'font-size':13, 'font':'Arial', 'x':80, 'y':170, 'val':f'Всего наименованний {data[4]}, на сумму {data[3]} сом', 'type':1},
            {'font-size':13, 'font':'Arial', 'x':80, 'y':150, 'val':f'{convert_number_to_words(data[3])} сом', 'type':1},
            {'x':60, 'y':750, 'val':'app\data\image\payCheckImages\Image_001.png', 'type':3, 'width':None, 'height':None},
            {'x':190, 'y':65, 'val':'app\data\image\payCheckImages\Image_003.png', 'type':3, 'width':None, 'height':None},
            {'font-size':13,'font':'Arial-Thick', 'x':80, 'y':70, 'val':'Руководитель                                                                       Бухгалтер','type':1},
            {'x':170, 'y':0, 'val':data[0], 'type':4, 'arr':sign_arr, 'place':data[5]}
        ]
    elif docType == 1:
        local_data = [
            {'x':100, 'y':720, 'val':'app\data\image\kpImages\emin.png', 'type': 3, 'width':140, 'height':55},
            {'font-size':15, 'font':'Arial-Thick', 'x':365, 'y':775, 'val':getTitle(data[0], 'title'), 'type': 1},
            {'font-size':10, 'font':'Arial', 'x':350, 'y':700, 'val':0, 'type':2, 'arr':[' г. Бишкек ул. Логвиненко 24/1~      ИНН 02207201510155~             https://emin.kg~           emin.ko@mail.ru~Тел: 0777 555 899, 0312 900 897 '], 'gap':15},
            {'x':85, 'y':670, 'val':'app\data\image\kpImages\Image_003.png', 'type':3, 'width':None, 'height':None},
            {'font-size':11, 'font':'Arial', 'x':85, 'y':655, 'val':f' «{date["currDay"]}» {date["currMoth"]}. {date["currYear"]} г.', 'type':1},
            {'font-size':11, 'font':'Arial', 'x':85, 'y':635, 'val':f'Исходящий документ №{data[1]}', 'type':1},
            {'font-size':15, 'font':'Arial-Thick', 'x':220, 'y':590, 'val':'Коммерческое предложение', 'type':1},
            {'font-size':11,'font':'Arial', 'x':120, 'y':560, 'val':f'{getTitle(data[0], "title")} выражает Вам свое уважение и предлагает рассмотреть Наше', 'type':1},
            {'font-size':11,'font':'Arial', 'x':85, 'y':540, 'val':f'предложение по реализации {data[2]}:', 'type':1},
            {'font-size':11,'font':'Arial', 'x':120, 'y':200, 'val':f'Итого настоящего коммерческого предложения составило: {data[3]}', 'type':1},
            {'font-size':11,'font':'Arial', 'x':85, 'y':180, 'val':f'({convert_number_to_words(data[3])}) сом', 'type':1},
            {'font-size':11,'font':'Arial', 'x':90, 'y':70, 'val':'С уважением,', 'type':1},
            {'font-size':11,'font':'Arial', 'x':90, 'y':55, 'val':getTitle(data[0], "chief"), 'type':1},
            {'x':200, 'y':0, 'val':data[0], 'type':4, 'arr':sign_arr, 'place':data[4]}
            
        ]
    return local_data
def getTitle(i, which):
    return kp_title[i][which]

def preparePdf(data, docName, docType,path):
    path = path + name_pdf(data, docName, docType) 
    c = canvas.Canvas(path, pagesize=A4)
    data = fillData(data, docType)
    
    
    
    for item in data:
        drawPDF(c, item)
    
    c.save()    
    c.showPage()
    open_pdf(path)
    

    