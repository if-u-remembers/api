from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from api import api_func_three
from apis import func_one, func_two, func_four, new_func_two_ck
import os,intomysql
import json
from apis import topo

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')  # 允许跨域请求
app.config.update(DEBUG=False)  # 开启bug无法展现

# 设备链接数据
api_url = 'https://li-say.top:6002'
user = "cisco"
pwd = "cisco123!"

# 思科设备数据
# api_url = 'https://ios-xe-mgmt-latest.cisco.com:9443'
# user = 'developer'
# pwd = 'Cisco12345'

# 数据库载入数据
host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'
# 实例化一个功能二类
funtwo = func_two.ApifuncTwoMysql(user, pwd, host, mysqluser, password, database)


# 功能一数据查询及修改设备信息，设备api操作
@app.route('/RestconfApiDataFunctionOne', methods=['POST', 'GET', 'PUT'])
def RestconfApiData():
    # get专属链接
    url = api_url + '/restconf/data/ietf-interfaces:interfaces/'
    if request.method == 'GET':
        return func_one.ApiFuncOne(url, user, pwd).getapis()
    elif request.method == 'POST' or 'PUT':
        datas = request.data
        return func_one.ApiFuncOne(url, user, pwd).putapis(datas)


c_url_api = 'https://sandboxdnac2.cisco.com'
functwo = new_func_two_ck.new_func_two(url=c_url_api, user='admin', pwd='Cisco1234!', modelhost=host, modeldatabase=database, modelpassword=password, modelmysqluser=mysqluser)


# 功能二批量下发及查询所有模板信息，数据库操作
@app.route('/RestconfApiDataFunctionTwo/<names>', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwo(names):
    if request.method == 'GET':
        if names == 'select':
            # 查询
            return functwo.redata()
        elif names == 'Reset':
            # 重置所有数据库中的模板
            code = intomysql.intonew(3)
            code2 = intomysql.intoNewModel_data(intomysql.new_val, 'yes')
            if code == code2 == '200':
                return '200'
            else:
                return '400'
        elif names == 'OllProject':
            return json.dumps(functwo.all_project())
    elif request.method == 'POST' or 'PUT':
        if names == 'CreateProject':
            # 创建一个空项目
            data = json.loads(request.data)['name']
            return functwo.create_project(data)
        elif names == 'SelectProject':
            # 查询某个项目的所有信息
            data = json.loads(request.data)['name']
            return functwo.get_project_id(data)
        elif names == 'CreateModel':
            pname = json.loads(request.data)['name']
            mid = json.loads(request.data)['id']
            return functwo.batch_create_model(pname, mid)
        elif names == 'GetProjectModel':
            data = json.loads(request.data)['name']
            return json.dumps(functwo.get_project_model(data))
        elif names == 'DelProjectModel':
            pname = json.loads(request.data)['name']
            mid = json.loads(request.data)['id']
            return json.dumps(functwo.batch_del_project_model(pname, mid))
        elif names == 'UpdataProjectModel':
            pname = json.loads(request.data)['name']
            mid = json.loads(request.data)['mid']
            model_data = json.loads(request.data)['modelData']
            model_name = json.loads(request.data)['modelName']
            return functwo.updata_project_model_data(pname, mid, model_data, model_name)
        elif names == 'DeployProjectModel':
            Pname = json.loads(request.data)['projectname']
            mname = json.loads(request.data)['modelname']
            tid = json.loads(request.data)['id']
            Ttype = json.loads(request.data)['type']
            return functwo.deploy_project_model(Pname, mname, tid, Ttype)


# 数据库中模板增删改查及重置
@app.route('/RestconfApiDataFunctionTwoMysql/<name>', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwoMysql(name):
    return functwo.mysqls(name, request.data)


# 功能三 ,暂时采用旧的方法
@app.route('/RestconfApiDataFunctionThree', methods=['GET'])
def RestconfApiDataFunctionThree():
    return api_func_three.intomysql()


root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
# root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apis")


@app.route('/htmls', methods=['POST', 'GET', 'PUT'])
def home():
    return send_from_directory(root, "topo-net.html")


# 功能四获取直接的json数据格式
@app.route('/RestconfApiDataFunctionFour', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionFour():
    url = api_url + '/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage'
    if request.method == 'GET':
        lennum = [{'id': 1, 'len': 25}, {'id': 2, 'len': 25}, {'id': 3, 'len': 25}, {'id': 4, 'len': 25},
                  {'id': 5, 'len': 25}]
        return func_four.ApiFuncFour(url, user, pwd).rejsondata(lennum)
    elif request.method == 'POST' or 'PUT':
        lens = json.loads(request.data)
        return func_four.ApiFuncFour(url, user, pwd).rejsondata(lens)


@app.route('/topos', methods=['POST', 'GET', 'PUT'])
def topos():
    roots = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apis")
    if request.method == 'GET':
        return send_from_directory(roots, "topo-net.html")
    elif request.method == 'POST' or 'PUT':
        datasss = json.loads(request.data)
        a = topo.TopoNewDataFiles(datasss)
        a.creates()
        return send_from_directory(roots, "topo.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)