# Flask
## Load dependencies
```
pip install -r requirements.txt
```
## Project setup

```python
python flaskapp.py 
```

## 项目结构
```
# 采用下划线连接结构命名
| -- __pycache__												//pycharm 执行文件
| -- api														//所有后端api文档
|    | -- img													//图片格式文件目录
|    |    | -- count.png
|    |    | -- five_minutes.png
|    |    | -- five_seconds.png
|    |    | -- one_minute.png
|    | -- api_func_four.py										//功能四算法文件
|    | -- api_func_four_new_img.py								//功能四图像生成文件
|    | -- three_mysql_and_func_def.py							//功能三数据库及其他相关该函数文件
|    | -- api_func_t.py											//功能三执行文件
|    | -- api_func_three.py										//功能三主体函数文件
|    | -- api_func_two_get.py									//功能二获取数据文件
|    | -- api_func_two_post_one_batch_distribution.py			//功能二批量下发执行文件
|    | -- api_func_two_post_two_Modify_Model.py					//功能二模板增删改查文件
|    | -- api_func_one_get.py									//功能一数据执行获取文件
|    | -- api_func_one_put.py									//功能一修改接口数据文件
|    | -- api_put.py											//所有数据执行put功能文件
|    | -- intoModel.py											//清空数据库及数据库模板重置文件
|    | -- MysqlApi.py											//数据库操作函数等
| -- venv														//python环境文件
| -- virtual_Environment										//虚拟环境
| -- vue_api													//vue连接flask文件
| -- .gitgnore													//git文件
| -- app.py														//flask主函数文件，用于启动执行项目
| -- readme.md															
| -- requirements.txt											//环境依赖	
| -- wsgi.py													//跨域请求处理文件
```

