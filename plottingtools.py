from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import helpfunctions
import seaborn as sns
from PyQt5 import QtCore
# main window

def plotFigure(self, filename, X, Y):
    sns.set()
    plt.plot(X, Y, label=filename)
    plt.xlim(0.1, X[-1])
    plt.xlabel('Incidence angle 2θ (°)')
    plt.ylabel('Intensity (arb. u)')
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    #self.canvas.draw()
    # fig = plt.figure()
    # canvas = FigureCanvas(fig)
    # window.addWidget(canvas)

def singlePlotonCanvas(self, layout, filename, X,Y):
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)
    plotFigure(self, filename, X, Y)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas



def plotonCanvas(self, layout, datatype):
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)
    shifter = 1
    # helpfunctions.plot2canvas(self, self.ReflectivityplotGrid_Xray)
    for i in range(len(self.samplelist)):
        if self.dialogWindow.SampleDBList.item(i,6).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
            try:
                if datatype.__eq__("XraySpec"):
                    XY = helpfunctions.openXY(path=self.samplelist[i].specularpathXray)  # load the XY data from the specular X-ray file
                elif datatype == "XrayoffSpec":
                    XY = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
                else:
                    XY = [[0],[0]]
            except:
                print("Can't open corresponding file, make sure it exists")
                XY = [[0], [0]]

            X = XY[0]  # split XY data
            Y = XY[1]
            if self.dialogWindow.checkBox_4.checkState() == QtCore.Qt.Checked: #if shifted vertically is checked
                Y = [element * shifter for element in Y]
                shifter /= 100000 #Divide each subsequent plot by 100k to shift them on log scale. Divide to make sure legend is in right order
                plotFigure(self, self.samplelist[i].sampleID, X, Y)
                plt.yticks([])
            else:
                plotFigure(self, self.samplelist[i].sampleID, X, Y)
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    figurecanvas = [figure, canvas]
    return figurecanvas

def insertLine(self,x):
    figure = self.figXrayspec[0]
    ax = figure.axes[0]
    self.lines = ax.axvline(x, color='k', linewidth=1.0, linestyle='--')