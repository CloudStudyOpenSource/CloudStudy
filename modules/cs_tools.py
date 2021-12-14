import json
import time
import datetime

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

def jsonResponse(message, data):
    # 返回json响应
    return(json.dumps({"message": message, "data": data}, cls=DateEncoder))
    #return(json.dumps({"message": message, "data": data}))


def generateToken(uid):
    # 生成随机token
    ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    token = cs_encrypt.sha512((json.dumps(
        {"uid": uid, "time": ntime})))
    return(ntime, token)
