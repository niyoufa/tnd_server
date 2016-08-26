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

class CommunityListCreateHandler(ListCreateAPIHandler):
    _model = "community.CommunityModel"
    mg_require_params = [] # get 方法必要参数
    mg_default_params = {} # get 方法默认参数
    mp_require_params = ["community_name","address","product"] #post 方法必要参数
    mp_default_params = dict( #post 方法默认参数
       logo="",
        product = dict(
            product_name = "一键记账",
            price = "300-500",
            desc="",
            description="",
            deadine="三个月",
        )
    )
    query_params = ["community_name"]

class CommunityRetrieveUpdateDestroyHandler(RetrieveUpdateDestroyAPIHandler):
    _model = "community.CommunityModel"
    mp_require_params = ["id"]  # put 方法必要参数
    mp_update_params = ["id","community_name","address","product","logo"] # put 方法允许参数

handlers = [
    (r"/api/community/list", CommunityListCreateHandler),
    (r"/api/community", CommunityRetrieveUpdateDestroyHandler),
]