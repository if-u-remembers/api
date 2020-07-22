import pymysql


conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='12345678',
        database='datas',
        charset='utf8'
)
cur = conn.cursor()
val =(('name'), ('guojia2'), ('guojia4'))



cur.close()
conn.close()