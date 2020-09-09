from apis import new_func_two_ck

url_api = 'https://sandboxdnac2.cisco.com'
user = 'admin'
pwd = 'Cisco1234!'
host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'

a = new_func_two_ck.new_func_two(url=url_api, user=user, pwd=pwd, modelhost=host, modelmysqluser=mysqluser, modelpassword=password, modeldatabase=database)
# print(a.create_model('guojia1', 3))
print(a.get_project_id('guojia123456'))
# a.del_project_model('guojia1', 1)
# print(a.get_project_model('guojia123456'))
# model = """interface loopback 112
# ip address 1.1.1.1 255.255.255.0
# no shut"""

# a.updata_project_model_data('guojia1', 1, model, 'loopbacks123456')
# print(a.get_project_model('guojia1'))

# a.get_device()
# a.deploy_project_model('guojia1', 'vlan', '10.10.20.81', 'MANAGED_DEVICE_IP')

# /api/v1/task/b087ab8d-ac66-41e5-bc35-a2fd023644f0?__preventCache=1599617075756