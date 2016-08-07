# -*- coding: utf-8 -*-
""" This Python Class contains all the functions needed to build the GUI 
interface, and to test all the INPUT parameters.

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
from __future__ import print_function
import csv

#Other Classes used
import GUI.MyPlotMainWindowUI
from Load_Sync import *
from Residual_Strain_Calc import *

from QtGuiLoader import QtMainWindowLoader, QtWidgetLoader, QtDialogLoader
#Class to connect the UI to the Python Script
from PyQt4 import QtGui, QtCore


#----------------Main Window Class---------------------------------------------
class MyPlotMainWindow(QtMainWindowLoader):
    """
    This is the Main Window UI Class.    
    
    _Init_- It converts the QTdesign file in a Python Script using the class
    QTGUILoader. It connects all the actions in the UI with the Python Code.
    Also it creates the internal variables that will be submitted later to the 
    other developed tools.    
    """
    def __init__(self):
        """
        Initiation of the Main Window
        """
        module = GUI.MyPlotMainWindowUI
        try:self.ui = module.Ui_Form() # Enables autocompletion
        except: pass
        QtMainWindowLoader.__init__(self, module)
        
        #Start the MessageBoard used to plot errors
        self.ui.MessageBoard.insertPlainText('>>')
        
        #Empty Dict. with path coordinates (Extract Stress/strain)
        self.PathCoordinates={}
        self.PathNumber=0
        
        #Empty list with FBG position and FBG array original wavelength-OSA
        self.FBGPosition=[]
        self.FBGOriginalWavel=[]
        #Empty list with FBG position and FBG array original wavelength-TR
        self.FBGPositionTR=[]
        self.FBGOriginalWavelTR=[]
           
        """--------------------------Tool Bar Buttons----------------------"""
    #Push Button:Wedbsite
    def actionCopyrigth(self):
        msgbox=QtGui.QMessageBox()
        msgbox.setIcon(1)
        msgbox.setWindowTitle('About the FBG_SiMul/Copyrigth')
        msgbox.setWindowIcon(QtGui.QIcon("DESIGN_Resource/plot.png"))
        msgbox.setTextFormat(1)
        msgbox.setText('The FBG_ReStrain is a software to synchronize data from FBG sensors and Thermocouples, and calculate the cure-induced strain. The software was developed to handle data from the BraggMeter Fibersensing (FBG) and DaqPRO 5300 (Thermocuple).<br> <br>\
        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.<br> <br>\
        Denmark Technical University, Department of Wind Energy (<a href="http://www.vindenergi.dtu.dk/english">DTU Wind Webpage</a>);')
        msgbox.exec_()

    def actionAbouttheauthor(self):
        msgbox=QtGui.QMessageBox()
        msgbox.setIcon(1)
        msgbox.setWindowTitle('About the author')
        msgbox.setWindowIcon(QtGui.QIcon("DESIGN_Resource/author.png"))
        msgbox.setTextFormat(1)
        msgbox.setText('Hi, <br> <br>\
        First, thanks for your interest in this software, my name is Gilmar F. Pereira and I\'m the FBG_ReStrain main developer.<br><br>\
        If you want to know more about the theory behind the code please take a look in some of my articles. You can find my list of publications here: <a href="http://tinyurl.com/nmxehwd">DTU Orbit</a><br><br>\
        Please check out my Linkdin profil: <a href="https://dk.linkedin.com/in/gilmarfp">Linkdin</a> <br><br>\
        Contact: gfpe@dtu.dk; Gilmar_fp@outlook.com <br><br>\
        All the best and have a good FBG_ReStrain simulation,<br>\
        Gilmar P.')
        msgbox.exec_()

    def actionExitProgram(self):
        self.terminate()
        """--------------------------File Format Buttons----------------------""" 
    def actionFilesFormat_FBG(self):
        msgbox=QtGui.QMessageBox()
        msgbox.setIcon(1)
        msgbox.setWindowTitle('About the author')
        msgbox.setWindowIcon(QtGui.QIcon("DESIGN_Resource/author.png"))
        msgbox.setTextFormat(1)
        msgbox.setText('FBG file format: .txt <br> <br>\
        -Point Separated numbers (1570.4333); <br>\
        -Local Data as 16-07-2015; <br>\
        -2 lines as header; <br>\
        -Columns order: Local Date; Local Time; Sample; FBG1; FBG2;etc. <br> <br>\
        File Example: <br> <br>\
        Samples per Second	1 <br>\
        Local Date	Local Time	Sample	CH1S001	CH2S001 <br>\
        16-07-2015	09:31:02	00001	1570.4819	1570.4333 <br>\
        16-07-2015	09:31:03	00002	1570.4796	1570.4315 <br>\
        16-07-2015	09:31:04	00003	1570.4791	1570.4311 ')
        msgbox.exec_()
        
    def actionFilesFormat_Term(self):        
        msgbox=QtGui.QMessageBox()
        msgbox.setIcon(1)
        msgbox.setWindowTitle('About the author')
        msgbox.setWindowIcon(QtGui.QIcon("DESIGN_Resource/author.png"))
        msgbox.setTextFormat(1)
        msgbox.setText('Thermocouple file format: .CSV <br> <br>\
        -Point Separated numbers (25.103); <br>\
        -Column Separated by ; <br>\
        -Local Data as 16-May-2015; <br>\
        -1 lines as header; <br>\
        -Columns order: Date; Time; Temperature1, etc. <br> <br>\
        File Example: <br> <br>\
        Date(dd-mmm-yy);Time(hh:mm:ss);Temp1;Temp2;Temp3 <br>\
        18-May-2016;14:46:18;25.103;23.915;24.293<br>\
        18-May-2016;14:46:19;25.211;23.915;24.239<br>\
        18-May-2016;14:46:20;25.13;23.996;24.131<br>\
        18-May-2016;14:46:21;25.184;23.888;24.347<br>\
        18-May-2016;14:46:22;25.049;23.888;24.212<br>\
        ')
        msgbox.exec_()        

        """--------------------------File Load-----------------
    In here, the files from the FBG and thermocoples are loaded and sync"""
    
    #FBG Files
    #Push Button: Add .txt files
    def actionAddFBGFiles(self):
        selectedfile = QtGui.QFileDialog.getOpenFileNames(self, "Select the FBG file(s) (.txt).",'*.txt')
        self.ui.listWidget_InputFBG.addItems(selectedfile)
        #self.ui.listWidget_stressStrainFiles.sortItems(0) #Sort the items

    #Push Button: Remove loaded files  
    def actionRemoveFBGfile(self):
        SelectedItem=self.ui.listWidget_InputFBG.currentRow()
        self.ui.listWidget_InputFBG.takeItem(SelectedItem)

    #Push Button: Clear all files 
    def actionFBGClearFiles(self):
        self.ui.listWidget_InputFBG.clear()
 
    #Thermocouple
    #Push Button: Add .csv files
    def actionAddTempFiles(self):
        selectedfile = QtGui.QFileDialog.getOpenFileNames(self, "Select the Thermocouple file(s) (.csv).",'*.csv')
        self.ui.listWidget_InputTemp.addItems(selectedfile)
        #self.ui.listWidget_stressStrainFiles.sortItems(0) #Sort the items
        
    #Push Button: Remove loaded files  
    def actionRemoveTempfile(self):
        SelectedItem=self.ui.listWidget_InputTemp.currentRow()
        self.ui.listWidget_InputTemp.takeItem(SelectedItem)
        
    #Push Button: Clear all files 
    def actionTempClearFiles(self):
        self.ui.listWidget_InputTemp.clear()

    """ Data Sync"""
    
    def actionDataSync(self):
        
        #Reset the progress bar
        self.ui.progressBar_sync.setValue(0)  
                
        #Check if input is not empty
        InputFileFBGNumber=self.ui.listWidget_InputFBG.count()
        if InputFileFBGNumber==0:
            self.ui.MessageBoard.insertPlainText('>>ERROR in (1)!!: Please insert the FBG file(s). \n')
            return
            
        InputFileTempNumber=self.ui.listWidget_InputTemp.count()
        if InputFileTempNumber==0:
            self.ui.MessageBoard.insertPlainText('>>ERROR in (1)!!: Please insert the Temperature file(s). \n')
            return
            
        #Progress Bar
        self.ui.progressBar_sync.setValue(10)    
        
        """ Now that the input data is corrected lets prepare to submit 
        it to the Load_Sync Class"""
        
        #FBG Path
        FBGPathList=[]
        for i in range(0,InputFileFBGNumber):
            FBGPathList.append(str(self.ui.listWidget_InputFBG.item(i).text().replace("\\","/",99)))
            
        #Thermocouple Path
        TempPathList=[]
        for i in range(0,InputFileTempNumber):
            TempPathList.append(str(self.ui.listWidget_InputTemp.item(i).text().replace("\\","/",99)))
                    
        
        #Number of FBG and Skip row
        NumberFBG=self.ui.spinBox_FBGNumber.value() #Int Number FBG
        SkipRowFBG=self.ui.spinBox_SkipRowFBG.value() #Int Number FBG            

        #Number of Thermocouple, Skip row and Time correction
        NumberTemp=self.ui.spinBox_TempNumber.value() #Int Number FBG
        SkipRowTemp=self.ui.spinBox_SkipRowTemp.value() #Int Number FBG 
        TimeCorrect=self.ui.spinBox_TimeCorrection.value()
        
        # FBG Separator comboBox
        FBGSepindex=self.ui.comboBox_FBGSep.currentIndex()
        if FBGSepindex==0:
            FBGSep='\t'
        elif FBGSepindex==1:
            FBGSep=';'
        elif FBGSepindex==2:
            FBGSep=','

        # Temp Separator comboBox
        TempSepindex=self.ui.comboBox_TempSep.currentIndex()
        if TempSepindex==0:
            TempSep=';'
        elif TempSepindex==1:
            TempSep='\t'
        elif TempSepindex==2:
            TempSep=','        

                        
        #Progress Bar
        self.ui.progressBar_sync.setValue(30)  
        
        #Name the different FBGs and Thermopl
        TempColNames=['Date','Time']
        for i in range (0,NumberTemp+10):
            TempColNames.append('Thermo-'+str(i+1))
        NumberTemp=NumberTemp+2

        FBGColNames=['Date','Time','Sample']
        for i in range (0,NumberFBG+50):
            FBGColNames.append('FBG-'+str(i+1))
        NumberFBG=NumberFBG+3
       
                
        """ Send to Sync Data Class"""
        try:self.SyncData=FBG_Temp_Loading(TempPathList,InputFileTempNumber,SkipRowTemp,TempSep,NumberTemp+10,TempColNames,FBGPathList,InputFileFBGNumber,SkipRowFBG,FBGSep,NumberFBG+50,FBGColNames,TimeCorrect)
        except:
            QtGui.QMessageBox.warning(self, "Error",'Error during the data loading. Please check if the number of FBGs and Thermocouple match the files.')
            self.ui.progressBar_sync.setValue(0)
            return
            
            
        #Progress Bar
        self.ui.MessageBoard.insertPlainText('>>The files were successfully loaded. \n')
        self.ui.progressBar_sync.setValue(50)  
       
        #Sync the Data
        self.SyncData.Syncron()
        self.ui.progressBar_sync.setValue(100)     
        self.ui.MessageBoard.insertPlainText('>>The files were successfully sync. \n')     
     
        """Set the FBG and Thermocuple Selector"""
        self.ui.listWidget_SelectThermocouple.clear()
        self.ui.listWidget_SelectFBG.clear()
        
        for i in range(0,NumberTemp-2):
            nametemp='Thermo-'+str(i+1)
            self.ui.listWidget_SelectThermocouple.addItem(nametemp)
        for i in range(0,NumberFBG-3):
            nametemp='FBG-'+str(i+1)
            self.ui.listWidget_SelectFBG.addItem(nametemp)       
        
    #Push Button: Save the SyncFile
    def actionSaveSyncData(self):
        #Check if data was generated
        fsize=None
        #Size of the file
        try:fsize=len(self.SyncData.SyncData['FBG-1'])
        except:pass
    
        collums=['Increment/Sample']  
        NumberFBG=self.ui.spinBox_FBGNumber.value() #Int Number FBG
        NumberTemp=self.ui.spinBox_TempNumber.value()#Int Number Themo
        for i in range (0,NumberTemp):
            collums.append('Thermo-'+str(i+1))
        for i in range (0,NumberFBG):
            collums.append('FBG-'+str(i+1))     
    
        if fsize:
            saveFile = str(QtGui.QFileDialog.getSaveFileName(self, "Save sync data as a file.",'*.csv'))
            if saveFile!='':
                self.SyncData.SyncData.to_csv(saveFile , sep=';',cols=collums)       
        else:
            self.ui.MessageBoard.insertPlainText(">> Error!! Insert and run the data Sync (2) before saving. \n ")
            return    

    #Push Button: Residual strain calculation
    def actionResidualStrainCalcul(self):
        
        #Progress Bar
        self.ui.progressBar_residual.setValue(0)          
    
        #Check if data sync was inserted
        fsize=None
        #Size of the file
        try:fsize=len(self.SyncData.SyncData['FBG-1'])
        except:pass

        if fsize==None:
            self.ui.MessageBoard.insertPlainText(">> Error!! Please insert the FBG and Thermocouple data and sync it. (Stage (1) and (2)) \n ")
            return

        #Check if FBG and Thermoucple are selected      
        SelectedFBG=self.ui.listWidget_SelectFBG.currentRow()
        if SelectedFBG==-1:
            self.ui.MessageBoard.insertPlainText('>>ERROR in (3)!!: Please Select a FBG. \n')
            return     

        SelectedThermo=self.ui.listWidget_SelectThermocouple.currentRow()
        if SelectedThermo==-1:
            self.ui.MessageBoard.insertPlainText('>>ERROR in (3)!!: Please Select a Thermocouple. \n')
            return         
        
         #Progress Bar
        self.ui.progressBar_residual.setValue(10)

        #Check if advanced parameters are correct        
        if self.ui.lineEdit_PhotoElastic.text()=='' \
            or self.ui.lineEdit_ThermalExpansion.text()=='' \
            or self.ui.lineEdit_ThermoOptic.text()=='' \
            or self.ui.lineEdit_tolerance.text()=='' \
            or self.ui.lineEdit_TempThresh .text()=='' :
                self.ui.MessageBoard.insertPlainText('>>ERROR in (3)!!: Please insert all advanced mode parameters. \n')
                self.ui.progressBar_residual.setValue(0)
                return
                
        try:
            PhotoElastic= float(self.ui.lineEdit_PhotoElastic.text())
            ThermalExpansion= float(self.ui.lineEdit_ThermalExpansion.text())
            ThermoOptic= float(self.ui.lineEdit_ThermoOptic.text())
            tolerance= float(self.ui.lineEdit_tolerance.text())
            TempThreshold=float(self.ui.lineEdit_TempThresh.text())
            float(self.ui.lineEdit_originalwavelength.text())
        except:
            self.ui.MessageBoard.insertPlainText('>>ERROR in (3)!!: Invalid format!! --advanced mode parameters. \n')
            self.ui.progressBar_residual.setValue(0)  
            return
                  
        #FBG data format
        if self.ui.radioButton_absolutevalue.isChecked():
            FBGmode=0
            InitWave=0
        else:
            FBGmode=1
            InitWave=float(self.ui.lineEdit_originalwavelength.text())
                               
         #Progress Bar
        self.ui.progressBar_residual.setValue(20) 

        #Residual Strain Calculation         
        FBGSensorName=str(self.ui.listWidget_SelectFBG.currentItem().text())
        ThermoName=str(self.ui.listWidget_SelectThermocouple.currentItem().text())

        #Progress Bar
        self.ui.progressBar_residual.setValue(30) 
              
        try: self.ResidualData=Residual_Strain_Calc(self.SyncData.SyncData,FBGSensorName,ThermoName,PhotoElastic,ThermalExpansion,ThermoOptic,tolerance,TempThreshold,FBGmode,InitWave)
        except:
            QtGui.QMessageBox.warning(self, "Error",'Error during the residual calculation!!! Please check the inserted data.')
            self.ui.progressBar_residual.setValue(0)
            return
         
        self.ui.progressBar_residual.setValue(100) 
        #Data,FBGSensorName,ThermoName,PhotoElastic,ThermalExpansion,ThermoOptic,tolerance,TempThreshold,FBGmode,InitWave=0)
        
        
    #Push Button: Save the Residual Strain File
    def actionResidualSave(self):

        #Check if data was generated
        fsize=None
        #Size of the file
        try:fsize=len(self.ResidualData.Data['FBG-1'])
        except:pass
    
        #Collums name
        collums=['Increment/Sample']  
        NumberFBG=self.ui.spinBox_FBGNumber.value() #Int Number FBG
        NumberTemp=self.ui.spinBox_TempNumber.value()#Int Number Themo
        for i in range (0,NumberTemp):
            collums.append('Thermo-'+str(i+1))
        for i in range (0,NumberFBG):
            collums.append('FBG-'+str(i+1))        
        collums.append('ResidualStrain')
        collums.append('Eq1')
        collums.append('Eq2')
              
        if fsize:
            saveFile = str(QtGui.QFileDialog.getSaveFileName(self, "Save sync data as a file.",'*.csv'))
            if saveFile!='':
                #Create File
                with open(saveFile, 'wb') as ResultFile:
                    heading=csv.writer(ResultFile)
                    information=[['#### Residual Strain Summary ###'],['FBG sensor number:'+str(self.ResidualData.FBGSensorName)],['Thermocouple number:'+str(self.ResidualData.ThermoName)],['Final Residual Strain (Strain):  '+str(self.ResidualData.FinalResidualStrain)],['Gel Point Time : '+str(self.ResidualData.CureInitTime)],['Time until Gel Point: '+str(self.ResidualData.TimeToGelPoint)],['Max. Exothermal Peak (C): '+str(self.ResidualData.MaxExoTemp)],['####                      ###'],['']]
                    heading.writerows(information)
                    self.ResidualData.Data.to_csv(ResultFile, sep=';',cols=collums,mode="a")  
        else:
            self.ui.MessageBoard.insertPlainText(">> Error!! Run the residual strain calculation (4) before saving. \n ")
            return    

    #Push button to plot residual strain        
    def actionPlotResidual(self):
        #Check if data was generated
        try:PlotWindow(None,False,self.ResidualData).start()
        except:
            self.ui.MessageBoard.insertPlainText(">> Error!! Please calculate the residual strain before ploting. \n ")
    

"""----------------------------Class to plot: OSA tab------------------------
"""
import GUI.PlotWindow
class PlotWindow(QtDialogLoader):
    def __init__(self, parent, modal,ResidualData):
        #Local Variables
        self.ResidualData=ResidualData
        self.linewidth=0.5
        self.LineColorUndeformed='grey'
        #This will start the dialog
        ui_module = GUI.PlotWindow
        try: self.ui = ui_module.Ui_Form()  #enable autocomplete
        except: pass
        QtDialogLoader.__init__(self, ui_module, parent, modal)        

        #Start the Canvas for OSA Plot
        self.osaplot = OSACanvas()
        self.ui.gridLayout_OSA_Plot.addWidget(self.osaplot)#Insert The canvas
        #Set the Axes names        
        self.osaplot.axes.set_xlabel('Time Increment (s)',fontsize=14)
        self.osaplot.axes.set_ylabel('Residual Strain',fontsize=14)
        #Connect widget signals to actionUpdatePlot
        self.ui.spinBox_YlimMin.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox_YlimMax.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox_XlimMin.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox_XlimMax.valueChanged.connect(self.actionUpdatePlot) 
        self.ui.checkBox_legend.clicked.connect(self.actionUpdatePlot)
        self.ui.checkBox_Grid.clicked.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox_LineWidth.valueChanged.connect(self.actionUpdatePlot)
        self.ui.comboBox_LineColorUndeformed.currentIndexChanged.connect(self.actionUpdatePlot)
 
        #Plot the Spectrum
        self.osaplot.axes.hold(True)
        self.Plot()
    
    def Plot(self):
        #Plot theresidual strain
        try:self.osaplot.axes.plot(self.ResidualData.Data['ResidualStrain'],color=self.LineColorUndeformed,linewidth=self.linewidth, label="Residual Strain") 
        except:pass
        
    def actionUpdatePlot(self):
        self.ui.gridLayout_OSA_Plot.removeWidget(self.osaplot)
        self.osaplot = OSACanvas()
        self.ui.gridLayout_OSA_Plot.addWidget(self.osaplot)        
        self.osaplot.axes.hold(True)
        #Set the Axes names        
        self.osaplot.axes.set_xlabel('Time Increment (s))',fontsize=14)
        self.osaplot.axes.set_ylabel('Residual Strain',fontsize=14)        
        #Set xlimits
        self.osaplot.axes.set_xlim([self.ui.spinBox_XlimMin.value(), self.ui.doubleSpinBox_XlimMax.value()])
        #Set ylimits        
        self.osaplot.axes.set_ylim([self.ui.spinBox_YlimMin.value(), self.ui.doubleSpinBox_YlimMax.value()])
        #Set LineWidth
        self.linewidth=self.ui.doubleSpinBox_LineWidth.value()
        #Set Line Colour
        self.LineColorUndeformed=str(self.ui.comboBox_LineColorUndeformed.currentText())
       #Plot the Spectrum
        self.osaplot.axes.hold(True)
        self.Plot()
        #Legend
        if self.ui.checkBox_legend.isChecked():
            self.osaplot.axes.legend(fontsize=10, loc="best")
         #Grid
        if self.ui.checkBox_Grid.isChecked():
            self.osaplot.axes.grid()         

    def actionSavePicture(self):
        savePictureFile = str(QtGui.QFileDialog.getSaveFileName(self, "Save Plot",'*.png'))
        if savePictureFile!='':
            self.osaplot.figure.savefig(str(savePictureFile))


from PyQt4.QtGui import QSizePolicy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from matplotlib import rcParams
rcParams['font.size'] = 9

class OSACanvas(Canvas):
    """
    The same as TRCanvas
    """
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=10, height=3, dpi=100, hold=False):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Residual Strain - FBG Measurement')
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        if xscale is not None:
            self.axes.set_xscale(xscale)
        if yscale is not None:
            self.axes.set_yscale(yscale)
        if xlim is not None:
            self.axes.set_xlim(*xlim)
        if ylim is not None:
            self.axes.set_ylim(*ylim)
        self.axes.hold(hold)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
