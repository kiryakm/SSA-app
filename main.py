import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

import pars
import ssaCore

date = []
mainData = []
data = []
forc = []
filt = []
trend = []
period = []
par = pars.Parser()
filename = ""
length = 0
mode = -1

plt.rcParams["date.autoformatter.hour"] = "%Y-%m-%d"

def drawPlot():
    global data, forc, filt, mode, trend, period, date, mainData
    if mode == -1:
        return
    begin, end = getSize()
    if mode == 0:
        fig.clf()
        ax = fig.add_subplot(111)
        if cvar1.get():
            ax.plot(date[begin:end], mainData[begin:end], linestyle='-', marker='o')
        else:
            ax.plot(date[begin:end], mainData[begin:end])
        ax.set_title("Начальные данные")
        fig.tight_layout()
        canvas.draw()

    elif mode == 1:
        fig.clf()
        ax1 = fig.add_subplot(221)
        if cvar1.get():
            ax1.plot(date[begin:end],  mainData[begin:end], linestyle='-', marker='o')
        else:
            ax1.plot(date[begin:end],  mainData[begin:end])
        ax1.set_title("Начальные данные")


        ax3 = fig.add_subplot(222)
        newDate = date[begin:end]
        for i in range(len(forc) - len(filt)):
            newDate.append(newDate[-1]+datetime.timedelta(days=1))
        t = newDate[end-begin-1:]
        b = len(forc)-len(t)
        if cvar1.get():
            ax3.plot(t, forc[b:], color = "red", label = "Предсказанные", linestyle='-', marker='o')
            ax3.plot(date[begin:end], filt, label = "Отфильтрованные", linestyle='-', marker='o')
        else:
            ax3.plot(t, forc[b:], color = "red", label = "Предсказанные")
            ax3.plot(date[begin:end], filt, label = "Отфильтрованные")
        ax3.set_title("Предсказанные данные")
        ax3.legend()

        ax4 = fig.add_subplot(223)
        if cvar1.get():
            ax4.plot(date[begin:end], mainData[begin:end], label = "Оригинальные", linestyle='-', marker='o')
            ax4.plot(date[begin:end], trend, color = "red", label = "Тренд", linestyle='-', marker='o')
        else:
            ax4.plot(date[begin:end], mainData[begin:end], label = "Оригинальные")
            ax4.plot(date[begin:end], trend, color = "red", label = "Тренд")
        ax4.set_title("Тренд")
        ax4.legend()

        ax4 = fig.add_subplot(224)
        if cvar1.get():
            ax4.plot(date[begin:end], mainData[begin:end], label = "Оригинальные", linestyle='-', marker='o')
            ax4.plot(date[begin:end], period, color = "red", label = "Период", linestyle='-', marker='o')
        else:
            ax4.plot(date[begin:end], mainData[begin:end], label = "Оригинальные")
            ax4.plot(date[begin:end], period, color = "red", label = "Период")
        ax4.set_title("Период")
        ax4.legend()

        canvas.draw()
    elif mode == 2:
        fig.clf()
        ax = fig.add_subplot(111)
        newDate = date[begin:end]
        for i in range(len(forc) - len(filt)):
            newDate.append(newDate[-1]+datetime.timedelta(days=1))
        t = newDate[end-begin-1:]
        t2 = date[begin:end+len(t)-1]
        b = len(forc)-len(t)
        if cvar1.get():
            ax.plot(t, forc[b:], color = "red", label = "Предсказанные", linestyle='-', marker='o')
            ax.plot(date[begin:end], filt, label = "Отфильтрованные", linestyle='-', marker='o')
            ax.plot(t2, mainData[begin:end+len(t)-1], color = "black", label = "Фактические", linestyle='-', marker='o')
        else:
            ax.plot(t, forc[b:], color = "red", label = "Предсказанные")
            ax.plot(date[begin:end], filt, label = "Отфильтрованные")
            ax.plot(t2, mainData[begin:end+len(t)-1], color = "black", label = "Фактические")
        ax.set_title("Прогноз-факт")
        ax.legend()
        canvas.draw()
    

def getSize():
    try:
        begin = int(beginT.get())
    except:
        beginT.delete(0,tk.END)
        beginT.insert(0,"0")
        return -1, -1
    try:
        end = int(endT.get())
    except:
        endT.delete(0,tk.END)
        endT.insert(0,str(length))
        return -1, -1

    if begin >= end:
        beginT.delete(0,tk.END)
        beginT.insert(0,"0")
        endT.delete(0,tk.END)
        endT.insert(0,str(length))
        return -1, -1

    if end < 1 or end > length:
        endT.delete(0,tk.END)
        endT.insert(0,str(length))
        return -1, -1
    if begin < 0:
        beginT.delete(0,tk.END)
        beginT.insert(0,"0")
        return -1, -1
    return begin, end

