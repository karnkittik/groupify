
class Message:
    def __init__(self, fromUsername, toUsername, body=dict()):
        self.fromUsername = fromUsername
        self.toUsername = toUsername
        self.timestamp = body.get('timestamp', '')
        self.message = body.get('message', '')


class BroadcastMessage:
    def __init__(self, fromUsername, body=dict()):
        self.fromUsername = fromUsername
        self.timestamp = body.get('timestamp', '')
        self.message = body.get('message', '')


class GroupMessage:
    def __init__(self, fromUsername, groupID, body=dict()):
        self.fromUsername = fromUsername
        self.groupID = groupID
        self.timestamp = body.get('timestamp', '')
        self.message = body.get('message', '')
