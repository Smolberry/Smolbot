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
import string
import charts
import random
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

def testing(bot, update):
    if update.message.chat_id not in smol.get_users():
        smol.add_user(update)
        bot.sendMessage(update.message.chat_id, text="Hello, you've been added to the bot's database")

def stop(bot, update):
    if update.message.chat.username in smol.get_admins():
        bot.sendMessage(update.message.chat_id, text="Closing")
        updater.stop()
    else:
        if update.message.chat.type == "private":
            bot.sendMessage(update.message.chat_id, text="No, I'm not closing")
            
def addAnAdmin(bot, update, args):
    if update.message.chat.username in smol.get_admins() and update.message.chat.type == "private":
        if args[0] in smol.get_users():
            smol.add_admin(smol.get_users()[args[0]]["chatobj"])
            bot.sendMessage(chat_id=update.message.chat_id, text="%s | %s has been added as an admin" % (smol.get_users()[args[0]]["chatobj"].username, smol.get_users()[args[0]]["chatobj"].id))

def getUsersCh(bot, update):
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

def badword(bot, update):
    random.shuffle(badwords)
    update.message.reply_text(badwords[0])

def saveU(bot, update):
    tempstorage.append(update.message.reply_to_message)
    update.message.reply_text("Saved")
    
##def saveS(bot, update):
##    tempstorage.append(update)
##    print("hi")

###################
##CUSTOM COMMANDS##

def customCommands(bot, update):
    admins = update.message.chat.get_administrators()
    adminlist = []
    for i in admins:
        adminlist.append(i.user.username)
    if update.message.text != None:
        txt = update.message.text[1:]
        command, args, argslist = txt.split(' ')[0], ' '.join(txt.split(' ')[1:]), txt.split(' ')[1:]
        isadmin = False
        if update.message.chat.type != "private":
            if update.message.from_user.username in adminlist:
                isadmin = True
            if command == "add" and isadmin:
                smol.addDB(update.message.chat_id, argslist[0], ' '.join(argslist[1:]))
                update.message.reply_text("Added %s" % argslist[0])
            elif command == "remove" and isadmin:
                smol.delDB(update.message.chat_id, argslist[0])
                update.message.reply_text("Removed %s" % argslist[0])
            elif command in smol.getDB(update.message.chat_id):
                if "photo" not in smol.getDB(update.message.chat_id)[command].keys():
                    update.message.reply_text(smol.getDB(update.message.chat_id)[command]["text"])
                else:
                    if smol.getDB(update.message.chat_id)[command]["text"] != None:
                        update.message.reply_photo(smol.getDB(update.message.chat_id)[command]["photo"], smol.getDB(update.message.chat_id)[command]["text"])
                    else:
                        update.message.reply_photo(smol.getDB(update.message.chat_id)[command]["photo"])
    else:
        txt = update.message.caption[1:]
        if len(txt.split(" ")) > 1:
            command, args, argslist = txt.split(' ')[0], ' '.join(txt.split(' ')[1:]), txt.split(' ')[1:]
        else:
            command, args, argslist = txt.split(' ')[0], None, None
        isadmin = False
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
            else:
                pass
#End of commands

class Detect(BaseFilter):
    def filter(self, message):
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
                self.thingy = MessageHandler(self.cute, customCommands)
                #Actual commands
                self.__dispatcher.add_handler(self.thingy)
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
                commandlist.append(CommandHandler('start', testing))
                commandlist.append(CommandHandler('wiki', wiki, pass_args=True))
                commandlist.append(CommandHandler('stop', stop))
                commandlist.append(CommandHandler('admin', addAnAdmin, pass_args=True))
                commandlist.append(CommandHandler('users', getUsersCh))
                commandlist.append(CommandHandler('aggro', badword))
##                commandlist.append(CommandHandler('save', saveU))
    ##            commandlist.append(CommandHandler('stop', stop))
                for i in commandlist:
                    self.__dispatcher.add_handler(i)
                self.__updater.start_polling()
            except:
                self.__updater.stop()
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
        except:
            print("add_admin - Non-chat object given")
    def get_admins(self):
        return self.__variables["admins"]

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
#GUI
class TehGUI:
    def __init__(self):
        self.__window = tkinter.Tk()
        self.__topframe =tkinter.Frame(self.__window)
        self.__midframe = tkinter.Frame(self.__window)
        self.__botframe = tkinter.Frame(self.__window)
        self.__startstop = tkinter.Frame(self.__window)
        self.__radio_var = tkinter.IntVar()
        self.__radio_var.set(1)
        self.__radio_buttons = []
        self.__entry1 = tkinter.Entry(self.__topframe)
        self.__button2 = tkinter.Button(self.__topframe, text="Send", command=self.send)
##        self.__button1 = tkinter.Button(self.__midframe, text="Refresh", command=self.refresh)
        self.__stopbotb = tkinter.Button(self.__startstop, text="Stop", command=self.stopbot)
        self.__buttonre = {}
        counter = 1
        #Creates as many radio buttons as there are users
        for i in smol.get_users().keys():
            newuser = ""
            for u in smol.get_users()[i]["username"]:
                if u in string.printable:
                    newuser+=u
            self.__radio_buttons.append(tkinter.Radiobutton(self.__botframe, text=newuser, variable=self.__radio_var, value = counter))
            self.__buttonre[counter] = i
            counter += 1

        self.__button2.pack(side="left")
        self.__entry1.pack(side="left")
        if len(self.__radio_buttons) > 0:
            for i in self.__radio_buttons:
                i.pack(side="left")
        self.__stopbotb.pack()
        self.__topframe.pack()
        self.__midframe.pack()
        self.__botframe.pack()
        self.__startstop.pack()
        tkinter.mainloop()
    def send(self):
        smol.sendMessage(self.__buttonre[self.__radio_var.get()], text=self.__entry1.get())
    def stopbot(self):
        smol.get_updater().stop()
        self.__window.destroy()

smol = MainStuff()

#Uncomment if you want a crappy GUI
##gui = TehGUI()
