##################################################33
#
#       @Smolberry's shit
#       Written on 12/9/2018
#       last edited 12/9/2018
#

import telegram
from telegram import MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import pickle
import os
global updater
import wiki_thing
import tkinter
import tkinter.messagebox as messagebox
import string
import charts
import random
import customtools
import threading
import time
custom = {}

configpath = "config.tgbot"
usersconfigpath = "userconfig.tgbot"
customdb = "custom.tgbot"
canrun=False
users = {}
commandlist = []
file = open("badwords.txt", 'r')
badwords = []
for i in file:
    badwords.append(i.replace("\n", ""))

tempstorage = []

##BASIC CONFIG
def writeToFile(elements):
    if os.path.isfile(configpath):
        try:
            file = open(configpath, 'wb')
            pickle.dump(elements, file)
            file.close()
        except:
            file.close()
    else:
        file = open(configpath, 'wb+')
        pickle.dump(elements, file)
        file.close()
        
def getFromFile():
    if os.path.isfile(configpath):
        file = open(configpath, 'rb')
        stuff = pickle.load(file)
    else:
        stuff = {}
    return stuff
##USERS DATABASE
def writeToUsers(elements):
    if os.path.isfile(usersconfigpath):
        try:
            file = open(usersconfigpath, 'wb')
            pickle.dump(elements, file)
            file.close()
        except:
            file.close()
    else:
        file = open(usersconfigpath, 'wb+')
        pickle.dump(elements, file)
        file.close()

def getUsersFromFile():
    if os.path.isfile(usersconfigpath):
        file = open(usersconfigpath, 'rb')
        stuff = pickle.load(file)
    else:
        stuff = {}
    return stuff

##CUSTOM COMMANDS DATABASE
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

##############
##COMMANDS####

def testing(bot, update, args=None):
    if update.message.chat_id not in smol.get_users():
        smol.add_user(update)
        bot.sendMessage(update.message.chat_id, text="Hello, you've been added to the bot's database")

def stop(bot, update, args=None):
    if update.message.chat.username in smol.get_admins():
        bot.sendMessage(update.message.chat_id, text="Closing")
        updater.stop()
    else:
        if update.message.chat.type == "private":
            bot.sendMessage(update.message.chat_id, text="No, I'm not closing")
            
def addAnAdmin(bot, update, args=None):
    if update.message.chat.username in smol.get_admins() and update.message.chat.type == "private":
        if args[0] in smol.get_users():
            smol.add_admin(smol.get_users()[args[0]]["chatobj"])
            bot.sendMessage(chat_id=update.message.chat_id, text="%s | %s has been added as an admin" % (smol.get_users()[args[0]]["chatobj"].username, smol.get_users()[args[0]]["chatobj"].id))

def getUsersCh(bot, update, args=None):
    if update.message.chat.username in smol.get_admins() and update.message.chat.type == "private":
        names = []
        ids = []
        for i in smol.get_users().keys():
            if smol.get_users()[i]["chatobj"].type == "private":
                names.append("@"+smol.get_users()[i]["chatobj"].username)
            else:
                names.append(smol.get_users()[i]["chatobj"].title)
            ids.append(str(smol.get_users()[i]["chatobj"].id))
        bot.sendMessage(chat_id=update.message.chat_id, text = charts.makeChart("Users", names, ids))
    else:
        if update.message.chat.type == "private":
            bot.sendMessage(chat_id=update.message.chat_id, text="Hell nah.") 

def wiki(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=wiki_thing.search(" ".join(args)))

def badword(bot, update, args=None):
    random.shuffle(badwords)
    update.message.reply_text(badwords[0])

def saveU(bot, update, args=None):
    tempstorage.append(update.message.reply_to_message)
    update.message.reply_text("Saved")

def getCommands(bot, update, args=None):
    update.message.reply_text(customtools.makeIndent(smol.catcher.get_commands()))
    
def getActive(bot, update, args=None):
    update.message.reply_text(customtools.makeIndent(smol.catcher.get_active()))

def saveS(bot, update, args=None):
    tempstorage.append(update)
    print("hi")

###################
##CUSTOM COMMANDS##
class customStringError(Exception):
    '''Base Class for errors here'''
    pass
class notAStringError(customStringError):
    '''Raised when the input is not a string'''
    pass
class notAnUpdateError(customStringError):
    '''Raised when a non-update object is trying to be passed'''
    pass
class notABotClassError(customStringError):
    '''Raised when a non-bot object is trying to be passed'''
    pass

