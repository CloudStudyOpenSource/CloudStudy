import mysql.connector
from modules import cs_config


def connectMysql():
    global con
    global cur
    con = mysql.connector.connect(**cs_config.mysql)
    cur = con.cursor()
    print("Connected to Mysql Server")


def mysqlExecute(*args):
    try:
        cur.execute(*args)
    except:
        print("Err: Lost connection to Mysql Server. Reconnecting...")
        cur.close()
        con.close()
        connectMysql()
        cur.execute(*args)
