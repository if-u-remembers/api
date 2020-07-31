import matplotlib.pyplot as plt
import squarify
from api import api_func_four


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


datas = datatof()


def countimg():
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
    plot = squarify.plot(sizes=values,  # 指定绘图数据
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
    plt.savefig("./img/count")


countimg()

