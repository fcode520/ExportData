# -*- coding: utf-8 -*-
__author__ = 'zl'
import  time
class HelpFunc:
    def __init__(self):
        self.domain="t.apcow.com"
    def TimeToStr(self,times):
        return str(time.strftime("%Y%m%d", time.localtime(times)))


    def GetMarkCode(self,row):
        path="uploads/article/"+self.TimeToStr(row['add_time'])+'/'+row['file_location']
        markCode="![file](http://"+self.domain+"/"+path+")"
        return markCode