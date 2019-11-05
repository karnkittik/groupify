from tkinter import *
import setup
from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *


class GlobalChat(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.header = Label(self, text="Global Chat")
        self.header.grid(row=0)

        self.chat = Text(self, width=25, height=10)
        self.chat.grid(row=1, column=0, columnspan=2, sticky="nsew")

        scrollb = Scrollbar(self, command=self.chat.yview)
        scrollb.grid(row=1, column=2, sticky="nsew")
        self.chat['yscrollcommand'] = scrollb.set

        self.var1 = StringVar()

        self.msg_field = Entry(self, textvariable=self.var1, width=25)
        self.msg_field.grid(row=2, column=0, pady=10)

        self.sent = Button(self, text="Sent", width=5, command=self.sent_msg)
        self.sent.grid(row=2, column=1, padx=10)

    def sent_msg(self):
        msg = message(setup.current_user.first_name, self.msg_field.get())

        self.update(msg)

    def update(self, msg):
        self.chat.config(state="normal")
        self.chat.insert(INSERT, msg.display_msg())
        self.chat.config(state="disabled")
        self.chat.see("end")
        self.var1.set("")
