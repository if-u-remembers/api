import pymysql
from datetime import date
import json





def selectData():
    try:
        # 连接数据库
        # conn = pymysql.connect(
        #     host='127.0.0.1',
        #     port=3306,
        #     user='root',
        #     password='12345678',
        #     database='data',
        #     charset='utf8'
        # )
        conn = pymysql.connect(
            host='li-say.top',
            port=3306,
            user='root',
            password='981002',
            database='office',
            charset='utf8'
        )
    except:
        # return 'error'
        exit(-1)

    cur = conn.cursor()
    sql = cur.execute('select * from model_data')
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


def jsonTodict(json):
    idc = json
    return 0

def updataData(dict):
    """

    :param dict:  传入一个字典，更新所有数据。
    :return:
    """
    return 0


def deleteData(list):
    """
    :param list: 传入一个数组，进行遍历删除并返回结果
    :return:
    """
    return 0
