# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-04-14
#
from suds import WebFault
from suds.client import Client
import pyDes
import base64
import types
# import logging
# import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# log_path = os.path.dirname(__file__)+'/../var/log/'
# print log_path
# if not os.path.exists(log_path):
#     os.makedirs(log_path)
#
# logging.basicConfig(level=logging.INFO, filename=os.path.join(log_path,'ws.log'))
# logging.getLogger('suds.client').setLevel(logging.DEBUG)

def encode(str):
    if type(str) == types.UnicodeType:
        str = str.encode("utf-8")
    key = pyDes.des('12312312',pyDes.CBC, "12312312", pad=None,padmode=pyDes.PAD_PKCS5)
    des_data = key.encrypt(str)
    b_data = base64.b64encode(des_data)
    return b_data

def decode(secret):
    key = pyDes.des('12312312',pyDes.CBC, "12312312", pad=None,padmode=pyDes.PAD_PKCS5)
    b_secret = base64.b64decode(secret)
    des_secret = key.decrypt(b_secret)
    return des_secret

def send_msg(mobile,content):

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <REQ>
    <SIGN>
    <USERNAME>CJWM0NMK</USERNAME>
    <PASSWORD>jv1p0fv38QZKnUkR</PASSWORD>
    </SIGN>
    <PARMAS>
    <ITEM>
    <MOBILE>%s</MOBILE>
    <MSGCONTENT>%s</MSGCONTENT>
    <MSGSIGN>21</MSGSIGN>
    </ITEM>
    </PARMAS>.
    </REQ>
    '''%(mobile,content)

    client = Client('http://192.168.99.84:8080/eis/webService/BizInvestService?wsdl')
    # client = Client('http://139.159.35.187:8080/eis/webService/BizInvestService?wsdl')
    # client = Client('http://192.168.201.69:8080/eis/webService/BizInvestService?wsdl')
    str = encode(xml)
    try:
        secret = client.service.sendMsgMd(str)
        res = decode(secret)
    except WebFault as detail:
        res = detail
    tree = ET.fromstring(res)
    code = tree.find('CODE').text
    return code

def test(str=''):
    if str == '':
        xml = '''
        <REQ>
        <SIGN>
        <USERNAME></USERNAME>
        <PASSWORD></PASSWORD>
        </SIGN>
        <PARMAS>
        <ITEM>
        <MOBILE></MOBILE>
        <MSGCONTENT></MSGCONTENT>
        </ITEM>
        </PARMAS>
        </REQ>
        '''
        print encode(xml)
    else:
        print decode(str)
if __name__ ==  "__main__":
    print send_msg(15151834774,"尊敬的用户您好，您本次的验证码为654321,30分钟内有效")