def uploadFile(event=None):
    """
    Загрузить файл
    """
    global filename, length, date
    filename = tkinter.filedialog.askopenfilename()
    cvar2.set(0)
    try:
        length = par.read(filename)
        labelText.set(filename.split("/")[-1] + "   Длина: " + str(length))
        lenT.delete(0,tk.END)
        lenT.insert(0,math.floor(length/4))
        beginT.delete(0,tk.END)
        beginT.insert(0,"0")
        endT.delete(0,tk.END)
        endT.insert(0,str(length))
        date = par.getDate()
        showData("_")
    except:
        labelText.set("Неверный файл")

def showData(_=""):
    """
    Показать данные
    """
    global mainData, data, forc, mode
    cvar2.set(0)
    data = par.getData(combBox.get())
    mainData = data
    forc = []
    begin, end = getSize()
    if begin == -1:
        return
    mode = 0
    drawPlot()
    
    
def forecast():
    """
    Предсказать и вывести
    """
    global length, data, filt, forc, mode, trend, period
    cvar2.set(0)
    begin, end = getSize()
    if begin == -1:
        return
    try:
        steps = int(forecastT.get())
        L = int(lenT.get())
        if L > (end - begin)/2 or L < 1:
            lenT.delete(0,tk.END)
            lenT.insert(0,math.floor((end - begin)/2))
            return
    except:
        return
    
    data = par.getData(combBox.get())
    ssa = ssaCore.SSA(data[begin:end], L)
    filt = ssa.getFilt()
    forc = ssa.forecast(steps)
    trend = ssa.getTrend()
    period = ssa.getPeriod()
    mode = 1
    drawPlot()    

    data = data[begin:end]

def save():
    """
    Сохранить текущие данные
    """
    global data, forc
    f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    mjd = par.MJD
    while len(mjd) < len(data)+len(forc):
        mjd.append(mjd[-1]+1)
    pred = []
    while len(pred) < len(data):
        pred.append("D")    
    while len(pred) < len(forc):
        pred.append("P")
    text = ""
    if len(forc) == 0:
        l = len(data)
    else:
        l = len(forc)
        data = forc
    for i in range(l):
        text += str(mjd[i]) + " " + str(data[i]) + " " + str(pred[i]) + "\n" 
    f.write(text)
    f.close()

def fact():
    global mainData, length, data, filt, forc, mode
    if cvar2.get():
        try:
            begin, end = getSize()
            if begin == -1:
                return
            absolute = 0
            relative = 0
            j = 0
            for i in range(len(filt), len(forc)):
                a = abs(mainData[end+j]-forc[i])
                absolute += a
                relative += abs(a / mainData[end+j])
                j+=1
            errorText.set("Абсолютная средняя ошибка: " + str(round(absolute/j,2)) + \
            "\n Относительная средняя ошибка: " +str(round(relative/j,1)*100) +"%")
            mode = 2 
            drawPlot()
        except:
            errorText.set("Нет данных для сравнения")
            cvar2.set(0)
    else:
        mode = 1
        drawPlot()

root = tk.Tk()
root.minsize(900, 500)
root.title("SSA")

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
combBox = ttk.Combobox(frame,  width=12, values=["X (A)", "Y (A)", "UTC-UT1 (A)", "X (B)", "Y (B)", "UTC-UT1 (B)"])
combBox.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
combBox.current(0)
combBox.bind('<<ComboboxSelected>>', showData)
beginL = tk.Label(frame, text="От:", background = "gray85")
beginL.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
beginT = tk.Entry(frame, width=5)
beginT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
endL = tk.Label(frame, text="До:", background = "gray85")
endL.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
endT = tk.Entry(frame, width=5)
endT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
calcLn = tk.Button(frame, text='Показать данные', command=showData)
calcLn.pack(side=tk.LEFT, padx=(10), pady=(5))

frame = tk.Frame()
frame.pack()
enterL = tk.Label(frame, text="Длина окна:", background = "gray85")
enterL.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
lenT = tk.Entry(frame, width=5)
lenT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
forcastB = tk.Button(frame, text='Предсказать на', command=forecast)
forcastB.pack(side=tk.LEFT, padx=(10, 5), pady=(5))
forecastT = tk.Entry(frame, width=5)
forecastT.pack(side=tk.LEFT, padx=(0, 10), pady=(5))
cvar1 = tk.BooleanVar()
cvar1.set(0)
c1 = tk.Checkbutton(frame, text="Отображать маркеры", variable=cvar1, onvalue=1, offvalue=0, command=drawPlot)
c1.pack(side=tk.LEFT, padx=(10), pady=(5))

frame = tk.Frame()
frame.pack()
errorText = tk.StringVar(root)
errorText.set("Абсолютная средняя ошибка:\n Относительная средняя ошибка:")
errorL = tk.Label(frame, textvariable=errorText, background = "gray85")
errorL.pack(side=tk.LEFT, padx=(10), pady=(5))
cvar2 = tk.BooleanVar()
cvar2.set(0)
c2 = tk.Checkbutton(frame, text="Прогноз-факт", variable=cvar2, onvalue=1, offvalue=0, command=fact)
c2.pack(side=tk.LEFT, padx=(10), pady=(5))

fig = Figure(figsize=(4, 3), dpi=100)
fig.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tkinter.BOTH, expand=1)

root.mainloop()
