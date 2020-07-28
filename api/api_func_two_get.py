from api.MysqlApi import selectData, WhereIdSelectData
import json
import ast


def get_func_two_mysql_select_data():
    # 查询到所有数据
    select_data = selectData()
    list_data = []
    for item in select_data:
        # 获取到所有的data并进行赋值
        id, modelname, model, url, dels, remarks, introduce, logo = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]
        children_dict = {}
        # 如果dels合法
        if dels == '0':
            # 如果dels为0则运行
            children_dict['id'], children_dict['modelname'], children_dict['remakes'] = id, modelname, remarks
            children_dict['introduce'], children_dict['model'], children_dict['url'], children_dict['logo'] = introduce, model, url, logo
            list_data.append(children_dict)
    return list_data


def get_return_vue_oll_data():
    data = get_func_two_mysql_select_data()
    list_data = []
    for item in data:
        children_dict = {}
        children_dict['id'], children_dict['modelname'], children_dict['remakes'], children_dict['introduce'], children_dict['logo'] = item['id'], item['modelname'], item['remakes'], item['introduce'], item['logo']
        list_data.append(children_dict)
    json_list = json.dumps(list_data)
    return json_list


def get_return_vue_one_id_data(id):
    mid = json.loads(id)['id']
    data = WhereIdSelectData(mid)
    list_data = []
    for item in data:
        id, modelname, model, url, dels, remarks, introduce, logo = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]
        children_dict = {}
        # 如果dels合法
        children_dict['id'], children_dict['modelname'], children_dict['remakes'] = id, modelname, remarks
        children_dict['introduce'], children_dict['model'], children_dict['url'], children_dict['logo'] = introduce, model, url, logo
        list_data.append(children_dict)
    return list_data


# print(get_return_vue_one_id_data(1))

# print(get_return_vue_oll_data())

