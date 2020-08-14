from apis import mysql, reApi
host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'


class ApiFuncThree:
    def __init__(self, host, mysqluser, password, database):
        self.mysql = mysql.inmysql(host, mysqluser, password, database)

    def select_ddos(self):
        data = self.mysql.select('ddos_journal')
        return data


a = ApiFuncThree(host, mysqluser, password, database)
for i in a.select_ddos():
    print(i)