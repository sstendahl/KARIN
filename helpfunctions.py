import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

def openXY(path):
   X, Y = [], []
   for line in open(path, 'r'):
       values = [float(s) for s in line.split()]
       print(values)
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