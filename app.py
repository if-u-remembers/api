from flask import Flask
from flask import request
import os
from vue_api import form_data
from api import api_func_one
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
app.config.update(DEBUG=False)


# 默认载入
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
        return '1'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)


# https://www.cnblogs.com/shumei/p/12826557.html
# https://www.jianshu.com/p/ead7317d01ec

