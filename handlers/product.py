# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-01-09
#

import datetime,pdb,json

from renren.libs import utils
from renren.handler import APIHandler

class ProductHandler(APIHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        try:
            product_id = self.get_argument("product_id","")
            product = self.coll.find_one({"_id":utils.create_objectid(product_id)})
            result["data"] = utils.dump(product)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

    def put(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        result = utils.init_response_data()
        try:
            sku = self.get_argument("sku","")
            name = self.get_argument("name","")
            sort = self.get_argument("sort",0)
            image = self.get_argument("image","")
            show_code = self.get_argument("show_code","")
            show_name = self.get_argument("show_name","")
            enable_flag = self.get_argument("enable_flag",1)
            on_sale_flag = self.get_argument("on_sale_flag",1)
            origin_price = self.get_argument("origin_price",0.0)
            price = self.get_argument("price",0.0)
            type = self.get_argument("type", "")
            desc = self.get_argument("desc","")

            add_time = datetime.datetime.now()

            if type == "":
                raise Exception("类型不能为空")

            query_params = dict(
                type = type,
            )
            if not self.model.is_exists(query_params):

                obj = self.model.create(dict(sku=sku,name=name,sort=sort,image=image,show_code=show_code,show_name=show_name,
                                    enable_flag=enable_flag,on_sale_flag=on_sale_flag,origin_price=origin_price,
                                    price=price,type=type,desc=desc,add_time=add_time))
                obj = utils.dump(obj)
                result["data"] = obj
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def delete(self, *args, **kwargs):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                self.model.delete(_id=_id)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class ProductListHandler(APIHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        query_list = {}
        try:
            page = self.get_argument("page",1)
            page_size = self.get_argument("page_size",15)
            type = self.get_argument("type",None)
            if type is not None:
                query_list['type'] = type
            query_list['enable_flag'] = 1
            result["data"],result["pager"] = self.model.list(query_list,page,page_size)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

class ProductShowHandler(APIHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        try:
            show_code = self.get_argument("show_code","")
            result["data"] = self.model.get_show_products(show_code)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)


handlers = [
            (r"/api/product/list", ProductListHandler),
            (r"/api/product", ProductHandler),
            (r"/api/product/show", ProductShowHandler),
            ]