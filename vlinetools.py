import helpfunctions
from scipy.signal import find_peaks
import numpy as np

def detectPeaks(self, datatype):
    for i in range(len(self.vlines)):
        self.vlines[i].remove()

    self.vlines = []
    if datatype == "xray":
        XY = helpfunctions.openXY(self.samplelist[int(self.selected[0])].specularpathXray)
    X = XY[0]
    Y = XY[1]
    peakindex = list(find_peaks(np.log(Y), prominence=2)[0])
    for index in peakindex:
        insertLine(self,X[index])
    self.figXrayspec[1].draw()
    return peakindex

def removeAllPeaks(self):
    for i in range(len(self.vlines)):
        self.vlines[i].remove()
    self.vlines = []
    self.peakindex = []
    self.figXrayspec[1].draw()

def removepeakMode(self, event):
    datatype = "xray"
    if datatype == "xray":
        X = helpfunctions.openXY(self.samplelist[int(self.selected[0])].specularpathXray)[0]
    for i in range(len(self.peakindex)):
        if abs(event.xdata - X[self.peakindex[i]]) < 0.15:
            self.vlines[i].remove()
            self.peakindex.pop(i)
            self.vlines.pop(i)
            self.figXrayspec[1].draw()
            break

def insertLine(self,x):
    figure = self.figXrayspec[0]
    ax = figure.axes[0]
    self.vlines.append(ax.axvline(x, color='k', linewidth=1.0, linestyle='--'))
    self.vlines = list(self.vlines)
    self.figXrayspec[1].draw
    return self.vlines
