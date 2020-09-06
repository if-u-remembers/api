import json
from apis import mysql, reApi
import intomysql


class ApifuncTwoMysql:
    def __init__(self, user, pwd, host, mysqluser, password, database):
        self.mysql = mysql.inmysql(host, mysqluser, password, database)
        self.user = user
        self.pwd = pwd

    def __getdata(self):
        # 获取并处理数据库中模板数据
        data = self.mysql.select('model_data')
        list_data = []
        for item in data:
            # 获取到所有的data并进行赋值
            id, modelname, model, url, dels, remarks, introduce, logo = item[0], item[1], item[2], item[3], item[4], \
                                                                        item[5], item[6], item[7]
            children_dict = {}
            # 如果dels合法
            if dels == '0':
                # 如果dels为0则运行
                children_dict['id'], children_dict['modelname'], children_dict['remakes'] = id, modelname, remarks
                children_dict['introduce'], children_dict['model'], children_dict['url'], children_dict[
                    'logo'], children_dict['dels'] = introduce, model, url, logo, dels
                list_data.append(children_dict)
        return list_data

    # def redata(self):
    #     # 返回用户可见的数据
    #     datsa = self.__getdata()
    #     list_data = []
    #     for item in datsa:
    #         children_dicts = {'id': item['id'], 'modelname': item['modelname'], 'remakes': item['remakes'],
    #                           'introduce': item['introduce'], 'logo': item['logo']}
    #         list_data.append(children_dicts)
    #     return json.dumps(list_data)

    # def redata_id(self, ids):
    #     # ids是一个数字格式的数据
    #     global children_dictss
    #     data = self.mysql.select_for_id('model_data', 'id', ids)
    #     for item in data:
    #         id, modelname, model, url, dels, remarks, introduce, logo = item[0], item[1], item[2], item[3], item[4], \
    #                                                                     item[5], item[6], item[7]
    #         children_dictss = {'id': id, 'modelname': modelname, 'remakes': remarks, 'introduce': introduce,
    #                            'model': model, 'url': url, 'logo': logo, 'dels': dels}
    #         # 返回字典格式数据
    #     return children_dictss

    def batch_distribution(self, dicts):
        """
            :return: 400 错误异常， 200 正常使用， 414 请求超时， 500 id不存在或者已经被禁用
        """
        # 获取数据
        lists = json.loads(dicts)['id']
        data = self.__getdata()
        # 构建一个空的列表存放运行数据
        re_list = []
        # 遍历所有数据
        for item in data:
            children_dict = {}
            if item['id'] in lists:
                if item['dels'] == '0':
                    model = eval(item['model'])
                    try:
                        # 对该模板进行put
                        ends = reApi.reapis(item['url'], self.user, self.pwd).putapi(model)
                    except:
                        ends = '400'
                    children_dict['id'] = item['id']
                    children_dict['code'] = ends
                elif item['dels'] == '1':
                    # dels字段为1则直接500 => 这里留个坑 => 不一定会用,一般都是0
                    children_dict['id'] = item['id']
                    children_dict['code'] = '500'
                re_list.append(children_dict)
        return json.dumps(re_list)

    # # 删改查部分:
    # def __select(self, data):
    #     try:
    #         select = json.loads(data)['id']
    #         if type(select) == type(1):
    #             return json.dumps(self.redata_id(select))
    #         else:
    #             selist = []
    #             for item in select:
    #                 selist.append(self.redata_id(item))
    #             return json.dumps(selist)
    #     except:
    #         # 异常返回一个空数据
    #         print('error')
    #         return json.dumps([])
    #
    # def __updata(self, data):
    #     # 返回数据为： 200， 400
    #     dicts = json.loads(data)
    #     id, modelname, remarks, introduce, url, model, logo = dicts['id'], dicts['modelname'], dicts['remarks'], dicts[
    #         'introduce'], dicts['url'], dicts['model'], dicts['logo']
    #     return self.mysql.fun2_updata(id, modelname, model, url, remarks, introduce, logo)
    #
    # def __adds(self, data):
    #     # 返回数据为： 200， 400
    #     dicts = json.loads(data)
    #     modelname, remarks, introduce, url, model, logo = dicts['modelname'], dicts['remarks'], dicts['introduce'], \
    #                                                       dicts['url'], dicts['model'], dicts['logo']
    #     return self.mysql.fun2_add(modelname, model, url, remarks, introduce, logo)
    #
    # def __dels(self, data):
    #     # 返回数据为一个id，error字段的字典嵌套数组
    #     dist = json.loads(data)['id']
    #     relist = []
    #     for item in dist:
    #         error = self.mysql.dels('model_data', 'id', item)
    #         newdist = {'id': item, 'error': error}
    #         relist.append(newdist)
    #     return json.dumps(relist)
    #
    # def mysqls(self, name, data):
    #     if name == 'del':
    #         return self.__dels(data)
    #     elif name == 'modify':
    #         return self.__updata(data)
    #     elif name == 'add':
    #         return self.__adds(data)
    #     elif name == 'select':
    #         # 这里返回多组数据,且保留id及空的情况
    #         return self.__select(data)
    #     # elif name == 'reset':
    #     #     return intomysql.remodeldata()
