from api import three_mysql_and_func_def
from api import api_func_one_get
import time
import datetime
from time import perf_counter
import json


def GetDdosData_new():
    # api = 'https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/'
    api = 'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/'
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    # basicauth = ("developer", "C1sco12345")
    basicauth = ("cisco", "cisco123!")

    try:
        datas = api_func_one_get.get_new_api_ones(api, headers, basicauth)
        data = json.loads(datas)
        # data = api_func_one_get.get_new_api_ones(api, headers, basicauth)
        listtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(data)
        # 查到每个设备的参数
        list = data['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']
        # 空数组收集所有被检查到的设备数据的信息
        intlist = []
        for item in list:
            # 循环每个设备
            acl = item['input-security-acl']
            # if acl == '101' and item['v4-protocol-stats']['in-pkts'] != '':
            if item['v4-protocol-stats']['in-pkts'] != '':
                # 获得新的数据
                children = {'id': int(item['if-index']), 'name': item['name'], 'pkts': int(item['v4-protocol-stats']['in-pkts']), 'time': listtime, 'acl': item['input-security-acl']}
                # 获取旧数据，若数据为空，则建立使得数据变成新的,通过设备的id查询
                olddata = three_mysql_and_func_def.select_ddos_one(item['if-index'])
                # 把新的数据载入数据库
                three_mysql_and_func_def.Add_ddos(children)
                if olddata == 0:
                    print('未有历史数据')
                    olddata_pkts, olddata_time = children['pkts'], children['time']
                else:
                    olddata_time, olddata_pkts = olddata[2], olddata[3]
                    print('一分钟前的数据为:', olddata_time, olddata_pkts)
                olddata_dist = {"time": olddata_time, "pkts": int(olddata_pkts)}
                # 把和旧 新时间载入得到当前设备的数据报告
                limit_time = 6000000000
                # 生成一个字典
                intlist.append(three_mysql_and_func_def.time_pkts(olddata_dist, children, limit_time))
            else:
                children = {}
        # 获得grade参数和 new参数
        grade_news_list = three_mysql_and_func_def.risk_assessment(intlist)
        grade = grade_news_list[0]
        news_intlist = grade_news_list[1]
        mysql_data = {"grade": grade, "intoerror": json.dumps(news_intlist), "time": listtime, "news": 'null'}
        val = ((mysql_data['grade'], mysql_data['news'], mysql_data['intoerror'], mysql_data['time']),)
        three_mysql_and_func_def.intoModelMysql(val)
        return mysql_data
    except:
        print(111)
        listtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mysql_data = {"grade": 0, "news": 'null', "intoerror": 'null', "time": listtime}
        val = ((mysql_data['grade'], mysql_data['news'], mysql_data['intoerror'], mysql_data['time']),)
        three_mysql_and_func_def.intoModelMysql(val)
        return mysql_data


# print(GetDdosData_new())


def intomysql():
    # 获取新的数据
    # 执行，但是数据不适用，备用
    GetDdosData_new()
    res = three_mysql_and_func_def.selectData()
    list = []
    for item in res:
        chilird = {}
        chilird['id'], chilird['time'], chilird['grade'], chilird['intoerror'] = item[0], item[1], item[2], json.loads(item[4])
        list.append(chilird)
    # print(len(list))
    return json.dumps(list)
    # return list
#

# for item in intomysql():
#     print(item)

