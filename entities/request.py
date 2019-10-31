class Request:
    def __init__(self, fromUsername, toUsername, groupID, message, body=dict()):
        self.fromUsername = fromUsername
        self.toUsername = toUsername
        self.groupID = groupID
        self.message = message
        self.body = body
