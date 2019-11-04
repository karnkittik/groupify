from tkinter import *
from data_class import *
from data_class_eiei import *

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

class freind_list:
     def __init__(self,root_frame):
        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()

        self.freind_list_label = Label(self.inside_frame1,text = "Friend List")
        self.freind_list_label.pack()
        
        self.list_box =  Listbox(self.inside_frame1)
        self.list_box.pack()

        self.inside_frame2 = Frame(root_frame)
        self.inside_frame2.pack()

        self.chat_btn = Button(self.inside_frame2,text = "Chat") 
        self.chat_btn.pack(side = LEFT)

        self.invite_btn = Button(self.inside_frame2,text = "Invite") 
        self.invite_btn.pack(side = LEFT)

class show_all_group:

    def __init__(self,root_frame,all_group):

        self.all_group = all_group

        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()

        self.group_name_label = Label(self.inside_frame1, text = 'GroupName')
        self.group_name_label.grid(row = 0,column = 0)

        self.name_entry_box =  Entry(self.inside_frame1)
        self.name_entry_box.grid(row = 0,column = 1)

        self.group_limit_label = Label(self.inside_frame1, text = 'GroupLimit')
        self.group_limit_label.grid(row = 1,column = 0)

        self.limit_entry_box =  Entry(self.inside_frame1)
        self.limit_entry_box.grid(row = 1,column = 1)

        self.submit_btn =  Button(self.inside_frame1, text = 'New Group', command = self.add_group_tolist)
        self.submit_btn.grid(row =2,column = 1)

        self.header1 = Label(self.inside_frame1,text = "List of Group")
        self.header1.grid(row = 3,column = 0)

        self.header2 = Label(self.inside_frame1,text = "List of Member")
        self.header2.grid(row = 3,column = 1)

        self.inside_frame2 = Frame(root_frame)
        self.inside_frame2.pack()

        self.list_box =  Listbox(self.inside_frame2)
        self.list_box.pack(side=LEFT)

        self.scrollbar = Scrollbar(self.inside_frame2, orient="vertical")
        self.scrollbar.config(command=self.list_box.yview)
        self.scrollbar.pack(side=LEFT,fill=Y)
        self.list_box.config(yscrollcommand=self.scrollbar.set)

        self.selected_node = Listbox(self.inside_frame2)
        self.selected_node.pack(side=LEFT)

        self.inside_frame3 = Frame(root_frame)
        self.inside_frame3.pack()

        # self.del_btn = Button(self.inside_frame3,text = "delete", command =self.del_list) 
        # self.del_btn.pack(side = LEFT)

        self.sel_btn = Button(self.inside_frame3,text = "Check Member", command =self.selected_node_update) 
        self.sel_btn.pack(side = LEFT)

        self.req_btn = Button(self.inside_frame3,text = "request to join") 
        self.req_btn.pack(side = LEFT)

    def add_group_tolist(self):
        self.all_group.add_group(group(self.name_entry_box.get(),4))
        print(self.all_group.get_alL_group_name())

    def refresh_list(self):
        self.list_box.delete(0,END)
        for x in self.all_group.get_alL_group_name():
            self.list_box.insert(END,x)
        self.all_group.is_change_to_view = False

    def del_list(self):
        rm_index = self.list_box.index(ANCHOR)
        self.all_group.del_group(rm_index)

    def selected_node_update(self):
        sel_index = self.list_box.index(ANCHOR)
        self.selected_node.delete(0,END)
        for x in self.all_group.get_group(sel_index).group_member:
            self.selected_node.insert(END,x)

#Initiate a user
current_user = user()

##mock up group
all_group = all_group()
g1 = group("test1",2)
g1.add_member("a")
g1.add_member("b")
g2 = group("test2",2)
g2.add_member("x")
g2.add_member("y")
all_group.add_group(g1)
all_group.add_group(g2)

#Initiate msg_queue
msg_queue = []

#Set up Main window
root = Tk()
root.title("Groupify")

#user information 
UserInformation(root).pack()


#group list
group_frame = Frame()
group_frame.pack(side = LEFT,fill = Y)
Group_list = show_all_group(group_frame,all_group)


#friend list
friend_frame = Frame()
friend_frame.pack(side = LEFT,fill = Y)
Freind_list = freind_list(friend_frame)

side_frame = Frame()
side_frame.pack(side = LEFT)

#global chat
global_chat = GlobalChat(side_frame)
global_chat.pack(side=LEFT,pady=20, padx=20)

#global chat mock
global_chat_mock = GlobalChatMock(side_frame)
global_chat_mock.pack(pady=20, padx=20)

#personal pack
PersonalChat(side_frame).pack(side=RIGHT,pady=20, padx=20)

while True:
    if Group_list.all_group.is_change_to_view == True:
        Group_list.refresh_list()
    root.update_idletasks()
    root.update()