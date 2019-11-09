import logging
from database.database import DB
from services.interfaces.EventHandlerInterface import EventHandlerInterface
from entities.node import Node
from entities.message import *
from entities.request import *
from entities.group import *

from services.user import UserService
from services.group import GroupService

import tkinter as tk
from tkinter import ttk


def popup_join_request(name):
    popup = tk.Tk()
    popup.wm_title('Request to group')
    label = ttk.Label(
        popup, text=name + ' would like to join your group. Accept?', font=("Helvetica", 10))
    label.pack(side='top', fill='x', pady=10)
    confirmBtn = ttk.Button(popup, text='Accept', command=popup.destroy)
    cancelBtn = ttk.Button(popup, text='Deny', command=popup.destroy)
    confirmBtn.pack()
    cancelBtn.pack()
    popup.mainloop()


class EventHandler(EventHandlerInterface):

    def __init__(self, net):
        self.net = net

    def nodeJoin(self, node: Node):
        # TODO: Join adhoc
        logger.info(f"Join node {node}")
        print(node)
        if (node.groupID != '0') and (GroupService.getGroup(node.groupID) is None):
            pass
            GroupService.addGroup(node.groupID, node.groupName, node.maxPerson)
        UserService.addUser(node.username, node.firstname,
                            node.lastname, node.faculty, node.year, node.groupID)

    def nodeLeave(self, node: Node):
        # TODO: Leave adhoc
        # Need to also remove group
        UserService.removeUser(node.username)
        logger.info(f"Node left {node}")

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        logger.info(f"Receive group broadcast {b}")

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        logger.info(f"Receive message broadcast {msg}")

    def receiveMessageGroup(self, msg: GroupMessage):
        logger.info(f"Receive group message {msg}")

    def receiveGroupJoinRequest(self, req: Request):
        logger.info(f"Receive request to joining group {req}")
        if UserService.isAdmin() and UserService.getProfile()[-1] == req.groupID:
            popup_join_request(req.fromUsername)

    def receiveJoinOK(self, groupID: int):
        logger.info(f"Confirm joining groupID={groupID}")

    def receiveJoinDeny(self, groupID: int):
        logger.info(f"Deny joining groupID={groupID}")

    def receiveMessage(self, msg: Message):
        logger.info(f"Receive message {msg}")


logger = logging.getLogger('Service')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
