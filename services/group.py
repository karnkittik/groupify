from database.database import DB


class GroupService:

    @staticmethod
    def getGroup(groupID=None):
        result = None
        if(groupID is None):
            result = DB.execute('SELECT * FROM `group`')
            for row in result:
                print(row)
        else:
            result = DB.execute(
                'SELECT * FROM `group` WHERE group_id=?', groupID)
            print(result)
        return result

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
            'SELECT * FROM `user` RIGHT JOIN `group_member` ON user.username=group_member.username WHERE group_id=?', (groupID))
        for row in result:
            print(row)
        return result

    @staticmethod
    def removeMember(username):
        result = DB.execute(
            'DELETE * FROM group_member WHERE username=?', username)
        print(result)
