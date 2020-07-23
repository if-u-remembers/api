import pymysql
from datetime import date
import json


def selectData():
    try:
        conn = pymysql.connect(
            host='li-say.top',
            port=3306,
            user='root',
            password='981002',
            database='office',
            charset='utf8'
        )
    except:
        return 'error'
        exit(-1)

    cur = conn.cursor()
    sql = cur.execute('select * from model_data')
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res


def WhereIdSelectData(id):
    try:
        conn = pymysql.connect(
            host='li-say.top',
            port=3306,
            user='root',
            password='981002',
            database='office',
            charset='utf8'
        )
    except:
        return 'error'
        exit(-1)

    cur = conn.cursor()
    sql = 'select * from model_data where id = {}'.format(id)
    sqls = cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res


# print(WhereIdSelectData(2))


# def updataData(id, name , model, url, remark , introduce):
#     """
#     :param dict:  传入一个字典，更新所有数据。
#     :return:
#     """
#     try:
#         conn = pymysql.connect(
#             host='li-say.top',
#             port=3306,
#             user='root',
#             password='981002',
#             database='office',
#             charset='utf8'
#         )
#     except:
#         return 'error'
#         exit(-1)
#
#     cur = conn.cursor()
#     sql = "UPDATE model_data SET name={},model={},url={},remark={},introduce={} where id = {};".format(name, model, url, remark, introduce, id)
#     currr = cur.execute(sql)
#     return 0
