from vue_api import form_data
from api import api_func_one_get
from api import api_func_one_put
from api import api_func_two_get
from api import api_func_two_post_one_batch_distribution
from api import api_func_two_post_two_Modify_Model
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')
app.config.update(DEBUG=False)


# 功能一
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


@app.route('/RestconfApiDataFunctionTwo', methods=['POST', 'GET', 'PUT'])
def RestconfApiDataFunctionTwo():
    if request.method == 'GET':
        return api_func_two_get.get_return_vue_oll_data()
    elif request.method == 'POST' or 'PUT':
        datas = api_func_two_post_one_batch_distribution.jsontolist(request.data)
        return json.dumps(api_func_two_post_one_batch_distribution.batch_distribution(datas))


@app.route('/SelectWhereId', methods=['POST'])
def SelectWhereId():
    return json.dumps(api_func_two_get.get_return_vue_one_id_data(request.data))


# 功能二修改模板
@app.route('/ModifyToModelInMysql', methods=['POST', 'PUT'])
def MysqlPutModel():
    return api_func_two_post_two_Modify_Model.ModifyModel(request.data)


@app.route('/ModifyToAddModelInMysql', methods=['POST', 'PUT'])
def ModifyToAddModelInMysql():
    return api_func_two_post_two_Modify_Model.AddModel(request.data)


@app.route('/ModifyToDeleteModelInMysql', methods=['POST', 'PUT'])
def ModifyToDeleteModelInMysql():
    return api_func_two_post_two_Modify_Model.DelModel(request.data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)


