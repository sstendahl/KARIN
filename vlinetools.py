import helpfunctions
from scipy.signal import find_peaks
import numpy as np

def addPeak(self, event):
    insertLine(self, event.xdata)
    self.peakobject.sort(key=lambda p: p.peak)
    self.figXrayspec[1].draw()
    updatePeaklist(self)
    if len(self.peakobject) >= 2:
        helpfunctions.calculatePeriod(self)

def detectPeaks(self, datatype):
    for i in range(len(self.peakobject)):
        self.peakobject[i].line.remove()
    self.peakobject = []
    if datatype == "xraySpec" and self.singlespec == False:
        XY = helpfunctions.openXY(self.samplelist[int(self.selected[0])].specularpathXray)
        X = XY[0]
        Y = XY[1]
    if self.singlespec == True:
        X = self.Xsinglespec
        Y = self.Ysinglespec
    peakindex = list(find_peaks(np.log(Y), prominence=2)[0])
    for index in peakindex:
        insertLine(self,X[index])
    updatePeaklist(self)
    self.figXrayspec[1].draw()

def removeAllPeaks(self):
    while True:
        try:
            for i in range(len(self.peakobject)):
                self.peakobject = []
                self.peakobject[i].line.remove()
            self.figXrayspec[1].draw()

        except:
            print("Could not remove peaks, you probably haven't defined any")
            break

        try:
            updatePeaklist(self)
            self.periodLabel.setText(f"Period: -- Å")
        except:
            print("Could not update peak list, perhaps the list does not exist?")
        self.figXrayspec[1].draw()
        break

def dragVline(self,event, datatype="XraySpec"):
    if datatype == "XraySpec":
        figure = self.figXrayspec[0]
        ax = figure.axes[0]
    self.peakobject[0].line.remove()
    self.peakobject[0].peak = event.xdata
    self.peakobject[0].line = (ax.axvline(event.xdata, color='k', linewidth=1.0, linestyle='--')) #Change the line in the list to new selected line
    self.figXrayspec[1].draw() #Refresh figure


def dragpeakMode(self, event, datatype="xraySpec"):
    if datatype == "xraySpec":
        figure = self.figXrayspec[0]
    ax = figure.axes[0]
    i = self.dragIndex
    if event.xdata == None:
        xvalue = 0
    else:
        xvalue = event.xdata

    self.peakobject[i].line.remove()
    self.peakobject[i].peak = xvalue #Change the peak position of the selected peak
    self.peakobject[i].line=(ax.axvline(xvalue, color='k', linewidth=1.0, linestyle='--')) #Change the line in the list to new selected line#Sort the peak list
    self.figXrayspec[1].draw() #Refresh figure
    updatePeaklist(self)


def removepeakMode(self, event):
    for i in range(len(self.peakobject)):
        if abs(event.xdata - self.peakobject[i].peak) < 0.15:
            self.peakobject[i].line.remove()
            self.peakobject.pop(i)
            self.figXrayspec[1].draw()
            break
    if len(self.peakobject) < 2:
        self.periodLabel.setText(f"Period: -- Å")
    updatePeaklist(self)

def insertLine(self,x, figure=None):
    if figure == None:
        figure = self.figXrayspec[0]
    else:
        figure = self.figXrayspec[0]
    print("hoi")
    ax = figure.axes[0]
    self.peakobject.append(Peak(x, ax.axvline(x, color='k', linewidth=1.0, linestyle='--')))
    return self.peakobject[-1].line

def updatePeaklist(self):
    self.peakList.clear()
    degree = u"\N{DEGREE SIGN}"
    for i in range(len(self.peakobject)):
        self.peakList.addItem(f"Theta {i + 1}: {self.peakobject[i].peak:.2f}{degree}")

class Peak:
    def __init__(self, peaks, lines):
        self.peak = peaks
        self.line = lines
