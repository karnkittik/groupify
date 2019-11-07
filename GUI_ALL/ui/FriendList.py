from tkinter import *
import setup
from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *

from services.user import UserService


class FriendList:
    def __init__(self, root_frame):
        self.username = []
        self.inside_frame1 = Frame(root_frame)
        self.inside_frame1.pack()

        self.freind_list_label = Label(self.inside_frame1, text="Friend List")
        self.freind_list_label.pack()

        self.list_box = Listbox(self.inside_frame1)
        self.list_box.pack()

        self.inside_frame2 = Frame(root_frame)
        self.inside_frame2.pack()

        self.refresh_btn = Button(
            self.inside_frame2, text="Refresh", command=self.getFriends)
        self.refresh_btn.pack(side=LEFT)

        self.chat_btn = Button(self.inside_frame2, text="Chat")
        self.chat_btn.pack(side=LEFT)

        # self.invite_btn = Button(self.inside_frame2, text="Invite")
        # self.invite_btn.pack(side=LEFT)

    def getFriends(self):
        self.list_box.delete(0, END)
        self.username = []
        availableFriends = UserService.getAvailableUser()
        for (username, firstname, lastname, faculty, year) in availableFriends:
            self.username.append(username)
            self.list_box.insert(END, faculty + '#' +
                                 str(year) + ' ' + firstname + ' ' + lastname)
