import plottingtools
from samples import Sample
import csv
import numpy as np
from scipy.signal import find_peaks

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

def removeSingleline(self):
    if self.lines is not None:
        self.lines.remove()
        self.lines = None

def loadSampleList(self):
    samplelist = []
    with open('samplelist.csv', 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                newSample = Sample(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                   row[10], row[11], row[12], row[13], row[14], row[15],
                                   row[16])  # SampleID, Date, BG pressure
                samplelist.append(newSample)
    return samplelist

def detectPeaks(self, datatype):
    for i in range(len(self.vlines)):
        self.vlines[i].remove()

    self.vlines = []
    if datatype == "xray":
        XY = openXY(self.samplelist[int(self.selected[0])].specularpathXray)
    X = XY[0]
    Y = XY[1]
    peakindex = list(find_peaks(np.log(Y), prominence=2)[0])
    for index in peakindex:
        plottingtools.insertLineNew(self,X[index])
    self.figXrayspec[1].draw()
    return peakindex