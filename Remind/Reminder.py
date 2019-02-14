import os
import threading
import time
text = """
#REMIND MODULE
#Essentially an event handler based on time.

#-------------------------------------------


#<remind> - start of a reminder
#name: nameofreminder
#time: time to set off
#day: days to work on, seperated by commas
#interval: interval for reminder to fire off (by minutes, does not exceed 60)
#give: what to print when going off (might be redundant depending on how you use it
#</remind> - end of a reminder

#Example:

#<remind>
#name: test
#time: 01:12PM
#day: Mon,Tue,Thu,Fri
#give: hey
#</remind>

"""
def getConfig(config="remind.conf"):
    filename = config
    if os.path.isfile(filename):
        file = open(filename, 'r')
        reminders = file.readlines()
        file.close()
    else:
        file = open(filename, 'w')
        file.write(text)
        file.close()
        reminders = []
    start = "<remind>"
    name = "name: "
    time = "time: "
    interv = "interval: "
    day = "day: "
    ret = "give: "
    end = "</remind>"
    heck = [start, name, time, interv, day, ret, end]
    rems = {}
    newthing = False
    current = ""
    for i in reminders:
        if i[0] != "#":
            if i.replace("\n", "") == start and current == "":
                newthing = True
            elif newthing and name in i:
                current = i.split(name)[1].replace("\n", "")
                rems[current] = {"time": None, "interval": None, "day": None, "msg": None}
                newthing = False
            elif time in i:
                rems[current]["time"] = i.split(time)[1].replace("\n", "")
            elif interv in i:
                rems[current]["interval"] = i.split(interv)[1].replace("\n", "")
            elif day in i:
                rems[current]["day"] = i.split(day)[1].replace("\n", "").replace(" ", "").split(",")
            elif ret in i:
                rems[current]["msg"] = i.split(ret)[1].replace("\n", "")
            elif end == i.replace("\n", ""):
                current = ""
    return rems

class RemindEvent:
    def __init__(self):
        self.reminders = []
    def add(self, stuff=None):
        self.reminders.append(stuff)
    def rem(self, stuff=None):
        if stuff in self.reminders:
            self.reminders.remove(stuff)
    def fire(self, time, day, args=None):
        for remind in self.reminders:
            remind.run(time, day, args)

class Say:
    def __init__(self):
        self.message = ""
    def chmes(self, message=""):
        self.message = message
    def setName(self, name="Heck"):
        self.name = name
    # Command triggered when the time/interval is reached, can be replaced with anything as long as it can handle the argument "args"
    def run(self, args=None):
        print(self.message)

class ReminderFunct:
    def __init__(self):
        self.interval = None
        self.firetime = None
        self.action = Say()
        self.days = []
        self.matchtime = False
        self.matchday = False
    def run(self, time=None, day=None, args = None):
        if self.days == [] or day in self.days:
            self.matchday = True
        else:
            self.matchday = False
        if self.firetime == time:
            self.matchtime = True
        elif self.interval == None:
            pass
        elif int(time.split(":")[1].replace("AM", "").replace("PM", "")) % int(self.interval) == 0:
            self.matchtime = True
        if self.matchday and self.matchtime:
            self.action.run(args)
            self.matchday = False
            self.matchtime = False
class ReminderData:
    def __init__(self, config="reminder.conf", funct = ReminderFunct):
        self.currentTime = time.strftime("%I:%M%p",time.localtime())
        self.events = RemindEvent()
        self.cont = True
        self.config = getConfig(config)
        self.verbose = False
        self.Funct = funct
thing = ReminderData()
class Reminders(threading.Thread):
    def run(self):
        self.data = thing
        print("Started event handler at %s" % self.data.currentTime)
        for i in self.data.config.keys():
            newthing = self.data.Funct()
            newthing.interval = self.data.config[i]["interval"]
            newthing.days = self.data.config[i]["day"]
            newthing.firetime = self.data.config[i]["time"]
            newthing.action.chmes(self.data.config[i]["msg"])
            newthing.action.setName(i)
            self.data.events.add(newthing)
        self.startLoop()
    def startLoop(self):
        while self.data.cont:
            self.data.currentTime = time.strftime("%I:%M%p",time.localtime())
            self.data.day = time.strftime("%a", time.localtime())
            if self.data.verbose:
                print(self.data.currentTime + ", " + self.data.day)
            #Runs a command in the event handler, if the time and day match it runs any according events, any function ran will be in self.events.reminders[#].action.run
            self.data.events.fire(self.data.currentTime, self.data.day)
            time.sleep(60)
    def stopLoop(self):
        self.data.cont = False
    def verboseOn(self):
        self.data.verbose = True
    def verboseOff(self):
        self.data.verbose = False
if __name__ == '__main__':
    main = Reminders()
    main.start()
