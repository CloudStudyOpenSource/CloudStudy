import json
import time
import copy

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql, cs_tools


def api_exam_getGroupNames(examId):
    fetch = cs_sql.session.query(cs_sql.Exam).get(examId)
    #print(fetch)
    groups = []
    #print(groups)
    for each in json.loads(fetch.permissions):
        groups.append(cs_sql.session.query(cs_sql.Group).get(each).name)
        #print(each)
    #print(groups)
    return groups


def api_exam_getlist():
    # jinja2渲染时使用接口，admin获取考试列表
    fetch = copy.deepcopy(cs_sql.session.query(cs_sql.Exam).all())
    r = []
    for each in fetch:
        each.permissions=api_exam_getGroupNames(each.id)
        r.append(each.to_dict())
    return(json.dumps(r))


def api_exam_get(id):
    # jinja2渲染时使用接口，admin获取考试信息
    fetch = cs_sql.session.query(cs_sql.Exam).get(id).to_dict()
    return(fetch)


def api_exam_new(data):
    data = json.loads(data)
    # print(data)
    li = []
    for each in data["groups"]:
        li.append(int(each["id"]))
    cs_sql.add(cs_sql.Exam(name=data["name"], description=data["description"], permissions=json.dumps(
        li), startTime=data['startTime'], endTime=data["endTime"]))
    return cs_tools.jsonResponse("success", None)


def api_exam_update(id,data):
    data = json.loads(data)
    # print(data)
    li = []
    for each in data["groups"]:
        li.append(int(each["id"]))
    fetch = cs_sql.session.query(cs_sql.Exam).get(id)
    fetch.name=data["name"]
    fetch.description = data["description"]
    fetch.permissions = json.dumps(        li)
    fetch.startTime = data['startTime']
    fetch.endTime = data["endTime"]
    cs_sql.commit()
    return cs_tools.jsonResponse("success", None)
