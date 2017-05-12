from models.database import Database
# from database import Database

class Group:
    # Open database connection
    cursor =  Database.get_connection().cursor()

    def __init__(self, gp_name):
        self.gp_name = gp_name

    def createGroup(self):
        sql = "INSERT INTO `group` (`group_name`) VALUES ('{0}')".format(self.gp_name)
        connection = Database.get_connection()
        Group.cursor.execute(sql)
        connection.commit()


    # def removeGroup(self):
    #     cursor = Group.db.cursor()
    #     sql = "DELETE FROM `group` WHERE group_id = {0} ".format("1")
    #     try:
    #         cursor.execute(sql)
    #         Group.db.commit()
    #     except:
    #         Group.db.rollback()

    @classmethod
    def selectAllgr(cls):
        Group.cursor.execute("SELECT * FROM `group`")
        return Group.cursor.fetchall()

    def getAllGroupMembers(self):
        sql = "SELECT user.user_id, user.name FROM `user` JOIN `user-groups` ON " \
              "`user`.`user_id`=`user-groups`.`user_id` JOIN `group`ON `group`.`group_id`=`user-groups`.`group_id` " \
              "WHERE `group`.`group_name`='{0}'".format(self.gp_name)
        Group.cursor.execute(sql)
        return Group.cursor.fetchall()

    @classmethod
    def getGroupId(cls, groupName):
        sql = "SELECT `group_id` FROM `group` WHERE `group_name` = %s"
        Group.cursor.execute(sql, (groupName))
        return Group.cursor.fetchone()['group_id']
