#CallUI.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from pathlib import Path
import vlinetools
import helpfunctions
import sampleDB
import plottingtools


Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")
Ui_dialog, DialogClass = uic.loadUiType("simple_dialog.ui")
Ui_sampleCreator, sampleCreatorClass = uic.loadUiType("sampleCreator.ui")
Ui_removeConfirmationwindow, removeConfirmationclass = uic.loadUiType("removeConfirmation.ui")

class removeConfirmation(removeConfirmationclass, Ui_removeConfirmationwindow):
    def __init__(self, parent=None):
        removeConfirmationclass.__init__(self, parent)
        self.setupUi(self)


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
        self.peaks = []
        self.vlines = []
        self.singlespec = False
        self.wavelength = 1.5406

    def connectActions(self):
        # Connect File actions
        self.actionAbout.triggered.connect(self.printHello)
        self.actionOpen_single_specular_file.triggered.connect(self.openSpecular)
        self.DetectPeaks_button.clicked.connect(self.detectPeaks)
        self.actionOpen_SampleDB.triggered.connect(lambda: sampleDB.openSampleDB(self))
        self.actionData_tools.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(1))
        self.actionDetect_peaks.triggered.connect(self.triggerDetectpeaks)
        self.openSampleDB_button.clicked.connect(lambda: sampleDB.openSampleDB(self))
        self.addPeak_button.clicked.connect(self.addpeakButtonclick)
        self.removePeak_button.clicked.connect(self.removepeakButtonclick)
        self.dragMode_button.clicked.connect(self.dragpeakButtonclick)
        self.Insert_line_button.clicked.connect(self.insertLine_button)
        self.shortcut_SampleDB = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_SampleDB.activated.connect(lambda: sampleDB.openSampleDB(self))
        self.removeAll_button.clicked.connect(self.removeallPeaks)

    def triggerDetectpeaks(self):
        self.SpecularTools.setCurrentIndex(0)
        self.insertLine_button.setChecked(False)

    def removepeakButtonclick(self):
        self.addPeak_button.setChecked(False)
        self.dragMode_button.setChecked(False)

    def addpeakButtonclick(self):
        self.removePeak_button.setChecked(False)
        self.dragMode_button.setChecked(False)

    def dragpeakButtonclick(self):
        self.addPeak_button.setChecked(False)
        self.removePeak_button.setChecked(False)


    def removeallPeaks(self):
        vlinetools.removeAllPeaks(self)

    def insertLine_button(self):
        vlinetools.removeAllPeaks(self)
        self.figXrayspec[1].draw()

    def detectPeaks(self, event):
        self.peaks = []
        self.peaks = vlinetools.detectPeaks(self, "xray")
        vlinetools.updatePeaklist(self)
        helpfunctions.calculatePeriod(self)

    def mouserelease(self, event):
        self.mousepressed = False
        vlinetools.updatePeaklist(self)
        helpfunctions.calculatePeriod(self)

    def mousepress(self,event):
        self.mousepressed = True
        xvalue = event.xdata

        if self.addPeak_button.isChecked():
            vlinetools.addPeak(self, event)

        if self.removePeak_button.isChecked():
            vlinetools.removepeakMode(self, event)

        if self.Insert_line_button.isChecked():
            vlinetools.removeAllPeaks(self)
            vlinetools.insertLine(self, xvalue)




    def hover(self, event):
        if self.dragMode_button.isChecked() and self.mousepressed:
            vlinetools.dragpeakMode(self, event)
            vlinetools.updatePeaklist(self)

        if self.Insert_line_button.isChecked() and self.mousepressed:
            xvalue = event.xdata
            vlinetools.removeAllPeaks(self)
            vlinetools.insertLine(self, xvalue)
            self.figXrayspec[1].draw()

    def openSpecular(self):
        self.singlespec = True
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Data files (*.txt, *.xy, *.dat);;All Files (*)", options=options)[0]
        filename = Path(path).name
        XY = helpfunctions.openXY(path)
        self.Xsinglespec = XY[0]
        self.Ysinglespec = XY[1]
        helpfunctions.clearLayout(self.SpecReflectivity_Xray)
        self.figXrayspec = plottingtools.singlePlotonCanvas(self, self.SpecReflectivity_Xray, filename, self.Xsinglespec, self.Ysinglespec)
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

