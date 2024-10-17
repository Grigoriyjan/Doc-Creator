import json
import tkinter as tk
from tkinter import ttk

doc_types = ['Счет на ОПЛ', 'КП']
props = ["ИП Алапаев","Эмин и Ко"]

def draw_header(root):
    top_titles = ['Реквизиты','Документ', 'Накладная', 'Имя', 'сумма', 'дата']
    for index, title in enumerate(top_titles):
        label = ttk.Label(root, text=title)
        label.grid(row = 2, column= index, padx=60, pady=15)

def drawPastDocs(root):
    with open('app\data\JSON\docHistory.json','r', encoding="utf-8") as file:
        doc_list = json.load(file)['docs']
    
    draw_header(root)
    
    for i in range(len(doc_list)):
        common = doc_list[i][len(doc_list[i]) - 1]
        ttk.Label(root, text=doc_types[common['docType']]).grid(row=i + 3, column=1, padx=30, pady=15)
        ttk.Label(root, text=props[doc_list[i][0]]).grid(row=i + 3, column=0, padx=30, pady=15)
        for j in range(3):
            ttk.Label(root, text=doc_list[i][j + 1]).grid(row=i + 3, column=j + 2, padx=70, pady=15)
        date = common['date']
        ttk.Label(root, text=f"{date['currDay']}.{date['currMoth']}.{date['currYear']}").grid(row=i + 3, column=j + 3, padx=70, pady=15)
    