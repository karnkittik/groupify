import logging
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
        logger.info(f"Join node {node}")

    def nodeLeave(self, node: Node):
        # TODO: Leave adhoc
        logger.info(f"Node left {node}")

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        logger.info(f"Receive group broadcast {b}")

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        logger.info(f"Receive message broadcast {msg}")

    def receiveMessageGroup(self, msg: GroupMessage):
        logger.info(f"Receive group message {msg}")

    def receiveGroupJoinRequest(self, req: Request):
        logger.info(f"Receive request to joining group {req}")
        popup_join_request()

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

