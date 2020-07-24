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


def updataData(id, name , model, url, remark , introduce):
    """
    :param dict:  传入一个字典，更新所有数据。
    :return:
    """
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
    sql = "UPDATE model_data SET name={},model={},url={},remark={},introduce={} where id = {};".format(name, model, url, remark, introduce, id)
    currr = cur.execute(sql)
    return 0


def intoModelMysql(val):
    """
    插入数据行
    :param val: 一个数据库信息 元组
    :return:
    """
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
        print("连接数据库失败")
        exit(-1)
    sql = "insert into model_data(name,model,url,del,remarks,introduce)values(%s,%s,%s,%s,%s,%s)"
    cur = conn.cursor()

    try:
        cur.executemany(sql, val)
        conn.commit()
    except:
        conn.rollback()
    reCount = cur.execute('select * from model_data')
    res = cur.fetchall()
    for i in res:
        print(i)
    cur.close()
    conn.close()


def delModelMysql():
    """
    删除数据库
    :return:
    """
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
    reCount = cur.execute('DROP TABLE model_data')
    cur.close()
    conn.close()
    return 0


def NewModelMysql():
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
    sql = '''create table model_data(id int(8) not null auto_increment, name varchar(25) null,model varchar(2000) null,url varchar(1000) null,del varchar(2) null,remarks varchar(500) null,introduce varchar(1000) null,PRIMARY KEY(id));'''

    cur = conn.cursor()
    reCount = cur.execute(sql)
    cur.close()
    conn.close()
    return 0