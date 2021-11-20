import json
import cs_encrypt
import time
from flask import jsonify
import mysql.connector
import cs_config

con = mysql.connector.connect(**cs_config.mysql)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS `users`(
   `uid` INT UNSIGNED AUTO_INCREMENT,
   `name` CHAR(20),
   `email` CHAR(250),
   `password` CHAR(128),
   `group` INT UNSIGNED,
   `login_time` DATETIME,
   `login_token` CHAR(128),
   PRIMARY KEY (`uid`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
con.commit()


def jsonResponse(message, data):
    return(jsonify({"message": message, "data": data}))


def api_user_login(email, pwd):
    cur.execute('''SELECT * FROM `users` WHERE `email` = %s''', (email,))
    fetch = cur.fetchall()
    if(len(fetch) == 0):
        return(jsonResponse("error", "用户不存在"))
    else:
        if(pwd == fetch[0][3]):
            ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(ntime)
            token = cs_encrypt.sha512((json.dumps(
                {"uid": fetch[0][0], "time": ntime})))
            cur.execute(
                '''UPDATE `users` SET `login_token` = %s WHERE `users`.`uid` = %s; ''', (token, fetch[0][0]))
            cur.execute(
                '''UPDATE `users` SET `login_time` = %s WHERE `users`.`uid` = %s; ''', (ntime, fetch[0][0]))
            con.commit()
            return(jsonResponse("success", token))
        else:
            return(jsonResponse("error", "密码错误"))


def api_user_register(name, email, pwd):
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


def api_user_getlist():
    return()


# cur.close()
# con.close()
