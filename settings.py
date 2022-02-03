import CallUI
import json
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem

import helpfunctions
import sampleDB

def openSettingsdialog(self):
    self.settingsdialog = CallUI.settingsUI()
    with open('config.json', 'r') as f:
        config = json.load(f)

    legend = config['legend']
    i = 0
    self.settingsdialog.legendAttributes.setColumnWidth(0, 200)  # Width for attribute column

    for key in legend:
        if config['legend'][key] == True:
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Checked)
            self.settingsdialog.legendAttributes.setItem(i, 1, chkBoxItem)
        i = i + 1

    theme = config['theme']
    self.settingsdialog.theme.setCurrentText(theme)
    context = config['context']
    self.settingsdialog.context.setCurrentText(context)
    xraywavelength = config['xraywavelength']
    self.settingsdialog.xraywavelength.setText(str(xraywavelength))
    neutronwavelength = config['neutronwavelength']
    self.settingsdialog.neutronwavelength.setText(str(neutronwavelength))

    self.settingsdialog.show()
    self.settingsdialog.accepted.connect(lambda: loadSettings(self))

def loadSettings(self):
    writeConfig(self)
    try:
        sampleDB.loadSampleDB(self)
    except:
        print("Can't load selected samples. You probably haven't opened the SampleDB yet")


def writeConfig(self):
    with open('config.json', 'r') as f:
        config = json.load(f)

    legend = config['legend']
    i = 0
    for key in legend:
        config['legend'][key] = False
        if self.settingsdialog.legendAttributes.item(i, 1).checkState() == QtCore.Qt.Checked:
            config['legend'][key] = True
        i = i + 1

    theme = str(self.settingsdialog.theme.currentText())
    config['theme'] = theme

    context = str(self.settingsdialog.context.currentText())
    config['context'] = context

    xraywavelength = str(self.settingsdialog.xraywavelength.text())
    config['xraywavelength'] = float(xraywavelength)

    neutronwavelength = str(self.settingsdialog.neutronwavelength.text())
    config['neutronwavelength'] = float(neutronwavelength)


    # write it back to the file
    with open('config.json', 'w') as f:
        json.dump(config, f)

def showAbout(self):
    self.aboutWindow = CallUI.aboutWindow()
    self.aboutWindow.show()

