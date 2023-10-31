#!/usr/bin/env python
# -*- coding: utf8 -*-
# --------------------------------------------------------------
#  push 命令 
# wangnanwang 2022 01
# --------------------------------------------------------------

import os
import pandas as pd
from lxml import etree

# 资源目录的路径
res_dir = 'res'

# 创建一个空的dataframe，用于存储数据
df = pd.DataFrame()

# 遍历资源目录下的所有子目录
for subdir in os.listdir(res_dir):
    if 'values' in subdir:
        # 子目录的完整路径
        subdir_path = os.path.join(res_dir, subdir)

        # strings.xml文件的完整路径
        strings_xml_path = os.path.join(subdir_path, 'strings.xml')

        # 确保strings.xml文件存在
        if os.path.isfile(strings_xml_path):
            # 从XML文件中提取数据
            tree = etree.parse(strings_xml_path)
            root = tree.getroot()

            # 提取每个<string>元素的name和text，并添加到dataframe中
            for string in root.findall('string'):
                name = string.attrib['name']
                text = string.text

                # 如果dataframe还未包含此name，创建一个新行
                if name not in df.index:
                    df.loc[name, 'name'] = name

                # 添加或更新此行的语言列
                df.loc[name, subdir] = text

# 将dataframe写入到Excel文件
df.to_excel('strings.xlsx', index=False)