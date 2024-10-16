from components import pdfConf
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter as tk
import uiElems as ue


main_window = None

def on_checkbutton_toggle(var):
    var.set(0 if var.get() == 1 else 1)
    global checkBtnVar
    checkBtnVar = var.get()

docConfigArr = [
    [
        {'val':None, 'name':"Реквизит", 'width':35, 'type':2, 'props':["ИП Алапаев Комерческий Банк","Эмин и Ко Оптима", "ИП Алапаев Оптима Банк"]},
        {'val':None, 'name':"Номер накладной",'validate':'key', 'width':35,'type':1},
        {'val':None, 'name':"Имя клиента", 'validate':None,  'width':35,'type':1},
        {'val':None, 'name':"Конечная стоимость",'validate':'key', 'width':35,'type':1},
        {'val':None, 'name':"Количество товаров",'validate':'key', 'width':30,'type':1},
        {'val':None, 'name':"Поставить печать", 'width':30,'type':3, 'func': on_checkbutton_toggle},
    ],
    [
        {'val':None, 'name':"Реквизит", 'width':35, 'type':2, 'props':["ИП Алапаев","Эмин и Ко Оптима"]},
        {'val':None, 'name':"Номер накладной",'validate':'key', 'width':35,'type':1},
        {'val':None, 'name':"Предложение",'validate':None, 'width':35,'type':1},
        {'val':None, 'name':"Конечная стоимость",'validate':'key', 'width':35,'type':1},
        {'val':None, 'name':"Поставить печать", 'width':30,'type':3, 'func': on_checkbutton_toggle},
    ]
]

title = [
    "Счет на оплату",
    "Комерческое предложение"
]
docType = 0
checkBtnVar = 0

def configurePdf(docData):
    path = fd.askdirectory()
    data = []
    for index, item in enumerate(docData):
        try:
            data.append(item.get() if index > 0 else int(item.current()))
        except AttributeError:
            data.append(checkBtnVar)
    pdfConf.preparePdf(data, title[docType], docType, path, main_window)

def drawUi(r):
    docData = []
    index = 0
    for item in docConfigArr[docType]:
        index += 1
        docData.append(ue.drawInputs(root=r,r=index, data=item))
    createBtn = ttk.Button(r,command=lambda: configurePdf(docData), text="Создать")
    createBtn.grid(row=index + 1, column=2, padx=15, pady=15)

def Start(main_win):
    global main_window
    main_window = main_win
    root = tk.Tk()
    root.title(title[docType])
    root.geometry("400x500")
    root.iconbitmap('app\data\docCreatorIco.ico')
    drawUi(root)
    root.mainloop()


    