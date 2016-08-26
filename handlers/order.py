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

class OrderListCreateHandler(ListCreateAPIHandler):
    _model = "order.OrderModel"
    mg_require_params = [] # get 方法必要参数
    mg_default_params = {} # get 方法默认参数
    mp_require_params = ["uid","product_name","price","desc",
                         "start_time","deadline",
                         "taxpayerstype","company_name","company_scale","specialty","register_address","address",
                         "mobile","checkcode","password1",
                         "discount_code",
                         "total_amount","actual_amount"] #post 方法必要参数
    mp_default_params = dict( #post 方法默认参数
        order_type="园区下单",
        order_status=3,
        servicesproviderid=None,
        payway="alipay",
    )
    query_params = []

    def post(self):
        ListCreateAPIHandler.post(self)

class OrderRetrieveUpdateDestroyHandler(RetrieveUpdateDestroyAPIHandler):
    _model = "order.OrderModel"

    def put(self):
        result = utils.init_response_data()
        try:
            raise Exception("操作限制！")
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
        self.finish(result)

handlers = [
    (r"/api/order/list", OrderListCreateHandler),
    (r"/api/order", OrderRetrieveUpdateDestroyHandler),
]