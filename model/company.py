# -*- coding:utf-8 -*-

import pdb,datetime

import renren.model.model as model
import renren.libs.utils as utils


class CompanyModel(model.BaseModel,model.Singleton):
    __name = "renren.company"

    def __init__(self):
        model.BaseModel.__init__(self,CompanyModel.__name)

    def search_list(self,page=1,page_size=10,type="all"):
        query_params = {}

        if type != "all":
            query_params.update({
                "type":type,
            })
        coll = self.get_coll()
        length = coll.find(query_params).count()
        pager = utils.count_page(length, page, page_size)
        cr = coll.find(query_params).sort("add_date", -1).limit(pager['page_size']).skip(pager['skip'])
        objs = [utils.dump(obj) for obj in cr]
        return objs, pager