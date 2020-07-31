import pymysql
from api import api_func_one_get
import json
import time
from datetime import datetime
from api import api_func_t


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
    try:
        reCount = cur.execute('DROP TABLE ddos_data')
        cur.close()
        conn.close()
        print('删除ddos表成功')
    except:
        print('删除ddos表失败')
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
    try:
        reCount = cur.execute('DROP TABLE ddos_journal')
        cur.close()
        conn.close()
        print('删除日志表成功')
    except:
        print('删除日志表失败')
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
    sql = '''create table ddos_journal(id int(8) not null auto_increment,times varchar(150),grade int(8),news varchar(10000) null,intoerror varchar(10000) null,PRIMARY KEY(id))character set utf8;'''
    cur = conn.cursor()
    try:
        reCount = cur.execute(sql)
        print('创建成功日志')
        cur.close()
        conn.close()
    except:
        print('创建表失败日志')
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
    try:

        sql = cur.execute(ssql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        # 返回一个数据库所有数据的元组
        return res[-1]
    except:
        return 0

# print(select_ddos_one(1))
# for i in select_ddos():
#     print(i)


def time_pkts(olddata_dist, newdata_dist, limit_time):
    # 计算单设备的数据情况
    newtime = datetime.strptime(newdata_dist['time'], '%Y-%m-%d %H:%M:%S')
    oldtime = datetime.strptime(olddata_dist['time'], '%Y-%m-%d %H:%M:%S')
    times = (newtime - oldtime).seconds
    if times <= limit_time:
        # 计算包的含量 为： （新的数据-旧的数据）÷ 时间差
        if newdata_dist['pkts'] - olddata_dist['pkts'] == 0:
            pkts_to_time = 0
        else:
            pkts_to_time = (newdata_dist['pkts'] - olddata_dist['pkts'])/times
        # 换算为bps单位：Kbps
        kbps = pkts_to_time*10
        if kbps < 5*1048576:
            error = '正常'
            order = 0
            # 若大于5G/s ，小于10G/s ...以此类推
        elif 5*1048576 <= kbps < 10*1048576:
            error = '警告!'
            order = 1
        elif 10*1048576 <= kbps < 30*1048576:
            error = '危险级别！已配置接口模板'
            order = 2
        elif 30*1048576 <= kbps:
            error = '高危级别！已关闭接口'
            order = 3
    else:
        error = '正常'
        order = 0
    print('旧时间', oldtime, '新时间', newtime, '时间差为', times, '秒，速率为', round(kbps, 2), 'kbps，设备id ：', newdata_dist['id'], '状态：', error)
    redist = {"id": newdata_dist['id'], "order": order, "rate": round(kbps, 2), "name": newdata_dist['name']}
    # redist = {"id": newdata_dist['id'], "order": order, "rate": round(kbps, 2), "time": datetime.strftime(newtime, "%Y-%m-%d %H:%M:%S")}
    return redist


def risk_assessment(lists):
    orders = []
    news_list = []
    for item in lists:
        orders.append(item['order'])
        new_dict = item
        if item['order'] == 0:
            new_dict['news'] = item['name'] + '接口一切正常'
            new_dict['operation'] = None
        elif item['order'] == 1:
            new_dict['news'] = item['name'] + '接口不正常，向您发出警告！ '
            new_dict['operation'] = '警告级别，未执行任何操作'
        elif item['order'] == 2:
            new_dict['news'] = item['name'] + '接口存在异常，系统将自动下发ACL配置防范DDOS攻击！'
            try:
                api_func_t.acl(item['name'])
                new_dict['operation'] = '危险级别，系统成功自动下发ACL配置防范DDOS攻击！'
            except:
                new_dict['operation'] = '危险级别，系统自动下发ACL配置防范DDOS攻击失败！'
        elif item['order'] == 3:
            new_dict['news'] = item['name'] + '接口存在严重异常，系统将自动将受到疑似DDOS攻击的端口关闭！'
            try:
                api_func_t.down(item['name'])
                new_dict['operation'] = '高危险级别，系统已成功自动将受到疑似DDOS攻击的端口关闭！'
            except:
                new_dict['operation'] = '高危险级别，系统自动将受到疑似DDOS攻击的端口关闭失败，请手动执行关闭！'
        news_list.append(new_dict)
    grade = max(orders)
    relist = [grade, news_list]
    # print(grade, news_list)
    return relist


# list = [
#         {'id': 1, 'order': 0, 'rate': 23.21, 'name': 'GigabitEthernet1'},
#         {'id': 0, 'order': 1, 'rate': 0, 'name': 'Control Plane'},
#         {'id': 1, 'order': 2, 'rate': 23.21, 'name': 'GigabitEthernet2'},
#         {'id': 0, 'order': 3, 'rate': 0, 'name': 'Control Plane0'}
# ]
# for i in risk_assessment(list)[1]:
#     print(i)
# old = {"time": '2020-07-28 23:30:04', "pkts": 6}
# new = {"time": '2020-07-28 23:31:03', "pkts": 481554, "id": 5}
# print(time_pkts(old, new, 6000))


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
    sql = "insert into ddos_journal(grade,news,intoerror,times)values(%s,%s,%s,%s)"
    cur = conn.cursor()

    try:
        cur.executemany(sql, val)
        conn.commit()
        print('插入数据成功')
    except:
        conn.rollback()
        print('插入数据失败')
    # reCount = cur.execute('select * from ddos_journal')
    # res = cur.fetchall()
    # for i in res:
    #     print(i)
    cur.close()
    conn.close()


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
    sql = cur.execute('select * from ddos_journal order by id desc')
    res = cur.fetchall()
    cur.close()
    conn.close()
    # 返回一个数据库所有数据的元组
    return res


# for item in selectData():
#     print(item)