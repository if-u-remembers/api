data = {
    "version": "1.0",
    "response": [
        {
            "time": "2020-09-02T00:55:00.000+0000",
            "healthScore": 100, # 健康分数
            "totalCount": 13,   # 设备总数量
            "goodCount": 13,   # 健康设备总数量
            "unmonCount": 0,
            "fairCount": 0,  # 公平计数
            "badCount": 0,  # 错误计数
            "entity": None,  # 实体
            "timeinMillis": 1599008100000  # 时间毫秒
        }
    ],
    "measuredBy": "global",  # 测量单位
    "latestMeasuredByEntity": None, # 最新测量值
    "latestHealthScore": 100,    # 最新健康分数
    "monitoredDevices": 13,     # 监控设备数量
    "monitoredHealthyDevices": 13,# 监测健康设备数
    "monitoredUnHealthyDevices": 0, # 监测不健康设备数
    "unMonitoredDevices": 0,# 不监测得设备
    "healthDistirubution": [ # 健康分布情况
        {
            "category": "Access",# 类别：访问
            "totalCount": 2,# 设备总数
            "healthScore": 100,# 健康分数
            "goodPercentage": 100,# 良好百分比
            "badPercentage": 0,# 错误百分比
            "fairPercentage": 0,# 公平百分比
            "unmonPercentage": 0,# 卸载百分比
            "goodCount": 2,# 设备良好总数
            "badCount": 0,# 设备错误总数
            "fairCount": 0,# 公平计算总数
            "unmonCount": 0 # 卸载总数
        },
        {
            "category": "WLC",
            "totalCount": 1,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 1,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0
        },
        {
            "category": "AP",
            "totalCount": 10,
            "healthScore": 100,
            "goodPercentage": 100,
            "badPercentage": 0,
            "fairPercentage": 0,
            "unmonPercentage": 0,
            "goodCount": 10,
            "badCount": 0,
            "fairCount": 0,
            "unmonCount": 0
        }
    ]
}
