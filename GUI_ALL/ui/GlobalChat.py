from tkinter import *
from dateutil import tz
import setup
from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *

from services.broadcastMessage import BroadcastMessage


class GlobalChat(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.header = Label(self, text="Global Chat")
        self.header.grid(row=0)

        # self.chat = Text(self, width=25, height=10)
        self.chat = Listbox(self)
        self.chat.grid(row=1, column=0, columnspan=2, sticky="nsew")

        scrollb = Scrollbar(self, command=self.chat.yview)
        scrollb.grid(row=1, column=2, sticky="nsew")
        self.chat['yscrollcommand'] = scrollb.set

        self.var1 = StringVar()

        self.msg_field = Entry(self, textvariable=self.var1, width=25)
        self.msg_field.grid(row=2, column=0, pady=10)

        self.sent = Button(self, text="Sent", width=5, command=self.sent_msg)
        self.sent.grid(row=2, column=1, padx=10)

        self.refresh()

    def sent_msg(self):
        BroadcastMessage.send(self.msg_field.get())
        self.var1.set('')
        # self.refresh()

    def refresh(self):
        self.chat.delete(0, END)
        messages = BroadcastMessage.getAll()
        for (firstname, time, message) in messages:
            print(time)
            fromZone = tz.tzutc()
            toZone = tz.tzlocal()
            dt = datetime.strptime(
                time, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=fromZone).astimezone(toZone)
            print(dt)
            self.chat.insert(END, firstname + ': ' +
                             message + '(' + dt.strftime('%H:%M') + ')')
        self.chat.after(1000, self.refresh)
