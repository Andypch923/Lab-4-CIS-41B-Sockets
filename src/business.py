import socket
import scrapper
import DataBase
from threading import Thread    
from socketserver import BaseRequestHandler, ThreadingMixIn
import json

class ClientThread(Thread):
    
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))


    def run(self):
        while True:
            #send list of countries
            countryList = database.fetchCountry()
            y = dict()
            for i in countryList:
                y[i] = ""
            y = json.dumps(y)
            conn.sendall(bytes(y,encoding ="utf-8"))
            #receive list of Parameters
            data = conn.recv(1024)
            data = data.decode('utf-8')
            listOfParams = list((json.loads(data)).keys())

            if (int(listOfParams[1]) == 1990 and int(listOfParams[2]) == 2017):
                dataToSend = database.fetchCountry(listOfParams[0])
            else:
                dataToSend = database.fetchDataByCountryAndYear(listOfParams[0],int(listOfParams[1]),int(listOfParams[2]))
            #send list of data fetched
            y2 = dict()
            for i in dataToSend:
                y2[i] = ""
            y2 = json.dumps(y2)
            y2 = y2.encode("utf-8")
            conn.sendall(y2)  # echo

dataStream= scrapper.scrapper()
dataStream.groupLists()

database = DataBase.DataBase(dataStream.getListOfRecords())

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Normally 1024


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(4)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
    tcpsock.close()
    break

for t in threads:
    t.join()

