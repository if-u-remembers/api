from vue_api import form_data
from api import api_func_one_get
from api import api_func_one_put
from api import api_func_two_get
from api import api_func_two_post_one_batch_distribution
from api import api_func_two_post_two_Modify_Model
from api import api_func_three
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
from PIL import Image
import PIL
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')
app.config.update(DEBUG=False)


# 功能一 查询所有接口信息 下发信息
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


# 功能二批量下发及查询所有模板信息
@app.route('/RestconfApiDataFunctionTwo', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwo():
    if request.method == 'GET':
        return api_func_two_get.get_return_vue_oll_data()
    elif request.method == 'POST' or 'PUT':
        datas = api_func_two_post_one_batch_distribution.jsontolist(request.data)
        return json.dumps(api_func_two_post_one_batch_distribution.batch_distribution(datas))


# 功能二查询模板
@app.route('/SelectWhereId', methods=['POST'])
def SelectWhereId():
    return json.dumps(api_func_two_get.get_return_vue_one_id_data(request.data))


# 功能二修改模板
@app.route('/ModifyToModelInMysql', methods=['POST', 'PUT'])
def MysqlPutModel():
    return api_func_two_post_two_Modify_Model.ModifyModel(request.data)


# 功能二添加模板
@app.route('/ModifyToAddModelInMysql', methods=['POST', 'PUT'])
def ModifyToAddModelInMysql():
    return api_func_two_post_two_Modify_Model.AddModel(request.data)


# 功能二删除模板
@app.route('/ModifyToDeleteModelInMysql', methods=['POST', 'PUT'])
def ModifyToDeleteModelInMysql():
    return api_func_two_post_two_Modify_Model.DelModel(request.data)


# 功能三
@app.route('/RestconfApiDataFunctionThree', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionThree():
    return api_func_three.intomysql()


# 功能四代码
@app.route('/img', methods=['GET'])
def index():
    # 数据准备
    x = np.arange(1440)
    y = x

    fig = plt.figure()
    plt.plot(x, y**2)
    canvas = fig.canvas
    # 上面这段代码和上面注释掉的代码效果一样
    # # 方法1
    buffer = io.BytesIO()
    canvas.print_png(buffer)
    data = buffer.getvalue()
    buffer.close()
    # 向前端返回图像
    res = app.make_response(data)
    res.headers["Content-Type"] = "image/png"
    print(res)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)


