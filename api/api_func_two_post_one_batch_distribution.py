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
        children_dict['id'], children_dict['model'], children_dict['url'] = id, model, url
        list_data.append(children_dict)
    return list_data


def batch_distribution():
    id_list = [1, 2]
    data = get_func_two_mysql_select_data()
    print(type(data))
    return data


# print(batch_distribution())