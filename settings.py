import CallUI
from configparser import ConfigParser


def openSettingsdialog(self):
    # This function loads the SampleDB itself. Filling in the neccesary items in the TableWidget
    self.settingsdialog = CallUI.settingsUI()
    self.settingsdialog.show()
    #Now mydata is a python dictionary

    config = ConfigParser(strict=False)

    config.read('folder//file.ini')
    config.read('config.ini')
    config.set('main', 'key1', '1')
    config.set('main', 'key2', '3')
    config.set('main', 'key3', '2')
    config.set('main', 'key4', '5')

    with open('config.ini', 'w') as f:
        config.write(f)

def showAbout(self):
    self.aboutWindow = CallUI.aboutWindow()
    self.aboutWindow.show()
    config = ConfigParser()
    config.read('config.ini')
    print(config.get('main', 'key1'))  # -> "value1"
    print(config.get('main', 'key2'))  # -> "value2"
    print(config.get('main', 'key3'))  # -> "value3"

    # getfloat() raises an exception if the value is not a float
    # getint() and getboolean() also do this for their respective types
    an_int = config.getint('main', 'key1')
