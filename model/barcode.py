# -*- coding: utf-8 -*-

"""
    alter by: daemon wnag
    alter on 2016-07-14
"""

import pdb

import renren.model.model as model
import renren.libs.utils as utils
import datetime
import os

from renren.libs.utils import options

class BarcodeModel(model.BaseModel,model.Singleton):
    __name = "renren.barcode"

    def __init__(self):
        model.BaseModel.__init__(self,BarcodeModel.__name)

    def generate(self,type,number):
        for i in range(0,int(number)):
            redirect_code = utils.get_random_num(20,'string')
            barcode = {
                "type":type,
                "amount":0,
                "enable_flag":1,
                "add_time":utils.get_now(),
                "expired_time":utils.get_now() + datetime.timedelta(days=365),
                "used_openid":"",
                "used_time":"",
                "remark":"",
                "redirect_code":redirect_code
            }
            self.get_coll().save(barcode)

    def to_file(self,type):
        path = os.path.join(options.root_path,'var','barcode')
        utils.mkdir(path)
        barcode = utils.JsonEncode(self.get_coll().find({"type":type}))
        try:
            f = open(os.path.join(path,'%s_barcodes.txt'%type),'w')
            for r in barcode:
                url = 'http://www.i-caiwu.com/a/r?id='
                data = url + r['redirect_code']
                f.write(data+'\n')
        except:
            print utils.format_error()