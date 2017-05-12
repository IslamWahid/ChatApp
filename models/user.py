#! /usr/bin/python3
from models.database import Database
from models.group import Group
# from database import Database
# from group import Group

class User:
    cursor = Database.get_connection().cursor()

    @classmethod
    def getUserId(cls,userName):
        sql = "SELECT `user_id` FROM `user` WHERE `name` = %s"
        User.cursor.execute(sql,(userName))
        result = User.cursor.fetchone()
        if result:
            return result['user_id']
        else:
            return result

    @classmethod
    def getUserName(cls,user_id):
        sql = "SELECT `name` FROM `user` WHERE `user_id` = %s"
        User.cursor.execute(sql,(user_id))
        result = User.cursor.fetchone()
        return result['name']

    @classmethod
    def selectAllUsers(cls):
        sql = "SELECT * FROM `user`"
        User.cursor.execute(sql)
        return User.cursor.fetchall()

    def __init__(self, name):
        self.name = name
        if User.getUserId(self.name) == None:
            self.id = self.__insert()
        else :
            self.id = User.getUserId(self.name)


    def setAllUserData(self):
        self.groups = self.getMyGroups()
        self.availGroups = self.getAvailGroups()
        self.friends = self.getMyFriends()
        self.availFriends = self.getAvailFriends()
    def createGroup(self,groupName):
        group = Group(groupName)
        group.createGroup()
        self.joinGroup(groupName)

    def joinGroup(self,groupName):
        group_id = Group.getGroupId(groupName)
        sql = "INSERT INTO `user-groups` SET `user_id` = %s ,`group_id` = %s "
        User.cursor.execute(sql, (self.id,group_id))

    def leaveGroup(self, groupName):
        group_id = Group.getGroupId(groupName)
        sql = "DELETE FROM `user-groups` WHERE `user_id` = %s AND `group_id` = %s "
        User.cursor.execute(sql, (self.id,group_id))

    def getMyGroups(self):
        sql = "SELECT `group`.`group_id`, `group`.`group_name` FROM `group` JOIN `user-groups` ON " \
              "`group`.`group_id`=`user-groups`.`group_id` JOIN `user` ON `user`.`user_id`=`user-groups`.`user_id` " \
              "WHERE `user`.`name`='{0}'".format(self.name)
        Group.cursor.execute(sql)
        return Group.cursor.fetchall()

    def getAvailGroups(self):
        groups = Group.selectAllgr()
        mygroups = self.getMyGroups()
        return [x for x in groups if x not in mygroups]

    def addFriend(self, friendName):
        friend_id = self.__class__.getUserId(friendName)
        sql = "INSERT INTO `user-friends` SET `user_id` = %s ,`friend_id` = %s "
        connection = Database.get_connection()
        User.cursor.execute(sql, (self.id,friend_id))
        User.cursor.execute(sql, (friend_id,self.id))
        connection.commit()

    def removeFriend(self, friendName):
        friend_id = self.__class__.getUserId(friendName)
        sql = "DELETE FROM `user-friends` WHERE `user_id` = %s AND `friend_id` = %s "
        connection = Database.get_connection()
        User.cursor.execute(sql, (self.id,friend_id))
        User.cursor.execute(sql, (friend_id,self.id))
        connection.commit()

    def getMyFriends(self):
        sql = "SELECT `friend_id` FROM `user-friends` WHERE `user_id` = %s "
        connection = Database.get_connection()
        User.cursor.execute(sql, (self.id))
        result = User.cursor.fetchall()
        friends=[]
        for friend in result:
            friendName = User.getUserName(friend['friend_id'])
            friends.append(User(friendName).__dict__)
        return friends

    def getAvailFriends(self):
        people = User.selectAllUsers()
        friends = self.getMyFriends()
        friendsIds=[ elmt['id'] for elmt in friends ]
        return [x for x in people if x['user_id'] not in friendsIds and x['user_id'] != self.id]

    def __insert(self):
        sql = "INSERT INTO `user` SET `name` = %s"
        connection = Database.get_connection()
        User.cursor.execute(sql, (self.name))
        connection.commit()
        return User.cursor.lastrowid


# print(User.getUserId("islam"))
# print(User.getUserName(1))
# print('ALL:')
# print (User.selectAllUsers())
# user = User("islam")
# print ('FRIENDS:')
# print(user.getMyFriends())
# print('AVAIL FRIENDS:')
# print(user.getAvailFriends())
# print(Group.selectAllgr())
# print(user.getMyGroups())
# print(user.getOtherGroups())
# user.joinGroup("PUBLIC")
# user.leaveGroup("PUBLIC")
# user.addFriend("samira")
# user.removeFriend("samira")
# print(user.selectAllFriends())
# print(user.selectAllNotFriends())
