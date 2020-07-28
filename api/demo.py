import pymysql
conn = pymysql.connect(
    host='li-say.top',
    port=3306,
    user='root',
    password='981002',
    database='office',
    charset='utf8'
)

cur = conn.cursor()
sql = 'select * from ddos_data'
cur.execute(sql)
res = cur.fetchall()
print(res)