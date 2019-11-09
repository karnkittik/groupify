class Node:
    def __init__(self, ip, body=dict()):
        self.ip = ip
        self.username = body['username']
        self.firstname = body['firstname']
        self.lastname = body['lastname']
        self.faculty = body['faculty']
        self.year = body['year']
        self.groupID = body['groupID']
        self.groupName = body.get('group_name', 'This is Group name')
        self.maxPerson = body.get('max_person', 5)
        self.body = body
