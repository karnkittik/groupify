from datetime import datetime

class user:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.nickname = ""
        self.year = ""
        self.faculty = ""
    
    def update(self,first_name,last_name,nickname,year,faculty):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.year = year
        self.faculty = faculty

class message:
    def __init__(self,sender,msg):
        self.sender = sender
        self.message = msg
        self.update = False
        # self.msg_queue = msg_queue
        # self.update_chat = False
        # self.no_of_msg = msg.length
    
    def display_msg(self):
        return self.sender+": "+self.message+"("+str(datetime.now().strftime("%H:%M"))+")\n"

    # def update_chat(self):
    #     self.update = True
