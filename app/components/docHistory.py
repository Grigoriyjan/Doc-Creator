import json
from tkinter import ttk

doc_types = ['Счет на ОПЛ', 'КП']
props = ["ИП Алапаев","Эмин и Ко"]

def draw_header(root):
    top_titles = ['Реквизиты','Документ', 'Накладная', 'Имя', 'сумма', 'дата']
    for index, title in enumerate(top_titles):
        ttk.Label(root, text=title).grid(row = 2, column= index, padx=60, pady=15)

def drawPastDocs(root):
    with open('app\data\JSON\docHistory.json', 'r', encoding="utf-8") as file:
        doc_list = json.load(file)['docs']
        draw_header(root)
        
        for i, doc in enumerate(doc_list):
            common = doc[-1]
            date = common['date']
            
            labels = [
                (doc_types[common['docType']], 1),
                (props[doc[0]], 0),
                (f"{date['currDay']}.{date['currMoth']}.{date['currYear']}", 5)
            ] + [(doc[j + 1], j + 2) for j in range(3)]
            print(labels)
            for text, col in labels:
                ttk.Label(root, text=text).grid(row=i + 3, column=col, padx=30, pady=15)
    