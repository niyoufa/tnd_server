# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-08-24
"""

import json,pdb
import oauth2
import datetime
import tornado
import urllib
from renren.handler import TokenAPIHandler
from renren.handler import APIHandler
import renren.libs.utils as utils

class ListCreateAPIHandler(APIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    mp_require_params = []  # post 方法必要参数
    mp_default_params = {}  # post 方法默认参数

    def get(self):
        result = utils.init_response_data()
        try:
            request_params = self.format_request_params()
            exec("""objs, pager = self.model.search_list(%s)"""%request_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)

    def post(self):
        result = utils.init_response_data()
        try:
            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()
            exec("""request_params = self.mp_default_params.update(%s)"""%request_params)
            request_params = self.mp_default_params

            query_params = {}
            for key in self.query_params:
                query_params.update({
                    key:request_params[key],
                })

            if query_params=={} or not self.model.is_exists(query_params) :
                obj = self.model.create(**request_params)
                result = utils.dump(obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class RetrieveUpdateDestroyAPIHandler(APIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    mp_require_params = []  # put 方法必要参数
    mp_default_params = {}  # put 方法默认参数
    mp_update_params  = []  # put 方法允许参数
    md_require_params = []  # delete 方法必要参数
    md_default_params = {}  # delete 方法默认参数

    def get(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)
            ret = self.model.search({"_id": _id})
            if ret:
                result["data"] = ret
            else:
                result["data"] = {}
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def put(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)

            address = self.get_argument("address", "")
            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()

            update_params = {}
            exec ("""update_params.update(%s)""" % request_params)
            self.check_update_params(update_params)
            update_params["_id"] = _id
            del update_params["id"]

            ret = self.model.update(query_params={"_id": _id}, update_params=update_params)
            result['data'] = ret
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def check_update_params(self,update_params):
            update_params_keys = update_params.keys()
            for param in update_params:
                if param not in self.mp_update_params:
                    raise Exception("无法修改：%s!"%param)

    def delete(self):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                self.model.delete(_id=_id)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class ListCreateTokenAPIHandler(TokenAPIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    mp_require_params = []  # post 方法必要参数
    mp_default_params = {}  # post 方法默认参数

    def get(self):
        result = utils.init_response_data()
        try:
            request_params = self.format_request_params()
            exec("""objs, pager = self.model.search_list(%s)"""%request_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)

    def post(self):
        result = utils.init_response_data()
        try:
            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()
            exec("""request_params = self.mp_default_params.update(%s)"""%request_params)
            request_params = self.mp_default_params

            query_params = {}
            for key in self.query_params:
                query_params.update({
                    key:request_params[key],
                })

            if not self.model.is_exists(query_params):
                obj = self.model.create(**request_params)
                result = utils.dump(obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class RetrieveUpdateDestroyTokenAPIHandler(TokenAPIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    mp_require_params = []  # put 方法必要参数
    mp_default_params = {}  # put 方法默认参数
    mp_update_params  = []  # put 方法允许参数
    md_require_params = []  # delete 方法必要参数
    md_default_params = {}  # delete 方法默认参数

    def get(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)
            ret = self.model.search({"_id": _id})
            if ret:
                result["data"] = ret
            else:
                result["data"] = {}
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def put(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)

            address = self.get_argument("address", "")
            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()

            update_params = {}
            exec ("""update_params.update(%s)""" % request_params)
            self.check_update_params(update_params)
            update_params["_id"] = _id
            del update_params["id"]

            ret = self.model.update(query_params={"_id": _id}, update_params=update_params)
            result['data'] = ret
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def check_update_params(self,update_params):
            update_params_keys = update_params.keys()
            for param in update_params:
                if param not in self.mp_update_params:
                    raise Exception("无法修改：%s!"%param)

    def delete(self):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                self.model.delete(_id=_id)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class ListAPIHandler(APIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    def get(self):
        result = utils.init_response_data()
        try:
            request_params = self.format_request_params()
            exec ("""objs, pager = self.model.search_list(%s)""" % request_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)

class ListTokenAPIHandler(TokenAPIHandler):
    mg_require_params = []  # get 方法必要参数
    mg_default_params = {}  # get 方法默认参数
    def get(self):
        result = utils.init_response_data()
        try:
            request_params = self.format_request_params()
            exec ("""objs, pager = self.model.search_list(%s)""" % request_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)