from api.MysqlApi import selectData
import json


def get_func_two_mysql():
    # 查询到所有数据
    select_data = selectData()
    for item in select_data:
        id, modelname, model, url, dels, remarks, introduce = item[0], item[1], item[2], item[3], item[4], item[5], item[6]
        print(id, modelname, model, url, dels, remarks, introduce)

    # select_dict = eval(select_data[4][2])
    return 1


# print(get_func_two_mysql())