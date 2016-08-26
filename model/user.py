# -*- coding:utf-8 -*-

import pdb,datetime,json

import renren.model.model as model
import renren.libs.utils as utils
import renren.libs.redislib as redis


class UserModel(model.BaseModel,model.Singleton):
    __name = "renren.user"

    def __init__(self):
        model.BaseModel.__init__(self,UserModel.__name)

    def search_list(self,page=1,page_size=10,type="all"):
        query_params = {}

        if type != "all":
            query_params.update({
                "type":type,
            })
        coll = self.get_coll()
        length = coll.find(query_params).count()
        pager = utils.count_page(length, page, page_size)
        cr = coll.find(query_params).sort("add_date", -1).limit(pager['page_size']).skip(pager['skip'])
        objs = [utils.dump(obj) for obj in cr]
        return objs, pager

    def get_token_uid(self, token):
        redis_tool = redis.RedisTool()
        uid = redis_tool.get(token)
        return uid

    def save_token_uid(self, token, uid):
        redis_tool = redis.RedisTool()
        if not redis_tool.get(token):
            redis_tool.set(token, uid)
        else:
            pass

    def delay_access_token(self, token):
        redis_tool = redis.RedisTool()
        oauth2_key = "oauth2_" + token
        access = redis_tool.get(oauth2_key)
        access = json.loads(access)
        access["expires_at"] += 3600 * 24 * 14
        access = json.dumps(access)
        redis_tool.set(oauth2_key, access)

    def _get_search_time(self, time_desc, start_time, end_time):
        if time_desc == "user_defined":
            if not start_time or not end_time:
                raise Exception("请选择时间！")
            # start_time = utils.strtodatetime(start_time, '%Y-%m-%d %H:%M:%S')
            # end_time = utils.strtodatetime(end_time,'%Y-%m-%d %H:%M:%S')
            start_time = utils.strtodatetime(start_time, '%Y-%m-%d %H:%M')
            end_time = utils.strtodatetime(end_time, '%Y-%m-%d %H:%M')
            return start_time, end_time
        else:
            curr_time = datetime.datetime.now()
            end_time = curr_time
            if time_desc == "nearly_three_days":
                start_time = curr_time - datetime.timedelta(days=3)
            elif time_desc == "nearly_a_week":
                start_time = curr_time - datetime.timedelta(days=7)
            elif time_desc == "nearly_a_month":
                start_time = curr_time - datetime.timedelta(days=30)
            else:
                raise Exception("查询时间未定义")
        return start_time, end_time
