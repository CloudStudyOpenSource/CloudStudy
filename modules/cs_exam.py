import json
import time

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql, cs_tools


def api_exam_getlist():
    # jinja2渲染时使用接口，admin获取考试列表
    fetch = cs_sql.session.query(cs_sql.Exam).all()
    return(fetch)


def api_exam_new(data):
    data = json.loads(data)
    #print(data)
    cs_sql.add(cs_sql.Exam(name=data["name"], description=data["description"], permissions=json.dumps(
        data["groups"]), startTime=data['startTime'], endTime=data["endTime"]))
    return cs_tools.jsonResponse("success", None)
