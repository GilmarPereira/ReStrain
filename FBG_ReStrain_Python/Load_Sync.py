""" Python Class To Load and Sync two files: Thermocouple and FBG

Copyright (C) Gilmar Pereira
2015 DTU Wind Energy

Author: Gilmar Pereira
Email: gfpe@dtu.dk; gilmar_fp@outlook.com
Last revision: 02-08-2016

***License***:

This file is part of FBG_ReStrain.

FBG_ReStrain is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FBG_ReStrain is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>
"""

#Packages
import pandas as pd
import datetime as dt

class FBG_Temp_Loading(object):
    def __init__(self,TempPaths,TempFileNum,TempSkipRows,TempSep,TempColNumb,TempColNames,FBGPaths,FBGFileNum,FBGSkipRows,FBGSep,FBGColNumb,FBGColNames,TimeCorrect=0):
        
        """ Initialized the FBG and Temp Loading Class file

        Input_Parameters:
        ----------

        """
        
        #Temp Input
        self.TempPaths=TempPaths
        self.TempFileNum=TempFileNum
        self.TempSkipRows=TempSkipRows #Skip to the begin of the Data (skip head)
        self.TempSep=TempSep # Data separador
        self.TempColNumb=TempColNumb
        self.TempColNames=TempColNames
        self.TimeCorrect=TimeCorrect
        
        #FBG Input        
        self.FBGPaths=FBGPaths
        self.FBGFileNum=FBGFileNum
        self.FBGSkipRows=FBGSkipRows#Skip to the begin of the Data (skip head)
        self.FBGSep=FBGSep # Data separador
        self.FBGColNumb=FBGColNumb
        self.FBGColNames=FBGColNames
               
        #Load File
        #Temp
        self.TempData=pd.DataFrame()
        for i in range (0,self.TempFileNum):
            TempPathtemp=self.TempPaths[i].replace("\\","/",99)
            TempDataTemp=pd.read_csv(TempPathtemp,sep=self.TempSep,names=self.TempColNames,skiprows=self.TempSkipRows,parse_dates=[['Date', 'Time']],dayfirst=True)
            
            #Merge Date and Hour
            self.TempData=pd.concat([self.TempData,TempDataTemp],ignore_index=True)
            
        #Correct Time
        self.TempData['Date_Time']=self.TempData['Date_Time']+dt.timedelta(hours=self.TimeCorrect)
            #Date_Time timestamp
            
        self.TempData=self.TempData.set_index('Date_Time')
        
        #FBG
        self.FBGData=pd.DataFrame()
        for i in range(0,self.FBGFileNum):
            FBGPathtemp=self.FBGPaths[i].replace("\\","/",99)
            FBGDataTemp=pd.read_csv(FBGPathtemp,sep=self.FBGSep,names=self.FBGColNames,skiprows=self.FBGSkipRows,parse_dates=[['Date', 'Time']],dayfirst=True)
            
            #Merge Date and Hour
            self.FBGData= pd.concat([self.FBGData,FBGDataTemp],ignore_index=True)
            
        #Delete collum Sample
        self.FBGData=self.FBGData.drop('Sample',1)
        #Organixe index
        self.FBGData=self.FBGData.set_index('Date_Time')


    def Syncron(self):
        """ Syncronize the FBG files and Temp files
       
        ----------
        """
        self.SyncData= pd.concat([self.FBGData,self.TempData],axis=1, join='inner')
        
        #Create collum with increment/sample serie
        #self.SyncData['Increment']=pd.Series(range(0,len(self.SyncData)), index=self.SyncData.index)
        self.SyncData.insert(0,'Increment/Sample',pd.Series(range(0,len(self.SyncData)), index=self.SyncData.index))
       
        
            
#Commands used to run this file without the GUI
"""
TempPath=['C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\sync\\temp.csv']
TempFileNum=1
TempColNumb=5
TempColNames=['Date','Time','Temp1','Temp2','Temp3']
TempSkipRows=1
TempSep=';'


FBGPaths=['C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\Sync\\BM Data [2015.07.16.09.31.02 ; 2015.07.16.10.31.01].txt','C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\Sync\\BM Data [2015.07.16.10.31.02 ; 2015.07.16.11.31.01].txt','C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\Sync\\BM Data [2015.07.16.11.31.02 ; 2015.07.16.12.31.01].txt']
FBGFileNum=3
FBGColNumb=5
FBGColNames=['Date','Time','Sample','FBG1','FBG2']
FBGSkipRows=2
FBGSep='\t'




test=FBG_Temp_Loading(TempPath,TempFileNum,TempSkipRows,TempSep,TempColNumb,TempColNames,FBGPaths,FBGFileNum,FBGSkipRows,FBGSep,FBGColNumb,FBGColNames)

#test.FBGData['FBG1'].plot()
test.Syncron()

#To save
test.FBGData.to_csv('C:\\Users\\gfpe\\Desktop\\FBG.csv', sep=';')
test.TempData.to_csv('C:\\Users\\gfpe\\Desktop\\temp.csv', sep=';')
test.SyncData.to_csv('C:\\Users\\gfpe\\Desktop\\res.csv', sep=';')

"""
