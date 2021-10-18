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
                newSample = Sample(sampleID=row[0], date=row[1], layers=row[2], materials=row[3], magPower=row[4], growthTimes=row[5], gasses=row[6], backgroundPressure=row[7], period=row[8], gamma=row[9],
                                   bias=row[10], comments=row[11], specularpathXray=row[12], offspecularpathXray=row[13], specularpathNeutron=row[14], offspecularpathNeutron=row[15],
                                   superAdamMapPath=row[16])  # SampleID, Date, BG pressure
                samplelist.append(newSample)
        samplelist = sorted(samplelist, key=lambda x: x.sampleID, reverse=False)
    return samplelist

def calculatePeriod(self):
    m = []
    for i in range(len(self.peaks)):
        m.append(i+1)

    mSquared = np.square(m)
    thetaSquared = np.square(np.sin((np.array(self.peaks) / 2) * np.pi / 180))
    coef = np.polyfit(mSquared, thetaSquared, 1)
    period = self.wavelength / (2 * np.sqrt(coef[0]))
    self.PeriodXray.setText(f"Period: {period:.2f} Å")
    pass
