from tkinter import *
from data_class import *

class UserInformation(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = Label(self, text="Information: ")
        self.label.grid(row=0)

        self.l1 = Label(self, text="First Name: ")
        self.l1.grid(row=1, column=0)

        self.e1 = Entry(self)
        self.e1.grid(row=1, column=1)

        self.l2 = Label(self, text="Last Name: ")
        self.l2.grid(row=1, column=2)

        self.e2 = Entry(self)
        self.e2.grid(row=1, column=3)

        self.l3 = Label(self, text="Nickname: ")
        self.l3.grid(row=1, column=4)

        self.e3 = Entry(self, width=10)
        self.e3.grid(row=1, column=5)
        
        self.l4 = Label(self, text="Year: ")
        self.l4.grid(row=1, column=6)

        self.e4 = Entry(self, width=5)
        self.e4.grid(row=1, column=7)

        self.l5 = Label(self, text="Faculty: ")
        self.l5.grid(row=1, column=8)

        self.e5 = Entry(self)
        self.e5.grid(row=1, column=9)

        self.update_button = Button(self, text="Update", command=self.update)
        self.update_button.grid(row=1, column=10, padx=10)

    def update(self):
        first_name = self.e1.get()
        last_name = self.e2.get()
        nickname = self.e3.get()
        year = self.e4.get()
        faculty = self.e5.get()

        current_user.update(first_name,last_name,nickname,year,faculty)
        print(first_name,last_name,nickname,year,faculty)

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
        msg = message(current_user.nickname,self.msg_field.get())

        self.update(msg)
        global_chat_mock.update(msg)
    
    def update(self,msg):
        self.chat.config(state="normal")
        self.chat.insert(INSERT, msg.display_msg())
        self.chat.config(state="disabled")
        self.chat.see("end")
        self.var1.set("")

class GlobalChatMock(Frame):
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
        msg = message(current_user.nickname,self.msg_field.get())

        self.update(msg)
        global_chat.update(msg)

    def update(self,msg):
        self.chat.config(state="normal")
        self.chat.insert(INSERT, msg.display_msg())
        self.chat.config(state="disabled")
        self.chat.see("end")
        self.var1.set("")

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
        self.chat2.configure(yscrollcommand = scrollb2.set)

        self.var2 = StringVar()

        self.msg_field2 = Entry(self, textvariable=self.var2, width=25)
        self.msg_field2.grid(row=2, column=0, pady=10)
        
        self.sent2 = Button(self, text="Sent", width=5, command=self.sent_msg)
        self.sent2.grid(row=2, column=1, padx=10)

    def sent_msg(self):
        msg = message(current_user.nickname,self.msg_field2.get())
        # msg_queue.append(msg)
        # msg.update_chat()

        self.update(msg)

    def update(self,msg):
        self.chat2.config(state="normal")
        self.chat2.insert(INSERT, msg.display_msg())
        self.chat2.config(state="disabled")
        self.chat2.see("end")
        self.var2.set("")

#Initiate a user
current_user = user()

#Initiate msg_queue
msg_queue = []

#Set up Main window
root = Tk()
root.title("Groupify")
# root.geometry("850x400")

side_frame = Frame()

UserInformation(root).pack()
side_frame.pack(side="right")

# GlobalChat(side_frame).pack(side="top", fill="both", pady=20, padx=20)
global_chat = GlobalChat(side_frame)
global_chat.pack(side="left",pady=20, padx=20)
# PersonalChat(side_frame).pack(side="bottom", fill="both", pady=20, padx=20)
global_chat_mock = GlobalChatMock(side_frame)
global_chat_mock.pack(pady=20, padx=20)
PersonalChat(side_frame).pack(side="right",pady=20, padx=20)

root.mainloop()