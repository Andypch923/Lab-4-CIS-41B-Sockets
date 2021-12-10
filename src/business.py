import socket
import scrapper
import DataBase

dataStream= scrapper.scrapper()
dataStream.groupLists()

database = DataBase.DataBase(dataStream.getListOfRecords())

s = socket.socket()
port = 12345
s.bind(('',port))

s.listen(5)

while True:
    
    c , addr = s.accept()
    dataFromClient = c.recv(1024)
    listOfParams = dataFromClient.decode()
    dataToSend = list()
    if (listOfParams[1] == 1990 and listOfParams[2] == 2017):
        dataToSend = database.fetchCountry(listOfParams[0])
    else:
        dataToSend = database.fetchDataByCountryAndYear(listOfParams[0],listOfParams[1],listOfParams[2])

    s.send(dataToSend.encode())
    c.close()

    break