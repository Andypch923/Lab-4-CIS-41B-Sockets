from collections import namedtuple
import pandas as pd
import scrapper
class DataBase:

    
    def __init__(self,tempObj):
        data = {}
        self.__country = []
        for i in tempObj:
            name = i[0]
            self.__country.append(name)
            temp = i
            del temp [0]
            data[name] = i
        self.__df = pd.DataFrame(data,index= [*range(1990,2018,1)])

    def fetchCountry(self):
        return self.__country
        
    def fetchDataByCountry(self,s):
        
        return self.__df[s].tolist()


    def fetchDataByCountryAndYear(self,s,start,end):
        if start == end:  
            return [self.__df[s][start]]
        items = []
        for i in range(start,end,1):
            items.append(self.__df[s][i])
        return items
        
        
