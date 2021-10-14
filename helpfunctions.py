from samples import Sample
import numpy as np
import csv

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
                newSample = Sample(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                   row[10], row[11], row[12], row[13], row[14], row[15],
                                   row[16])  # SampleID, Date, BG pressure
                samplelist.append(newSample)
    return samplelist

def calculatePeriod(self):
    m = []
    print(self.peaks)
    for i in range(len(self.peaks)):
        m.append(i+1)

    mSquared = np.square(m)
    print(mSquared)
    thetaSquared = np.square(np.sin((np.array(self.peaks) / 2) * np.pi / 180))
    print(thetaSquared)
    coef = np.polyfit(mSquared, thetaSquared, 1)
    self.xraywavelength = 1.54
    period = self.xraywavelength / (2 * np.sqrt(coef[0]))
    self.PeriodXray.setText(f"Period: {period:.2f} Å")
    pass
