import json
import time

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql,cs_tools


def api_exam_getlist():
    cs_sql.mysqlExecute('''SELECT * FROM `exams`''')
    return(cs_sql.cur.fetchall())


def api_exam_new(data):
    data = json.loads(data)
    print(data)
    cs_sql.mysqlExecute(
        '''INSERT INTO exams(name,description,permissions,startTime,endTime) VALUES(%s, %s, %s, %s, %s);''', (data["name"], data["description"], json.dumps(data["groups"]), data['startTime'], data["endTime"]))
    cs_sql.con.commit()
    return cs_tools.jsonResponse("success",None)
