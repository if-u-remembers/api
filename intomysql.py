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

new_val = (
    # 新的模板数据一共5个字段
    # 第一个是命令，第二个名字，第三个logo标号，第四个介绍，第五个使用方法等
    ("""interface loopback 112
ip address 1.1.1.1 255.255.255.0
no shut""", "创建环回口", 1, "包括环回口的IP地址和掩码", " "),
    ("""vlan 8""", "vlan", 1, "包括vlan的名称", " "),
    ("""router isis
net 49.0001.0001.0001.0001.00
is-type level-1""", "ISIS", 1, "激活并设置ISIS并设置路由器类型", " "),
    ("""router bgp www
bgp 65001
neighbor 192.168.1.1
neighbor 192.168.1.1 timers 10 30 30
neighbor $CSRTunnelIP2 remote-as $NeighborBgpASNOfCloudRouter2
neighbor $CSRTunnelIP2 timers 10 30 30""", "BGP", 1 , "配置邻居路由器的AS号和IP", " "),
    ("""access-list 1 deny ip 192.168.10.0 any any
access-list 1 permit ip 10.10.20.0 any any""", "ACL", 1, "ACL名称、序列号，允许或拒绝哪个网段和策略IP等", " "),
    ("""ospf 100
network 10.10.20.0 0.0.0.255 area 1""", "OSPF", 1, "router-id和宣告相应的网段", " "),
    ("""ip dhcp pool wlan
network 192.168.10.0 255.255.255.0
default-router 192.168.10.254
dns-server 202.102.128.68 202.102.134.68
ip dhcp excluded-address 192.168.10.200 192.168.10.254""",  "dhcp", 1, "排除的地址，租约的长短，DHCP服务器分配的网段和网关", " "),
    ("""hostname AAA""", "修改设备名称", 1, "修改主机名", " ")
)


host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'

sql = mysql.intomysql(host, mysqluser, password, database)
sql.printtable()


def intonew(numss):
    if numss:
        nums = numss
    else:
        nums = int(input('输入需要重置的数据表:（输入-1退出重置）\n'))
    if nums == -1:
        print('退出重置')
    else:
        try:
            sql.deltable(nums)
        except:
            pass
        sql.createtable(nums)
        return '200'


def intoModel_data(vals):
    a = input("确认是否载入模板？（输入yes/no）")
    if a == 'yes':
        tablename = ['name', 'model', 'url', 'del', 'remarks', 'introduce', 'logo']
        sql.add_data(vals, 'model_data', tablename)
        print('载入模板')
    else:
        print('取消载入')


def intoNewModel_data(vals, ass):
    if ass == 'yes':
        a = ass
    else:
        a = input("确认是否载入模板？（输入yes/no）")
    if a == 'yes':
        tablename = ['model', 'name', 'logo', 'introduce', 'remarks']
        sql.add_data(vals, 'cisco_model_data', tablename)
        print('载入模板')
        return '200'
    else:
        print('取消载入')
        return '400'


# 重置数据表
# # 插入模板数据，插入数据列（旧的功能二模板数据库）
# intoModel_data(val)
# intonew(4)
# intoNewModel_data(new_val, 'yes')






