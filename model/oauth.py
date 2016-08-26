# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
"""

from bson.son import SON
import renren.model.model as model
import renren.libs.mongolib as mongo
import renren.consts as consts
import renren.libs.utils as utils

class OauthModel(model.BaseModel,model.Singleton):
    __name = "renren.oauth_clients"

    def __init__(self):
        model.BaseModel.__init__(self,OauthModel.__name)