#Partly spaghetti
class customString:
    def __init__(self):
        self.__trace = ""
        self.__callback = self.nofunction
    def trace(self, string, callback):
        if isinstance(string, str):
            self.__trace = string
            self.__callback = callback
        else:
            raise notAStringError
    def setstr(self, string, bot,  update, args):
        if isinstance(bot, telegram.Bot):            
            if isinstance(string, str) and isinstance(update, telegram.Update):
                if string == self.__trace:
                    self.__callback(bot, update, args)
            else:
                raise notAnUpdateError
        else:
            raise notABotClassError
    def nofunction(*args):
        print("There isn't a callback")
    def getTracer():
        return self.__trace

#Should catch any code and send it out    
class customCatcher:
    def __init__(self):
        self.__registered = {}
        self.__active = []
        self.__always = []
        self.__needed = ["activate", "remove", "addgl", "remgl"]
    def initiate(self, smolobj):
        self.__smol = smolobj
    def add_command(self, string, thefunction):
        thing = customString()
        try:
            thing.trace(string, thefunction)
        except Exception as err:
            print(err)
        self.__registered[string] = thing
    def passthrough(self, string, bot, update, isadmin, args):
        if string in self.__active or string in self.__always:
            self.__registered[string].setstr(string, bot, update, args)
        elif isadmin and string in self.__needed:
            if string == "activate":
                self.activate(args[0], update)
            elif string == "remove":
                self.deactivate(args[0], update)
            elif string == "addgl":
                self.add_global(args[0], update)
            elif string == "remgl":
                self.remove_global(args[0], update)
    def activate(self, string, update):
        if isinstance(string, str):
            if string in list(self.__registered.keys()) and not string in self.__always:
                stuff = self.__smol.getVars(self)
                self.__active.append(string)
                stuff["active"].append(string)
                writeToFile(stuff)
                update.message.reply_text("Activated %s" % string)
            else:
                print("Could not activate %s" % string)
        else:
            raise notAStringError
        
    def activateB(self, string):
        if isinstance(string, str):
            if string in list(self.__registered.keys()) and not string in self.__always:
                self.__active.append(string)
            else:
                print("Could not activate %s" % string)
        else:
            raise notAStringError
        
    def deactivate(self, string, update):
        if isinstance(string, str):
            if string in list(self.__registered.keys()) and string in self.__active and not string in self.__always:
                stuff = self.__smol.getVars(self)
                self.__active.remove(string)
                stuff["active"].remove(string)
                ###
                writeToFile(stuff)
                update.message.reply_text("Deactivated %s" % string)
        else:
            raise notAStringError
        
    def add_global(self, string, update):
        if isinstance(string, str):
            stuff = self.__smol.getVars(self)
            if string in list(self.__registered.keys()) and not string in self.__active and not string in self.__always:
                self.__always.append(string)
                stuff["globals"].append(string)
                writeToFile(stuff)
                update.message.reply_text("Added %s to globals" % string)
            elif string in list(self.__registered.keys()) and not string in self.__always:
                self.deactivate(string, update)
                self.__always.append(string)
                stuff["globals"].append(string)
                writeToFile(stuff)
                update.message.reply_text("Added %s to globals" % string)
            else:
                print("Command %s is not registered" % string)
        else:
             raise notAStringError

    def add_globalB(self, string):
        if isinstance(string, str):
            stuff = self.__smol.getVars(self)
            if string in list(self.__registered.keys()) and not string in self.__active and not string in self.__always:
                self.__always.append(string)
                stuff["globals"].append(string)
            elif string in list(self.__registered.keys()) and not string in self.__always:
                self.deactivate(string)
                self.__always.append(string)
            else:
                print("Command %s is not registered" % string)
        else:
             raise notAStringError

    def remove_global(self, string, update):
        if isinstance(string, str):
            if string in list(self.__registered.keys()) and not string in self.__active and string in self.__always:
                self.__always.remove(string)
                stuff = self.__smol.getVars(self)
                stuff["globals"].remove(string)
                writeToFile(stuff)
                update.message.reply_text("Removed %s from globals" % string)
            else:
                print("Not a global command")
        else:
            raise notAStringError
    def get_active(self):
        return self.__active
    def get_commands(self):
        thelist = list(self.__registered)
        thelist.append("Always has:")
        thelist += self.__needed
        return thelist
    def get_registered(self):
        return self.__registered
    
