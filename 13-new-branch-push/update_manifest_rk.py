# -*- coding: utf-8 -*-
import csv
from lxml import etree

# 加载CSV文件
with open('prj.csv', 'r') as f:
    reader = csv.reader(f)
    paths = [row[0] for row in reader]  # 将CSV文件中的数据转换为一个列表

# 加载并解析XML文件
tree = etree.parse('unicair0618.xml')
root = tree.getroot()

# 获取默认revision
default_revision = root.find('default').get('revision')

# 遍历所有project节点
for project in root.findall('project'):
    path = project.get('path')

    # 如果project在CSV文件中
    if path in paths:
        # 如果没有revision属性，则添加默认revision
        if 'revision' not in project.attrib:
            project.set('revision', default_revision)
    else:
        # 如果project不在CSV文件中，删除revision属性
        if 'revision' in project.attrib:
            del project.attrib['revision']

# 将修改后的XML树写回到文件
tree.write('new_manifest.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')