# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#

from tornado.options import options

def get_status_from_value(dict,value,desc=1):
    for d,x in dict.items():
        if x[0] == value:
            return x[desc]

def get_consts(dict,key,index=0):
    return dict[key][index]

CATEGORY_AMERICAS = "Americas"
CATEGORY_EUROPE = "Europe"
CATEGORY_ASIA = "Asia"
CATEGORYS = (CATEGORY_AMERICAS, CATEGORY_EUROPE, CATEGORY_ASIA)

SUBSCRIBE_STATUS_ON = "on"
SUBSCRIBE_STATUS_OFF = "off"