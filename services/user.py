from typing import Union
from database.database import DB


class UserService:

    @staticmethod
    def initMe(username: str, firstname, lastname, faculty, year):
        username = username.replace(':', '')
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
        user_info = DB.execute(
            'SELECT `user`.username, `user`.firstname, `user`.lastname, `user`.faculty, `user`.year, `user`.group_id, `self`.is_admin, `self`.is_member FROM `user` INNER JOIN `self` ON `user`.username=`self`.username').fetchone()
        role = 'none'
        if user_info[6] == 1:  # isAdmin
            role = 'admin'
        elif user_info[7] == 1:
            role = 'member'
        info = {
            'username': user_info[0],
            'role': role,
            'firstname': user_info[1],
            'lastname': user_info[2],
            'faculty': user_info[3],
            'year': user_info[4],
            'isAdmin': user_info[6],
            'isMember': user_info[7],
            'groupID': user_info[5],
            'group_name': '',
            'max_person': 0
        }
        if (user_info[5] != '0'):
            group_info = DB.execute(
                'SELECT * FROM `group` WHERE group_id=? LIMIT 1', (user_info[5],)).fetchone()
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
        username = username.replace(':', '')
        DB.execute('REPLACE INTO `user`(username, firstname, lastname, faculty, year, group_id) VALUES (?,?,?,?,?,?)',
                   (username, firstname, lastname, faculty, year, group_id))

    @staticmethod
    def removeUser(username):
        DB.execute('DELETE FROM `user` WHERE username=?', (username,))

    @staticmethod
    def updateGroup(username, newGroupID):
        username = username.replace(':', '')
        curr_username = UserService.getProfile()[0]
        if curr_username == username:
            DB.executemultiplesql([
                ('UPDATE `user` SET group_id=? WHERE username=?',
                 (newGroupID, username)),
                ('UPDATE `self` SET is_member=1 WHERE username=?', (username,))
            ])
        else:
            DB.execute(
                'UPDATE `user` SET group_id=? WHERE username=?', (newGroupID, username,))

    @staticmethod
    def getAvailableUser() -> list:
        result = DB.execute(
            'SELECT username, firstname, lastname, faculty, year FROM `user` WHERE group_id="0"')
        return result.fetchall()
