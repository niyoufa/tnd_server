# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-08-22
"""

import json,pdb
import oauth2
import datetime
import tornado
import urllib
from renren.handler import TokenAPIHandler
from renren.handler import APIHandler
import renren.libs.utils as utils
from base import *

class CompanyListCreateHandler(ListCreateAPIHandler):
    _model = "company.CompanyModel"
    mg_require_params = [] # get 方法必要参数
    mg_default_params = {} # get 方法默认参数
    mp_require_params = ["company_name","company_scale","specialty","address"] #post 方法必要参数
    mp_default_params = dict( #post 方法默认参数
        taxpayers_type="",
        company_property = "",
        phone="",
        email="",
        province="",
        city="",
        area="",
        remark="",
        register_address=""
    )
    query_params = ["company_name"]

class CompanyRetrieveUpdateDestroyHandler(RetrieveUpdateDestroyAPIHandler):
    _model = "company.CompanyModel"
    mp_require_params = ["id"]  # put 方法必要参数
    mp_update_params = ["id","address","province","city","remark","company_property",
                        "area","specialty","register_address","email","phone","taxpayers_type",
                        "company_scale","company_name"] # put 方法允许参数

handlers = [
    (r"/api/company/list", CompanyListCreateHandler),
    (r"/api/company", CompanyRetrieveUpdateDestroyHandler),
]