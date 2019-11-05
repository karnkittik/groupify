from tkinter import *


class freind_list:
     def __init__(self,root_frame):
        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()
        
        self.list_box =  Listbox(self.inside_frame1)
        self.list_box.pack()

        self.inside_frame2 = Frame(root_frame)
        self.inside_frame2.pack()

        self.chat_btn = Button(self.inside_frame2,text = "Chat") 
        self.chat_btn.pack(side = LEFT)

        self.invite_btn = Button(self.inside_frame2,text = "Invite") 
        self.invite_btn.pack(side = LEFT)



