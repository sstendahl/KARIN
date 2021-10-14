#CallUI.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from pathlib import Path
import vlinetools
#from scipy.signal import find_peaks
import helpfunctions
import plottingtools
#from matplotlib.figure import Figure
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
        self.selected = []
        self.shiftvertical = False
        self.mousepressed = False
        self.lines = []
        self.vlines = []


    def connectActions(self):
        # Connect File actions
        self.actionAbout.triggered.connect(self.printHello)
        self.actionOpen_single_specular_file.triggered.connect(self.openSpecular)
        self.DetectPeaks_button.clicked.connect(self.detectPeaks)
        self.actionOpen_SampleDB.triggered.connect(self.openSampleDB)
        self.actionData_tools.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(1))
        self.actionDetect_peaks.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(0))
        self.openSampleDB_button.clicked.connect(self.openSampleDB)
        self.Insert_line_button.clicked.connect(self.insertLine_button)
        self.shortcut_SampleDB = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_SampleDB.activated.connect(self.openSampleDB)
        self.removeAll_button.clicked.connect(self.removeallPeaks)

    def removeallPeaks(self):
        vlinetools.removeAllPeaks(self)

    def insertLine_button(self):
        vlinetools.removeAllPeaks(self)
        self.figXrayspec[1].draw()

    def addSample(self):
        self.addSampleWindow.show()

    def openSampleDB(self):
        #This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget

        self.samplelist = helpfunctions.loadSampleList(self)
        self.dialogWindow = dialogUI()
        if self.shiftvertical == True:
            self.dialogWindow.checkBox_4.setChecked(True)
        self.addSampleWindow = SampleCreator()
        self.dialogWindow.addSample_button.clicked.connect(self.addSample)
        self.dialogWindow.SampleDBList.setColumnCount(8)
        self.dialogWindow.SampleDBList.setRowCount(len(self.samplelist))
        for i in range(len(self.samplelist)): #Add items to the TableWidget
            self.dialogWindow.SampleDBList.setItem(i, 0, QTableWidgetItem((self.samplelist[i].sampleID)))
            self.dialogWindow.SampleDBList.setItem(i, 1, QTableWidgetItem((self.samplelist[i].date)))
            self.dialogWindow.SampleDBList.setItem(i, 2, QTableWidgetItem((self.samplelist[i].layers)))
            self.dialogWindow.SampleDBList.setItem(i, 3, QTableWidgetItem((self.samplelist[i].materials)))
            self.dialogWindow.SampleDBList.setItem(i, 4, QTableWidgetItem((self.samplelist[i].bias)))
            self.dialogWindow.SampleDBList.setItem(i, 5, QTableWidgetItem((self.samplelist[i].growthTimes)))
            self.dialogWindow.SampleDBList.setItem(i, 6, QTableWidgetItem((self.samplelist[i].comments)))
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.dialogWindow.SampleDBList.setItem(i, 7, chkBoxItem)
        for element in self.selected: #Check which checkboxes were selected previously and check those
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Checked)
            self.dialogWindow.SampleDBList.setItem(element, 7, chkBoxItem)
        self.selected = [] #To make sure unchecked items will remain unchecked
        self.shiftvertical = False
        self.dialogWindow.accepted.connect(self.loadSampleDB)
        self.dialogWindow.show()


    def detectPeaks(self, event):
        self.peaks = []
        self.peaks = vlinetools.detectPeaks(self, "xray")
        helpfunctions.updatePeaklist(self)
        helpfunctions.calculatePeriod(self)

    def loadSampleDB(self):
        #plottingtools.createcanvas(self)
        #This module loads when OK is pressed on the SampleDB. Loading the selected data and plotting them in the application.
        self.dialogWindow.SampleDBList.sortItems(0, QtCore.Qt.AscendingOrder)
        helpfunctions.clearLayout(self.SpecReflectivity_Xray)
        for i in range(len(self.samplelist)):
            if self.dialogWindow.SampleDBList.item(i,7).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
                self.selected.append(i)
        self.figXrayspec = plottingtools.plotonCanvas(self, self.SpecReflectivity_Xray, "XraySpec")
        self.figXrayspec[1].mpl_connect("motion_notify_event", self.hover)
        self.figXrayspec[1].mpl_connect("button_press_event", self.mousepress)
        self.figXrayspec[1].mpl_connect("button_release_event", self.mouserelease)
        helpfunctions.clearLayout(self.offSpecReflectivity_Xray)
        self.figXrayoffspec = plottingtools.plotonCanvas(self, self.offSpecReflectivity_Xray, "XrayoffSpec")
        #plotting X-ray


    def mouserelease(self, event):
        self.mousepressed = False
        helpfunctions.updatePeaklist(self)
        helpfunctions.calculatePeriod(self)

    def mousepress(self,event):
        self.mousepressed = True
        xvalue = event.xdata

        if self.removePeak_button.isChecked():
            vlinetools.removepeakMode(self, event)

        if self.Insert_line_button.isChecked():
            vlinetools.removeAllPeaks(self)
            vlinetools.insertLine(self, xvalue)




    def hover(self, event):
        if self.dragMode_button.isChecked() and self.mousepressed:
            vlinetools.dragpeakMode(self, event)
            helpfunctions.updatePeaklist(self)

        if self.Insert_line_button.isChecked() and self.mousepressed:
            xvalue = event.xdata
            vlinetools.removeAllPeaks(self)
            vlinetools.insertLine(self, xvalue)
            self.figXrayspec[1].draw()

    def openSpecular(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Data files (*.txt, *.xy, *.dat);;All Files (*)", options=options)[0]
        filename = Path(path).name
        XY = helpfunctions.openXY(path)
        X = XY[0]
        Y = XY[1]
        helpfunctions.clearLayout(self.SpecReflectivity_Xray)
        self.figXrayspec = plottingtools.singlePlotonCanvas(self, self.SpecReflectivity_Xray, filename, X, Y)
        self.figXrayspec[1].mpl_connect("motion_notify_event", self.hover)
        self.figXrayspec[1].mpl_connect("button_press_event", self.mousepress)
        self.figXrayspec[1].mpl_connect("button_release_event", self.mouserelease)




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

