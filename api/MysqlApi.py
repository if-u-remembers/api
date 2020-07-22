import pymysql
from datetime import date


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
        print("连接数据库失败")
        exit(-1)

    cur = conn.cursor()
    reCount = cur.execute('select * from model_data')
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


# def updataData(dict):
# #     # SQL 更新update语句
# #     sql = "UPDATE USER SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
# #     try:
# #         # 执行SQL语句
# #         cursor.execute(sql)
# #         # 提交数据库执行
# #         db.commit()
# #     except:
# #         # 错误时回滚
# #         db.rollback()
# print(selectData())
