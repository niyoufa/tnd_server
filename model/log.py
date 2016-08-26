# -*- coding:utf-8 -*-

import pdb
import sys, os
import renren.model.model as model
import renren.libs.utils as utils

class LogModel(model.BaseModel,model.Singleton):
    __name = "renren.log"

    def __init__(self):
        model.BaseModel.__init__(self,LogModel.__name)


    def write_log(self,request,response={},type="normal"):
        log_coll = self.get_coll()
        headers = {}
        log_document = {
            "method":request.method,
            "uri":request.uri,
            "remote_ip":request.remote_ip,
            "time":utils.get_current_time(),
            "headers":headers,
            "params":'',
            "response":response,
            "type":type,
        }

        log_coll.insert_one(log_document)
        self.write_log_to_file(log_document)

    def write_log_to_file(self,log_document):
        if not os.path.exists("var/log"):
            os.makedirs("var/log")
        f = open("var/log/log.txt","w")
        f.write(str(log_document["time"])+'  '+str(log_document["remote_ip"])+'  '+str(log_document["headers"])+"\n")
        f.close()

