from tkinter import *
from data_class_eiei import *

class show_all_group:

    def __init__(self,root_frame,all_group):

        self.all_group = all_group

        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()

        self.entry_box =  Entry(self.inside_frame1)
        self.entry_box.grid(row = 0,column = 0)

        self.submit_btn =  Button(self.inside_frame1, text = 'New Group', command = self.add_group_tolist)
        self.submit_btn.grid(row =0,column = 1)

        self.header1 = Label(self.inside_frame1,text = "List of Group")
        self.header1.grid(row = 1,column = 0)

        self.header2 = Label(self.inside_frame1,text = "List of Member")
        self.header2.grid(row = 1,column = 1)

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
        self.all_group.add_group(group(self.entry_box.get(),4))
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


