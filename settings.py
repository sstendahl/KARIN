import CallUI
from configparser import ConfigParser
import json


def openSettingsdialog(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.settingsdialog = CallUI.settingsUI()
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(config['label'])
    self.settingsdialog.show()
    #Now mydata is a python dictionary

def showAbout(self):

    config = {"label": "self.samplelist[i].sampleID", "key2": "value2"}

    with open('config.json', 'w') as f:
        json.dump(config, f)

