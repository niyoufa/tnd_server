# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#

import traceback
import logging
import logging.config
import urllib
import hashlib
import json,time,pdb
import renren.libs.redislib as Redis
import inspect
import sys
import re

from tornado import escape
from tornado.options import options
from tornado.web import RequestHandler as BaseRequestHandler, HTTPError
from renren import exceptions
from renren.libs import utils
from renren.model.model import BaseModel

try:
    import importlib
except:
    from renren.libs import importlib

class Dict(dict):
    def __missing__(self, key):
        rv = self[key] = Dict()
        return rv
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)

class BaseHandler(BaseRequestHandler):
    _model = None

    def initialize(self):
        self.set_model()
        super(BaseHandler,self).initialize()

    def set_model(self):
        self.model = BaseModel.get_model(self._model)
        if self.model is not None:
            self.coll = self.model.get_coll()
        else:
            self.coll = None

    def get(self, *args, **kwargs):
        # enable GET request when enable delegate get to post
        if options.app_get_to_post:
            self.post(*args, **kwargs)
        else:
            raise exceptions.HTTPAPIError(405)

    def prepare(self):
        self.traffic_control()
        pass

    def traffic_control(self):
        # traffic control hooks for api call etc
        self.log_apicall()
        pass

    def log_apicall(self):
        pass

    def format_arguments(self):
        arguments = self.request.arguments
        obj = Dict()
        for (k,v) in arguments.items():
            try:
                exec("%s = '%s'"%(k,v[0].decode()))
            except UnicodeDecodeError as e:
                exec("%s = '%s'"%(k,v[0]))
            except Exception as e:
                print(e)
                pass
        return obj

    def format_request_params(self):
        arguments = self.request.arguments
        format_params = u""
        for (k, v) in arguments.items():
            try:
                try:
                    format_params += unicode("%s = %s," % (k, json.loads(v[0].decode())))
                except:
                    format_params += unicode("%s = '%s'," % (k, v[0].decode()))
            except UnicodeDecodeError as e:
                try:
                    temp = "%s = %s," % (k, json.loads(v[0]))
                except:
                    temp = "%s = '%s'," % (k, v[0])
                format_params += temp.decode("utf-8")
            except Exception as e:
                print(e)
                pass
        return format_params

    def check_request_params(self,require_params=[]):
        arguments_keys = self.request.arguments.keys()
        for require_param in require_params:
            if require_param not in arguments_keys:
                raise Exception("params %s 不能为空！"%require_param)

class RequestHandler(BaseHandler):
    pass


class APIHandler(BaseHandler):
    def get_current_user(self):
        pass

    def finish(self, chunk=None, notification=None,origin=False,status_code=200):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","X-Requested-With,Set-Cookie")
        self.set_header("Access-Control-Allow-Methods","PUT,DELETE,POST,GET")
        self.set_header('Content-type', 'application/x-www-form-urlencoded; charset=utf-8')
        #设置header键值对
        if chunk is None:
            chunk = {}

        if isinstance(chunk, dict):#chunk默认情况下给chunk一个dict地址值，并执行下列步骤
            if origin != True:
                chunk = {"meta": {"code": status_code}, "response": chunk}  #orgin默认情况下给chunk赋"meta"={"code":200}
                                                                        #"response"=上次的chunk的字典内容

            if notification:
                chunk["notification"] = {"message": notification}#如果notification有值则再chunk中添加notification键值对

        callback = escape.utf8(self.get_argument("callback", None))

        #self.set_header("Access-Control-Allow-Credentials",'true')

        if callback:
            self.set_header("Content-Type", "application/x-javascript; charset=utf-8;")

            if isinstance(chunk, dict):
                chunk = escape.json_encode(chunk)

            self._write_buffer = [callback, "(", chunk, ")"] if chunk else []
            super(APIHandler, self).finish()
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            super(APIHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        debug = self.settings.get("debug", False)
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]

            if isinstance(e, exceptions.HTTPAPIError):
                pass
            elif isinstance(e, HTTPError):
                e = exceptions.HTTPAPIError(e.status_code)
            else:
                e = exceptions.HTTPAPIError(500)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            if status_code == 500 and not debug:
                #self._send_error_email(exception)
                e.response["exception"] = exception

            if debug:
                e.response["exception"] = exception

            self.clear()
            self.set_status(200)  # always return 200 OK for API errors
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish(unicode(e))
        except Exception:
            logging.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)
'''
    def _send_error_email(self, exception):
        try:
            # send email
            subject = "[%s]Internal Server Error" % options.sitename
            body = self.render_string("errors/500_email.html",
                                      exception=exception)
            if options.send_error_email:
                email_tasks.send_email_task.delay(options.email_from,
                                                  options.admins, subject, body)
        except Exception:
            logging.error(traceback.format_exc())
'''

#带加密字段的处理器
class TokenAPIHandler(APIHandler):

    def initialize(self, provider):
        self.provider = provider

    # authenticate tokens
    def prepare(self):
        try:
            token = self.get_argument('access_token', None)
            if not token:
                auth_header = self.request.headers.get('Authorization', None)
                if not auth_header:
                    raise Exception('This resource need a authorization token')
                token = auth_header[7:]

            key = 'oauth2_{}'.format(token)
            access = self.provider["provider"].access_token_store.rs.get(key)
            if access:
                access = json.loads(access.decode())
            else:
                raise Exception('Invalid Token')
            if access['expires_at'] <= int(time.time()):
                raise Exception('expired token')
            authority = importlib.import_module("renren.authority").authority
            authority.process(self.request,access)
        except Exception as err:
            self.set_header('Content-Type', 'application/json')
            self.set_status(401)
            result = utils.reset_response_data(0, str(err))
            self.finish(result,status_code=401)

    def get_user_id(self):
        token = self.get_argument('access_token', None)
        if not token:
            auth_header = self.request.headers.get('Authorization', None)
            if not auth_header:
                raise Exception('This resource need a authorization token')
            token = auth_header[7:]
        redis_tool = Redis.RedisTool()
        user_id = redis_tool.get(token)
        return utils.create_objectid(user_id)

class ErrorHandler(RequestHandler):
    """Default 404: Not Found handler."""
    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise HTTPError(404)


class APIErrorHandler(APIHandler):
    """Default API 404: Not Found handler."""
    def prepare(self):
        super(APIErrorHandler, self).prepare()
        raise exceptions.HTTPAPIError(404)
