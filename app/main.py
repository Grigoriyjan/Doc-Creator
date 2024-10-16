import sys

sys.path.append('app\components')
sys.path.append('app')

from tkinter import Tk
from tkinter import ttk
from components import uiConf as uc
from components import docHistory as dh


max_docTypes = 2
doc_types = ['Счет на ОПЛ', 'КП']


main_window = Tk()
main_window.title("Document Creator V2")
main_window.geometry("1024x860")

main_window.iconbitmap('app\data\docCreatorIco.ico')

def prepareWindow(index):
    uc.docType = index
    uc.Start(main_window)

def updateList():
    dh.drawPastDocs(main_window)

updateList()

for index in range(max_docTypes):
    ttk.Button(main_window, text=doc_types[index], command=lambda i=index: prepareWindow(i)).grid(row=1, column=index, padx=15, pady=15)


main_window.mainloop()