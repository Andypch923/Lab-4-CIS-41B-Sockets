import socket
import scrapper
import DataBase
from tkinter.constants import CENTER, LEFT, TOP
import tkinter as tk
from tkinter import *
import plot

dataStream= scrapper.scrapper()
dataStream.groupLists()

database = DataBase.DataBase(dataStream.getListOfRecords())

s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))


root = tk.Tk()
root.geometry("900x720")

l1 = Listbox()
l2 = Listbox()
l3 = Listbox()

for item in database.fetchCountry():
    l1.insert(END, item)

yearList = [*range(1990,2018,1)]
for item in yearList:
    l2.insert(END,item)
    l3.insert(END,item)

l1.grid(row=0, column=0)
l2.grid(row=0, column=1)
l3.grid(row=0, column=2)
listbox3Select = l3.bind('<<ListboxSelect>>',lambda event: onselect())


def onselect():
    country = database.fetchCountry()[sum(l1.curselection())]
    startYear = yearList[sum(l2.curselection())]
    endYear = yearList[sum(l3.curselection())]
    data = list()
    data.append(country)
    data.append(startYear)
    data.append(endYear)
    s.send(data.encode())
    dataFromServer = s.recv(1024)
    grapher = plot.Graph()
    rangedYearList = [*range(startYear,endYear,1)]
    grapher.xyPlot(rangedYearList,dataFromServer)
root.mainloop()
s.close()