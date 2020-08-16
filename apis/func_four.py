import json
from apis import reApi


class ApiFuncFour:
    def __init__(self, url, user, pwd):
        self.api = reApi.reapis(url, user, pwd).getapis()

    def __getdata(self):
        jsonstr_to_dist = json.loads(self.api)
        list = jsonstr_to_dist['Cisco-IOS-XE-process-cpu-oper:cpu-usage']['cpu-utilization']['cpu-usage-processes']['cpu-usage-process']
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

        relist = []
        listname = ['Usage times of CPU', 'Average CPU usage time', 'CPU usage in five seconds', 'CPU usage per minute', 'CPU usage in five minutes']
        i = 0
        for item in [recount_list, reavg_list, refive_secinds_list, reone_min_list, refive_min_list]:
            name = listname[i]
            i += 1
            relist.append({'id': i, 'data': item, 'name': name})
            # 返回一个列表格式的数据
        return relist

    def redatas(self):
        return self.__getdata()

    def rejsondata(self, lens):
        # 获取到数据
        # lenlist = json.loads(lens)
        lenlist = lens
        data = self.__getdata()
        newdata = []
        num = 0
        keyname = ['invocation_count', 'avg_run_time', 'five_seconds', 'one_minute', 'five_minutes']
        for item in data:
            # 拆解出数据
            newlist = newlists(item['data'], keyname[num])
            print(lenlist[num]['len'])
            relists = lenlists(newlist, lenlist[num]['len'])
            # # 限制长度
            num += 1
            newredict = {'id': item['id'], 'name': item['name'], 'data': relists}
            newdata.append(newredict)
        return json.dumps(newdata)


def newlists(lists, key):
    newlist = []
    if lists:
        for item in lists:
            name = item['name']
            value = item[key]
            newlist.append({'value': value, 'name': name})
        return newlist
    else:
        return None


def lenlists(lists, lens):
    if lists:
        oldlen = len(lists)
    else:
        oldlen = 0

    if oldlen == 0:
        return None
    elif oldlen >= lens:
        return lists[0:lens]
    else:
        return lists


# a = ApiFuncFour('https://li-say.top:6002/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage', 'cisco', 'cisco123!')
# for i in a.rejsondata(lennum):
#     print(i)
# print(a.redatas()[2])