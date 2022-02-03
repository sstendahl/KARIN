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
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from scipy.signal import find_peaks
import settings


Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")
Ui_dialog, DialogClass = uic.loadUiType("simple_dialog.ui")
Ui_sampleCreator, sampleCreatorClass = uic.loadUiType("sampleCreator.ui")
Ui_settingsDialog, settingsDialogClass = uic.loadUiType("settingsdialog.ui")
Ui_removeConfirmationwindow, removeConfirmationclass = uic.loadUiType("removeConfirmation.ui")
Ui_aboutWindow, aboutWindowClass = uic.loadUiType("aboutwindow.ui")


class aboutWindow(aboutWindowClass, Ui_aboutWindow):
    def __init__(self, parent=None):
        aboutWindowClass.__init__(self, parent)
        self.setupUi(self)



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
        self.peakobject = []
        self.dragPeakmode = False
        self.singlespec = False
        self.wavelength = 1.5406


    def connectActions(self):
        # Connect File actions
        self.actionAbout.triggered.connect(lambda: settings.showAbout(self))
        self.actionOpen_single_specular_file.triggered.connect(self.openSpecular)
        self.DetectPeaks_button.clicked.connect(self.detectPeaks)
        self.actionOpen_SampleDB.triggered.connect(lambda: sampleDB.openSampleDB(self))
        self.actionSettings.triggered.connect(lambda: settings.openSettingsdialog(self))
        self.actionData_tools.triggered.connect(lambda: self.SpecularTools.setCurrentIndex(1))
        self.actionDetect_peaks.triggered.connect(self.triggerDetectpeaks)
        self.openSampleDB_button.clicked.connect(lambda: sampleDB.openSampleDB(self))
        self.addPeak_button.clicked.connect(self.addpeakButtonclick)
        self.removePeak_button.clicked.connect(self.removepeakButtonclick)
        self.dragMode_button.clicked.connect(self.dragpeakButtonclick)
        self.Insert_line_button.clicked.connect(self.insertLine_pressed)
        self.shortcut_SampleDB = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_SampleDB.activated.connect(lambda: sampleDB.openSampleDB(self))
        self.removeAll_button.clicked.connect(lambda: vlinetools.removeAllPeaks(self))
        self.normalizeToSpec_button.clicked.connect(self.normalizetoSpec)
        self.centerPeak_button.clicked.connect(self.centerPeak)
        self.temp_button.clicked.connect(self.normalizeAndCenter)
        self.shortcut_settings= QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_settings.activated.connect(lambda: settings.openSettingsdialog(self))


#This function below is temporary just as a showcase. Will be removed and implemented properly later on
#This function is painfully ugly, but works as proof of concept
    def normalizeAndCenter(self, datatype):
        datatype = "xrayoffSpec"
        if datatype == "xrayoffSpec":
            layout = self.offSpecReflectivity_Xray
        helpfunctions.clearLayout(layout)
        plotWidget = plottingtools.PlotWidget(xlabel="Rocking angle ω(°)")
        for i in self.selected:
            error = False
            if datatype == "xrayoffSpec":
                title = "Off-specular X-ray scattering"
                XY_spec = helpfunctions.openXY(path=self.samplelist[i].specularpathXray)
                try:
                    XY_offspec = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
                except:
                    print(f"Could not find an off-specular data file for {self.samplelist[i].sampleID}")
                    XY_offspec = [0][0]
                    error = True
            if error == False:
                X_spec = XY_spec[0]
                Y_spec = XY_spec[1]
                X_offspec = XY_offspec[0]
                Y_offspec = XY_offspec[1]
                peakindex = list(find_peaks(np.log(Y_spec), prominence=2)[0])

                #Make sure that we haven't accidently identified the critical angle as first Bragg peak
                if X_spec[peakindex[0]] > 1:
                    peak_value =  Y_spec[peakindex[0]]
                else:
                    peak_value = Y_spec[peakindex[1]]
                normfactor = peak_value / max(Y_offspec)
                Y_offspec = [element * normfactor for element in Y_offspec]
                max_value = max(Y_offspec)
                peak_index = Y_offspec.index(max_value)
                X_offspec = [i - X_offspec[peak_index] for i in X_offspec]
                plottingtools.plotFigure(X_offspec, Y_offspec, plotWidget, self.samplelist[i].sampleID, title=title)
        canvas = plotWidget.canvas
        self.toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(canvas)
        layout.addWidget(self.toolbar)




    def centerPeak(self, datatype):
        datatype = "xrayoffSpec"
        if datatype == "xrayoffSpec":
            layout = self.offSpecReflectivity_Xray
        helpfunctions.clearLayout(layout)
        plotWidget = plottingtools.PlotWidget(xlabel="Rocking angle ω(°)")
        for i in self.selected:
            if datatype == "xrayoffSpec":
                title = "Off-specular X-ray scattering"
                XY_offspec = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
            X_offspec = XY_offspec[0]
            Y_offspec = XY_offspec[1]
            max_value = max(Y_offspec)
            peak_index = Y_offspec.index(max_value)
            X_offspec = [i - X_offspec[peak_index] for i in X_offspec]
            plottingtools.plotFigure(X_offspec, Y_offspec, plotWidget, self.samplelist[i].sampleID, title=title)
        canvas = plotWidget.canvas
        self.toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(canvas)
        layout.addWidget(self.toolbar)



