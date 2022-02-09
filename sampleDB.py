import helpfunctions
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import CallUI
import plottingtools
import csv
from pathlib import Path
import exportPDF
from samples import Sample

def loadEdit(self, j):
    i = getSampleIDrow(self, j)
    self.addSampleWindow.sampleIDline.setText(self.samplelist[i].sampleID)
    self.addSampleWindow.dateLine.setText(self.samplelist[i].date)
    self.addSampleWindow.layersLine.setText(self.samplelist[i].layers)
    self.addSampleWindow.materialsLine.setText(self.samplelist[i].materials)
    self.addSampleWindow.magPowerLine.setText(self.samplelist[i].magPower)
    self.addSampleWindow.depTimeLine.setText(self.samplelist[i].growthTimes)
    self.addSampleWindow.SputteringGasLine.setText(self.samplelist[i].gasses)
    self.addSampleWindow.bgPressureLine.setText(self.samplelist[i].backgroundPressure)
    self.addSampleWindow.periodLine.setText(self.samplelist[i].period)
    self.addSampleWindow.gammaLine.setText(self.samplelist[i].gamma)
    self.addSampleWindow.biasLine.setText(self.samplelist[i].bias)
    self.addSampleWindow.CommentsLine.setText(self.samplelist[i].comments)
    self.addSampleWindow.pathXraySpecLine.setText(self.samplelist[i].specularpathXray)
    self.addSampleWindow.pathOffSpecXline.setText(self.samplelist[i].offspecularpathXray)
    self.addSampleWindow.pathNspecLine.setText(self.samplelist[i].specularpathNeutron)
    self.addSampleWindow.pathOffSpecNline.setText(self.samplelist[i].offspecularpathNeutron)

def getSampleIDrow(self, i):
    sampleID = self.dialogWindow.SampleDBList.item(i, 0).text()
    for sample in range(len(self.samplelist)):
        if self.samplelist[sample].sampleID == sampleID:
            j = sample
    return j

def savetoSampleDB(self):
    period = self.periodLabel.text()[8:]
    self.confirmPeriodWindow = CallUI.confirmPeriodWindow()
    self.confirmPeriodWindow.warning_period.setText(f"The period {period} will be written to sample  {self.samplelist[int(self.selected[0])].sampleID}. Are you sure?")
    self.confirmPeriodWindow.show()
    self.confirmPeriodWindow.accepted.connect(lambda: periodAccept(self, period))

def periodAccept(self, period):
    self.samplelist[int(self.selected[0])].period = period
    writeToSampleList(self)

def editSample(self):
    i = self.dialogWindow.SampleDBList.currentRow()
    sampleID = getSampleIDrow(self, i)
    loadEdit(self,i)
    self.addSampleWindow.show()
    self.addSampleWindow.accepted.disconnect()
    self.addSampleWindow.accepted.connect(lambda: editSampleAccepted(self,i))


def editSampleAccepted(self,i):
    self.samplelist[i] = defineSample(self)
    writeToSampleList(self)
    refreshSampleDB(self)
    self.addSampleWindow.accepted.disconnect()
    self.addSampleWindow.accepted.connect(lambda: newSample(self))

def defineSample(self):
    sampleID = self.addSampleWindow.sampleIDline.displayText()
    date = self.addSampleWindow.dateLine.displayText()
    layers = self.addSampleWindow.layersLine.displayText()
    materials = self.addSampleWindow.materialsLine.displayText()
    magPower = self.addSampleWindow.magPowerLine.displayText()
    growthTimes = self.addSampleWindow.depTimeLine.displayText()
    gasses = self.addSampleWindow.SputteringGasLine.displayText()
    bgpressure = self.addSampleWindow.bgPressureLine.displayText()
    period = self.addSampleWindow.periodLine.displayText()
    gamma = self.addSampleWindow.gammaLine.displayText()
    bias = self.addSampleWindow.biasLine.displayText()
    comments = self.addSampleWindow.CommentsLine.displayText()
    specxraypath = self.addSampleWindow.pathXraySpecLine.displayText()
    offspecxraypath = self.addSampleWindow.pathOffSpecXline.displayText()
    specneutronpath = self.addSampleWindow.pathNspecLine.displayText()
    offspecneutronpath = self.addSampleWindow.pathOffSpecNline.displayText()
    newSample = Sample(sampleID=sampleID, date=date, layers=layers, materials=materials, magPower=magPower, growthTimes=growthTimes, gasses=gasses, backgroundPressure=bgpressure, period=period,
                     gamma=gamma, bias=bias, comments=comments, specularpathXray=specxraypath, offspecularpathXray=offspecxraypath, specularpathNeutron=specneutronpath,
                     offspecularpathNeutron=offspecneutronpath)
    return newSample

