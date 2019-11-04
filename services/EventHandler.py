from database.database import DB
from services.interfaces.EventHandlerInterface import EventHandlerInterface


class EventHandler(EventHandlerInterface):
    def nodeJoin(self, node: Node):
        print("Join node", node)

    def nodeLeave(self, node: Node):
        print("Node left", node)

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        print("Receive group broadcast", b)

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        print("Receive message broadcast", msg)

    def receiveMessageGroup(self, msg: GroupMessage):
        print("Receive group message", msg)

    def receiveGroupJoinRequest(self, req: Request):
        print("Receive request to joining group", req)

    def receiveJoinOK(self, groupID: int):
        print("Confirm joining groupID=", groupID)

    def receiveJoinDeny(self, groupID: int):
        print("Deny joining groupID=", groupID)

    def receiveMessage(self, msg: Message):
        print("Receive message", msg)
