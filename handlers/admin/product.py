
# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-01-09
#


from renren.libs import utils
from renren.handler import BaseHandler
from renren.model.model import BaseModel

class AdminProductListHandler(BaseHandler):
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

class AdminProductCreateHandler(BaseHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        result['mode'] = ''
        self.render("admin/product/product-create.html",result=result)

    def post(self):
        result = utils.init_response_data()
        arguments = self.format_arguments()
        try:
            for (k,v) in arguments.items():
                if k in ['price','origin_price']:
                    del arguments[k]
                    try:
                        arguments[k] = float(v)
                    except:
                        raise ValueError(u"价格格式有误")
                if k in ['on_sale_flag','sort']:
                    del arguments[k]
                    try:
                        arguments[k] = int(v)
                    except:
                        raise ValueError(u"%s栏位应为整数"%k)
            arguments['add_time'] = utils.get_now()
            arguments['enable_flag'] = 1
            arguments['on_sale_flag'] = 1

            self.model.create(arguments)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        result['alert'] = 1
        self.render("admin/product/product-create.html",result=result,search='')

class AdminProductEditHandler(BaseHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        product_id = self.get_argument("product_id","")
        try:
            if not self.model.is_exist(product_id):
                raise ValueError(u"该商品不存在")
            result['data'] = self.coll.find_one({"_id":utils.create_objectid(product_id)})
            result['mode'] = ''
        except Exception as e:
            result['alert'] = 1
            result = utils.reset_response_data(0,unicode(e))
        self.render("admin/product/product-edit.html",result=result)

    def post(self):
        result = utils.init_response_data()
        arguments = self.format_arguments()
        try:
            for (k,v) in arguments.items():
                if k in ['price','origin_price']:
                    del arguments[k]
                    try:
                        arguments[k] = float(v)
                    except:
                        raise ValueError(u"价格格式有误")
                if k in ['on_sale_flag','sort']:
                    del arguments[k]
                    try:
                        arguments[k] = int(v)
                    except:
                        raise ValueError(u"%s栏位应为整数"%k)

            self.model.edit(arguments)
            result['data'] = arguments
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        result['alert'] = 1
        self.render("admin/product/product-edit.html",result=result,search='')

class AdminProductDeleteHandler(BaseHandler):
    _model = 'product.ProductModel'

    def get(self):
        result = utils.init_response_data()
        product_id = self.get_argument("product_id","")
        try:
            if not self.model.is_exist(product_id):
                raise ValueError(u"该商品不存在")
            self.model.edit({"enable_flag":0,"_id":utils.create_objectid(product_id)})
            result['data'],result['pager'] = self.model.list()
            result['mode'] = ''
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        result['alert'] = 1
        self.render("admin/product/product-list.html",result=result,search='')


handlers = [
            (r"/admin/product/list", AdminProductListHandler),
            (r"/admin/product/create", AdminProductCreateHandler),
            (r"/admin/product/edit", AdminProductEditHandler),
            (r"/admin/product/delete", AdminProductDeleteHandler),
            ]
