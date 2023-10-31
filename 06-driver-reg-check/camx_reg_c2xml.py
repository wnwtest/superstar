import re
from lxml import etree
# 从输入文件读取C数组
with open('mm-camera.txt', 'r') as file:
    c_array = file.read()
# 使用正则表达式提取数组数据
array_data = re.findall(r'{(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)}', c_array)
# 创建XML根元素
root = etree.Element("resSettings")
# 将数组数据添加到XML
for addr, data, delay in array_data:
    reg_setting = etree.SubElement(root, "resSetting")
    etree.SubElement(reg_setting, "registerAddr").text = addr
    etree.SubElement(reg_setting, "registerData").text = data
    etree.SubElement(reg_setting, "regAddrType", attrib={"range": "[1,4]"}).text = "2"
    etree.SubElement(reg_setting, "regDataType", attrib={"range": "[1,4]"}).text = "2"
    etree.SubElement(reg_setting, "operation").text = "WRITE"
    etree.SubElement(reg_setting, "delayUs").text = delay
# 将格式化的XML写入到输出文件
with open('output-camx.xml', 'wb') as file:
    file.write(etree.tostring(root, pretty_print=True))
