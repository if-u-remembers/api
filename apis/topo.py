import os

datas = {
    "height":500,
    "data":[
        {
            "name":"DNAC",
            "coordinate-x":100,
            "coordinate-y":-50,
            "image":"Q.Graphs.server",
            "size":{"width":30, "height":-1},
            "type":"Name: DNA-Center Controller",
            "ipaddress":None,
            "hostname":None,
            "macAddress":None,
            "edge":None
        },
        {
            "name":"C3850_A",
            "coordinate-x":100,
            "coordinate-y":160,
            "image":"http://demo.qunee.com/editor/data/cisco/multilayerSwitch.Png",
            "size":{"width":50, "height":-1},
            "ipaddress":"10.10.20.85",
            "hostname":"spine1.abc.inc",
            "macAddress":"70:01:b5:5d:1b:00",
            "type":"Type: Cisco Catalyst38xx stack-able ethernet switch",
            "edge":{"start":"DNAC","end":"C3850_A"}
        }
    ]
}


class TopoNewDataFiles:
    def __init__(self, data):
        print('载入')
        self.data1 = '''<!DOCTYPE html>   
<html>
<head>
    <title>topo</title>
    <meta charset="utf-8">
</head>
<body>'''
        self.data2 = '''<script src="http://demo.qunee.com/lib/qunee-min.js"></script>
<script>
        var graph = new Q.Graph('canvas');'''
        self.data3 = '''
    edge.setStyle(Q.Styles.LABEL_OFFSET_Y, -10);
    edge.setStyle(Q.Styles.LABEL_POSITION, Q.Position.CENTER_TOP);
    edge.setStyle(Q.Styles.LABEL_ANCHOR_POSITION, Q.Position.CENTER_BOTTOM);
    edge.setStyle(Q.Styles.LABEL_BORDER, 1);
    edge.setStyle(Q.Styles.LABEL_POINTER, true);
    edge.setStyle(Q.Styles.LABEL_PADDING, new Q.Insets(2, 5));
    edge.setStyle(Q.Styles.LABEL_BACKGROUND_GRADIENT,
            Q.Gradient.LINEAR_GRADIENT_VERTICAL);
</script>
</body>
</html>'''
        self.data = data['data']
        self.height = data['auto']

    def __dataremore(self):
        bodydata = ''''''
        for item in self.data:
            names = '''
            var ''' + item['name'] + '''= graph.createNode("''' + item['name'] + '''",''' + str(item['coordinate-x']) + ''',''' + str(item['coordinate-y']) + ''');
            '''
            # 这一步区分默认格式图片内容和外链图片
            if item['image'].lower().endswith('png') or item['image'].lower().endswith('jpg'):
                imge = item['name'] + '''.image = "''' + item['image'] + '''";
                '''
            else:
                imge = item['name'] + '''.image = ''' + item['image'] + ''';
                '''
            size = item['name'] + '''.size = {width:''' + str(item['size']['width']) + ''',height:''' + str(item['size']['height']) + '''};
            '''
            tooltip = item['name'] + '''.tooltip = "''' + item['type']
            if item['hostname']:
                tooltip += '''<br>hostname:''' + item['hostname']
            if item['ipaddress']:
                tooltip += '''<br>ipaddress:''' + item['ipaddress']
            if item['macAddress']:
                tooltip += '''<br>macAddress:''' + item['macAddress']
            tooltip += '''";
            '''
            if item['edge']:
                edge = '''var edge = graph.createEdge("''' + item['edge']['start'] + '''--->>''' + item['edge']['end'] + '''",''' + item['edge']['start'] + ''',''' + item['edge']['end'] + ''');'''
            else:
                edge = ''''''
            bodydata += names + imge + size + tooltip + edge + '''
            '''
        return bodydata

    def creates(self):
        newfile = open('topo.html', "w")
        newfile.write(self.data1)
        hestr = '''<div style="height: ''' + str(self.height) + '''px;" id="canvas"/>'''
        newfile.write(hestr)
        newfile.write(self.data2)
        newfile.write(self.__dataremore())
        newfile.write(self.data3)
        newfile.close()
        print("生成成功")


# a = TopoNewDataFile(datas)
# a.creates()