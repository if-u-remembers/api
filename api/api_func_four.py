from api import api_func_one_get
import json
import time


def getdata():
    '''
    直接请求
    :return:  返回五个被清洗过的cpu数据:
    '''
    startime = time.time()
    print('开始获取数据')
    try:
        # 获取指定api的数据
        # api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage"
        api_url = "https://li-say.top:6002/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage"
        headers = {"Accept": "application/yang-data+json",
                   "Content-type": "application/yang-data+json"
                   }
        # basicauth = ("developer", "C1sco12345")
        basicauth = ("cisco", "cisco123!")
        data = api_func_one_get.get_new_api_ones(api_url, headers, basicauth)
        # print(data)
        jsonstr_to_dist = json.loads(data)
        list = jsonstr_to_dist['Cisco-IOS-XE-process-cpu-oper:cpu-usage']['cpu-utilization']['cpu-usage-processes'][
            'cpu-usage-process']
        count_list, avg_list, five_secinds_list, one_min_list, five_min_list = [], [], [], [], []
        for item in list:
            #  清洗数据
            '''
            分别是 调用进程次数, 平均运行时间, 五秒使用cpu百分比,一分钟内占用cpu百分比, 五分钟内使用cpu百分比
            '''
            invocation_count, avg_run_time = item['invocation-count'], item['avg-run-time']
            five_seconds, one_minute, five_minutes = item['five-seconds'], item['one-minute'], item['five-minutes']
            pid, name = item['pid'], item['name']
            if invocation_count:
                dict1 = {"invocation_count": invocation_count, "id": pid, "name": name}
                count_list.append(dict1)
            if float(avg_run_time):
                dict2 = {"avg_run_time": float(avg_run_time), "id": pid, "name": name}
                avg_list.append(dict2)
            if float(five_seconds):
                dict3 = {"five_seconds": float(five_seconds), "id": pid, "name": name}
                five_secinds_list.append(dict3)
            if float(one_minute):
                dict4 = {"one_minute": float(one_minute), "id": pid, "name": name}
                one_min_list.append(dict4)
            if float(five_minutes):
                dict5 = {"five_minutes": float(five_minutes), "id": pid, "name": name}
                five_min_list.append(dict5)

        recount_list = sorted(count_list, key=lambda keys: keys['invocation_count'], reverse=True)
        reavg_list = sorted(avg_list, key=lambda keys: keys['avg_run_time'], reverse=True)
        refive_secinds_list = sorted(five_secinds_list, key=lambda keys: keys['five_seconds'], reverse=True)
        reone_min_list = sorted(one_min_list, key=lambda keys: keys['one_minute'], reverse=True)
        refive_min_list = sorted(five_min_list, key=lambda keys: keys['five_minutes'], reverse=True)
        endtime = time.time()
        print('获取数据结束：')
        # for item in [recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list]:
        #     print(item)
        print('运行时间:', endtime - startime, '秒')
        return recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list
    except:
        endtime = time.time()
        print('出现异常,运行时间:', endtime - startime, '秒')
        error = [{"error_id": 1, "error": 100}]
        recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list = error,error,error, error, error
        return recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list


print(getdata())


def datalitmt(lists, lenss):
    new_list = lists
    if len(lists) >= lenss:
        del new_list[lenss:len(lists)]
        return new_list
    elif len(lists) == 0:
        return None


def listdictdatatolist(lists, list_key):
    if lists:
        new_list = []
        for item in lists:
            data = item[list_key]
            name = item['name']
            new_dict = {"data": data, "name": name}
            new_list.append(new_dict)
        return new_list
    else:
        return None


def rejsondata(lenss):
    recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list = getdata()
    relict = {
        "InvocationCount": listdictdatatolist(datalitmt(recount_list, lenss), 'invocation_count'),
        "avgruntime": listdictdatatolist(datalitmt(reavg_list, lenss), 'avg_run_time'),
        "fiveseconds": listdictdatatolist(datalitmt(refive_secinds_list, lenss), 'five_seconds'),
        "oneminute": listdictdatatolist(datalitmt(reone_min_list, lenss), 'one_minute'),
        "fiveminutes": listdictdatatolist(datalitmt(refive_min_list, lenss), 'five_minutes')
    }
    return json.dumps(relict)





# print(rejsondata())
# reimg()