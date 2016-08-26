# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-14
"""

import pdb
import renren.model.model as model
import renren.libs.mongolib as mongo
import renren.consts as consts
import renren.libs.utils as utils
from bson.son import SON

class CheckCode(model.BaseModel,model.Singleton):
    __name = "renren.checkcode"

    def __init__(self):
        model.BaseModel.__init__(self,CheckCode.__name)
