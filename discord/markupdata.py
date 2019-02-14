desc = """
#A module for custom markup storage

#<data name='name'>
#namestr: dataval(int, str, boolean, float)
#</data>

"""

import os

class data:
    def __init__(self):
        self.dicti = {}
        self.name = ""
    def addDict(self, dict):
        self.dicti.update(dict)
    def chName(self, name):
        self.name = name
class dataHandler:
    def __init__(self, filepath="data.conf"):
        self.filepath = filepath
        self.data = []
    def getConfig(self):
        if os.path.isfile(self.filepath):
            file = open(self.filepath, 'r')
            contents = file.readlines()
            file.close()
        else:
            file = open(self.filepath, 'w')
            contents = []
            file.write(desc)
            file.close()
        dicti = {}
        inData = False
        name = ""
        dat = []
        for line in contents:
            i = line.replace("\n", "")
            if inData:
                if ":" in i:
                    key, value = i.split(":")[0], ":".join(i.split(":")[1:])
                    print(key, value)
                    if key not in dicti.keys():
                        dicti[key] = value
                elif i == "</data>":
                    print("end of data")
                    newthing = data()
                    newthing.addDict(dicti)
                    dat.append(newthing)
                    newthing.chName(name)
                    dicti = {}
                    name = ""
                    inData = False
            elif i.startswith("<data"):
                print("found data")
                inData = True
                if "name=" in i:
                    if '"' in i:
                        name = i.split('name="')[1].split('"')[0]
                    elif "'" in i:
                        name = i.split("name='")[1].split("'")[0]
        return dat
    def writeConfig(self, listOfData):
        for i in listOfData:
            bigbits = []
            if isinstance(i, data):
                header = "\n<data name='%s'>" % i.name
                bits = [header]
                out = "</data>"
                for u in i.dicti.keys():
                    key, value = u, i.dicti[u]
                    if isinstance(key, str) and isinstance(value, str):
                        lilbit = "%s:%s" % (key, value)
                        bits.append(lilbit)
                    else:
                        bits.append("#%s ERR: must be a string" % key)
                bits.append(out)
                bigbits += bits
            else:
                bigbits.append("#Whatever is suppose to be here wasn't in the correct format")
        if isinstance(listOfData, list):
            if isinstance(listOfData[0], data): 
                file = open(self.filepath, 'a')
                file.write("\n".join(bigbits))
