import pymysql
import json

'''
    这个文件是为了对数据库进行协调操作的父类
'''


class inmysql:
    '''
        这个类是为了便捷得对数据进行增删改查，同时尾端部分载入一些功能一、二、三等功能模块
    '''

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __conn(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8'
            )
            return conn
        except:
            exit(-1)
            return 0

    def select(self, table):
        '''
        查询表数据
        :param table: 传入表参数
        :return: 返回一个元组格式的数据
        '''
        conn = self.__conn()
        cur = conn.cursor()
        sql = cur.execute('select * from %s;' % table)
        print(123)
        res = cur.fetchall()
        print(456)
        cur.close()
        conn.close()
        # 返回一个数据库所有数据的元组
        return res

    def select_for_id(self, table: str, name: str, name_data):
        '''
            输入单独的字段名，和查询的相关数据，查询单条数据
        :param table: 表名
        :param name: 字段名
        :param name_data: 所需查询数据
        :return:
        '''
        conn = self.__conn()
        cur = conn.cursor()
        sql = 'select * from %s where %s = "%s" order by id desc; ' % (table, name, name_data)
        try:
            sqls = cur.execute(sql)
            res = cur.fetchall()
            if len(res) == 0:
                print('数据库无数据')
            cur.close()
            conn.close()
            # 返回一个数据库所有数据为id的元组
            return res
        except:
            return '400'

    def dels(self, table, key, data):
        conn = self.__conn()
        cur = conn.cursor()
        # 若该数据为数字格式
        if type(data) == type(1):
            sql = "delete from %s where %s = %s" % (table, key, data)
        elif type(data) == type([1, 2]):
            newdata = ''
            for item in data:
                newdata += key + '=' + str(item) + 'or'
            newdata = newdata[:-2]
            sql = "delete from %s where %s" % (table, newdata)
        try:
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return '200'
        except:
            conn.rollback()
            return '400'

    def new_func2_updata(self, table, model, introduce, name):
        conn = self.__conn()
        cur = conn.cursor()
        sql = "UPDATE {} set `model`='{}',`introduce`='{}' where `name` = {};".format(table, model, introduce, name)
        print(sql)
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

    def fun2_updata(self, tablename, mid, name, model, remark, introduce, logo):
        conn = self.__conn()
        cur = conn.cursor()
        sql = "UPDATE {} set `name`='{}',`model`='{}',`remarks`='{}',`introduce`='{}', `logo`={} where `id` = {};".format(tablename, name, model, remark, introduce, logo, mid)
        print(sql)
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

    def fun2_add(self, tablename, *data):

        conn = self.__conn()
        cur = conn.cursor()
        val = ((data[0], data[1], data[2], data[3], data[4]),)
        sql = "insert into {}(`model`, `name`, `logo`, `introduce`, `remarks`)values(%s,%s,%s,%s,%s)".format(tablename)
        print(sql)
        try:
            cur.executemany(sql, val)
            conn.commit()
            cur.close()
            conn.close()
            return '200'
        except:
            conn.rollback()
            return '400'


a = inmysql(host='47.112.160.89', user='test', database='test', password='123456')
print(a.select('simple_banner'))


class intomysql:
    def __init__(self, host, user, password, database):
        sql_model = '''create table model_data(
        id int(8) not null auto_increment, 
        name varchar(25) null,
        model varchar(2000) null,
        url varchar(1000) null,
        del varchar(2) null,
        remarks varchar(500) null,
        introduce varchar(1000) null,
        logo int(8) null,PRIMARY KEY(id));'''
        sql_ddos_journal = 'create table ddos_journal(id int(8) not null auto_increment,' \
                           'times varchar(150),' \
                           'grade int(8),' \
                           'news varchar(10000) null,' \
                           'intoerror varchar(10000) null,PRIMARY KEY(id))character set utf8;'
        sql_ddos_data = '''create table ddos_data(
        id int(8) not null auto_increment,
        mid varchar(10),
        times varchar(150),
        ddos varchar(40),
        name varchar(300),
        error varchar(1000) null,PRIMARY KEY(id))character set utf8;'''
        sql_cisco_model_data = '''create table cisco_model_data(
id int(8) not null auto_increment,
model varchar(4000),
name varchar(100),
logo int(8),
introduce varchar(1000),
remarks varchar(500),
PRIMARY KEY(id))character set utf8;'''
        # 健康度
        sql_health = '''create table health(
id int(8) not null auto_increment,
time varchar(200),
data varchar(1000),
PRIMARY KEY(id))character set utf8;'''
        # 修复功能二的冗余数据库
        sql_cisco_model_data2 = '''create table cisco_model_data2(
id int(8) not null auto_increment,
model varchar(4000),
name varchar(100),
introduce varchar(1000),
PRIMARY KEY(id))character set utf8;
'''
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.data = [sql_model, sql_ddos_journal, sql_ddos_data, sql_cisco_model_data, sql_health, sql_cisco_model_data2]
        self.name = ['model_data', 'ddos_journal', 'ddos_data', 'cisco_model_data', 'health', 'cisco_model_data2']

    def __conn(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8'
            )
            return conn
        except:
            exit(-1)
            return 0

    def printtable(self):
        # 打印所有的表名字
        print('-------------------------')
        print('--------所有表数据--------')
        i = 0
        for item in self.name:
            print(i, item)
            i += 1
        print('-------------------------')
        print('表名标号代表表的标号')
        print('请执行或者进行其他操作')
        print('-------------------------')

    def createtable(self, table_num):
        '''
        创建预设好的数据表
        :param table_num: 数据表id
        :return: 0
        '''
        conn = self.__conn()
        cur = conn.cursor()
        try:
            sqls = cur.execute(self.data[table_num])
            print('表' + self.name[table_num] + '创建成功')
            print('-------------------------')
            cur.close()
            conn.close()
            return '200'
        except:
            print('表' + self.name[table_num] + '创建失败')
            print('-------------------------')
            exit(-1)
            cur.close()
            conn.close()
            return '400'

    def deltable(self, table_num):
        '''
        删除数据表
        :param table_num: 数据表的id
        :return: 0
        '''
        conn = self.__conn()
        cur = conn.cursor()
        try:
            reCount = cur.execute('DROP TABLE %s' % (self.name[table_num]))
            print('表' + self.name[table_num] + '删除成功')
            print('-------------------------')
            cur.close()
            conn.close()
            return '200'
        except:
            print('表' + self.name[table_num] + '删除失败')
            print('-------------------------')
            exit(-1)
            cur.close()
            conn.close()
            return '400'

    def add_data(self, val, table: str, tablenames: list):
        '''
            通过
        :param val: 输入一个数据元组
        :param table:  输入表名
        :param tablenames:  输入表字段名
        :return: 0
        '''
        conn = self.__conn()
        cur = conn.cursor()
        tname, vs = '', ''
        for item in tablenames:
            add = item + ','
            vs += '%s,'
            tname += add
        tname, vs = tname[:-1], vs[:-1]
        sql = 'insert into ' + table + '(' + tname + ')values(' + vs + ');'
        # print(sql)
        # print(val)
        try:
            cur.executemany(sql, val)
            conn.commit()
            print(table, '载入数据成功！')
            print('-------------------------')
            cur.close()
            conn.close()
            return '200'
        except:
            print(table, '载入数据失败！')
            print('-------------------------')
            conn.rollback()
            cur.close()
            conn.close()
            return '400'


