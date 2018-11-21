import pymysql
from DBUtils.PooledDB import PooledDB

from main.dbconfig import mysqlInfo


class OPMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql,
                              mincached=10,
                              maxcached=20,
                              maxconnections=40,
                              blocking=True,
                              host=mysqlInfo['host'],
                              user=mysqlInfo['user'],
                              passwd=mysqlInfo['passwd'],
                              db=mysqlInfo['db'],
                              port=mysqlInfo['port'],
                              charset=mysqlInfo['charset'])
            print(__pool)
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql, *args):
        # print('op_insert', sql)
        insert_num = self.cur.execute(sql, *args)
        # print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql, *args):
        # print('op_select', sql)
        self.cur.execute(sql, *args)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        # print('op_select', select_res)
        return select_res

    # 释放资源
    def closeall(self):
        # pass
        self.cur.close()
        self.coon.close()

mysql_con = OPMysql()

# if __name__ == '__main__':
#     mysql_con = OPMysql()
#     db = mysql_con.getmysqlconn()
#     sql = 'select * from tb_rawdata;'
#
#     sql1 = r'insert into tb_userinfo (UserID,Username,Password,Usertype)' \
#            'value({UserID},"{Username}","{Password}",{Usertype});'.format(
#         UserID=3, Username='tom', Password='123456', Usertype=0)
#
#     data = mysql_con.op_select(sql)
#     # mysql_con.op_insert(sql1)
#     print(data)
#     mysql_con.closeall()
