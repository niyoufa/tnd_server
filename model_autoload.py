#coding=utf-8

import pdb
import os
import importlib

_model_file_list = os.listdir(os.path.dirname(__file__)+"/model")
model_module_names = [name.split(".")[0] for name in _model_file_list \
                      if not name.endswith(".pyc") and name not in ["__init__.py","mongo.py","Redis.py"]]
def _generate_collections(root_module,model_module_names):
    for name in model_module_names:
        model_module = importlib.import_module(".%s" % name, root_module)
        model_name = getattr(model_module, "", None)

collections = _generate_collections("renren.model",model_module_names)