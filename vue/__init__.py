from os import makedirs
from os.path import dirname


def getTemp(path):
    temp_file = open(path, 'r')
    temp = temp_file.read()
    temp_file.close()
    return temp


def writeToVue(pathNow, content):
    makedirs(dirname(pathNow), exist_ok=True)
    infoWr = open(pathNow, 'w')
    infoWr.write(content)
    infoWr.close()
