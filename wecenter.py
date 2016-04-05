# -*- coding: utf-8 -*-
__author__ = 'zl'
import pymysql.cursors
class WenCenterdb:
    # def __init__(self):
    def OpenDb(self,dbhost,user,pwd,db):
        self.connection=pymysql.connect(host=dbhost,user=user,password=pwd,db=db,charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
        if self.connection:
            return True;
        else:
            return False;
    def Eexcul(self,sql):
        try:
            Cursor=self.connection.cursor()
            Cursor.execute(sql)
            print(Cursor.description)
            # for row in Cursor:
            #     print(row)
            result=Cursor.fetchall();
            # print(result)
        finally:
            self.connection.close()
        return result
    def UserTables(self,limit=0):
        if limit>0:
            mysql="select * from aws_users limit %d" %(limit)
        else:
            mysql="select * from aws_users"
        return self.Eexcul(mysql)
    def GetTopics(self,limit=0):
        if limit > 0:
            mysql="select * from aws_article limit %d" %(limit)
        else:
            mysql="select * from aws_article"
        return self.Eexcul(mysql)

    def GetReplies(self,limit=0):
        if limit > 0:
            mysql = "SELECT * FROM aws_article_comments limit %d" % (limit)
        else:
            mysql = "SELECT * FROM aws_article_comments"
        return self.Eexcul(mysql)
