from tkinter import *
import setup
from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *


class PersonalChat(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.header2 = Label(self, text="Personal Chat")
        self.header2.grid(row=0)

        self.chat2 = Text(self, width=25, height=10)
        self.chat2.grid(row=1, column=0, columnspan=2, sticky="nsew")

        scrollb2 = Scrollbar(self, command=self.chat2.yview)
        scrollb2.grid(row=1, column=2, sticky="nsew")
        self.chat2.configure(yscrollcommand=scrollb2.set)

        self.var2 = StringVar()

        self.msg_field2 = Entry(self, textvariable=self.var2, width=25)
        self.msg_field2.grid(row=2, column=0, pady=10)

        self.sent2 = Button(self, text="Sent", width=5, command=self.sent_msg)
        self.sent2.grid(row=2, column=1, padx=10)

    def sent_msg(self):
        msg = message(setup.current_user.first_name, self.msg_field2.get())
        # msg_queue.append(msg)
        # msg.update_chat()

        self.update(msg)

    def update(self, msg):
        self.chat2.config(state="normal")
        self.chat2.insert(INSERT, msg.display_msg())
        self.chat2.config(state="disabled")
        self.chat2.see("end")
        self.var2.set("")
