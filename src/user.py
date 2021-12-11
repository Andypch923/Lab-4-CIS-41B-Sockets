import socket
import scrapper
import DataBase
from tkinter.constants import CENTER, LEFT, TOP
import tkinter as tk
from tkinter import *
import plot


def onselect1(event1):
    w = event1.widget
    index = w.curselection()
    country = database.fetchCountry()[sum(index)]
    dataList.append(country)

def onselect2(event2):
    w = event2.widget
    index = w.curselection()
    startYear = yearList[sum(index)]
    dataList.append(startYear)

def onselect3(event3):
    w = event3.widget
    index = w.curselection()
    endYear = yearList[sum(index)]
    dataList.append(endYear)

def sendAndPlot():
    del dataList[2]
    del dataList[3]
    for i in dataList:
        s.send(i.encode())
    dataFromServer = list(s.recv(1024))
    grapher = plot.Graph()
    rangedYearList = [*range(dataList[1],dataList[2],1)]
    grapher.xyPlot(rangedYearList,dataFromServer)
    


dataList = []
dataStream= scrapper.scrapper()
dataStream.groupLists()

database = DataBase.DataBase(dataStream.getListOfRecords())

s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))


root = tk.Tk()
root.geometry("900x720")
frame = tk.Frame(root, bg = "white")

l1 = Listbox(frame)
l2 = Listbox(frame)
l3 = Listbox(frame)

for item in database.fetchCountry():
    l1.insert(END, item)

yearList = [*range(1990,2018,1)]
for item in yearList:
    l2.insert(END,item)
    l3.insert(END,item)

l1.grid(row=0, column=0)
listbox1Select = l1.bind('<<ListboxSelect>>',lambda event1: onselect1(event1))
l2.grid(row=0, column=1)
listbox2Select = l2.bind('<<ListboxSelect>>',lambda event2: onselect2(event2))
l3.grid(row=0, column=2)
listbox3Select = l3.bind('<<ListboxSelect>>',lambda event3: onselect3(event3))

frame.place(relwidth=0.8, relheight =0.8,relx = 0.1, rely=0.1)

Button(root, text='PLOT',command=sendAndPlot).pack(pady=30)
show = Label(root)
show.pack()

root.mainloop()

s.close()