#Need to clean up the next code bit and move it to correct classes
    def normalizetoSpec(self, datatype):
        #Placeholder to support neutron implementation in the future
        datatype = "xrayoffSpec"
        if datatype == "xrayoffSpec":
            layout = self.offSpecReflectivity_Xray
        helpfunctions.clearLayout(layout)
        plotWidget = plottingtools.PlotWidget(xlabel="Rocking angle ω(°)")
        for i in self.selected:
            if datatype == "xrayoffSpec":
                title = "Off-specular X-ray scattering"
                XY_spec = helpfunctions.openXY(path=self.samplelist[i].specularpathXray)
                XY_offspec = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
            X_spec = XY_spec[0]
            Y_spec = XY_spec[1]
            X_offspec = XY_offspec[0]
            Y_offspec = XY_offspec[1]
            peakindex = list(find_peaks(np.log(Y_spec), prominence=2)[0])

            #Make sure that we haven't accidently identified the critical angle as first Bragg peak
            if X_spec[peakindex[0]] > 1:
                peak_value =  Y_spec[peakindex[0]]
            else:
                print(X_spec[peakindex[0]])
                peak_value = Y_spec[peakindex[1]]
            normfactor = peak_value / max(Y_offspec)
            Y_offspec = [element * normfactor for element in Y_offspec]
            plottingtools.plotFigure(X_offspec, Y_offspec, plotWidget, self.samplelist[i].sampleID, title=title)
        canvas = plotWidget.canvas
        self.toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(canvas)
        layout.addWidget(self.toolbar)

    def triggerDetectpeaks(self):
        self.SpecularTools.setCurrentIndex(0)
        self.Insert_line_button.setChecked(False)

    def removepeakButtonclick(self):
        self.addPeak_button.setChecked(False)
        self.dragMode_button.setChecked(False)

    def addpeakButtonclick(self):
        self.removePeak_button.setChecked(False)
        self.dragMode_button.setChecked(False)

    def dragpeakButtonclick(self):
        self.addPeak_button.setChecked(False)
        self.removePeak_button.setChecked(False)

    def insertLine_pressed(self):
        vlinetools.removeAllPeaks(self)
        self.figXrayspec[1].draw()

    def detectPeaks(self, event):
        vlinetools.detectPeaks(self, "xraySpec")
        if len(self.peakobject) >= 2:
            helpfunctions.calculatePeriod(self)
        else:
            self.PeriodXray.setText(f"Period: -- Å")


    def mouserelease(self, event):
        self.mousepressed = False
        self.dragIndex = 0
        self.dragPeakmode = False
        if len(self.peakobject) > 0:
            self.peakobject.sort(key=lambda p: p.peak)
        if self.Insert_line_button.isChecked() == False and len(self.peakobject) > 1: #Calculating period from one peak only is a very bad idea and should not be condoned, hence > 1
            helpfunctions.calculatePeriod(self)
        vlinetools.updatePeaklist(self)


    def mousepress(self,event):
        self.mousepressed = True

        if self.dragMode_button.isChecked():
            for i in range(len(self.peakobject)):
                if event.xdata != None and abs(event.xdata - self.peakobject[i].peak) < 0.35:  # Make sure user is inside of plot and that peak is selected
                    self.dragPeakmode = True
                    self.dragIndex = i

        if self.addPeak_button.isChecked():
            vlinetools.addPeak(self, event)

        if self.removePeak_button.isChecked():
            vlinetools.removepeakMode(self, event)

        if self.Insert_line_button.isChecked():
            vlinetools.removeAllPeaks(self)
            vlinetools.addPeak(self, event)
            self.figXrayspec[1].draw()

    def hover(self, event):
        if self.dragMode_button.isChecked() and self.mousepressed and self.dragPeakmode == True:
            vlinetools.dragpeakMode(self, event)

        if self.Insert_line_button.isChecked() and self.mousepressed:
            vlinetools.dragVline(self, event)

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
        self.figXrayspec = plottingtools.singlePlotonCanvas(self, self.SpecReflectivity_Xray, filename, self.Xsinglespec, self.Ysinglespec, xlim=0)
        self.figXrayspec[1].mpl_connect("motion_notify_event", self.hover)
        self.figXrayspec[1].mpl_connect("button_press_event", self.mousepress)
        self.figXrayspec[1].mpl_connect("button_release_event", self.mouserelease)

class dialogUI(DialogClass, Ui_dialog):
    def __init__(self, parent=None):
        DialogClass.__init__(self, parent)
        self.setupUi(self)

class settingsUI(settingsDialogClass, Ui_settingsDialog):
    def __init__(self, parent=None):
        settingsDialogClass.__init__(self, parent)
        self.setupUi(self)

def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())