def customCommands(bot, update):
    #Gets chat administrators and puts them into adminlist

    isadmin = False
    if update.message.from_user.username in smol.get_admins():
        isadmin = True
    #If there is text
    if update.message.text[0] == "!":
        if update.message.text != None:
            txt = update.message.text[1:]
            command, args, argslist = txt.split(' ')[0], ' '.join(txt.split(' ')[1:]), txt.split(' ')[1:]
            isadmin = False
            if update.message.chat.type != "private":
                admins = update.message.chat.get_administrators()
                adminlist = []
                for i in admins:
                    adminlist.append(i.user.username)
                if update.message.from_user.username in adminlist:
                    isadmin = True
                if command == "add" and isadmin:
                    smol.addDB(update.message.chat_id, argslist[0], ' '.join(argslist[1:]))
                    update.message.reply_text("Added %s" % argslist[0])
                elif command == "remove" and isadmin:
                    smol.delDB(update.message.chat_id, argslist[0])
                    update.message.reply_text("Removed %s" % argslist[0])
                elif command == "commands":
                    update.message.reply_text(customtools.get_commands(update.message.chat_id))
                elif command in smol.getDB(update.message.chat_id):
                    #Check if it's a photo (always skips this bc I'm too lazy to fix it)
                    if "photo" not in smol.getDB(update.message.chat_id)[command].keys():
                        update.message.reply_text(smol.getDB(update.message.chat_id)[command]["text"])
                    else:
                        #If there is text send with text
                        if smol.getDB(update.message.chat_id)[command]["text"] != None:
                            update.message.reply_photo(smol.getDB(update.message.chat_id)[command]["photo"], smol.getDB(update.message.chat_id)[command]["text"])
                        else:
                            update.message.reply_photo(smol.getDB(update.message.chat_id)[command]["photo"])
        #No text, assume it is media
        else:
            #Omitting the "!" in txt
            txt = update.message.caption[1:]
            if len(txt.split(" ")) > 1:
                command, args, argslist = txt.split(' ')[0], ' '.join(txt.split(' ')[1:]), txt.split(' ')[1:]
            else:
                command, args, argslist = txt.split(' ')[0], None, None
            isadmin = False
            #Don't run if in private messages
            if update.message.chat.type != "private":
                if update.message.from_user.username in adminlist:
                    isadmin = True
                if command == "add" and isadmin:
                    if len(txt.split(" ")) > 1:
                        smol.addDB(update.message.chat_id, argslist[0], ' '.join(argslist[1:]), photo=update.message.photo[-1], isPhoto=True)
                    else:
                        smol.addDB(update.message.chat_id, argslist[0], None, photo=update.message.photo[-1], isPhoto=True)
                    update.message.reply_text("Added %s" % argslist[0])
                elif command == "remove" and isadmin:
                    smol.delDB(update.message.chat_id, argslist[0])
                    update.message.reply_text("Removed %s" % argslist[0])
                #No one is going to run a command with a picture
                else:
                    pass
    elif update.message.text[0] == "/":
        command, args = update.message.text[1:].split(" ")[0], update.message.text.split(" ")[1:]
        if "@" in command:
            command = command.split("@")[0]
        smol.catcher.passthrough(command, bot, update, isadmin, args)
#End of commands

##Message filter

class Detect(BaseFilter):
    def filter(self, message):
        if message.text != None:
            if "!" in message.text[0] or "/" in message.text[0] or message.chat.type == "private": 
                smol.sendToGUI(message)
                return True
        if message.text != None:
            return '!' in message.text[0]
        elif message.caption != None:
            return '!' in message.caption[0]
        else:
            return False


###BOT###
class MainStuff(telegram.Bot):
    def __init__(self):
        
        self.__variables = getFromFile()
        self.__users = getUsersFromFile()
        self.isgui = False

        if "token" in self.__variables.keys():
            self.__token1 = self.__variables["token"]
            canrun=True
        else:
            print("No token, please enter the token")
            token1 = ""
            while token1 == "" or token1 == " ":
                token1 = input("Enter the token")
            self.__variables["token"] = token1
            writeToFile(self.__variables)
        #Basically checks if there's a token
        if canrun:
            try:
                telegram.Bot.__init__(self, token=self.__token1)
                self.__updater = Updater(token=self.__token1)
                self.__dispatcher = self.__updater.dispatcher
                #Handling custom commands
                self.__customdb = getDBFromFile()
                self.cute = Detect()




                
                ####Custom detector command handling
                self.catcher = customCatcher()
                self.catcher.initiate(self)
                self.catcher.add_command('start', testing)
                self.catcher.add_command('wiki', wiki)
                self.catcher.add_command('stop', stop)
                self.catcher.add_command('admin', addAnAdmin)
                self.catcher.add_command('users', getUsersCh)
                self.catcher.add_command('aggro', badword)
                self.catcher.add_command('save', saveU)
                self.catcher.add_command('commands', getCommands)
                self.catcher.add_command('active', getActive)

                if "active" in list(self.__variables):
                    for i in self.__variables["active"]:
                        self.catcher.activateB(i)
                else:
                    self.__variables["active"] = []
                    writeToFile(self.__variables)
                if "globals" in list(self.__variables.keys()):
                    for i in self.__variables["globals"]:
                        self.catcher.add_global(i)
                else:
                    self.__variables["globals"] = []
                    writeToFile(self.__variables)


                
