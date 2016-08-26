# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-01-09
#

from renren.libs import utils
from renren.handler import APIHandler

class BarcodeHandler(APIHandler):
    _model = 'barcode.BarcodeModel'

    def post(self):
        result = utils.init_response_data()
        try:
            type = self.get_argument("type","BAR001")
            number = self.get_argument("number",0)
            self.model.generate(type,number)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

    def put(self):
        result = utils.init_response_data()
        try:
            type = self.get_argument("type","BAR001")
            self.model.to_file(type)
        except Exception as e:
            result = utils.reset_response_data(0,unicode(e))
        self.finish(result)

handlers = [
            (r"/api/barcode", BarcodeHandler),
            ]