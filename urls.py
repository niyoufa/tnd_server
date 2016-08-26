# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#

from tornado.options import options
from tornado.web import url
from renren.handler import APIErrorHandler
import sys

handlers = []
ui_modules = {}

# the module names in handlers folder


# TODO 写一个函数自动获取该list值
handler_names = ["main","product","company","community","user","oauth","checkcode","order"]
admin_names = ["admin","product"]
modelnames = ["log","product","company","community","user","oauth","checkcode","order"]

def _generate_handler_patterns(root_module, handler_names, prefix=""):
    for name in handler_names:
        module_name = "%s.%s" % (root_module,name)
        __import__(module_name)
        module = sys.modules[module_name]
        module_hanlders = getattr(module, "handlers", None)
        if module_hanlders:
            _handlers = []
            for handler in module_hanlders:
                try:
                    patten = r"%s%s" % (prefix, handler[0])
                    if len(handler) == 2:
                        _handlers.append((patten,
                                          handler[1]))
                    elif len(handler) == 3:
                        _handlers.append(url(patten,
                                             handler[1],
                                             {"provider":handler[2]})
                                         )
                    else:
                        pass
                except IndexError:
                    pass

            handlers.extend(_handlers)

def _autoload_models(root_module,modelnames):
    for name in modelnames:
        module_name = "%s.%s" % (root_module,name)
        __import__(module_name)

_generate_handler_patterns("renren.handlers", handler_names)
_generate_handler_patterns("renren.handlers.admin", admin_names)
_autoload_models("renren.model",modelnames)


# Override Tornado default ErrorHandler
handlers.append((r".*", APIErrorHandler))
