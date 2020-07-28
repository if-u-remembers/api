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
    sql = "select * from model_data where id = %s" % (int(id))
    sqls = cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res
# print(WhereIdSelectData(1))


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
    sql = "insert into model_data(name,model,url,del,remarks,introduce,logo)values(%s,%s,%s,%s,%s,%s,%s)"
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
    sql = '''create table model_data(id int(8) not null auto_increment, name varchar(25) null,model varchar(2000) null,url varchar(1000) null,del varchar(2) null,remarks varchar(500) null,introduce varchar(1000) null,logo varchar(1000) null,PRIMARY KEY(id));'''

    cur = conn.cursor()
    reCount = cur.execute(sql)
    cur.close()
    conn.close()
    return 0


def updataData(id, name , model, url, remark , introduce, logo):
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
    sql = "UPDATE model_data set `name`='{}',`model`={} ,`url`={},`remarks`='{}',`introduce`='{}', `del` = {}, `logo`={} where `id` = {};".format(name, json.dumps(model), json.dumps(pymysql.escape_string(url)), remark, introduce,'0', logo, id)
    currr = cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    if currr == 1:
        return '200'
    elif currr == 0:
        return '100'
    else:
        return '400'

# id = 1
# name = 'LoopBack2444dasd45'
# model = '''{"ietf-interfaces:interface": {"name": "Loopback6", "description": "WHATEVER6", "type": "iana-if-type:softwareLoopback","enabled": True,"ietf-ip:ipv4": {"address": [{"ip": "6.6.6.6","netmask": "255.255.255.0"}]},"ietf-ip:ipv6": {}}}'''
# url = '''https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=Loopback6'''
# remark = '创汇还'
# introduce = '回环'
# logo = '2'
# print(updataData(id, name, model, url, remark, introduce, logo))
# print(selectData())


def AddData(name , model, url, remark , introduce, logo):
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
    val = ((name, model, url, remark, introduce, '0', logo),)
    # sql = """INSERT INTO model_data(`name`,`model`,`url`,`remarks`,`introduce`,`del`,`logo`) values({},{},{},{},{},{},{}) ;""".format(json.dumps(name), json.dumps(model), json.dumps(pymysql.escape_string(url)), json.dumps(remark), json.dumps(introduce), '0', logo)
    sql = "insert into model_data(`name`,`model`,`url`,`remarks`,`introduce`,`del`,`logo`)values(%s,%s,%s,%s,%s,%s,%s)"
    try:
        cur.executemany(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return '200'
    except:
        conn.rollback()
        return '400'


# name = 'LoopBack244445'
# model = '{"ietf-interfaces:interface": {"name": "Loopback6", "description": "WHATEVER6", "type": "iana-if-type:softwareLoopback","enabled": True,"ietf-ip:ipv4": {"address": [{"ip": "6.6.6.6","netmask": "255.255.255.0"}]},"ietf-ip:ipv6": {}}}'
# url = 'https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=Loopback6'
# remark = '创汇还'
# introduce = '回环'
# logo = '2'
# # val = ((name, model, url, remark, introduce, '0', logo),)
# print(AddData(name, model, url, remark, introduce,  logo))
# # print(intoModelMysql(val))
#
# for i in selectData():
#     print(i)


def DelData(id):
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
    sql = "delete from model_data where id ={}".format(id)
    try:
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return '200'
    except:
        conn.rollback()
        return '400'


# print(DelData(1))
# print(selectData())