##                self.__feed = GuiFeed()
##                self.__guifeed = MessageHandler(self.__feed, self.sendToGUI)
                self.thingy = MessageHandler(self.cute, customCommands)
                #Actual commands
                self.__dispatcher.add_handler(self.thingy)
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
##                commandlist.append(CommandHandler('start', testing))
##                commandlist.append(CommandHandler('wiki', wiki, pass_args=True))
##                commandlist.append(CommandHandler('stop', stop))
##                commandlist.append(CommandHandler('admin', addAnAdmin, pass_args=True))
##                commandlist.append(CommandHandler('users', getUsersCh))
##                commandlist.append(CommandHandler('aggro', badword))
##                commandlist.append(CommandHandler('save', saveU))
##                for i in commandlist:
##                    self.__dispatcher.add_handler(i)
                self.__updater.start_polling()
            except Exception as err:
                self.__updater.stop()
                print(err)
    def get_bot(self):
        return self.__bot
    
    def get_updater(self):
        return self.__updater

    #For adding a command to the bot (commandhandler)
    def add_command(self, command, thing):
        self.__dispatcher.add_handler(CommandHandler(command, thing))

    #For adding users to database
    def add_user(self, theobj):
        if theobj.message.chat.type == "private":
            theusername = theobj.message.from_user.full_name
        else:
            theusername = theobj.message.chat.title
        self.__users[theobj.message.chat_id] = {"username": theusername, "chatobj": theobj.message.chat}
        writeToUsers(self.__users)
        print("Added %s to the user database" % theusername)
    def get_users(self):
        return self.__users

    #Bot admins, different from chat admins
    def add_admin(self, user):
        try:
            if "admins" not in self.__variables.keys():
                if user.type == "private":
                    self.__variables["admins"] = {}
                    self.__variables["admins"][user.username] = user
                    writeToFile(self.__variables)
                else:
                    print("add_admin - Non-user was trying to be added")
            else:
                self.__variables["admins"][user.username] = user
                writeToFile(self.__variables)
        except Exception as theerror:
            print("add_admin - Non-chat object given \n%s" % theerror)
    def get_admins(self):
        if "admins" in list(self.__variables.keys()):
            return self.__variables["admins"]
        else:
            return "No admins, add one via console or smthn"

    #Custom command databases, databases are different per chat, stored in the same file
    def getDB(self, id):
        if id in self.__customdb.keys():
            result = self.__customdb[id]
        else:
            result = {}
        return result
    def addDB(self, id, command, output, photo=None, isPhoto=False):
        if id in self.__customdb.keys():
            if not isPhoto:
                self.__customdb[id][command] = {}
                self.__customdb[id][command]["text"] = output
                writeToDB(self.__customdb)
            else:
                self.__customdb[id][command] = {}
                if output != None:
                    self.__customdb[id][command]["text"] = output
                else:
                    self.__customdb[id][command]["text"] = None
                self.__customdb[id][command]["photo"] = photo
                writeToDB(self.__customdb)
        else:
            if not isPhoto:
                self.__customdb[id] = {}
                self.__customdb[id][command] = {}
                self.__customdb[id][command]["text"] = output
                writeToDB(self.__customdb)
            else:
                self.__customdb[id] = {}
                self.__customdb[id][command] = {}
                if output != None:
                    self.__customdb[id][command]["text"] = output
                self.__customdb[id][command]["photo"] = photo
                writeToDB(self.__customdb)
 
    def delDB(self, id, command):
        if id in self.__customdb.keys() and command in self.__customdb[id].keys():
            del self.__customdb[id][command]
            writeToDB(self.__customdb)
        else:
            print("Tried to delete a command that wasn't present %s" % id)


    #Sends messages to the gui
    def sendToGUI(self, message):
        if self.isgui:
            self.gui.receive(message)
    #Receives GUI object, stores it in self.gui
    def initiateGUI(self, gui):
        self.isgui = True
        self.gui = gui
        return True

    #deletes the gui and no longer sens stuff there
    def deGUI(self):
        self.isgui = False
        del self.gui
    def getVars(self, thing):
        if thing == self.catcher:
            return self.__variables
