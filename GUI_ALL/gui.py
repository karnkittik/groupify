import setup
from tkinter import *
import threading

## import ui
from GUI_ALL.ui.UserInformation import UserInformation
from GUI_ALL.ui.GlobalChat import GlobalChat
from GUI_ALL.ui.PersonalChat import PersonalChat
from GUI_ALL.ui.FriendList import FriendList
from GUI_ALL.ui.GroupList import GroupList
from GUI_ALL.ui.GroupChat import GroupChat


from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *

root = Tk()
root.title("Groupify")


def closeUI():
    global root
    print('Closing the app')
    print(setup.net)
    root.destroy()
    # setup.net.disconnect()


def initUI():
    global all_group
    # mock up group
    # all_group = all_group()
    # g1 = group("test1", 2)
    # g1.add_member("a")
    # g1.add_member("b")
    # g2 = group("test2", 2)
    # g2.add_member("x")
    # g2.add_member("y")
    # all_group.add_group(g1)
    # all_group.add_group(g2)

    # Initiate msg_queue
    msg_queue = []

    # Set up Main window
    # root = Tk()
    # root.title("Groupify")

    # user information
    UserInformation(root).pack()

    # group list
    group_frame = Frame()
    group_frame.pack(side=LEFT, fill=Y)
    Group_list = GroupList(group_frame, all_group)

    # friend list
    friend_frame = Frame()
    friend_frame.pack(side=LEFT, fill=Y)
    Friend_list = FriendList(friend_frame)

    side_frame = Frame()
    side_frame.pack(side=LEFT)

    #global chat
    global_chat = GlobalChat(side_frame)
    global_chat.pack(side=LEFT, pady=20, padx=20)

    group_chat = GroupChat(side_frame)
    group_chat.pack(side=LEFT, pady=20, padx=2)

    # personal pack
    # PersonalChat(side_frame).pack(side=RIGHT, pady=20, padx=20)

    # while True:
    #     if Group_list.all_group.is_change_to_view == True:
    #         Group_list.refresh_list()
    #     root.update_idletasks()
    #     root.update()
    root.protocol('WM_DELETE_WINDOW', closeUI)
    root.mainloop()
