from typing import Union
from database.database import DB
from services.user import UserService


class GroupService:

    @staticmethod
    def getGroup(groupID: str = None) -> Union[list, tuple]:
        groups = []
        if(groupID is None):
            result = DB.execute(
                'SELECT `group`.group_id, `group`.group_name, `group`.max_person, COUNT(username) FROM `user` LEFT JOIN `group` WHERE `group`.group_id=`user`.group_id AND `group`.group_id != "0"')
            groups = result.fetchall()
            print(groups)
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
            ('UPDATE `user` SET group_id=? WHERE username=?', (username, username, )),
            ('UPDATE self SET is_admin=true WHERE username=?', (username,))
        ])

    @staticmethod
    def addGroup(groupID, groupName, maxPerson=4):
        DB.execute('INSERT INTO `group`(group_id, group_name, max_person) VALUES (?,?,?)',
                   (groupID, groupName, maxPerson))

    @staticmethod
    def addMember(groupID, username):
        DB.executemultiplesql([
            ('UPDATE `user` SET group_id=? WHERE username=?', (groupID, username)),
            ('UPDATE `self` SET is_member=true WHERE username=?', (username))
        ])

    @staticmethod
    def getMember(groupID):
        result = DB.execute(
            'SELECT * FROM `user` WHERE group_id=?', (groupID,))
        return result.fetchall()

    @staticmethod
    def removeMember(username):
        result = DB.execute(
            'DELETE * FROM group_member WHERE username=?', (username,))
        print(result)
