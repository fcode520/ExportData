# -*- coding: utf-8 -*-
__author__ = 'zl'
import pymysql.cursors
import markdown
import HelpFunc
import wecenter
import re
import time
class phDb:
    def __init__(self):
        bopen=self.OpenDb('192.168.10.10','homestead','secret','phphub')
        if bopen==True:
            print"连接phphub成功"
        else:
            print "连接phphub失败"
    def OpenDb(self,dbhost,user,pwd,db):
        self.connection=pymysql.connect(host=dbhost,user=user,password=pwd,db=db,charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
        if self.connection:
            return True;
        else:
            return False;
    def InsertUser(self,uid,email,username,password,salt,status,createdatetime,updatetime):
        try:
            sqlstr="INSERT INTO `users` VALUES (%d,'%s','%s','%s','%s',0,0,0,0,'def_avatars.png',NULL,NULL,NULL,'%s','%s','%d',NULL)" %(
                uid,email,username,password,salt,createdatetime,updatetime,status);
            print(sqlstr)
            if username=='xiaoming':
                print "zat"
            Cursor=self.connection.cursor()
            Cursor.execute(sqlstr)
            self.connection.commit()
            return True
        except:
            return False

    def Eexcul(self,sql):
        try:
            Cursor=self.connection.cursor()
            Cursor.execute(sql)
            # print(Cursor.description)
            # for row in Cursor:
            #     print(row)
            result=Cursor.fetchall();
            print(result)
        finally:
            self.connection.close()
        return result
    def markdownToHtml(self,text):
        html=markdown.markdown(text)
        return html
    def RepaceAttach(self,Text,articleID):
        #从数据库找到对应的附件
        WeDb=wecenter.WenCenterdb()
        db=WeDb.OpenDb('192.168.10.10','homestead','secret','wecenter')

        sql="SELECT * FROM `aws_attach`WHERE `item_id`=%d" %(articleID)
        result=WeDb.Eexcul(sql)
        HFC=HelpFunc.HelpFunc()
        for row in result:
            if row['is_image']==1:
                markCode=HFC.GetMarkCode(row)
                odlstr="[attach]%d[/attach]"%(row['id'])
                TextTmp=Text.replace(odlstr,markCode)
                Text=TextTmp
            else:
                TextTmp=re.sub('\[attach\].*\[/attach\]','',Text)
                Text=TextTmp
        #查找attach 都有那些
        return Text
    def ReplaceOldMarkdown(self,Text):
        TextTmp=re.findall('!\(.*?\)',Text)
        for  MyTemp in TextTmp:
            newStr="![]("+MyTemp[2:-1]+")"
            TmpTmp=Text.replace(MyTemp,newStr)
            Text=TmpTmp
        return Text
    def InsertTopics(self,topicobj):

        if topicobj['has_attach']==1:
            body_original=self.RepaceAttach(topicobj['message'],topicobj['id'])
        else:
            body_original=topicobj['message']
        body_original=self.ReplaceOldMarkdown(body_original)
        body=self.markdownToHtml(body_original)
        title=topicobj['title']
        user_id=topicobj['uid']
        if topicobj['category_id']==49:
            node_id=6
        else:
            node_id=3
        reply_count=topicobj['comments']
        view_count=topicobj['views']
        vote_count=topicobj['votes']
        create_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(topicobj['add_time'])))
        zhuanyi_body=body.replace('\'','\\\'')
        zhuanyi_body_original=body_original.replace('\'','\\\'')
        sqlstr="INSERT INTO `topics` VALUES (%d,'%s','%s',%d,%d,0,0,0,%d,%d,0,%d,0,NULL,'%s','%s',0,'%s','%s')" %(
               topicobj['id'],title,zhuanyi_body,user_id,node_id,reply_count,view_count,vote_count,create_time,create_time,zhuanyi_body_original,zhuanyi_body_original[0:100]);

        Cursor=self.connection.cursor()
        print("|******************************************************************************|")
        print(sqlstr)
        Cursor.execute(sqlstr.encode('utf-8'))

        self.connection.commit()
        return True
    def listTodirescoty(self,list):
        my_dict = {}
        for row in list:
            my_dict[row['id']]=row['username']
        return my_dict


    def InsertReplies(self,repliesObj):
        myUsersSql="SELECT id ,username FROM `users`"
        myusersList=self.Eexcul(myUsersSql)
        myusers=self.listTodirescoty(myusersList)
        hpfunc=HelpFunc.HelpFunc()
        id=repliesObj['id']
        body=repliesObj['message']
        user_id=repliesObj['uid']
        topic_id=repliesObj['article_id']
        is_block=0
        vote_count=repliesObj['votes']
        create_at=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(repliesObj['add_time'])))
        updated_at=create_at
        if repliesObj['at_uid']!=0 :
            username=myusers.get(repliesObj['at_uid'])
            if username is None:
                body_original = repliesObj['message']
            else:
                body_original=""
                tmpbody_original=body_original+"@"+username+" "+repliesObj['message']
                body_original=tmpbody_original
        else:
            body_original=repliesObj['message']
        #        \@(\S)+   |\@(\S+)\s
        body=self.markdownToHtml(body_original)
        zhuanyi_body=body.replace('\'','\\\'')
        zhuanyi_body_original=body_original.replace('\'','\\\'')
        insertSql="INSERT INTO 'relies' VALUES (%d,'%s',%d,%d,%d,%d,'%s','%s','%s',NULL) " %(
            id,zhuanyi_body,user_id,topic_id,is_block,vote_count,create_at,create_at,zhuanyi_body_original
        )
        print insertSql