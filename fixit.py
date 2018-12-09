import os
import pickle

customdb = "C:/Users/andre/OneDrive/Desktop/Folders of Stuff/College/custom.tgbot"

def writeToDB(elements):
    if os.path.isfile(customdb):
        try:
            file = open(customdb, 'wb+')
            pickle.dump(elements, file)
            file.close()
        except:
            file.close()
    else:
        file = open(customdb, 'wb+')
        pickle.dump(elements, file)
        file.close()

def getDBFromFile():
    if os.path.isfile(customdb):
        file = open(customdb, 'rb')
        stuff = pickle.load(file)
        file.close()
    else:
        stuff = {}
    return stuff
newstuff = getDBFromFile()
for i in newstuff.keys():
    for u in newstuff[i].keys():
        text = newstuff[i][u]
        newstuff[i][u] = {}
        newstuff[i][u]["text"] = text
        newstuff[i][u]["photo"] = None
print(newstuff)
