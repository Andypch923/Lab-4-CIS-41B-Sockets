from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from collections import namedtuple
#Scrape records off UNData.xml, store in namedTuple and create a list of namedtuples storing data 
class scrapper:

    def __init__(self):
        #Using beautiful soup to scrape UNData.xml
        namedTupleOfRecord = namedtuple("record", ["country","year","dataValue"])
        self.__listOfRecords = [] 
        with open("UNData.xml","r") as file:
            content = file.readlines()
            content = "".join(content)
            page_soup = bs(content,"lxml")

            records = page_soup.find_all("record")
            for i in records:
                recordData = i.text.split("\n")
                tempTuple = namedTupleOfRecord(recordData[1],recordData[2],recordData[3])
                self.__listOfRecords.append(tempTuple)

    def groupLists(self):
        self.__listOfRecordsByCountry = list()
        tempListOfData = []
        country = ""
        counter = 0
        for i in self.__listOfRecords:
            if counter < 28:
                country = i[0]
                tempListOfData.append(i[2])
                counter += 1
                if (country == "United States of America" and counter == 28):
                    tempListOfData = tempListOfData[::-1]       
                    tempCountry = list()
                    tempCountry.append(country)
                    self.__listOfRecordsByCountry.append(tempCountry + tempListOfData)
            else:
                tempListOfData = tempListOfData[::-1]                    
                tempCountry = list()
                tempCountry.append(country)
                self.__listOfRecordsByCountry.append(tempCountry + tempListOfData)
                tempListOfData.clear()
                tempListOfData.append(i[2])
                counter = 1
        

    def getListOfRecords(self):
        return self.__listOfRecordsByCountry
        
            


    