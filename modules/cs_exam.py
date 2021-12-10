import json
import time

from flask import jsonify

from modules import cs_config, cs_encrypt, cs_sql


def api_exam_getlist():
    cs_sql.mysqlExecute('''SELECT * FROM `exams`''')
    return(cs_sql.cur.fetchall())