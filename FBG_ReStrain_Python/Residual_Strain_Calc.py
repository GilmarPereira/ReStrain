""" Python Class to calculate the residual strain

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

import pandas as pd

class Residual_Strain_Calc(object):
    def __init__(self,Data,FBGSensorName,ThermoName,PhotoElastic,ThermalExpansion,ThermoOptic,tolerance,TempThreshold,FBGmode,InitWave=0):
        
        """ Initialized the FBG and Temp Loading Class file

        Input_Parameters:
        ----------
        TempThresho- Threshold of the temperature used to calculate the gel time 
        
        FBGmode: The FBG file is in wavelength shift or absolute values?
                0- absolute values
                1-wavelngth shift               
        """
        
        #Save the Sync Data as internal variable
        self.Data=Data
        self.FBGSensorName=FBGSensorName
        self.ThermoName=ThermoName
   
        """------ FBG mode---"""
        if FBGmode==0:
            #Save the first wavelength as original wavelength
            self.InitialWavelength=self.Data[FBGSensorName][0]
            #Save the first temperature as reference
            self.InitialTemp=self.Data[ThermoName][0]
            #Residual strain Calc
            self.Data['Eq1']=(((self.Data[FBGSensorName]-self.InitialWavelength)/self.InitialWavelength)-(((1-PhotoElastic)*ThermalExpansion+ThermoOptic)*(self.Data[ThermoName]-self.InitialTemp)))/(1-PhotoElastic)
            self.Data['Eq2']=(((self.Data[FBGSensorName]-self.InitialWavelength)/self.InitialWavelength)-(ThermoOptic*(self.Data[ThermoName]-self.InitialTemp)))/(1-PhotoElastic)
        
        if FBGmode==1:
            #Save the first temperature as reference
            self.InitialTemp=self.Data[ThermoName][0]
            #Residual strain Calcu
            self.Data['Eq1']=(((self.Data[FBGSensorName])/InitWave)-(((1-PhotoElastic)*ThermalExpansion+ThermoOptic)*(self.Data[ThermoName]-self.InitialTemp)))/(1-PhotoElastic)
            self.Data['Eq2']=(((self.Data[FBGSensorName])/InitWave)-(ThermoOptic*(self.Data[ThermoName]-self.InitialTemp)))/(1-PhotoElastic)

  
        """---------Calculate the gel point--------------"""
        #Point for gel transition
        try:Time1=self.Data[self.Data['Eq1']>tolerance].index[0]
        except:Time1=pd.datetime.today()
        try:Time2=self.Data[self.Data['Eq1']<-tolerance].index[0]
        except:Time2=pd.datetime.today()
        if Time1<Time2:
            self.GelPoint=Time1
        else:
            self.GelPoint=Time2
            
        #Begining of the cure
        self.CureInitTime=self.Data[self.Data[ThermoName]>TempThreshold].index[0]
        
        #Time to gel Time
        self.TimeToGelPoint=self.GelPoint-self.CureInitTime
        
        """----------Residual strain Graph------------- """   
        self.Data['ResidualStrain']=self.Data['Eq2']-self.Data['Eq2'][self.GelPoint]
        self.Data['ResidualStrain'][0:self.GelPoint]=0
        
        """-----------Final Residual strain and maximum temp peak------"""
        #Residual Strain
        self.FinalResidualStrain=self.Data['ResidualStrain'].iget(-1)
        #Max Temp
        self.MaxExoTemp=self.Data[ThermoName].max()
 
 #Commands used to run this file without the GUI
 
"""
from Load_Sync import *

#TempPath=['C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\75\\final.csv']
TempPath=['C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\Sync\\temp.csv']
TempFileNum=1
TempColNumb=5
TempColNames=['Date','Time','Thermo-1','Thermo-2','Thermo-3']
TempSkipRows=1
TempSep=';'

#p='C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\75\\'
p='C:\\Users\\gfpe\\Desktop\\Example_Temp_File\\Sync\\'
#FBGPaths=[p+'1.txt',p+'2.txt',p+'3.txt',p+'4.txt',p+'5.txt',p+'6.txt',p+'7.txt',p+'8.txt',p+'9.txt',p+'10.txt',p+'11.txt',p+'12.txt',p+'13.txt',p+'14.txt',p+'15.txt',p+'16.txt',p+'17.txt',p+'18.txt',p+'19.txt']
FBGPaths=[p+'1.txt',p+'2.txt',p+'3.txt']
#FBGFileNum=19
FBGFileNum=3
#FBGColNumb=4
FBGColNumb=5
#FBGColNames=['Date','Time','Sample','FBG-1']
FBGColNames=['Date','Time','Sample','FBG-1','FBG-2']
FBGSkipRows=2
FBGSep='\t'

test=FBG_Temp_Loading(TempPath,TempFileNum,TempSkipRows,TempSep,TempColNumb,TempColNames,FBGPaths,FBGFileNum,FBGSkipRows,FBGSep,FBGColNumb,FBGColNames)

#test.FBGData['FBG1'].plot()
test.Syncron()


#To save
test.FBGData.to_csv('C:\\Users\\gfpe\\Desktop\\FBG.csv', sep=';')
test.TempData.to_csv('C:\\Users\\gfpe\\Desktop\\temp.csv', sep=';')
test.SyncData.to_csv('C:\\Users\\gfpe\\Desktop\\res.csv', sep=';')

Final=Residual_Strain_Calc(test.SyncData,'FBG-1','Thermo-1',0.22,8.3E-6,0.55E-6,0.0001,25.0,0,0)
"""