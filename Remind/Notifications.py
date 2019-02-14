import Reminder
from win10toast import ToastNotifier

class Notification(Reminder.Say):
    def __init__(self):
        Reminder.Say.__init__(self)
        self.toast = ToastNotifier()
    def run(self, args=None):
        self.toast.show_toast(self.name, self.message, threaded=True)
class NotificationsFunct(Reminder.ReminderFunct):
    def __init__(self):
        Reminder.ReminderFunct.__init__(self)
        self.action = Notification()

heck = Reminder.Reminders()
Reminder.thing.Funct = NotificationsFunct
Reminder.thing.config = Reminder.getConfig("notifications.conf")
heck.start()