def newSample(self):
    newSample = defineSample(self)
    self.samplelist.append(newSample)
    self.samplelist = sorted(self.samplelist, key=lambda x: x.sampleID, reverse=False)
    writeToSampleList(self)
    refreshSampleDB(self)

def getPath(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    path = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Data files (*.txt, *.xy, *.dat);;All Files (*)", options=options)[0]
    return path

def loadSampleDB(self):
    # plottingtools.createcanvas(self)
    # This module loads when OK is pressed on the SampleDB. Loading the selected data and plotting them in the application.
    source = helpfunctions.getSource()
    self.selected = []  # To make sure unchecked items will remain unchecked
    self.shiftvertical = False
    self.normalize = False
    self.dialogWindow.SampleDBList.sortItems(0, QtCore.Qt.AscendingOrder)
    helpfunctions.clearLayout(self.SpecReflectivity_Xray)
    for i in range(len(self.samplelist)):
        if self.dialogWindow.SampleDBList.item(i, self.includeColumn).checkState() == QtCore.Qt.Checked:
            self.selected.append(i)
    if source == "x-ray":
        datatypeSpec = "xraySpec"
        titlespec = "Specular X-Ray Reflectivity"
        datatypeoffSpec = "xrayoffSpec"
        titleoffspec = "Off-specular Neutron Reflectivity"

    else:
        datatypeSpec = "neutronSpec"
        titlespec = "Specular Neutron Reflectivity"
        datatypeoffSpec = "neutronoffSpec"
        titleoffspec = "Off-specular Neutron Reflectivity"

    self.figXrayspec = plottingtools.plotonCanvas(self, self.SpecReflectivity_Xray, datatypeSpec,title=titlespec)
    self.figXrayspec[1]
    self.figXrayspec[1].mpl_connect("motion_notify_event", self.hover)
    self.figXrayspec[1].mpl_connect("button_press_event", self.mousepress)
    self.figXrayspec[1].mpl_connect("button_release_event", self.mouserelease)
    helpfunctions.clearLayout(self.offSpecReflectivity_Xray)
    self.figXrayoffspec = plottingtools.plotonCanvas(self, self.offSpecReflectivity_Xray, datatypeoffSpec,
                                                     xlabel="Rocking angle ω(°)",title=titleoffspec)

def refreshSampleDB(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.singlespec = False
    self.samplelist = helpfunctions.loadSampleList(self)
    if self.shiftvertical == True:
        self.dialogWindow.checkBox_4.setChecked(True)
    if self.normalize == True:
        self.dialogWindow.normalizeBox.setChecked(True)

    self.dialogWindow.SampleDBList.setColumnCount(11)
    i = Incrementer()
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 100)  # Width for SampleID
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 100)  # Width for date
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 50)  # Width for layers
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 170)  # Width for materials
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 75)  # Width for Period
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 225)  # Width for magnetron power
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 85)  # Width for bias
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 175)  # Column width for deposition times
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 150)  # Width for background pressure
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 250)  # Width for comments
    self.dialogWindow.SampleDBList.setColumnWidth(i(), 75)  # Width for Include column


    self.dialogWindow.SampleDBList.setRowCount(len(self.samplelist))
    for i in range(len(self.samplelist)):  # Add items to the TableWidget
        j = Incrementer()
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].sampleID)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].date)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].layers)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].materials)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].period)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].magPower)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].bias)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].growthTimes)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].backgroundPressure)))
        self.dialogWindow.SampleDBList.setItem(i, j(), QTableWidgetItem((self.samplelist[i].comments)))
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        self.includeColumn = j()
        self.dialogWindow.SampleDBList.setItem(i, self.includeColumn, chkBoxItem)
    for element in self.selected:  # Check which checkboxes were selected previously and check those
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Checked)
        self.dialogWindow.SampleDBList.setItem(element, self.includeColumn, chkBoxItem)

