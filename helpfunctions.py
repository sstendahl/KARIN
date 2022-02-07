from samples import Sample
import numpy as np
import csv
import json
from PyQt5.QtWidgets import QFileDialog
import seaborn as sns


def saveFileDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                              "Portable Document Format (PDF) (*.pdf)", options=options)
    return fileName

def setSource(source):
    with open('config.json', 'r') as f:
        config = json.load(f)
    config['source'] = source
    with open('config.json', 'w') as f:
        json.dump(config, f)


def getSource():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['source'].lower()

def setGraphTheme():
    with open('config.json', 'r') as f:
        config = json.load(f)
    theme = config['theme'].lower()
    sns.set_style(theme)

def setGraphContext():
    with open('config.json', 'r') as f:
        config = json.load(f)
    context = config['context'].lower()
    sns.set_context(context)

def createLabel(self, index):
    attributes = getLabelAttributes()
    label = ""
    for item in attributes:
        if getattr(self.samplelist[index], item) != "":
            label = label + getattr(self.samplelist[index], item) + " - "
    label = label[:-3] #Remove dash in the end
    return label

def getWavelength(source):
    with open('config.json', 'r') as f:
        config = json.load(f)
        source = source.lower()
    if source == "x-ray":
        return config['xraywavelength']
    if source == "neutron":
        return config['neutronwavelength']



def getSkipdata():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['skipspecdata']

def getLabelAttributes():
    with open('config.json', 'r') as f:
        config = json.load(f)
    config = config['legend']
    attributes = []
    for key in config:
        if config.get(key) == True:
            attributes.append(key)
    return attributes


def openXY(path):
   X, Y = [], []
   for line in open(path, 'r'):
       values = [float(s) for s in line.split()]
       X.append(values[0])
       Y.append(values[1])
   XY = [X, Y]
   return XY

def multiplyList(myList, multiplier):
    for x in myList:
        result = multiplier * x
    return result

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

def loadSampleList(self):
    samplelist = []
    with open('samplelist.csv', 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                newSample = Sample(sampleID=row[0], date=row[1], layers=row[2], materials=row[3], magPower=row[4], growthTimes=row[5], gasses=row[6], backgroundPressure=row[7], period=row[8], gamma=row[9],
                                   bias=row[10], comments=row[11], specularpathXray=row[12], offspecularpathXray=row[13], specularpathNeutron=row[14], offspecularpathNeutron=row[15],
                                   superAdamMapPath=row[16])  # SampleID, Date, BG pressure
                samplelist.append(newSample)
        samplelist = sorted(samplelist, key=lambda x: x.sampleID, reverse=False)
    return samplelist

def calculatePeriod(self):
    source = getSource()
    wavelength = getWavelength(source)
    m = []
    for i in range(len(self.peakobject)):
        m.append(i+1)
    peaks = []
    for element in self.peakobject:
        peaks.append(element.peak)
    mSquared = np.square(m)
    thetaSquared = np.square(np.sin((np.array(peaks) / 2) * np.pi / 180))
    coef = np.polyfit(mSquared, thetaSquared, 1)
    period = wavelength / (2 * np.sqrt(coef[0]))
    self.PeriodXray.setText(f"Period: {period:.2f} Å")
