"""
        这个文件的作用在于便捷数据库的清空，使得数据得以重置
"""
from apis import mysql
import json
val = (
          ('LoopBack6',
           '{"ietf-interfaces:interface": {"name": "Loopback6","description": "WHATEVER6","type": "iana-if-type:softwareLoopback","enabled": True,"ietf-ip:ipv4": {"address": [{"ip": "6.6.6.6","netmask": "255.255.255.0"}]},"ietf-ip:ipv6": {}}}',
           'https://li-say.top:6002/restconf/data/ietf-interfaces:interfaces/interface=Loopback6',
           '0', '创环回口', '可批量下发环回口配置、IP、掩码等', 6),
          ('ospf',
           '{"Cisco-IOS-XE-native:router": {"Cisco-IOS-XE-ospf:ospf": [{"id": 1,"router-id": "192.168.1.60","network": [{ "ip": "172.16.19.0","mask": "0.0.0.255","area": 0},{"ip": "172.16.20.0","mask": "0.0.0.255","area": 9}]},{"id": 2,"router-id": "192.168.1.10","network": [{"ip": "172.16.19.0","mask": "0.0.0.255","area": 0},{"ip": "172.16.20.0","mask": "0.0.0.255","area": 9}]}]}}',
           'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-native:native/router', '0',
           '创OSPF模板', '可以配置router-id和宣告相应的网段等', 5),
          ('acl',
           '{"Cisco-IOS-XE-native:access-list": {"Cisco-IOS-XE-acl:standard": [{"name": "cisco1","access-list-seq-rule": [{"sequence": "20","deny": {"std-ace": {"ipv4-prefix": "1.1.1.0"}}},{"sequence": "30","permit": {"std-ace": {"ipv4-prefix": "192.168.50.100"}}}]}],"Cisco-IOS-XE-acl:extended": [{"name": "meraki-fqdn-dns"}]}}',
           'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-native:native/ip/access-list',
           '0', '创建ACL模板', '可以修改ACL名称、序列号，允许或拒绝哪个网段和策略IP等', 1),
          ('dhcp',
           '{"Cisco-IOS-XE-native:dhcp": {"Cisco-IOS-XE-dhcp:excluded-address": {"low-high-address-list": [{"low-address": "192.168.56.50","high-address": "192.168.56.100"}]},"Cisco-IOS-XE-dhcp:pool": [{"id": "cisco1","lease": {"lease-value": {"days":6}},"default-router": {"default-router-list": ["192.168.56.1"]},"network": {"primary-network": {"number": "192.168.56.0","mask": "255.255.255.0"}}}]}}',
           'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp', '0',
           '创建DHCP模板', '可以修改配置：如排除的地址，租约的长短，DHCP服务器分配的网段和网关等', 2),
          ('isis',
        '{"Cisco-IOS-XE-isis:isis": {"metric-style": {"narrow": {}},"is-type": "level-1","lsp-refresh-interval": 400,"max-lsp-lifetime": 35,"net": [{"tag": "49.0002.0002.0002.0002.00"}]}}',
        'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-native:native/router/isis', '0',
        '创建ISIS模板', '可以改变lsp的链路刷新时间、最大存活时间以及isis实体tag等', 3),
        ('nat',
         '{"Cisco-IOS-XE-nat:nat": {"pool": [{"id": "cisco1","start-address": "172.16.1.10","end-address": "172.16.1.66","netmask": "255.255.255.0"}],"inside": {"source": {"list": [{"id": 66,"pool-with-vrf": {"pool": [{"name": "cisco1"}]}}],"static": {"nat-static-transport-list": [{"local-ip": "172.16.1.3","global-ip": "10.10.20.48"}]}}}}}',
        'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-native:native/ip/nat', '0',
        '创建NAT模板', '可配置nat地址池，实现公网和私网的转换等', 4)
)
host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'

sql = mysql.intomysql(host, mysqluser, password, database)
sql.printtable()


def intonew():
    nums = int(input('输入需要重置的数据表:（输入-1退出重置）\n'))
    if nums == -1:
        print('退出重置')
    else:
        sql.deltable(nums)
        sql.createtable(nums)


def intoModel_data(val):
    a = input("确认是否载入模板？（输入yes/no）")
    if a == 'yes':
        tablename = ['name', 'model', 'url', 'del', 'remarks', 'introduce', 'logo']
        sql.add_data(val, 'model_data', tablename)
        print('载入模板')
    else:
        print('取消载入')


def remodeldata():
    tablename = ['name', 'model', 'url', 'del', 'remarks', 'introduce', 'logo']
    return sql.add_data(val, 'model_data', tablename)


# intonew()
# intoModel_data(val)







