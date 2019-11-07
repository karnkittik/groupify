from typing import Union
from database.database import DB


class UserService:

    @staticmethod
    def initMe(username, firstname, lastname, faculty, year):
        DB.executemultiplesql([
            ('REPLACE INTO `user`(username, firstname, lastname, faculty, year) VALUES(?,?,?,?,?)',
             (username, firstname, lastname, faculty, year,)),
            ('REPLACE INTO self(username) VALUES (?)', (username,))
        ])

    @staticmethod
    def getProfile() -> tuple:
        username = DB.execute('SELECT * FROM self').fetchone()[0]
        return UserService.getUser(username)

    @staticmethod
    def isAdmin() -> bool:
        return DB.execute('SELECT * FROM self LIMIT 1').fetchone()[1]

    @staticmethod
    def infoBroadcast() -> dict:
        cur_user = UserService.getProfile()
        info = {
            'username': cur_user[0],
            'firstname': cur_user[1],
            'lastname': cur_user[2],
            'faculty': cur_user[3],
            'group_id': cur_user[4],
            'group_name': '',
            'max_person': 0
        }
        if (cur_user[4] != '0'):
            group_info = DB.execute(
                'SELECT * FROM `group` WHERE group_id=? LIMIT 1', (cur_user[4],))
            info['group_name'] = group_info[1]
            info['max_person'] = group_info[2]
        return info

    @staticmethod
    def isMember() -> bool:
        return DB.execute('SELCT * FROM self LIMIT 1').fetchone()[2]

    @staticmethod
    def updateProfile(firstname, lastname, faculty, year):
        username = UserService.getProfile()[0]
        DB.execute('UPDATE `user` SET firstname=?, lastname=?, faculty=?, year=? WHERE username=?',
                   (firstname, lastname, faculty, year, username))

    @staticmethod
    def getUser(username=None) -> Union[list, tuple]:
        users = []
        if(username is None):
            result = DB.execute('SELECT * FROM `user`')
            users = result.fetchall()
        else:
            result = DB.execute(
                'SELECT * FROM `user` WHERE username=? LIMIT 1', (username,))
            users = result.fetchone()
        return users

    @staticmethod
    def addUser(username, firstname, lastname, faculty, year, group_id='0'):
        DB.execute('REPLACE INTO `user`(username, firstname, lastname, faculty, year, group_id) VALUES (?,?,?,?,?,?)',
                   (username, firstname, lastname, faculty, year, group_id))

    @staticmethod
    def removeUser(username):
        DB.execute('DELETE * FROM `user` WHERE username=?', (username,))

    @staticmethod
    def updateGroup(username, newGroupID):
        curr_username = UserService.getProfile()[0]
        if curr_username == username:
            DB.executemultiplesql([
                ('UPDATE `user` SET group_id=? WHERE username=?',
                 (newGroupID, username)),
                ('UPDATE `self` SET is_member=1 WHERE username=?', (username))
            ])
        else:
            DB.execute(
                'UPDATE `user` SET group_id=? WHERE username=?', (newGroupID, username,))

    @staticmethod
    def getAvailableUser() -> list:
        result = DB.execute(
            'SELECT username, firstname, lastname, faculty, year FROM `user` WHERE group_id="0"')
        return result.fetchall()
