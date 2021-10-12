#CallUI.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import os
#from scipy.signal import find_peaks
import helpfunctions
import plottingtools
#from matplotlib.figure import Figure
import functions
from PyQt5.QtWidgets import QTableWidgetItem
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backends.backend_qt5agg import (
#    FigureCanvasQTAgg as FigureCanvas,
#    NavigationToolbar2QT as NavigationToolbar)


Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")
Ui_dialog, DialogClass = uic.loadUiType("simple_dialog.ui")
Ui_sampleCreator, sampleCreatorClass = uic.loadUiType("sampleCreator.ui")

class SampleCreator(sampleCreatorClass, Ui_sampleCreator):
    def __init__(self, parent=None):
        sampleCreatorClass.__init__(self, parent)
        self.setupUi(self)


class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectActions()

    def connectActions(self):
        # Connect File actions
        print("Connecting actions")
        self.actionAbout.triggered.connect(self.printHello)
        self.actionOpen_single_specular_file.triggered.connect(self.openSpecular)
        self.DetectPeaks_button.clicked.connect(self.detectPeaks)
        self.actionOpen_SampleDB.triggered.connect(self.openSampleDB)
        self.openSampleDB_button.clicked.connect(self.openSampleDB)

    def addSample(self):
        self.addSampleWindow.show()

    def openSampleDB(self):
        self.samplelist = functions.loadSampleList(self)
        self.dialogWindow = dialogUI()
        self.addSampleWindow = SampleCreator()
        self.dialogWindow.addSample_button.clicked.connect(self.addSample)
        self.dialogWindow.SampleDBList.setColumnCount(7)
        self.dialogWindow.SampleDBList.setRowCount(len(self.samplelist))
        for i in range(len(self.samplelist)):
            #Lägga till valda val
            self.dialogWindow.SampleDBList.setItem(i, 0, QTableWidgetItem((self.samplelist[i].sampleID)))
            self.dialogWindow.SampleDBList.setItem(i, 1, QTableWidgetItem((self.samplelist[i].date)))
            self.dialogWindow.SampleDBList.setItem(i, 2, QTableWidgetItem((self.samplelist[i].layers)))
            self.dialogWindow.SampleDBList.setItem(i, 3, QTableWidgetItem((self.samplelist[i].materials)))
            self.dialogWindow.SampleDBList.setItem(i, 4, QTableWidgetItem((self.samplelist[i].comments)))
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.dialogWindow.SampleDBList.setItem(i, 6, chkBoxItem)
        self.dialogWindow.accepted.connect(self.loadSampleDB)
        self.dialogWindow.show()


    def detectPeaks(self):
        print("Detect peaks pressed")

    def loadSampleDB(self):
        #plottingtools.createcanvas(self)
        helpfunctions.clearLayout(self.SpecReflectivity_Xray)
        plottingtools.plotonCanvas(self, self.SpecReflectivity_Xray, "XraySpec")
        helpfunctions.clearLayout(self.offSpecReflectivity_Xray)
        plottingtools.plotonCanvas(self, self.offSpecReflectivity_Xray, "XrayoffSpec")
        #plotting X-ray


    def openSpecular(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Data files (*.txt, *.xy, *.dat);;All Files (*)", options=options)[0]
        filename = Path(path).name
        window = self.ReflectivityplotGrid_Xray
        XY = helpfunctions.openXY(path)
        X = XY[0]
        Y = XY[1]
        self.specfigX = helpfunctions.plotFigure(self, window, filename, X, Y)
        print(QtCore.Qt.Checked)




    def printHello(self):
        print("Hello")

class dialogUI(DialogClass, Ui_dialog):
    def __init__(self, parent=None):
        DialogClass.__init__(self, parent)
        self.setupUi(self)


def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())

