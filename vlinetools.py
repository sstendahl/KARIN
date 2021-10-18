import helpfunctions
from scipy.signal import find_peaks
import numpy as np

def addPeak(self, event):
    i = 0
    line = insertLine(self, event.xdata)
    del self.vlines[-1]
    if len(self.peaks) < 3 or event.xdata > self.peaks[-1]:
        self.peaks.append(event.xdata)
        self.vlines.append(line)
    else:
        for position in self.peaks:
            if event.xdata < position:
                self.vlines.insert(i, line)
                self.peaks.insert(i, event.xdata)
                break
            i += 1
    self.figXrayspec[1].draw()
    updatePeaklist(self)


def detectPeaks(self, datatype):
    for i in range(len(self.vlines)):
        self.vlines[i].remove()

    self.vlines = []
    if datatype == "xray" and self.singlespec == False:
        XY = helpfunctions.openXY(self.samplelist[int(self.selected[0])].specularpathXray)
        X = XY[0]
        Y = XY[1]
    if self.singlespec == True:
        X = self.Xsinglespec
        Y = self.Ysinglespec
    peaks = []
    peakindex = list(find_peaks(np.log(Y), prominence=2)[0])
    for index in peakindex:
        insertLine(self,X[index])
        peaks.append(X[index])
    self.figXrayspec[1].draw()
    return peaks

def removeAllPeaks(self):
    for i in range(len(self.vlines)):
        self.vlines[i].remove()
    self.vlines = []
    self.peaks = []
    try:
        updatePeaklist(self)
        self.PeriodXray.setText(f"Period: -- Å")
    except:
        print("Could not update peak list, perhaps the list does not exist?")
    self.figXrayspec[1].draw()


def dragpeakMode(self, event, datatype="XraySpec"):
    if datatype == "XraySpec":
        figure = self.figXrayspec[0]
        ax = figure.axes[0]
    for i in range(len(self.peaks)):
        if event.xdata != None and abs(event.xdata - self.peaks[i]) < 0.35: #Make sure user is inside of plot and that peak is selected
            self.vlines[i].remove() #Remove the vertical line form plot
            self.peaks[i] = event.xdata #Change the peak on this position to the new selected position
            self.vlines[i]=(ax.axvline(event.xdata, color='k', linewidth=1.0, linestyle='--')) #Change the line in the list to new selected line
            self.vlines = list(self.vlines) #Convert vlines array to list
            self.figXrayspec[1].draw() #Refresh figure


def removepeakMode(self, event):
    for i in range(len(self.peaks)):
        if abs(event.xdata - self.peaks[i]) < 0.15:
            self.vlines[i].remove()
            self.peaks.pop(i)
            self.vlines.pop(i)
            self.figXrayspec[1].draw()
            break
    if len(self.peaks) < 2:
        self.PeriodXray.setText(f"Period: -- Å")

def insertLine(self,x):
    figure = self.figXrayspec[0]
    ax = figure.axes[0]
    self.vlines.append(ax.axvline(x, color='k', linewidth=1.0, linestyle='--'))
    self.vlines = list(self.vlines)
    self.figXrayspec[1].draw
    return self.vlines[-1]

def updatePeaklist(self):
    self.peakList.clear()
    degree = u"\N{DEGREE SIGN}"
    for i in range(len(self.peaks)):
        self.peakList.addItem(f"Theta {i + 1}: {self.peaks[i]:.2f}{degree}")

