from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from apis import func_one, func_two
import os

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
# pwd = 'C1sco12345'

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


# 功能二批量下发及查询所有模板信息，数据库操作
@app.route('/RestconfApiDataFunctionTwo', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwo():
    if request.method == 'GET':
        # 查询
        return funtwo.redata()
    elif request.method == 'POST' or 'PUT':
        # 批量下发操作
        return funtwo.batch_distribution(request.data)


# 模板增删改查
@app.route('/RestconfApiDataFunctionTwoMysql/<name>', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwoMysql(name):
    return funtwo.mysqls(name, request.data)


root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")


@app.route('/htmls', methods=['POST', 'GET', 'PUT'])
def home():
    return send_from_directory(root, "topo.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)