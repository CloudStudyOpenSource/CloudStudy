from datetime import datetime
import json
import time

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql, cs_tools

from server import app




def checkTokenAvailable(token):
    if(token != None):
        fetch = cs_sql.session.query(cs_sql.User).filter(
            cs_sql.User.loginToken == token)
        if(fetch.count() == 0):
            return("error", "登录失效")
        else:
            return("success", token)
    else:
        return("error", "登录失效")


def getUserData(token):
    if(token != None):
        fetch = cs_sql.session.query(cs_sql.User).filter(
            cs_sql.User.loginToken == token)
        if(fetch.count() == 0):
            return("error", "登录失效")
        else:
            return("success", fetch.first().to_dict())
    else:
        return("error", "登录失效")


def uploadUserData(token, data):
    data = json.loads(data)
    if(token != None):
        fetch = cs_sql.session.query(cs_sql.User).filter(
            cs_sql.User.loginToken == token)
        if(fetch.count() == 0):
            return("error", "登录失效")
        else:
            if(data["email"] != ""):
                fetch.first().name = data["name"]
                fetch.first().email = data["email"]
                fetch.first().avatar = data["avatar"]
                fetch.first().password = data["password"]
                fetch.first().settings = data["settings"]
                cs_sql.commit()
                return("success", None)
            else:
                return("error", "邮箱不能为空")
    else:
        return("error", "登录失效")


def api_user_login(email, pwd):
    # 前端用户登录
    fetch = cs_sql.session.query(cs_sql.User).filter(
        cs_sql.User.email == email)
    if(fetch.count() == 0):
        return(cs_tools.jsonResponse("error", "用户不存在"))
    else:
        if(pwd == fetch.first().password):
            ntime, token = cs_tools.generateToken(fetch.first().id)
            fetch.first().loginToken = token
            fetch.first().loginTime = ntime
            cs_sql.commit()
            return(cs_tools.jsonResponse("success", token))
        else:
            return(cs_tools.jsonResponse("error", "密码错误"))


def api_user_register(name, email, pwd):
    # 前端用户注册
    fetch = cs_sql.session.query(cs_sql.User).filter(
        cs_sql.User.email == email)
    if(fetch.count() == 0):
        cs_sql.add(cs_sql.User(name=name, email=email,
                   avatar="/static/favicon.png", password=pwd, group="1", createTime=datetime.now(), settings="{}"))
        cs_sql.commit()
        return(cs_tools.jsonResponse("success", ""))
    else:
        return(cs_tools.jsonResponse("error", "用户已存在"))


def api_user_checkLogin(token):
    # 前端检查token有效
    return(cs_tools.jsonResponse(*checkTokenAvailable(token)))


def api_get_user_data(token):
    return(cs_tools.jsonResponse(*getUserData(token)))


def api_upload_user_data(token, data):
    return(cs_tools.jsonResponse(*uploadUserData(token, data)))


def api_get_user_object(token):
    # jinja2渲染时使用接口，获取当前登录用户
    user = getUserData(token)
    if(user[0] == "success"):
        user = user[1]
    else:
        user = None
    return user


def api_user_getlist():
    # jinja2渲染时使用接口，admin获取用户列表
    fetch = cs_sql.session.query(cs_sql.User).all()
    return(fetch)


def api_group_getlist():
    # jinja2渲染时使用接口，admin获取分组列表
    fetch = cs_sql.session.query(cs_sql.Group).all()
    return(fetch)
