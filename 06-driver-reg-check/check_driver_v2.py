#coding=utf-8
import re
from lxml import etree

# 从文本文件读取C数组
with open('input.txt', 'r') as file:
    c_array = file.read()

# 使用正则表达式提取数组数据
array_data_txt = re.findall(r'{(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)}', c_array)

# 从XML文件读取数据
tree = etree.parse('hi1336_sensor.xml')
root = tree.getroot()

array_data_xml = []
for reg_setting in root.findall('regSetting'):
    addr = reg_setting.find('registerAddr').text
    data = reg_setting.find('registerData').text
    array_data_xml.append((addr, data))

# 比较两组数据
for (addr_txt, data_txt), (addr_xml, data_xml) in zip(array_data_txt, array_data_xml):
    if addr_txt != addr_xml or data_txt != data_xml:
        print(f"Warning: Data mismatch! Text: ({addr_txt}, {data_txt}), XML: ({addr_xml}, {data_xml})")