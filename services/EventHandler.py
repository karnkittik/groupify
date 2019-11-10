import logging
from database.database import DB
from services.interfaces.EventHandlerInterface import EventHandlerInterface

from entities.node import Node
from entities.message import *
from entities.request import *
from entities.group import *

from services.user import UserService
from services.group import GroupService
from services.broadcastMessage import BroadcastMessage
from services.groupMessage import GroupMessage

from GUI_ALL.ui.JoinRequest import JoinRequest
from tkinter import messagebox


class EventHandler(EventHandlerInterface):

    def __init__(self, net):
        self.net = net

    def nodeJoin(self, node: Node):
        logger.info(f"Join node {node}")
        print(node)
        if (node.groupID != '0') and (GroupService.getGroup(node.groupID) is None):
            GroupService.addGroup(node.groupID, node.groupName, node.maxPerson)
        UserService.addUser(node.username, node.firstname,
                            node.lastname, node.faculty, node.year, node.groupID)

    def nodeLeave(self, node: Node):
        # Need to also remove group
        UserService.removeUser(node.username)
        logger.info(f"Node left {node}")

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        logger.info(f"Receive group broadcast {b}")
        print('Group broadcast body: ', b.body)
        UserService.addUser(b.username, b.body.get('firstname', 'test'), b.body.get(
            'lastname', 'Test L'), b.body.get('faculty', 'test faculty'), b.body.get('year', 4), b.groupID)

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        logger.info(f"Receive message broadcast {msg}")
        BroadcastMessage.receive(msg.fromUsername, msg.timestamp, msg.message)

    def receiveMessageGroup(self, msg: GroupMessage):
        logger.info(f"Receive group message {msg}")
        GroupMessage.receive(
            msg.fromUsername, msg.groupID, msg.body.get('timestamp', ''), msg.body.get('message', ''))

    def receiveGroupJoinRequest(self, req: Request):
        logger.info(f"Receive request to joining group {req}")
        if UserService.isAdmin() and UserService.getProfile()[-1] == req.groupID:
            JoinRequest(req)

    def receiveJoinOK(self, groupID: int):
        logger.info(f"Confirm joining groupID={groupID}")
        username = UserService.getProfile()[0]
        UserService.updateGroup(username, groupID)
        messagebox.showinfo('Accept request', 'Joined group ' + str(groupID))

    def receiveJoinDeny(self, groupID: int):
        logger.info(f"Deny joining groupID={groupID}")
        messagebox.showerror('Deny request', str(
            groupID) + ' denied your request!')

    def receiveMessage(self, msg: Message):
        logger.info(f"Receive message {msg}")


logger = logging.getLogger('Service')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
