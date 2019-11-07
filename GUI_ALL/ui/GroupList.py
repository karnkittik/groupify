from tkinter import *
import setup

# Data class
from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *

# Service
from services.group import GroupService


class GroupList:

    def __init__(self, root_frame, all_group):

        self.all_group = all_group
        self.groups = []
        self.group_id = []

        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()

        # Init group form
        self.group_name_label = Label(self.inside_frame1, text='GroupName')
        self.group_name_label.grid(row=0, column=0)

        self.name_entry_box = Entry(self.inside_frame1)
        self.name_entry_box.grid(row=0, column=1)

        self.group_limit_label = Label(self.inside_frame1, text='GroupLimit')
        self.group_limit_label.grid(row=1, column=0)

        self.limit_entry_box = Entry(self.inside_frame1)
        self.limit_entry_box.grid(row=1, column=1)

        self.submit_btn = Button(
            self.inside_frame1, text='New Group', command=self.add_group_tolist)
        self.submit_btn.grid(row=2, column=1)

        # Group List
        self.header1 = Label(self.inside_frame1, text="List of Group")
        self.header1.grid(row=3, column=0)

        self.header2 = Label(self.inside_frame1, text="List of Member")
        self.header2.grid(row=3, column=1)

        self.inside_frame2 = Frame(root_frame)
        self.inside_frame2.pack()

        self.list_box = Listbox(self.inside_frame2)
        self.list_box.pack(side=LEFT)

        self.scrollbar = Scrollbar(self.inside_frame2, orient="vertical")
        self.scrollbar.config(command=self.list_box.yview)
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.list_box.config(yscrollcommand=self.scrollbar.set)

        self.selected_node = Listbox(self.inside_frame2)
        self.selected_node.pack(side=LEFT)

        self.inside_frame3 = Frame(root_frame)
        self.inside_frame3.pack()

        # self.del_btn = Button(self.inside_frame3,text = "delete", command =self.del_list)
        # self.del_btn.pack(side = LEFT)

        self.refresh_btn = Button(
            self.inside_frame3, text="Refresh", command=self.refresh_list)
        self.refresh_btn.pack(side=LEFT)

        self.sel_btn = Button(
            self.inside_frame3, text="Check Member", command=self.selected_node_update)
        self.sel_btn.pack(side=LEFT)

        self.req_btn = Button(self.inside_frame3, text="request to join")
        self.req_btn.pack(side=LEFT)

    def add_group_tolist(self):
        # self.all_group.add_group(group(self.name_entry_box.get(), 4))
        GroupService.createGroup(
            self.name_entry_box.get(), self.limit_entry_box.get())
        self.refresh_list()
        # print(self.all_group.get_alL_group_name())

    def refresh_list(self):
        self.list_box.delete(0, END)
        # for x in self.all_group.get_alL_group_name():
        #     self.list_box.insert(END, x)
        groups = GroupService.getGroup()
        self.group_id = []
        for (groupID, name, limitPerson, quanMembers) in groups:
            self.list_box.insert(
                END, name + " (" + str(quanMembers) + '/' + str(limitPerson) + ')')
            self.group_id.append(groupID)
        # self.all_group.is_change_to_view = False
        self.inside_frame2.update()

    def del_list(self):
        rm_index = self.list_box.index(ANCHOR)
        self.all_group.del_group(rm_index)

    def selected_node_update(self):
        sel_index = self.list_box.index(ANCHOR)
        self.selected_node.delete(0, END)
        members = GroupService.getMember(self.group_id[sel_index])
        # for x in self.all_group.get_group(sel_index).group_member:
        #     self.selected_node.insert(END, x)
        for (username, firstname, lastname, faculty, year, group_id) in members:
            self.selected_node.insert(END, faculty + '#' +
                                      str(year) + ' ' + firstname + ' ' + lastname)