#GUI
#Established as a thread so the bot can still be mucked around with in the command line
class TehGUI(threading.Thread):
    def run(self):
        self.__window = tkinter.Tk()
        self.root = self.__window
        self.__window.title("Smolbot")
        self.__window.geometry("500x200")
        self.__window.resizable(0, 0)
        self.__sep = tkinter.Toplevel(self.__window)
        self.__topframe =tkinter.Frame(self.__window)
        self.__midframe = tkinter.Frame(self.__window)
        self.__botframe = tkinter.Frame(self.__window)

        self.__scrollbar = tkinter.Scrollbar(self.__botframe, orient=tkinter.VERTICAL)
        self.__listb = tkinter.Listbox(self.__botframe, yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__listb.yview)
        self.__entry1 = tkinter.Entry(self.__topframe)
        self.__button2 = tkinter.Button(self.__topframe, text="Send", command=self.send)
        self.__stopbotb = tkinter.Button(self.__botframe, text="Stop", command=self.stopbot)
        self.__getusersb = tkinter.Button(self.__botframe, text="Get Users", command=self.getUsers)


        #Second window

        self.chat = tkinter.StringVar()
        self.__label = tkinter.Label(self.__sep, textvariable=self.chat)
        self.__initiate = tkinter.Button(self.__topframe, text="Show Chat", command=self.initiateGUI)
        self.__buttonre = {}
        counter = 1
        for i in smol.get_users().keys():
            newuser = ""
            for u in smol.get_users()[i]["username"]:
                if u in string.printable:
                    newuser+=u
            self.__buttonre[newuser] = i
            self.__listb.insert(tkinter.END, newuser)
        self.__listb.insert(tkinter.END, "All")
        self.__button2.pack(side="left")
        self.__entry1.pack(side="left")
        self.__initiate.pack(side="left")
        self.__getusersb.pack(side="bottom")
        
        self.__scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.__listb.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)
        self.__stopbotb.pack(side=tkinter.BOTTOM)
        self.__topframe.pack(side=tkinter.LEFT)
        self.__midframe.pack(side=tkinter.LEFT)
        self.__botframe.pack(side=tkinter.RIGHT)

        #Second
        self.__label.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand=1)
        tkinter.mainloop()


    def send(self):
##        smol.sendMessage(self.__buttonre[self.__radio_var.get()], text=self.__entry1.get())
        if self.__listb.get(tkinter.ACTIVE) == "All":
            self.announce(self.__entry1.get())
        else:
            smol.sendMessage(self.__buttonre[self.__listb.get(tkinter.ACTIVE)], text=self.__entry1.get())
            thechat = self.chat.get()
            newchat = "%s: %s" % (smol.username, self.__entry1.get()) + "\n"
            self.chat.set(thechat+newchat)
    def stopbot(self):
        smol.get_updater().stop()
        self.__window.destroy()
    def receive(self, message):
        thechat = self.chat.get()
        newchat = "%s: %s" % (message.from_user.username, message.text) + "\n"
        self.chat.set(thechat+newchat)
    #Sends GUI Object
    def initiateGUI(self):
        self.chat.set("started at %s\n" % time.strftime(format("%c")))
        smol.initiateGUI(self)
    #Currently only command-line gui.deGUI()
    def deGUI(self):
        smol.deGUI()
    #Also currently only command-line
    def announce(self, message):
        counter = 5
        for i in list(smol.get_users().keys()):
            if counter > 5:
                counter = 0
                time.sleep(20)
            smol.sendMessage(i, text=message)
##            print(i, message)
    def getUsers(self):
        names = []
        ids = []
        for i in smol.get_users().keys():
            if smol.get_users()[i]["chatobj"].type == "private":
                names.append("@"+smol.get_users()[i]["chatobj"].username)
            else:
                names.append(smol.get_users()[i]["chatobj"].title)
            ids.append(str(smol.get_users()[i]["chatobj"].id))
        messagebox.showinfo("Users", charts.makeChart("Users", names, ids))
            

smol = MainStuff()

#Uncomment if you want a crappy GUI
gui = TehGUI()
gui.start()
