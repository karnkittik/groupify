class Request:
    def __init__(self, fromUsername, groupID, body=dict()):
        self.fromUsername = fromUsername
        self.groupID = groupID
        self.message = body.get('message','')
        self.body = body
