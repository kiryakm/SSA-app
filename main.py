import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import math

import pars
import ssaCore

data = []
par = pars.Parser()
filename = ""
length = 0

def uploadFile(event=None):
    global filename, length
    filename = tkinter.filedialog.askopenfilename()
    try:
        length = par.read(filename)
        labelText.set(filename.split("/")[-1] + "   Длина: " + str(length))
        lenT.delete(0,tk.END)
        lenT.insert(0,math.floor(length/4))
    except:
        labelText.set("Неверный файл")

def showData():
    global data
    data = par.getData(combBox.get())
    t = np.arange(len(data))
    fig.clf()
    fig.add_subplot(111).plot(t, data)
    canvas.draw()

def showFilt():        
    global length, data
    try:
        L = int(lenT.get())
        if L > length/2 or L < 1:
            lenT.delete(0,tk.END)
            lenT.insert(0,math.floor(length/4))
            return
    except:
        return
    data = par.getData(combBox.get())
    ssa = ssaCore.SSA(data, L)
    data = ssa.getFilt()
    t = np.arange(len(data))
    fig.clf()
    fig.add_subplot(111).plot(t, data)
    canvas.draw()
    
def forecast():
    global length, data
    try:
        steps = int(forecastT.get())
        L = int(lenT.get())
        if L > length/2 or L < 1:
            lenT.delete(0,tk.END)
            lenT.insert(0,math.floor(length/4))
            return
    except:
        return
    data = par.getData(combBox.get())
    ssa = ssaCore.SSA(data, L)
    filt = ssa.getFilt()
    data = ssa.forecast(steps)
    fig.clf()
    fig.add_subplot(111).plot(np.arange(len(filt)), filt)
    t = np.arange(len(filt)-1, len(data)-1)
    fig.add_subplot(111).plot(t, data[len(filt):], color = "red")
    canvas.draw()

def save():
    global data
    f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    mjd = par.MJD
    while len(mjd) < len(data):
        mjd.append(mjd[-1]+1)
    text = ""
    for i in range(len(data)):
        text += str(mjd[i]) + " " + str(data[i]) + "\n" 
    f.write(text)
    f.close()

root = tk.Tk()
root.minsize(500, 450)

frame = tk.Frame()
frame.pack()
labelText = tk.StringVar(root)
labelText.set("Выберите файл с данными")
messageBox = tk.Label(frame, textvariable=labelText, background = "gray85")
messageBox.pack(side=tk.LEFT, padx=(10), pady=(5))
fileChoose = tk.Button(frame, text='Выбрать файл', command=uploadFile)
fileChoose.pack(side=tk.LEFT, padx=(10), pady=(5))
saveData = tk.Button(frame, text='Сохранить данные', command=save)
saveData.pack(side=tk.LEFT, padx=(10), pady=(5))

frame = tk.Frame()
frame.pack()
messageBox1 = tk.Label(frame, text = "Использовать:", background = "gray85")
messageBox1.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
combBox = ttk.Combobox(frame, width=12, values=["X (A)", "Y (A)", "UTC-UT1 (A)", "X (B)", "Y (B)", "UTC-UT1 (B)"])
combBox.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
combBox.current(0)
calcLn = tk.Button(frame, text='Показать данные', command=showData)
calcLn.pack(side=tk.LEFT, padx=(10), pady=(5))

# calcLn = tk.Button(frame, text='Показать ln')
# calcLn.pack(side=tk.LEFT, padx=(10), pady=(5))
# showComp = tk.Button(frame, text='Востонофить по компонентам')
# showComp.pack(side=tk.LEFT, padx=(10), pady=(5))
# enterComps = tk.Entry(frame, width=15)
# enterComps.pack(side=tk.LEFT, padx=(10), pady=(5))

frame = tk.Frame()
frame.pack()
enterL = tk.Label(frame, text="Длина окна:", background = "gray85")
enterL.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
lenT = tk.Entry(frame, width=5)
lenT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
filterB = tk.Button(frame, text='Отфильтровать', command=showFilt)
filterB.pack(side=tk.LEFT, padx=(10), pady=(5))
# trendB = tk.Button(frame, text='Тренд')
# trendB.pack(side=tk.LEFT, padx=(10), pady=(5))
# perB = tk.Button(frame, text='Переод')
# perB.pack(side=tk.LEFT, padx=(10), pady=(5))
forcastB = tk.Button(frame, text='Предсказать на', command=forecast)
forcastB.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
forecastT = tk.Entry(frame, width=5)
forecastT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))

# saveData = tk.Button(root, text='Сохранить текущие данные')
# saveData.grid(row=3, column=0, padx=(10), pady=(5), columnspan=2, sticky="ew")
# savePlot = tk.Button(root, text='Сохранить текущий график')
# savePlot.grid(row=3, column=2, padx=(10), pady=(5), columnspan=2, sticky="ew")

fig = Figure(figsize=(4, 3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tk.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tkinter.BOTH, expand=1)


root.mainloop()