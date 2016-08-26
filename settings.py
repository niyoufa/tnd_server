# -*- coding: utf-8 -*-
#
# @author: Daemon wang
# Created on 2016-03-02
#

import platform
import os
import time

import renren
root_dir = os.path.dirname(os.path.abspath(renren.__file__))
root_path = root_dir

###配置区开始
hostname = "iZ2370ct37bZ"
port = 9000
mongo = {
            "host":"localhost",
            "port":27017,
            "database":"renren",
            "user":"renren",
            "password":"renrenAdmin",
        }

redis = {
    "host":"localhost",
    "port":6379,
    "db":0
}

smtp = {"host": "",
        "user": "",
        "password": "",
        "duration": 30,
        "tls": True
        }
root_log_path = os.path.join(root_path,'var','log')
###配置区结束

loglevel = "INFO"  # for celeryd
app_url_prefix = ""
sitename = "renren api"
domain = ""
home_url = "http://%s/api" % domain


cookie_secret = "ace87395-8272-4749-b2f2-dcabd3901a1c"
xsrf_cookies = False

if platform.node() == hostname:
    debug = False
    host = 'personcredit'
    login_url = "https://www.personcredit.com/login"
else:
    debug = True
    host = 'localhost:8002'
    login_url = "http://localhost:8002/login"

###分页相关设置
#一页显示的条数
page_size = 15
#最多显示的页数
page_show = 10
