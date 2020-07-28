from api.MysqlApi import selectData
from api import api_put
import json
import ast


def get_func_two_mysql_select_data():
    # 查询到所有数据
    select_data = selectData()
    list_data = []
    for item in select_data:
        id, modelname, model, url, dels, remarks, introduce, logo = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]
        children_dict = {}
        children_dict['id'], children_dict['model'], children_dict['url'], children_dict['dels'], children_dict['logo'] = id, model, url, dels, logo
        list_data.append(children_dict)
    return list_data


def jsontolist(newjson):
    dist = json.loads(newjson)
    list = dist['id']
    return list


def batch_distribution(list):
    """
    :return: 400 错误异常， 200 正常使用， 414 请求超时， 500 id不存在或者已经被禁用
    """
    data = get_func_two_mysql_select_data()
    try:
        re_list = []
        for item in data:
            children_dict = {}
            if item['id'] in list:
                if item['dels'] == '1':
                    children_dict['id'] = item['id']
                    children_dict['error'] = '500'
                    # print(children_dict)
                elif item['dels'] == '0':
                    model = eval(item['model'])
                    ends = api_put.put_api(item['url'], model)
                    children_dict['id'] = item['id']
                    children_dict['error'] = ends
                re_list.append(children_dict)
            # print(re_list)
        return re_list
    except:
        re_list2 = []
        for item in data:
            children_dict2 = {}
            if item['id'] in list:
                children_dict2['id'] = item['id']
                children_dict2['error'] = '414'
                re_list2.append(children_dict2)
        return re_list2



# print(batch_distribution())