import socket
import scrapper
import DataBase
from tkinter.constants import CENTER, LEFT, TOP
import tkinter as tk
from tkinter import *
import plot
import json

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
    if int(dataList[1]) > int(dataList[2]) and len(dataList) > 3:
        print("Error: Ending Year cannot be less than Starting Year")
        dataList.clear()
    else:
        tempDict = dict()
        for i in dataList:
            tempDict[i] = ""
        tempDict = json.dumps(tempDict)
        s.sendall(bytes(tempDict,encoding ="utf-8"))

        dataFromServer = s.recv(1024)
        dataFromServer = dataFromServer.decode('utf-8')
        dataFromServer = list((json.loads(dataFromServer)).keys())
        floatDataFromServer = []
        for i in dataFromServer:
            floatDataFromServer.append(float(i))
        grapher = plot.Graph()
        rangedYearList = [*range(dataList[1],dataList[2],1)]
        grapher.xyPlot(rangedYearList,floatDataFromServer)
        dataList.clear()

dataList = []
dataStream= scrapper.scrapper()
dataStream.groupLists()

database = DataBase.DataBase(dataStream.getListOfRecords())

s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))
#Receive List of Countries
data = s.recv(1024)
data = data.decode('utf-8')
countryList = (json.loads(data)).keys()


root = tk.Tk()
root.title('Year and Country: Find your data!')
root.geometry("900x720")


frame = tk.Frame(root, bg = "white")

l1 = Listbox(frame)
l2 = Listbox(frame)
l3 = Listbox(frame)

for item in countryList:
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


canvas1 = tk.Canvas(root, height =150, width = 700)
canvas1.create_text(250,100, text="""\n\nClick on the listbox from left to right to select the country, 
starting year and ending year. This will plot an xy plot of the 
data from the respectively country.""", fill ="black", font = ('Helvetica 10 italic'))
canvas1.pack(side=BOTTOM,padx=10,pady=10)

frame.place(relwidth=0.8, relheight =0.8,relx = 0.1, rely=0.1)

Button(root, text='PLOT',command=sendAndPlot).pack(pady=30)
show = Label(root)
show.pack()

root.mainloop()

s.close()