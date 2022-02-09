from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import helpfunctions
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure
from PyQt5 import QtCore
import CallUI
import plottingtools

def showPeriodGraph(self):
    while True:
        self.periodGraph = CallUI.periodGraph()
        layout = self.periodGraph.periodGraph
        helpfunctions.clearLayout(self.periodGraph.periodGraph)
        try:
            XY = helpfunctions.calculatePeriod(self)
        except:
            "Could not calculate period, make sure the sample is loaded"
            break
        print(min(XY[0]))
        X = np.linspace(min(XY[0]),max(XY[0]),100)
        Y = XY[2][0]*X + XY[2][1]
        plotWidget = PlotWidget(xlabel="m squared", ylabel="theta squared")
        # 100 linearly spaced numbers
        x = np.linspace(-5, 5, 100)
        plotFigure(XY[0], XY[1], plotWidget, scale="linear", marker ="o", linestyle=None, filename="Peaks")
        plotFigure(X, Y, plotWidget, scale="linear", filename="Fit")

        figure = plotWidget.figure
        canvas = plotWidget.canvas

        layout.addWidget(canvas)
        self.periodGraph.show()
        break

def singlePlotonCanvas(self, layout, filename, X, Y, xlim=None, scale="log", marker=None):
    canvas = PlotWidget(xlabel="Incidence angle 2θ (°)")
    figure = canvas.figure
    plotFigure(X, Y, canvas, filename, xlim, scale=scale, marker=marker)
    layout.addWidget(canvas)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas


def plotonCanvas(self, layout, datatype="xraySpec", xlabel="Incidence angle 2θ (°)", title="", scale="log"):
    shifter = 1
    plotWidget = PlotWidget(xlabel=xlabel)
    for i in self.selected:
        error = False
        if self.dialogWindow.SampleDBList.item(i,
                                               self.includeColumn).checkState() == QtCore.Qt.Checked:  # checks for every box if they're checked
            try:
                if datatype.__eq__("xraySpec"):
                    XY = helpfunctions.openXY(
                        path=self.samplelist[i].specularpathXray)  # load the XY data from the specular X-ray file
                    xlim = 0
                elif datatype.__eq__("neutronSpec"):
                    XY = helpfunctions.openXY(
                        path=self.samplelist[i].specularpathNeutron)  # load the XY data from the specular neutron file
                    xlim = 0
                elif datatype.__eq__("neutronoffSpec"):
                    XY = helpfunctions.openXY(
                        path=self.samplelist[i].offspecularpathNeutron)  # load the XY data from the specular neutron file
                    xlim = None
                elif datatype == "xrayoffSpec":
                    XY = helpfunctions.openXY(path=self.samplelist[i].offspecularpathXray)
                    xlim = None
                else:
                    XY = [[0], [0]]
            except:
                error = True
                print("I was unable to open reflectivity file.")
                XY = [[0], [0]]

            X = XY[0]  # split XY data
            Y = XY[1]
            skip = int(self.dialogWindow.skipdata.text())
            Y = Y[skip:]
            X = X[skip:]
            legend = helpfunctions.createLabel(self, i)
            if not error:
                if self.dialogWindow.normalizeBox.checkState() == QtCore.Qt.Checked:
                    self.normalize = True
                    Y = [element / max(Y) for element in Y]
                if self.dialogWindow.checkBox_4.checkState() == QtCore.Qt.Checked:  # if shifted vertically is checked
                    self.shiftvertical = True
                    Y = [element * shifter for element in Y]
                    shifter /= 100000  # Divide each subsequent plot by 100k to shift them on log scale. Divide to make sure legend is in right order
                    plotWidget.theplot.set_yticks([])
                plotFigure(X, Y, plotWidget, legend, xlim, title)

    figure = plotWidget.figure
    canvas = plotWidget.canvas
    self.toolbar = NavigationToolbar(canvas, self)

    layout.addWidget(canvas)
    layout.addWidget(self.toolbar)

    figurecanvas = [figure, canvas]
    return figurecanvas


def plotFigure(X, Y, canvas, filename="", xlim=None, title="", scale="log",marker=None, linestyle="solid"):
    fig = canvas.theplot
    fig.plot(X, Y, label=filename, marker=marker, linestyle=linestyle)
    canvas.theplot.legend()
    canvas.theplot.set_title(title)
    canvas.theplot.set_xlim(xlim)
    print(scale)
    canvas.theplot.set_yscale(scale)



class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xlabel=None, ylabel='Intensity (arb. u)', title="", scale="log"):
        super(PlotWidget, self).__init__(Figure())
        sns.set()
        helpfunctions.setGraphTheme()
        helpfunctions.setGraphContext()
        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.theplot = self.figure.add_subplot(111)
        self.theplot.set_yscale(scale)
        self.theplot.set_title(title)
        self.theplot.set_xlabel(xlabel)
        self.theplot.set_ylabel(ylabel)
        self.figure.set_tight_layout(True)
