import CallUI
import json
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem
import sampleDB

def openSettingsdialog(self):
    self.settingsdialog = CallUI.settingsUI()
    with open('config.json', 'r') as f:
        config = json.load(f)

    legend = config['legend'][0]
    i = 0
    self.settingsdialog.legendAttributes.setColumnWidth(0, 200)  # Width for attribute column

    for key in legend:
        if config['legend'][0][key] == True:
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Checked)
            self.settingsdialog.legendAttributes.setItem(i, 1, chkBoxItem)
        i = i + 1


    self.settingsdialog.show()
    self.settingsdialog.accepted.connect(lambda: loadSettings(self))

def loadSettings(self):
    print("loading settings")
    writeConfig(self)
    sampleDB.loadSampleDB(self)


def writeConfig(self):
    with open('config.json', 'r') as f:
        config = json.load(f)

    legend = config['legend'][0]
    attributes = []
    i = 0
    for key in legend:
        config['legend'][0][key] = False
        if self.settingsdialog.legendAttributes.item(i, 1).checkState() == QtCore.Qt.Checked:
            print(f"Number {i} was checked!")
            config['legend'][0][key] = True
        i = i + 1

    # write it back to the file
    with open('config.json', 'w') as f:
        json.dump(config, f)

def showAbout(self):
    data = {
        'legend': [
            {
                'sampleID': True,
                'backgroundPressure': True,
                'magPower': True,
                'comments': True
            }]
    }

    with open('config.json', 'w') as f:
        json.dump(data, f)

