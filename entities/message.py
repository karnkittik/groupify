class Message:
    def __init__(self, fromUsername, toUsername, timestamp, body=dict()):
        self.fromUsername = fromUsername
        self.fromUsername = fromUsername
        self.timestamp = timestamp
        self.message = body.get('message', '')


class BroadcastMessage:
    def __init__(self, fromUsername, timestamp, body=dict()):
        self.fromUsername = fromUsername
        self.timestamp = timestamp
        self.message = body.get('message', '')


class GroupMessage:
    def __init__(self, fromUsername, groupID, timestamp, body=dict()):
        self.fromUsername = fromUsername
        self.groupID = groupID
        self.timestamp = timestamp
        self.message = body.get('message', '')
