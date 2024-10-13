import tkinter as tk
from tkinter import ttk

def validate_input(P):
    # Проверка, что введенный текст - целое число
    try:
        int(P)
        return True
    except ValueError:
        return False

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def drawInputs(root,r,data):
    tkInput = None
    label = ttk.Label(root, text=data['name'])
    label.grid(row=r, column=1, padx=15, pady=15)
    if data['type'] == 1:
        tkInput = ttk.Entry(root,validate=data['validate'],validatecommand=(root.register(validate_input), "%S"), width=data['width'])
        tkInput.bind("<Key>", _onKeyRelease)
        tkInput.grid(row=r, column=2, padx=15, pady=15)
    elif data['type'] == 2:
        tkInput = ttk.Combobox(root, values = data['props'], width=data['width'])
        tkInput['state'] = 'readonly'
        tkInput.grid(row=r, column=2, padx=15, pady=15)
    elif data['type'] == 3:
        checkbutton_var = tk.IntVar()
        checkbutton_var.set(0)
        tkInput = ttk.Checkbutton(root, text=data['name'], variable= checkbutton_var, command=lambda: data['func'](checkbutton_var))
        tkInput.grid(row=r, column=2, padx=15, pady=15)
    return tkInput