# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-01-09
#


from renren.libs import utils
from renren.handler import BaseHandler
from renren.model.model import BaseModel

class AdminHandler(BaseHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        query_list = {}
        try:
            page = self.get_argument("page",1)
            page_size = self.get_argument("page_size",15)

            query_list['enable_flag'] = 1
            result["data"],result["pager"] = self.model.list(query_list,page,page_size)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.render("admin/product/product-list.html",result=result,search='')


handlers = [
            (r"/admin", AdminHandler),
            ]
