from PIL import Image
import PIL
import matplotlib.pyplot as plt
import numpy as np
import io


# def index():
#     # 数据准备
#     x = np.arange(1440)
#     y = x
#
#     fig = plt.figure()
#     plt.plot(x, y**2)
#     canvas = fig.canvas
#     # 上面这段代码和上面注释掉的代码效果一样
#     # # 方法1
#     buffer = io.BytesIO()
#     canvas.print_png(buffer)
#     data = buffer.getvalue()
#     buffer.close()
#     # 向前端返回图像
#     res = app.make_response(data)
#     res.headers["Content-Type"] = "image/png"
#     print(res)
#     return res