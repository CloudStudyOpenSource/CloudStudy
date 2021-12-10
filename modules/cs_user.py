import json
import time

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql, cs_tools


def checkTokenAvailable(token):
    if(token != None):
        cs_sql.mysqlExecute(
            '''SELECT userId FROM `users` WHERE `loginToken` = %s''', (token,))
        fetch = cs_sql.cur.fetchall()
        # print(fetch,fetch["name"])
        if(len(fetch) == 0):
            return("error", "登录失效")
        else:
            return("success", token)
    else:
        return("error", "登录失效")


def getUserData(token):
    if(token != None):
        cs_sql.mysqlExecute(
            '''SELECT `userId`,`name`,`email`,`avatar`,`group`,`createTime`,`settings` FROM `users` WHERE `loginToken` = %s''', (token,))
        fetch = cs_sql.cur.fetchall()
        if(len(fetch) == 0):
            return("error", "登录失效")
        else:
            return("success", fetch)
    else:
        return("error", "登录失效")


def uploadUserData(token, data):
    data = json.loads(data)
    fetch = checkTokenAvailable(token)
    if(fetch[0] == "success"):
        if(data[2] != ""):
            cs_sql.mysqlExecute(
                '''UPDATE `users` SET `name` = %s,`email` = %s,`avatar` = %s,`settings` = %s WHERE `users`.`userId` = %s; ''', (data[1], data[2], data[3],  data[6], fetch[1][0]))
            cs_sql.con.commit()
            return("success", None)
        else:
            return("error", "邮箱不能为空")
    else:
        return(fetch)


def api_user_login(email, pwd):
    # 前端用户登录
    cs_sql.mysqlExecute(
        '''SELECT userId,password FROM `users` WHERE `email` = %s''', (email,))
    fetch = cs_sql.cur.fetchall()
    # print(fetch)
    if(len(fetch) == 0):
        return(cs_tools.jsonResponse("error", "用户不存在"))
    else:
        if(pwd == fetch[0][1]):
            ntime, token = cs_tools.generateToken(fetch[0][0])
            print(ntime, token)
            cs_sql.mysqlExecute(
                '''UPDATE `users` SET `loginToken` = %s WHERE `users`.`userId` = %s; ''', (token, fetch[0][0]))
            cs_sql.mysqlExecute(
                '''UPDATE `users` SET `loginTime` = %s WHERE `users`.`userId` = %s; ''', (ntime, fetch[0][0]))
            cs_sql.con.commit()
            return(cs_tools.jsonResponse("success", token))
        else:
            return(cs_tools.jsonResponse("error", "密码错误"))


def api_user_register(name, email, pwd):
    # 前端用户注册
    cs_sql.mysqlExecute(
        '''SELECT userId FROM `users` WHERE `email` = %s''', (email,))
    if(len(cs_sql.cur.fetchall()) == 0):
        cs_sql.mysqlExecute(
            '''INSERT INTO `users` (`name`, `email`, `avatar`, `password`, `settings`) VALUES (%s, %s, %s, %s, %s);''', (name, email, "{}", pwd, "{}"))
        cs_sql.con.commit()
        # cs_sql.mysqlExecute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
        # cs_sql.cur.fetchall()
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
        user = user[1][0]
    else:
        user = None
    return user


def api_user_getlist():
    # jinja2渲染时使用接口，admin获取用户列表
    cs_sql.mysqlExecute('''SELECT * FROM `users`''')
    return(cs_sql.cur.fetchall())


def api_group_getlist():
    # jinja2渲染时使用接口，admin获取分组列表
    cs_sql.mysqlExecute('''SELECT * FROM `groups`''')
    return(cs_sql.cur.fetchall())
