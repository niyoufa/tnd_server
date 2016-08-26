# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
"""

import pdb
import renren.libs.mongolib as mongo
import renren.libs.utils as utils
import sys
import inspect
import datetime

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class BaseModel(object):

    def __init__(self,name):
        self.__name = name

    def coll_name(self):
        return self.__name.split(".")[1]

    def db_name(self):
        return self.__name.split(".")[0]

    def get_coll(self):
        coll_name = self.coll_name()
        coll = mongo.get_coll(coll_name)
        return coll

    def get_columns(self):
        columns = []
        coll = self.get_coll()
        if coll.find().count() > 0:
            document = coll.find_one()
            columns = document.keys()
        return columns

    def is_exist(self,id,column='_id',is_objectid=True):
        if is_objectid:
            items = self.get_coll().find_one({column:utils.create_objectid(id)})
        else:
            items = self.get_coll().find_one({column:id})
        return items != None

    @classmethod
    def get_model(cls,model_name):
        try:
            model_filename = model_name.split(".")[0]
            model_classname = model_name.split(".")[1]
            model_obj = sys.modules['%s.%s'%("renren.model",model_filename)]
            models = inspect.getmembers(model_obj,inspect.isclass)
            for m in models:
                if m[0] == model_classname:
                    model = m[1]()
        except Exception as e:
            model = None
        return model

    def is_exists(self, query_params):
        obj = self.get_coll().find_one(query_params)
        return obj != None

    def create(self, **obj):
        coll = self.get_coll()
        curr_time = datetime.datetime.now()
        obj["add_time"] = str(curr_time)
        coll.insert_one(obj)
        return utils.dump(obj)

    def search(self, query_params):
        coll = self.get_coll()
        obj = coll.find_one(query_params)
        obj = utils.dump(obj)
        return obj

    def update(self, query_params, update_params):
        coll = self.get_coll()
        obj = coll.find_one(query_params)
        if obj:
            obj.update(update_params)
            ret = coll.save(obj)
        else:
            obj = {}
        return utils.dump(obj)

    def delete(self, **query_params):
        coll = self.get_coll()
        ret = coll.remove(query_params)
        return ret

    def search_list(self, page=1, page_size=10):
        query_params = {}
        coll = self.get_coll()
        length = coll.find(query_params).count()
        pager = utils.count_page(length, page, page_size)
        cr = coll.find(query_params).sort("add_date", -1).limit(pager['page_size']).skip(pager['skip'])
        objs = [utils.dump(obj) for obj in cr]
        return objs, pager
