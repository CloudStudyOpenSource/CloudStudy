import json
import time

import mysql.connector
from flask import jsonify

from modules import cs_config, cs_encrypt


# 连接数据库
def connectMysql():
    global con
    global cur
    con = mysql.connector.connect(**cs_config.mysql)
    cur = con.cursor()
    print("Connected to Mysql Server")


connectMysql()

cur.execute('''CREATE TABLE IF NOT EXISTS `users`(
   `uid` INT UNSIGNED AUTO_INCREMENT,
   `name` CHAR(20),
   `email` CHAR(250),
   `avatar` JSON,
   `password` CHAR(128),
   `group` INT UNSIGNED,
   `login_time` DATETIME,
   `login_token` CHAR(128),
   PRIMARY KEY (`uid`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
cur.execute('''CREATE TABLE IF NOT EXISTS `groups`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `name` CHAR(20),
   `isAdmin` BOOLEAN,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
cur.execute('''CREATE TABLE IF NOT EXISTS `exams`(
    `id` INT UNSIGNED AUTO_INCREMENT , 
    `name` CHAR(250) , 
    `description` TEXT , 
    `permissions` JSON , 
    `startTime` DATETIME , 
    `endTime` DATETIME , 
    `questions` JSON ,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
cur.execute('''CREATE TABLE IF NOT EXISTS `settings`(
   `key` CHAR(50),
   `value` TEXT,
   PRIMARY KEY (`key`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
con.commit()


def mysqlExecute(*args):
    try:
        cur.execute(*args)
    except:
        print("Err: Lost connection to Mysql Server. Reconnecting...")
        cur.close()
        con.close()
        connectMysql()
        cur.execute(*args)


def jsonResponse(message, data):
    # 返回json响应
    return(jsonify({"message": message, "data": data}))


def generateToken(uid):
    # 生成随机token
    ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    token = cs_encrypt.sha512((json.dumps(
        {"uid": uid, "time": ntime})))
    return(ntime, token)


def checkTokenAvailable(token):
    if(token != None):
        mysqlExecute(
            '''SELECT * FROM `users` WHERE `login_token` = %s''', (token,))
        fetch = cur.fetchall()
        if(len(fetch) == 0):
            return("error", "登录失效")
        else:
            return("success", token)
    else:
        return("error", "登录失效")


def getUserData(token):
    if(token != None):
        cur.execute(
            '''SELECT * FROM `users` WHERE `login_token` = %s''', (token,))
        fetch = cur.fetchall()
        if(len(fetch) == 0):
            return("error", "登录失效")
        else:
            return("success", fetch)
    else:
        return("error", "登录失效")


def api_user_login(email, pwd):
    # 前端用户登录
    mysqlExecute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
    fetch = cur.fetchall()
    if(len(fetch) == 0):
        return(jsonResponse("error", "用户不存在"))
    else:
        if(pwd == fetch[0][3]):
            ntime, token = generateToken(fetch[0][0])
            print(ntime, token)
            cur.execute(
                '''UPDATE `users` SET `login_token` = %s WHERE `users`.`uid` = %s; ''', (token, fetch[0][0]))
            cur.execute(
                '''UPDATE `users` SET `login_time` = %s WHERE `users`.`uid` = %s; ''', (ntime, fetch[0][0]))
            con.commit()
            return(jsonResponse("success", token))
        else:
            return(jsonResponse("error", "密码错误"))


def api_user_register(name, email, pwd):
    # 前端用户注册
    cur.execute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
    if(len(cur.fetchall()) == 0):
        cur.execute(
            '''INSERT INTO `users` (`name`, `email`, `password`) VALUES (%s, %s, %s);''', (name, email, pwd))
        con.commit()
        cur.execute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
        cur.fetchall()
        return(jsonResponse("success", ""))
    else:
        return(jsonResponse("error", "用户已存在"))


def api_user_checkLogin(token):
    # 前端检查token有效
    return(jsonResponse(*checkTokenAvailable(token)))


def api_get_user_data(token):
    return(jsonResponse(*getUserData(token)))


def api_user_getlist():
    return()


# cur.close()
# con.close()
