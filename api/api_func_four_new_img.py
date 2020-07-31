import base64
import json
import matplotlib
import squarify
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from pywaffle import Waffle
from api import api_func_four

"""
    参考代码https://blog.csdn.net/qq_30614345/article/details/99053555?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param
"""

# fdata = [{'one_minute': 0.52, 'id': 308, 'name': 'HTTP CORE'}, {'one_minute': 0.08, 'id': 9, 'name': 'Check heaps'}, {'one_minute': 0.04, 'id': 208, 'name': 'IP ARP Retry Ager'}, {'one_minute': 0.03, 'id': 196, 'name': 'VRRS Main thread'}, {'one_minute': 0.03, 'id': 205, 'name': 'IPAM Manager'}, {'one_minute': 0.02, 'id': 143, 'name': 'SASRcvWQWrk2'}, {'one_minute': 0.02, 'id': 212, 'name': 'SEP_webui_wsma_http'}, {'one_minute': 0.02, 'id': 457, 'name': 'TPS IPC Process'}, {'one_minute': 0.01, 'id': 124, 'name': 'IOSXE-RP Punt Service Process'}, {'one_minute': 0.01, 'id': 145, 'name': 'Per-minute Jobs'}, {'one_minute': 0.01, 'id': 232, 'name': 'Tunnel BGP'}, {'one_minute': 0.01, 'id': 435, 'name': 'MMA DB TIMER'}, {'one_minute': 0.01, 'id': 445, 'name': 'LOCAL AAA'}]
# for i in fdata:
#     print(i)


class newimg:
    def __init__(self, list_data, key, imgname):
        self.new_list = []
        self.name_list = []
        self.key = key
        for item in list_data:
            self.new_list.append(item[key]*100)
        for items in list_data:
            self.name_list.append(items['name'])
        self.new_dict = dict(zip(self.name_list, self.new_list))
        self.imgname = imgname

    def Waffle(self):
        total = sum(self.new_dict.values())
        # lables_list = []
        # for v, k in self.new_dict.items():
        #     str = '{}{}%'.format(k, v*100)
        #     lables_list.append(str)
        plt.figure(
            FigureClass=Waffle,
            rows=10,
            columns=13,
            values=self.new_dict,
            # 设置图例的位置
            legend={
                'loc': 'upper left',
                'bbox_to_anchor': (1, 1),
                # 'ncol': len(self.new_list),
                'framealpha': 0,
                'fontsize': 17
            },
            figsize=(15, 8),
            dpi=150,
            labels=['{:.1f}% {} {}'.format((v/total*100),' ', k) for k, v in self.new_dict.items()]
            # title={
            #     'label': self.imgname,
            #     'loc': 'left',
            #     'fontdict': {
            #         'fontsize': 30,
            #     }
            # }
        )
        plt.savefig("./api/img/{}".format(self.key))
        # plt.show()


# ad = newimg(fdata, 'one_minute', 'one_minute4')
# print(ad.Pie())
# ad.Lines()
# ad.Waffle()
def reimg_cup_time():
    # 三个cup占比的时间
    Ldata = api_func_four.getdata()
    new_list = [Ldata[2], Ldata[3], Ldata[4]]
    list = ['five_seconds', 'one_minute', 'five_minutes']
    namelist = ['Cup ratio in five seconds', 'Proportion of cup per minute', 'Proportion of cup in five minutes']
    i = 0
    while i <= 2:
        ad = newimg(new_list[i], list[i], namelist[i])
        ad.Waffle()
        print('成功生成', list[i])
        i += 1


def datatof():
    data = api_func_four.getdata()[0]
    lens = len(data)
    order = data[19:lens]
    order_num = 0
    new_dict = {}
    for item in order:
        order_num += item['invocation_count']
    new_dict['order'] = order_num
    for item in data[0:19]:
        new_dict[item['name']] = item['invocation_count']

    return new_dict


def countimg():
    datas = datatof()
    # 中文及负号处理办法
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False

    # 数据创建
    keys = list(datas.keys())
    values = list(datas.values())
    # 绘图details
    colors = ['steelblue', '#9999ff', 'red', 'indianred', 'deepskyblue', 'lime', 'magenta', 'violet', 'peru', 'green',
              'yellow', 'orange', 'tomato', 'lawngreen', 'cyan', 'darkcyan', 'dodgerblue', 'teal', 'tan', 'royalblue']
    plt.figure(figsize=(22.5, 12))
    plot = squarify.plot(
                         norm_x=100,
                         norm_y=100,
                         sizes=values,  # 指定绘图数据
                         label=keys,  # 指定标签
                         color=colors,  # 指定自定义颜色
                         alpha=1,  # 指定透明度
                         value=values,  # 添加数值标签
                         edgecolor='white',  # 设置边界框为白色
                         linewidth=10  # 设置边框宽度为3
                         )

    # 设置标签大小为10
    # plt.rc('font', size=10)
    # 除坐标轴
    plt.axis('off')
    # 除上边框和右边框刻度
    plt.tick_params(top='off', right='off')
    # 图形展示
    plt.savefig("./api/img/count")
    # plt.savefig("./img/count")
    print('成功生成count')

# countimg()


def rebase64():
    countimg()
    reimg_cup_time()
    list1 = ['five_seconds', 'one_minute', 'five_minutes']
    namelist1 = ['Cup ratio in five seconds', 'Proportion of cup per minute', 'Proportion of cup in five minutes']
    relistdata = []
    i = 0
    with open("./api/img/count.png", 'rb') as c:
        base64_data = base64.b64encode(c.read())
        cs = base64_data.decode()
        dictss = {"title": 'All thread runs', "base64": cs}
        relistdata.append(dictss)
    for item in list1:
        with open("./api/img/{}.png".format(item), 'rb') as f:
            # with open("./api/img/{}.png".format(item), 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            dict = {"title": namelist1[i], "base64": s}
            relistdata.append(dict)
    return relistdata

