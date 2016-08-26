# -*- coding:utf-8 -*-

import pdb,datetime

import renren.model.model as model
import renren.libs.utils as utils


class CommunityModel(model.BaseModel,model.Singleton):
    __name = "renren.community"

    def __init__(self):
        model.BaseModel.__init__(self,CommunityModel.__name)