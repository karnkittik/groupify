import setup
from database.database import DB
from datetime import datetime

from services.user import UserService


class BroadcastMessage:

    @staticmethod
    def getAll():
        result = DB.execute(
            'SELECT `user`.firstname, time, message FROM message_broadcast INNER JOIN `user` ON message_broadcast.from_username=`user`.username ORDER BY time ASC')
        return result.fetchall()

    @staticmethod
    def send(msg):
        username = UserService.getProfile()[0]
        setup.net.sendMessageBroadcast(msg)
        DB.execute('INSERT INTO message_broadcast(from_username, time, message) VALUES (?,?,?)',
                   (username, datetime.utcnow(), msg))

    @staticmethod
    def receive(username, time, msg):
        DB.execute(
            'INSERT INTO message_broadcast(from_username, time, message) VALUES (?,?,?)', (username, time, msg))
