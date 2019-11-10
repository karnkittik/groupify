import setup
from database.database import DB
from datetime import datetime

from entities.message import BroadcastMessage as BroadcastMessageEntity

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
        timestamp = datetime.utcnow()
        msgEntity = BroadcastMessageEntity(username, {
            'timestamp': str(timestamp),
            'message': msg
        })
        setup.net.sendMessageBroadcast(msgEntity)
        DB.execute('INSERT INTO message_broadcast(from_username, time, message) VALUES (?,?,?)',
                   (username, str(timestamp), msg))

    @staticmethod
    def receive(username, time, msg):
        DB.execute(
            'INSERT INTO message_broadcast(from_username, time, message) VALUES (?,?,?)', (username, time, msg))
