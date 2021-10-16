import helpfunctions
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import CallUI
import plottingtools
import csv
import matplotlib.pyplot as plt
from samples import Sample

def loadEdit(self, i):
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
    self.addSampleWindow.pathoffspecNline.setText(self.samplelist[i].offspecularpathNeutron)


def editSample(self):
    i = self.dialogWindow.SampleDBList.currentRow()
    loadEdit(self,i)
    self.addSampleWindow.show()
    self.addSampleWindow.accepted.disconnect()
    self.addSampleWindow.accepted.connect(lambda: editSampleAccepted(self,i))
    print(len(self.samplelist))



def editSampleAccepted(self,i):
    self.samplelist[i] = defineSample(self)
    writeToSampleList(self)
    print(len(self.samplelist))
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
    offspecneutronpath = self.addSampleWindow.pathoffspecNline.displayText()
    newSample = Sample(sampleID, date, layers, materials, magPower, growthTimes, gasses, bgpressure, period,
                     gamma, bias, comments, specxraypath, offspecxraypath, specneutronpath,
                     offspecneutronpath)
    return newSample

def newSample(self):
    newSample = defineSample(self)
    self.samplelist.append(newSample)
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
    self.dialogWindow.SampleDBList.sortItems(0, QtCore.Qt.AscendingOrder)
    helpfunctions.clearLayout(self.SpecReflectivity_Xray)
    for i in range(len(self.samplelist)):
        if self.dialogWindow.SampleDBList.item(i,
                                               7).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
            self.selected.append(i)
    self.figXrayspec = plottingtools.plotonCanvas(self, self.SpecReflectivity_Xray, "XraySpec")
    self.figXrayspec[1]
    plt.xlim(0.1)
    self.figXrayspec[1].mpl_connect("motion_notify_event", self.hover)
    self.figXrayspec[1].mpl_connect("button_press_event", self.mousepress)
    self.figXrayspec[1].mpl_connect("button_release_event", self.mouserelease)
    helpfunctions.clearLayout(self.offSpecReflectivity_Xray)
    self.figXrayoffspec = plottingtools.plotonCanvas(self, self.offSpecReflectivity_Xray, "XrayoffSpec",
                                                     xlabel="Rocking angle ω(°)")


def refreshSampleDB(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.singlespec = False
    self.samplelist = helpfunctions.loadSampleList(self)
    if self.shiftvertical == True:
        self.dialogWindow.checkBox_4.setChecked(True)
    self.dialogWindow.SampleDBList.setColumnCount(8)
    self.dialogWindow.SampleDBList.setColumnWidth(2, 50)  # Width for layers
    self.dialogWindow.SampleDBList.setColumnWidth(3, 150)  # Width for materials
    self.dialogWindow.SampleDBList.setColumnWidth(4, 80)  # Width for bias
    self.dialogWindow.SampleDBList.setColumnWidth(5, 200)  # Column width for growth times
    self.dialogWindow.SampleDBList.setColumnWidth(6, 200)  # Width for comments

    self.dialogWindow.SampleDBList.setRowCount(len(self.samplelist))
    for i in range(len(self.samplelist)):  # Add items to the TableWidget
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
    for element in self.selected:  # Check which checkboxes were selected previously and check those
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Checked)
        self.dialogWindow.SampleDBList.setItem(element, 7, chkBoxItem)
    self.selected = []  # To make sure unchecked items will remain unchecked
    self.shiftvertical = False

def openSampleDB(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.singlespec = False
    self.samplelist = helpfunctions.loadSampleList(self)
    self.dialogWindow = CallUI.dialogUI()
    if self.shiftvertical == True:
        self.dialogWindow.checkBox_4.setChecked(True)
    self.addSampleWindow = CallUI.SampleCreator()
    self.addSampleWindow.accepted.connect(lambda: newSample(self))
    self.dialogWindow.addSample_button.clicked.connect(lambda: self.addSampleWindow.show())
    self.dialogWindow.removeSample_button.clicked.connect(lambda: removeSample(self))
    self.dialogWindow.editSample_button.clicked.connect(lambda: editSample(self))
    self.dialogWindow.SampleDBList.setColumnCount(8)
    self.dialogWindow.SampleDBList.setColumnWidth(2, 50)  # Width for layers
    self.dialogWindow.SampleDBList.setColumnWidth(3, 150)  # Width for materials
    self.dialogWindow.SampleDBList.setColumnWidth(4, 80)  # Width for bias
    self.dialogWindow.SampleDBList.setColumnWidth(5, 200)  # Column width for growth times
    self.dialogWindow.SampleDBList.setColumnWidth(6, 200)  # Width for comments

    self.dialogWindow.SampleDBList.setRowCount(len(self.samplelist))
    for i in range(len(self.samplelist)):  # Add items to the TableWidget
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
    for element in self.selected:  # Check which checkboxes were selected previously and check those
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Checked)
        self.dialogWindow.SampleDBList.setItem(element, 7, chkBoxItem)
    self.selected = []  # To make sure unchecked items will remain unchecked
    self.shiftvertical = False
    self.dialogWindow.accepted.connect(lambda: loadSampleDB(self))
    self.dialogWindow.show()


def removeSample(self):
    i = self.dialogWindow.SampleDBList.currentRow()
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