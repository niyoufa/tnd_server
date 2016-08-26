# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-08-25
"""
import json,pdb
import oauth2
import datetime
import tornado
import urllib
from tornado.options import options

from renren.handler import TokenAPIHandler
from renren.handler import APIHandler
import renren.libs.utils as utils
from renren.model.model import BaseModel
from base import *

class UserSignUp(APIHandler):
    _model = "user.UserModel"

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        try:
            user_coll = self.model.get_coll()
            oauth_coll = BaseModel.get_model("oauth.OauthModel").get_coll()
            checkcode_coll = BaseModel.get_model("checkcode.CheckCode").get_coll()

            mobile = self.get_argument("mobile")
            mobile_code = self.get_argument("mobile_code")
            password1 = self.get_argument("password1")
            password2 = self.get_argument("password2")
            type = self.get_argument("type","b")

            if mobile == "":
                raise Exception("请输入手机号!")
            elif mobile_code == "":
                raise Exception("请输入手机验证码")
            elif password1 == "":
                raise Exception("请输入password1!")
            elif password2 == "":
                raise Exception("请确认password2！")

            # 检查手机验证码
            utils.check_code(checkcode_coll, mobile, mobile_code)
            # # 检查邮箱验证码
            # utils.check_code(checkcode_coll, email, email_code, type="email")

            add_time = datetime.datetime.now()
            login_date = ""
            headimgurl = ""
            nickname = ""
            username = ""
            active = 0
            sex = 0
            city = ""
            address = ""
            privilege = 0
            province = ""

            if not user_coll.find_one({'mobile': mobile}):

                user_coll.insert_one({
                    'mobile':mobile,
                    'password1':password1,
                    'password2':password2,
                    'add_time':add_time,
                    'login_date':login_date,
                    'headimgurl':headimgurl,
                    'nickname':nickname,
                    'username':'',
                    'active':active,
                    'sex':sex,
                    'city':city,
                    'address':address,
                    'privilege':privilege,
                    'province':province,
                    'type':type,
                })
                oauth_coll.insert_one({'identifier': mobile,
                                 'secret': password1,
                                 'redirect_uris': [],
                                 'authorized_grants': [oauth2.grant.ClientCredentialsGrant.grant_type]})
            params = {
                'login': mobile,
                'password': password1,
            }
            body = urllib.urlencode(params)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(
                client.fetch,
                "http://localhost:9000" + "/api/user/signin",
                method='POST',
                body=body)
            response_body = json.loads(response.body)
            if response_body.has_key("error"):
                result = utils.reset_response_data(0,response_body["error"] + response_body["error_description"])
                self.finish(result)
                return

            result["data"] = response_body["response"]["data"]
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
        finally:
            logger = BaseModel.get_model("log.LogModel")
            logger.write_log(self.request, result)

        self.finish(result)

class UserSignIn(APIHandler):
    _model = "user.UserModel"

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        user_coll = self.model.get_coll()
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            is_save_password = int(self.get_argument("is_save_password", False))
            if login == "":
                raise Exception("请输入用户名!")
            elif user_coll.find({"mobile":login}).count() == 0 \
                              and user_coll.find({"email":login}).count() == 0:
                raise Exception("手机或邮箱不存在！")
            elif password == "":
                raise Exception("请输入密码!")

            user = user_coll.find_one({"mobile":login}) or user_coll.find_one({"email":login})
            if user["password1"] != password:
                raise Exception("密码错误！")

            user["login_date"] = datetime.datetime.now()
            user_coll.save(user)

            params = {
                'client_id':user["mobile"],
                'client_secret':password,
                'grant_type':'client_credentials',
                'scope':'font-api',
            }
            body = urllib.urlencode(params)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(
                client.fetch,
                  "http://localhost:9000/token",
                  method='POST',
                  body=body)
            response_body = json.loads(response.body)
            try:
                access_token = response_body["access_token"]
            except Exception ,e:
                result = utils.reset_response_data(-1, str(e) + \
                                                   response_body["error"]+" "+\
                                                   response_body["error_description"]+\
                                                   " or password error!")
                self.finish(result)
                return
            if is_save_password:
                self.model.delay_access_token(access_token)

            user["_id"] = str(user["_id"])

            # 存储 token-uid
            self.model.save_token_uid(access_token, user["_id"])

            user["add_time"] = str(user["add_time"]).split(".")[0]
            user["login_date"] = str(user["login_date"]).split(".")[0]
            del user["password1"]
            del user["password2"]
            result["data"] = user
            result["data"]["access_token"] = access_token
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
        finally:
            logger = BaseModel.get_model("log.LogModel")
            logger.write_log(self.request, result)
        self.finish(result)

class UserListHandler(ListAPIHandler):
    _model = "user.UserModel"

class UserRetrieveUpdateDestroyHandler(RetrieveUpdateDestroyAPIHandler):
    _model = "user.UserModel"
    mp_require_params = ["id"]  # put 方法必要参数
    mp_update_params = ["id","mobile","password1","password2","nickname","username"] # put 方法允许参数

    def delete(self):
        result = utils.init_response_data()
        try:
            raise Exception("操作限制！")
        except Exception,e:
            result = utils.reset_response_data(0, str(e))
        self.finish(result)

handlers = [
                (r"/api/user/signup", UserSignUp),
                (r"/api/user/signin", UserSignIn),
                (r"/api/user/list", UserListHandler),
                (r"/api/user", UserRetrieveUpdateDestroyHandler),
            ]
