class SenderInterface(object):
    def sendMessage(self, msg: Message):
        raise NotImplementedError("Should have implemented this")

    def sendMessageBroadcast(self, msg: BroadcastMessage):
        raise NotImplementedError("Should have implemented this")

    def sendMessageGroup(self, msg: GroupMessage):
        raise NotImplementedError("Should have implemented this")

    def sendGroupJoinRequest(self, req: Request):
        raise NotImplementedError("Should have implemented this")

    def sendGroupAcknowledgeRequest(self, req: Request):
        raise NotImplementedError("Should have implemented this")

    def sendGroupDenyRequest(self, req: Request):
        raise NotImplementedError("Should have implemented this")
