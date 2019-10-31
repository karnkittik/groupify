from entities.node import Node


class EventHandlerInterface(object):
    def nodeJoin(self, node: Node):
        raise NotImplementedError("Should have implemented this")

    def nodeLeave(self, node: Node):
        raise NotImplementedError("Should have implemented this")

    def receiveGroupBroadcast(self, b: GroupBroadcast):
        raise NotImplementedError("Should have implemented this")

    def receiveMessageBroadcast(self, msg: BroadcastMessage):
        raise NotImplementedError("Should have implemented this")

    def receiveMessageGroup(self, msg: GroupMessage):
        raise NotImplementedError("Should have implemented this")

    def receiveGroupJoinRequest(self, req: Request):
        raise NotImplementedError("Should have implemented this")

    def receiveJoinOK(self, groupID: int):
        raise NotImplementedError("Should have implemented this")

    def receiveJoinDeny(self, groupID: int):
        raise NotImplementedError("Should have implemented this")

    def receiveMessage(self, msg: Message):
        raise NotImplementedError("Should have implemented this")
