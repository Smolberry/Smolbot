##@Smolberry's stuff
##Custom command db tools
##
##
##
##
import charts
import pickle
import os
customdb = "custom.tgbot"

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

def makeIndent(text):
    result = ""
    if len(text) > 2:
        for i in text[:-1]:
            result += i + "\n" \
                      ""
        result += text[-1]
    elif len(text) == 2:
        result += text[0] + "\n" \
                  ""+text[1]
    else:
        result = text[0]
    return result

def get_commands(id):
    commands = getDBFromFile()
    commandlist = []
    if id in list(commands.keys()):
        for i in list(commands[id].keys()):
            commandlist.append(i)
        result = makeIndent(commandlist)
    else:
        result = "None"
    return result

def get_commands_list(id):
    commands = getDBFromFile()
    commandlist = []
    if id in list(commands.keys()):
        for i in list(commands[id].keys()):
            commandlist.append(i)
    return commandlist

def get_all_commands():
    commands = getDBFromFile()
    commandlists = []
    counter = 0
    chatlist = []
    for i in list(commands.keys()):
        commandss = ""
        for u in list(commands[i].keys())[:-2]:
            commandss += u + ", "
        
        commandlists.append(commandss)
        chatlist.append(str(i))
    return charts.makeChart("Commands For All Chats", chatlist, commandlists)
