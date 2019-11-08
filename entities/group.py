class GroupBroadcast:
    def __init__(self, body=None):
        self.username = body['username']
        self.groupID = body['groupID']
        self.role = body['role']
        self.body = body
