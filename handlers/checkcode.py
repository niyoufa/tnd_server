# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-07-14
"""
import json,pdb
import oauth2
import datetime
import tornado
import urllib
from renren.handler import TokenAPIHandler
from renren.handler import APIHandler
import renren.libs.utils as utils
import renren.handlers.oauth as oauth
import renren.libs.wslib as wslib
from renren.mail import send_email

class MobileCheckCode(APIHandler):
    _model = "checkcode.CheckCode"

    def get(self):

        result = utils.init_response_data()
        checkcode_coll = self.model.get_coll()
        try:
            mobile = self.get_argument("mobile")
            curr_time = datetime.datetime.now()
            if checkcode_coll.find({"mobile":mobile,"enable_flag":True}).count() > 0:
                # 验证码请求限制 每小时限制5条
                if checkcode_coll.find({"mobile":mobile,
                        "create_date":{
                            "$gte":curr_time - datetime.timedelta(hours=1),
                            "$lte":curr_time + datetime.timedelta(hours=1),
                        }
                    }).count() >= 5:
                    raise Exception("验证码请求限制，每小时限制5条！")

                cr = checkcode_coll.find({"mobile":mobile,"enable_flag":True})
                for checkcode in cr:
                    checkcode["enable_flag"] = False
                    checkcode_coll.save(checkcode)
            else:
                pass
            random_code = utils.get_random_num(6,mode="number")

            checkcode_coll.insert_one({
                "mobile":mobile,
                "enable_flag":True,
                "create_date":curr_time,
                "type":"mobile",
                "code":random_code,
            })
            res = wslib.send_msg(mobile,"尊敬的用户您好，您本次的验证码为%s,30分钟内有效"%random_code)
            if res != "0" :
                raise ValueError(u"短信发送失败")
            result["code"] = random_code
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class EmailCheckCode(APIHandler):
    def get(self):
        result = utils.init_response_data()
        checkcode_coll = self.model.get_coll()
        try:
            email = self.get_argument("email")

            curr_time = datetime.datetime.now()
            if checkcode_coll.find({"email": email, "enable_flag": True}).count() > 0:
                # 验证码请求限制 每天限制5条
                if checkcode_coll.find({"email": email,
                                        "create_date": {
                                            "$gte": curr_time - datetime.timedelta(hours=1),
                                            "$lte": curr_time + datetime.timedelta(hours=1),
                                        }
                                        }).count() >= 5:
                    raise Exception("验证码请求限制，每小时限制5条！")

                cr = checkcode_coll.find({"email": email, "enable_flag": True})
                for checkcode in cr:
                    checkcode["enable_flag"] = False
                    checkcode_coll.save(checkcode)
            else:
                pass
            random_code = utils.get_random_num(6,mode="number")
            checkcode_coll.insert_one({
                "email": email,
                "enable_flag": True,
                "create_date": curr_time,
                "type": "email",
                "code": random_code,
            })
            result['res'] = send_email('jltx@personcredit.com',[email],u'风控系统邮件验证','',html=u"【风控系统】尊敬的用户您好，您本次的验证码为%s,30分钟内有效"%random_code)
            # result['res'] = send_email('admin@dhui100.com',[email],u'风控系统邮件验证','',html=u"【风控系统】尊敬的用户您好，您本次的验证码为%s,30分钟内有效"%random_code)
            result["code"] = random_code
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)


handlers = [
    (r"/api/checkcode/mobile", MobileCheckCode),
    (r"/api/checkcode/email", EmailCheckCode),
]
