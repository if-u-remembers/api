from api.MysqlApi import selectData
import json
import ast

def get_func_two_mysql_select_data():
    # 查询到所有数据
    select_data = selectData()
    list_data = []
    for item in select_data:
        id, modelname, model, url, dels, remarks, introduce = item[0], item[1], item[2], item[3], item[4], item[5], item[6]
        children_dict = {}
        if dels == '0':
            children_dict['id'], children_dict['modelname'], children_dict['remakes'] = id, modelname, remarks
            children_dict['introduce'], children_dict['model'], children_dict['url'] = introduce, model, url
            list_data.append(children_dict)
    return list_data


def get_return_vue_oll_data():
    data = get_func_two_mysql_select_data()
    list_data = []
    for item in data:
        children_dict = {}
        children_dict['id'], children_dict['modelname'], children_dict['remakes'], children_dict['introduce'] = item['id'], item['modelname'], item['remakes'], item['introduce']
        list_data.append(children_dict)
    json_list = json.dumps(list_data)
    return json_list




# print(get_return_vue_oll_data())