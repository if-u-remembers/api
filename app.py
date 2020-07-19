from flask import Flask
from flask import request
import os
from vue_api import form_data
from api import api_func_one
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')
app.config.update(DEBUG=False)


# 默认载入测试
@app.route('/', methods= ['POST', 'GET', 'PUT'])
def get_post():
    if request.method == 'POST':
        return '你进入了post'
    elif request.method == 'GET':
        return '你进入了GET'
    elif request.method == 'PUT':
        return '你进入了PUT'


# vue使用的app开始
@app.route('/login')
def vue():
    return '进入#login'


# 接口设备状态
@app.route('/interfaceStatus/interfaceStatusInformation', methods=['POST', 'GET'])
def ve():
    a = form_data.Datas()
    if request.method == 'POST':
        return a.formData()
    else:
        return a.jsonData()


@app.route('/RestconfApiDataFunctionOne', methods=['POST', 'GET', 'PUT'])
def RestconfApiData():
    if request.method == 'GET':
        return api_func_one.get_api_one()
    elif request.method == 'POST' or 'PUT':
        return api_func_one.put_api_ones()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)



