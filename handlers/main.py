# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-07-14
#
from renren.handler import APIHandler,TokenAPIHandler
import renren.libs.utils as utils

class MainHandler(APIHandler):
    #获取文件列表
    def get(self):
        result = utils.init_response_data()
        try:
            result['data']= "Api home page"
            result['version']= "v0.2.0"
            result['pack_date']= "2016-08-09"
            result['update_msg']= u"1.修改邮箱为集团邮箱 2.修改后台文档删除后不能重新更新的bug"
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

class MainTestHandler(APIHandler):
    #获取文件列表
    def get(self):
        import renren.libs.wslib as wslib
        result = utils.init_response_data()
        try:
            res = wslib.send_msg(18752036998,"【东汇征信】尊敬的用户您好，您本次的验证码为12345,30分钟内有效")
            result['data']= res
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

handlers = [(r'/api/main/test', MainTestHandler),
            (r'/api/main', MainHandler),

            ]