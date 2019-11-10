import setup
from database.database import DB
from datetime import datetime

from entities.message import GroupMessage as GroupMessageEntity

from services.user import UserService


class GroupMessage:
    @staticmethod
    def getAll():
        groupID = UserService.getProfile()[-1]
        result = DB.execute(
            'SELECT `user`.firstname, time, message FROM message_group INNER JOIN `user` ON message_group.from_username=`user`.username WHERE message_group.group_id=? ORDER BY time ASC', (groupID, ))
        return result.fetchall()

    @staticmethod
    def send(msg):
        user = UserService.getProfile()
        username = user[0]
        groupID = user[-1]
        if(groupID != '0'):
            timestamp = datetime.utcnow()
            msgEntity = GroupMessageEntity(username, groupID, {
                'timestamp': str(timestamp),
                'message': msg
            })
            setup.net.sendMessageGroup(msgEntity)
            DB.execute('INSERT INTO message_group(from_username, group_id, time, message) VALUES (?,?,?,?)',
                       (username, groupID, str(timestamp), msg))

    @staticmethod
    def receive(username, groupID, time, msg):
        user = UserService.getProfile()
        user_groupID = user[-1]
        if user_groupID == groupID:
            DB.execute(
                'INSERT INTO message_group(from_username, group_id, time, message) VALUES (?,?,?,?)', (username, groupID, time, msg))
