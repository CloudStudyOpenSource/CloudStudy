import json
import time

import mysql.connector
from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql


# 连接数据库

cs_sql.connectMysql()

cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `users`(
   `userId` INT UNSIGNED AUTO_INCREMENT,
   `name` CHAR(20),
   `email` CHAR(250),
   `avatar` JSON,
   `password` CHAR(128),
   `group` INT DEFAULT '1',
   `loginTime` DATETIME,
   `loginToken` CHAR(128),
   `createTime` DATETIME DEFAULT CURRENT_TIMESTAMP,
   `settings` JSON,
   PRIMARY KEY (`userId`)
)DEFAULT CHARSET=utf8;''')
cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `groups`(
   `groupId` INT UNSIGNED AUTO_INCREMENT,
   `name` CHAR(20),
   `isAdmin` BOOLEAN,
   `permissions` JSON,
   PRIMARY KEY (`groupId`)
)DEFAULT CHARSET=utf8;''')
cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `exams`(
    `examId` INT UNSIGNED AUTO_INCREMENT , 
    `name` CHAR(250) , 
    `description` TEXT , 
    `permissions` JSON , 
    `startTime` DATETIME , 
    `endTime` DATETIME , 
    `questions` JSON ,
   PRIMARY KEY (`examId`)
)DEFAULT CHARSET=utf8;''')
cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `questions`(
    `questionId` INT UNSIGNED AUTO_INCREMENT , 
    `examId` INT , 
    `type` TEXT , 
    `question` TEXT , 
    `answer` TEXT , 
    `score` FLOAT , 
   PRIMARY KEY (`questionId`)
)DEFAULT CHARSET=utf8;''')
cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `answers`(
    `answerId` INT UNSIGNED AUTO_INCREMENT , 
    `questionId` INT , 
    `userId` INT , 
    `answer` TEXT , 
    `score` FLOAT , 
   PRIMARY KEY (`answerId`)
)DEFAULT CHARSET=utf8;''')
cs_sql.mysqlExecute('''CREATE TABLE IF NOT EXISTS `settings`(
   `key` CHAR(50),
   `value` TEXT,
   PRIMARY KEY (`key`)
)DEFAULT CHARSET=utf8;''')
cs_sql.con.commit()


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
            '''SELECT * FROM `users` WHERE `loginToken` = %s''', (token,))
        fetch = cs_sql.cur.fetchall()
        if(len(fetch) == 0):
            return("error", "登录失效")
        else:
            return("success", fetch)
    else:
        return("error", "登录失效")


def api_user_login(email, pwd):
    # 前端用户登录
    cs_sql.mysqlExecute(
        '''SELECT userId,password FROM `users` WHERE `email` = %s''', (email,))
    fetch = cs_sql.cur.fetchall()
    # print(fetch)
    if(len(fetch) == 0):
        return(jsonResponse("error", "用户不存在"))
    else:
        if(pwd == fetch[0][1]):
            ntime, token = generateToken(fetch[0][0])
            print(ntime, token)
            cs_sql.mysqlExecute(
                '''UPDATE `users` SET `loginToken` = %s WHERE `users`.`userId` = %s; ''', (token, fetch[0][0]))
            cs_sql.mysqlExecute(
                '''UPDATE `users` SET `loginTime` = %s WHERE `users`.`userId` = %s; ''', (ntime, fetch[0][0]))
            cs_sql.con.commit()
            return(jsonResponse("success", token))
        else:
            return(jsonResponse("error", "密码错误"))


def api_user_register(name, email, pwd):
    # 前端用户注册
    cs_sql.mysqlExecute(
        '''SELECT userId FROM `users` WHERE `email` = %s''', (email,))
    if(len(cs_sql.cur.fetchall()) == 0):
        cs_sql.mysqlExecute(
            '''INSERT INTO `users` (`name`, `email`, `avatar`, `password`, `settings`) VALUES (%s, %s, %s, %s);''', (name, email, "{}", pwd, "{}"))
        cs_sql.con.commit()
        # cs_sql.mysqlExecute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
        # cs_sql.cur.fetchall()
        return(jsonResponse("success", ""))
    else:
        return(jsonResponse("error", "用户已存在"))


def api_user_checkLogin(token):
    # 前端检查token有效
    return(jsonResponse(*checkTokenAvailable(token)))


def api_get_user_data(token):
    return(jsonResponse(*getUserData(token)))


def api_get_user_object(token):
    user = getUserData(token)
    if(user[0] == "success"):
        user = user[1][0]
    else:
        user = None
    return user


def api_user_getlist():
    cs_sql.mysqlExecute('''SELECT * FROM `users`''')
    return(cs_sql.cur.fetchall())
