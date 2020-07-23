from vue_api import form_data
from api import api_func_one_get
from api import api_func_one_put
from api import api_func_two_get
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from api import MysqlApi

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')
app.config.update(DEBUG=False)


# 默认载入测试
@app.route('/', methods=['POST', 'GET', 'PUT'])
def get_post():
    if request.method == 'POST':
        return '你进入了post'
    elif request.method == 'GET':
        return '你进入了GET'
    elif request.method == 'PUT':
        return '你进入了PUT'


# vue使用的app开始

# 原本ip
@app.route('/RestconfApiDataFunctionOne', methods=['POST', 'GET', 'PUT'])
def RestconfApiData():
    if request.method == 'GET':
        # return api_func_one_get.page()
        # return api_func_one_get.get_api_one()
        # return api_func_one_get.jsonTodata()
        return api_func_one_get.new_dict(api_func_one_get.jsonTodata())
        # return api_func_one_get.new_dict(api_func_one_get.twoIPdata())
    elif request.method == 'POST' or 'PUT':
        datas = request.data
        return api_func_one_put.put_api_ones(datas)


# 多ip测试接口 * put/post 接口时发送数据
@app.route('/RestconfApiDataFunctionOne2', methods=['POST', 'GET', 'PUT'])
def RestconfApiData2():
    if request.method == 'GET':
        return api_func_one_get.new_dict(api_func_one_get.twoIPdata())
    elif request.method == 'POST' or 'PUT':
        return api_func_one_put.put_api_one()


@app.route('/RestconfApiDataFunctionTwo', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwo():
    if request.method == 'GET':
        return api_func_two_get.get_return_vue_oll_data()
    elif request.method == 'POST' or 'PUT':
        return '0'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



