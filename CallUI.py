#CallUI.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from pathlib import Path
#from scipy.signal import find_peaks
import helpfunctions
import plottingtools
#from matplotlib.figure import Figure
import functions
import mplcursors
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
        self.mousepressed = False


    def connectActions(self):
        # Connect File actions
        self.actionAbout.triggered.connect(self.printHello)
        self.actionOpen_single_specular_file.triggered.connect(self.openSpecular)
        self.DetectPeaks_button.clicked.connect(self.detectPeaks)
        self.actionOpen_SampleDB.triggered.connect(self.openSampleDB)
        self.actionData_tools.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(1))
        self.actionDetect_peaks.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(0))
        self.openSampleDB_button.clicked.connect(self.openSampleDB)
        self.Insert_line_button.clicked.connect(self.insertLine)
        self.shortcut_SampleDB = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_SampleDB.activated.connect(self.openSampleDB)

    def insertLine(self):
        try:
            self.lines.remove()
            self.figXrayspec[1].draw()
        except:
            print("No lines to remove")

    def addSample(self):
        self.addSampleWindow.show()

    def openSampleDB(self):
        #item = self.ui.tableWidget.item(lastIndex, 0)
        #self.ui.tableWidget.scrollToItem(item, QtGui.QAbstractItemView.PositionAtTop)
        #self.ui.tableWidget.selectRow(lastIndex)
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
        for element in self.selected:
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Checked)
            self.dialogWindow.SampleDBList.setItem(element, 6, chkBoxItem)
        self.selected = []
        self.dialogWindow.accepted.connect(self.loadSampleDB)
        self.dialogWindow.show()


    def detectPeaks(self, event):
        print("Detect peaks pressed")

    def loadSampleDB(self):
        #plottingtools.createcanvas(self)
        self.dialogWindow.SampleDBList.sortItems(0, QtCore.Qt.AscendingOrder)
        helpfunctions.clearLayout(self.SpecReflectivity_Xray)
        for i in range(len(self.samplelist)):
            if self.dialogWindow.SampleDBList.item(i,6).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
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


    def mousepress(self,event):
        self.mousepressed = True
        xvalue = event.xdata
        if self.Insert_line_button.isChecked():
            try:
                self.lines.remove()
            except:
                print("No lines to remove")
            plottingtools.insertLine(self, xvalue)
            self.figXrayspec[1].draw()




    def hover(self, event):
        if self.Insert_line_button.isChecked() and self.mousepressed:
            xvalue = event.xdata
            try:
                self.lines.remove()
            except:
                print("No lines to remove")
            plottingtools.insertLine(self, xvalue)
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

