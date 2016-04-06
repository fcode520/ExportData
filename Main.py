# -*- coding: utf-8 -*-
__author__ = 'zl'
import wecenter
import phphub
import time
import DateTime


def Time2ISOString(mytimeStamp):
    timeStamp = time.localtime(float(mytimeStamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStamp)
    return otherStyleTime


def ImportUserTable():
    WeDb = wecenter.WenCenterdb()
    db = WeDb.OpenDb('192.168.10.10', 'homestead', 'secret', 'wecenter')
    if db:
        print("连接WeCenter成功")
    else:
        print("连接连接WeCenter成功失败")
    result = WeDb.UserTables()
    if (result):
        print("获取用户表成功")
    phpdb = phphub.phDb()
    if (phphub):
        print("打开phphub数据库成功")
    count=0
    for row in result:
        if (row['valid_email'] == 0) or (row['email'] is None):
            continue
        rst = phpdb.InsertUser(row['uid'],
                               row['email'],
                               row['user_name'],
                               row['password'],
                               row['salt'],
                               row['valid_email'],
                               Time2ISOString(int(row['reg_time'])),
                               Time2ISOString(int(row['last_login'])),
                               )
        count=count+1
        print("插入成功")
    print('导入总条数=%d' % (count))


def ImportTopics():
    WeDb = wecenter.WenCenterdb()
    db = WeDb.OpenDb('192.168.10.10', 'homestead', 'secret', 'wecenter')
    if db:
        print("连接成功")
    else:
        print("连接失败")
    phpdb = phphub.phDb()
    result = WeDb.GetTopics()
    for row in result:
        rst = phpdb.InsertTopics(row)

    print rst
def ImportReplies():
    WeDb = wecenter.WenCenterdb()
    db = WeDb.OpenDb('192.168.10.10', 'homestead', 'secret', 'wecenter')
    if db:
        print("连接成功")
    else:
        print("连接失败")
    phpdb = phphub.phDb()
    result = WeDb.GetReplies()
    for row in result:
        rst = phpdb.InsertReplies(row)

    print rst
def UpdateTopicesLastReply():
    phpdb = phphub.phDb()
    result = phpdb.UpdateTopicesLastReply()

def ImportHeader():
    WeDb = wecenter.WenCenterdb()
    db = WeDb.OpenDb('192.168.10.10', 'homestead', 'secret', 'wecenter')
    if db:
        print("连接成功")
    else:
        print("连接失败")
    phpdb = phphub.phDb()
    result = WeDb.GetHeaders()
    for row in result:
        rst = phpdb.InsertHeaders(row)
    print rst
if __name__ == '__main__':

    ImportUserTable()
    ImportTopics()
    ImportReplies()
    UpdateTopicesLastReply()
    ImportHeader()