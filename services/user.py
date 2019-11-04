from database.database import DB


class UserService:

    @staticmethod:
    def getUser(username=None):
        result = None
        if(username is None):
            result = DB.execute('SELECT * FROM `user`')
            for row in result:
                print(row)
        else:
            result = DB.execute(
                'SELECT * FROM `user` WHERE username=?', (username))
            print(result)
        return result

    @staticmethod
    def updateGroup(username, newGroupID):
        DB.execute(
            'REPLACE INTO group_member(group_id) VALUES (?) WHERE username=?', (newGroupID, username))
