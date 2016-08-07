"""
File to correct the FBG files when there is peak spliting.

@author: Gilmar Ferreira Pereira (gfpe@dtu.dk; gilmar_fp@outlook.com)
"""
import glob, os
import numpy as np
import scipy as sp
import sympy
import matplotlib.pyplot as plt
import math
import pandas as pd


"""************************** Data that the user can change**************** """
#Directory with the files
Filepath='C:\Users\gfpe\Desktop\Python_Script_To_Correct_Multi_FBG\Test'
#FBG channel to correct
FBGToCorrect='FBG2'
"""*************************************************************************"""





"""------------------This data can be also modified-------------------------"""
#Number of columns per file
FBGColNumb=5
#Name of each column
FBGColNames=['Date','Time','Sample','FBG1','FBG2']
#Lines to skip of header (for loading the file)
FBGSkipRows=2
#Column separater (\t means tab)
FBGSep='\t'
#Amount of slipts (not important)
Nsplit=90
"""-------------------------------------------------------------------------"""


#Get files in the folder
Filepath=Filepath.replace("\\","/",99)
FileNameList=[]
os.chdir(Filepath)
for file in glob.glob("*.txt"):
    FileNameList.append(str(file))

for i in range(0,Nsplit):
    FBGColNames.append('Extra'+str(i+1))

for a in range(0,len(FileNameList)):
    print FileNameList[a]
    
    Data=pd.read_csv(FileNameList[a],sep=FBGSep,names=FBGColNames,skiprows=FBGSkipRows)
       
    #Cycle per line
    for i in range(0,len(Data['Sample'])):
        if i==0 and np.isnan(Data['Extra1'][i])==False:
            Data[FBGToCorrect][i]=TempFromPrevFile
            
        if i>0 and np.isnan(Data['Extra1'][i])==False:
            #savePrevious value
            temp=Data[FBGToCorrect][i-1]
            Div=99999999
            Extraindex=1
            #Check which value is the closest
            for j in range(0,Nsplit):
                tempname=str('Extra'+str(j+1))
                if abs(temp-Data[tempname][i])<Div:
                    Extraindex=j+1
                    Div=abs(temp-Data[tempname][i])
            #Replace FBG for the correct values
            Data[FBGToCorrect][i]=Data['Extra'+str(Extraindex)][i]
        TempFromPrevFile=Data[FBGToCorrect][i]

#Save the corrected file    
    file=open("_(correct)"+ FileNameList[a],"w")
    
    #Header
    for i in range(0,FBGColNumb):
        file.write(str(FBGColNames[i])+ '\t')
    file.write('\n')    
    #Text
    for a in range(0,len(Data['Sample'])):
        for i in range(0,FBGColNumb):
            file.write('%10s \t' %(Data[FBGColNames[i]][a]))
        file.write('\n')        
    file.close()

       