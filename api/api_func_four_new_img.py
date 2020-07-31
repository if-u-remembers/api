import base64

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from pywaffle import Waffle

from api import api_func_four

"""
    参考代码https://blog.csdn.net/qq_30614345/article/details/99053555?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param
"""

fdata = [{'one_minute': 0.52, 'id': 308, 'name': 'HTTP CORE'}, {'one_minute': 0.08, 'id': 9, 'name': 'Check heaps'}, {'one_minute': 0.04, 'id': 208, 'name': 'IP ARP Retry Ager'}, {'one_minute': 0.03, 'id': 196, 'name': 'VRRS Main thread'}, {'one_minute': 0.03, 'id': 205, 'name': 'IPAM Manager'}, {'one_minute': 0.02, 'id': 143, 'name': 'SASRcvWQWrk2'}, {'one_minute': 0.02, 'id': 212, 'name': 'SEP_webui_wsma_http'}, {'one_minute': 0.02, 'id': 457, 'name': 'TPS IPC Process'}, {'one_minute': 0.01, 'id': 124, 'name': 'IOSXE-RP Punt Service Process'}, {'one_minute': 0.01, 'id': 145, 'name': 'Per-minute Jobs'}, {'one_minute': 0.01, 'id': 232, 'name': 'Tunnel BGP'}, {'one_minute': 0.01, 'id': 435, 'name': 'MMA DB TIMER'}, {'one_minute': 0.01, 'id': 445, 'name': 'LOCAL AAA'}]
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

    def Pie(self) -> object:
        return 0

    def Lines(self):
        return 0

    def Waffle(self):
        total = sum(self.new_dict.values())
        # lables_list = []
        # for v, k in self.new_dict.items():
        #     str = '{}{}%'.format(k, v*100)
        #     lables_list.append(str)
        plt.figure(
            FigureClass=Waffle,
            rows=12,
            # columns=10,
            values=self.new_dict,
            # 设置图例的位置
            legend={
                'loc': 'upper left',
                'bbox_to_anchor': (1, 1),
                # 'ncol': len(self.new_list),
                'framealpha': 0,
                'fontsize': 12
            },
            dpi=100,
            labels = ['{} {:.1f}%'.format(k, (v/total*100)) for k, v in self.new_dict.items()],
            title={
                'label': "CPU Occupy",
                'loc': 'left',
                'fontdict': {
                    'fontsize': 16,
                }
            }
        )
        plt.savefig("./img/{}".format(self.imgname))
        plt.show()


# ad = newimg(fdata, 'one_minute', 'one_minute')
# # print(ad.Pie())
# # ad.Lines()
# ad.Waffle()
