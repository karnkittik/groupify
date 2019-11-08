class Node:
    def __init__(self, ip, body=dict()):
        self.ip = ip
        self.username = body['username']
        self.firstname = body['firstname']
        self.lastname = body['lastname']
        self.faculty = body['faculty']
        self.year = body['year']
        self.groupID = body['groupID']
        self.body = body
