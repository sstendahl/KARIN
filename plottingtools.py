import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import helpfunctions
from PyQt5 import QtCore

# main window

def plotFigure(self, filename, X, Y):
    plt.plot(X, Y, label=filename)
    plt.xlim(0.2, X[-1])
    plt.xlabel('Incidence angle 2θ (°)')
    plt.ylabel('Intensity (arb. u)')
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    self.canvas.draw()
    # fig = plt.figure()
    # canvas = FigureCanvas(fig)
    # window.addWidget(canvas)

def plotonCanvas(self, layout, datatypo):
    print("Hoi jongen")
    self.figure = plt.figure()
    print(type(datatypo))
    self.canvas = FigureCanvas(self.figure)
    layout.addWidget(self.canvas)
    shifter = 1
    # helpfunctions.plot2canvas(self, self.ReflectivityplotGrid_Xray)
    for i in range(len(self.samplelist)):
        if self.dialogWindow.SampleDBList.item(i,6).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
            if datatypo.__eq__("XraySpec"):
                XY = helpfunctions.openXY(path=self.samplelist[i].specularpathXray)  # load the XY data from the specular X-ray file
            elif datatypo == "XrayoffSpec":
                XY = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
            else:
                XY = [0,0]

            X = XY[0]  # split XY data
            Y = XY[1]
            if self.dialogWindow.checkBox_4.checkState() == QtCore.Qt.Checked:
                Y = [element * shifter for element in Y]
                shifter *= 100000
            plotFigure(self, self.samplelist[i].sampleID, X, Y)
    self.toolbar = NavigationToolbar(self.canvas, self)
    layout.addWidget(self.toolbar)
    plt.tight_layout()