def openSampleDB(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.dialogWindow = CallUI.dialogUI()
    self.addSampleWindow = CallUI.SampleCreator()
    self.addSampleWindow.accepted.connect(lambda: newSample(self))
    self.dialogWindow.addSample_button.clicked.connect(lambda: addSampleButton(self))
    self.dialogWindow.exportPDF_button.clicked.connect(lambda: exportPDF.exportcsvtoPDF(self))
    self.dialogWindow.removeSample_button.clicked.connect(lambda: removeSample(self))
    self.dialogWindow.editSample_button.clicked.connect(lambda: editSample(self))
    self.addSampleWindow.openSpecXpath_button.clicked.connect(lambda: getSamplelocation(self, "specX"))
    self.addSampleWindow.openSpecNpath_button.clicked.connect(lambda: getSamplelocation(self, "specN"))
    self.addSampleWindow.openOffSpecXpath_button.clicked.connect(lambda: getSamplelocation(self, "offspecX"))
    self.addSampleWindow.openOffSpecNpath_button.clicked.connect(lambda: getSamplelocation(self, "offspecN"))
    refreshSampleDB(self)
    self.dialogWindow.accepted.connect(lambda: loadSampleDB(self))
    self.dialogWindow.show()

def addSampleButton(self):
    try:
        self.addSampleWindow.accepted.disconnect()
        self.addSampleWindow.accepted.connect(lambda: newSample(self))
    except:
        self.addSampleWindow.accepted.connect(lambda: newSample(self))
    self.addSampleWindow.show()


def getSamplelocation(self,datatype):
    path = getPath(self)
    if datatype == "specX":
        self.addSampleWindow.pathXraySpecLine.setText(path)
    if datatype == "specN":
        self.addSampleWindow.pathNspecLine.setText(path)
    if datatype == "offspecX":
        self.addSampleWindow.pathOffSpecXline.setText(path)
    if datatype == "offspecN":
        self.addSampleWindow.pathOffSpecNline.setText(path)

def removeSample(self):
    j = self.dialogWindow.SampleDBList.currentRow()
    i = getSampleIDrow(self, j)
    self.removeConfirmation = CallUI.removeConfirmation()
    self.removeConfirmation.warning_removesample.setText(f"You are about to remove {self.samplelist[i].sampleID} from the SampleDB. Are you sure?")
    self.removeConfirmation.show()
    self.removeConfirmation.accepted.connect(lambda: confirmRemoval(self,i))

def confirmRemoval(self, i):
    del self.samplelist[i]
    writeToSampleList(self)
    refreshSampleDB(self)


def writeToSampleList(self):
    with open('samplelist.csv', 'w', newline='') as file:
        file.seek(0)
        writer = csv.writer(file)
        writer.writerow(["Sample ID", "Date", "Amount of Layers", "Materials", "Magnetron Powers", "Growth Times",
                         "Inlet gasses", "Background Pressure", "Period", "Gamma ratio", "Bias", "Comments",
                         "Specular X-ray file location", "Off-specular X-Ray file location",
                         "Specular Neutron file location", "Off-specular Neutron file location", "2D Map location"])
        for i in range(len(self.samplelist)):
            writer.writerow([self.samplelist[i].sampleID, self.samplelist[i].date, self.samplelist[i].layers,
                             self.samplelist[i].materials, self.samplelist[i].magPower,
                             self.samplelist[i].growthTimes, self.samplelist[i].gasses,
                             self.samplelist[i].backgroundPressure, self.samplelist[i].period,
                             self.samplelist[i].gamma, self.samplelist[i].bias, self.samplelist[i].comments,
                             self.samplelist[i].specularpathXray, self.samplelist[i].offspecularpathXray,
                             self.samplelist[i].specularpathNeutron, self.samplelist[i].offspecularpathNeutron,
                             self.samplelist[i].superAdamMapPath])
        file.truncate()

class Incrementer:
    def __init__(self):
        self.value = -1

    def __call__(self):
        self.value += 1
        return self.value
