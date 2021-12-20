import json
import time
import datetime

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql



def jsonResponse(message, data):
    # 返回json响应
    return(json.dumps({"message": message, "data": data}))
    #return(json.dumps({"message": message, "data": data}))


def generateToken(uid):
    # 生成随机token
    ntime = int(time.time())
    token = cs_encrypt.sha512((json.dumps(
        {"uid": uid, "time": ntime})))
    return(ntime, token)
