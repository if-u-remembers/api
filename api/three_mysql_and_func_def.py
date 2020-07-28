import pymysql
from api import api_func_one_get
import json
import time


def CreateMysqlTable():
    """
    运行则清空数据表,并进行新建数据表,载入一段数据...
    :return:
    """
    return 0


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
    reCount = cur.execute('DROP TABLE ddos_data')
    cur.close()
    conn.close()
    print('删除ddos表成功')
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
    sql = '''create table ddos_data(id int(8) not null auto_increment,mid varchar(10),times varchar(150),ddos varchar(40),name varchar(300),error varchar(1000) null,PRIMARY KEY(id))character set utf8;'''
    cur = conn.cursor()
    try:
        reCount = cur.execute(sql)
        print('创建成功ddos')
        cur.close()
        conn.close()
    except:
        print('创建表失败ddos')
    return 0


def Add_ddos(dist):
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
    mid, times, ddos, name, acl = dist['id'], dist['time'], dist['pkts'], dist['name'], dist['acl']
    val = ((mid, times, ddos, name, acl),)
    sql = 'insert into ddos_data(mid, times, ddos, `name`, error)values(%s,%s,%s,%s,%s)'
    try:
        cur.executemany(sql, val)
        conn.commit()
        print('id', dist['id'], '载入数据成功！')
        cur.close()
        conn.close()
    except:
        print('id', dist['id'], '载入数据失败！')
        conn.rollback()
        cur.close()
        conn.close()
# NewModelMysql()

#
# dist = {'id': 1, 'name': 'GigabitEthernet1', 'pkts': '7942', 'time': '2020-07-27 20:48:06'}
# Add_ddos(dist)


def select_ddos():
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
    sql = cur.execute('select * from ddos_data')
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res


def select_ddos_one(mid):
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
    ssql = "select * from ddos_data where `mid` = {}".format(mid)
    sql = cur.execute(ssql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res[-1]


# print(select_ddos_one(1))
# for i in select_ddos():
#     print(i)





