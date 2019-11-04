from typing import Union
from database.database import DB
from services.user import UserService


class GroupService:

    @staticmethod
    def getGroup(groupID: str = None) -> Union[list, tuple]:
        groups = []
        if(groupID is None):
            result = DB.execute('SELECT * FROM `group`')
            groups = result.fetchall()
        else:
            result = DB.execute(
                'SELECT * FROM `group` WHERE group_id=? LIMIT 1', (groupID,))
            groups = result.fetchone()
        return groups

    @staticmethod
    def createGroup(groupName, limitPerson):
        username = UserService.getProfile()[0]
        DB.executemultiplesql([
            ('REPLACE INTO `group`(group_id, group_name, max_person) VALUES (?,?,?)',
             (username, groupName, limitPerson)),
            ('UPDATE self SET is_admin=true', None)
        ])

    @staticmethod
    def addGroup(groupID, groupName, maxPerson=4):
        DB.execute('INSERT INTO `group`(group_id, group_name, max_person) VALUES (?,?,?)',
                   (groupID, groupName, maxPerson))

    @staticmethod
    def addMember(groupID, username):
        DB.execute(
            'INSERT INTO `group_member`(group_id, username) VALUES (?,?)', (groupID, username))

    @staticmethod
    def getMember(groupID):
        result = DB.execute(
            'SELECT * FROM `user` RIGHT JOIN `group_member` ON user.username=group_member.username WHERE group_id=?', (groupID,))
        return result.fetchall()

    @staticmethod
    def removeMember(username):
        result = DB.execute(
            'DELETE * FROM group_member WHERE username=?', (username,))
        print(result)
