from database.database import DB
from services.interfaces.EventHandlerInterface import EventHandlerInterface
from entities.node import Node
from entities.message import *
from entities.request import *
from entities.group import *

import tkinter as tk
from tkinter import ttk


def popup_join_request():
    popup = tk.Tk()
    popup.wm_title('Invite to group')
    label = ttk.Label(
        popup, text='Would you like to join group?', font=("Helvetica", 10))
    label.pack(side='top', fill='x', pady=10)
    confirmBtn = ttk.Button(popup, text='Join', command=popup.destroy)
    cancelBtn = ttk.Button(popup, text='Cancel', command=popup.destroy)
    confirmBtn.pack()
    cancelBtn.pack()
    popup.mainloop()


class EventHandler(EventHandlerInterface):
    def nodeJoin(self, node: Node):
        # TODO: Join adhoc
        print("Join node", node)

    def nodeLeave(self, node: Node):
        # TODO: Leave adhoc
        print("Node left", node)

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        print("Receive group broadcast", b)

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        print("Receive message broadcast", msg)

    def receiveMessageGroup(self, msg: GroupMessage):
        print("Receive group message", msg)

    def receiveGroupJoinRequest(self, req: Request):
        print("Receive request to joining group", req)
        popup_join_request()

    def receiveJoinOK(self, groupID: int):
        print("Confirm joining groupID=", groupID)

    def receiveJoinDeny(self, groupID: int):
        print("Deny joining groupID=", groupID)

    def receiveMessage(self, msg: Message):
        print("Receive message", msg)
