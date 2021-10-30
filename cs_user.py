import json
from os import getuid
import cs_encrypt
import time
#import sqlite3


#sql_conn = sqlite3.connect('./data/users/list.db')
#sql_cur = sql_conn.cursor()
#
#sql_cur.execute('''CREATE TABLE IF NOT EXISTS sc
#           (name TEXT,
#            email TEXT,
#            password TEXT);''')
#
#sql_conn.commit()
#sql_cur.close()
#sql_conn.close()

file_users = open("./data/users/list.json", "r+")
file_users_json = json.loads(file_users.read())

file_online = open("./data/users/online.json", "r+")
file_online_json = json.loads(file_online.read())


def file_users_update():
    file_users.seek(0)
    file_users.truncate()
    file_users.write(json.dumps(file_users_json))
    file_users.flush()
    
def file_online_update():
    file_online.seek(0)
    file_online.truncate()
    file_online.write(json.dumps(file_online_json))
    file_online.flush()




def verify_user(email, pwd):
    email = email.lower()
    pwd = pwd
    if(email in file_users_json):
        if(file_users_json[email]["pwd"] == pwd):
            return True
        else:
            return ("密码错误")
    else:
        return ("账号错误")

def get_user_info(email):
    email=email.lower()
    r=json.loads(json.dumps(file_users_json[email]))
    r.pop("pwd")
    return(r)

def generate_key(email,time):
    return(cs_encrypt.sha512(email+str(time)))

def user_online(email):
    ntime=time.time
    key=generate_key(email,ntime)
    

def api_user_login(email,pwd):
    r=verify_user(email,pwd)
    if(r == True):
        return(get_user_info(email))
    else:
        return(r)

def api_user_register(name,email,pwd):
    if (email in file_users_json):
        return ("用户已存在")
    else:
        add_user(name,email,pwd)
        return (get_user_info(email))

def add_user(name,email,pwd):
    file_users_json[email.lower()]={"name":name,"email":email,"pwd":pwd}
    file_users_update()
