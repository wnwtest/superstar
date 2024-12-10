# coding=utf-8
#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET
import copy

def process_manifests(a_file, b_file):
    # 解析 XML 文件
    tree_a = ET.parse(a_file)
    root_a = tree_a.getroot()
    tree_b = ET.parse(b_file)
    root_b = tree_b.getroot()

    # 遍历 a.xml 中的项目
    for project_a in list(root_a.findall('project')):
        name_a = project_a.get('name')
        path_a = project_a.get('path')

        # 寻找 b.xml 中的匹配项目
        for project_b in root_b.findall('project'):
            name_b = project_b.get('name')
            path_b = project_b.get('path')

            # 检查项目名称是否只相差一级
            if name_a.count('/') == name_b.count('/') + 1 and name_a.endswith(name_b.split('/', 1)[-1]):
                # 创建新的项目元素
                new_project = copy.deepcopy(project_b)

                # 添加注释
                comment = ET.Comment(" Clone project ")
                root_a.insert(list(root_a).index(project_a) + 1, comment)
                
                # 添加一个空白行（用换行符表示）
                #root_a.insert(list(root_a).index(project_a) + 2, ET.Comment('\n'))

                # 在 a.xml 中的原项目后面添加新项目
                root_a.insert(list(root_a).index(project_a) + 3, new_project)
                
                # 再添加一个空白行
                #root_a.insert(list(root_a).index(new_project) + 1, ET.Comment('\n'))

                # 从 b.xml 中删除匹配的项目
                root_b.remove(project_b)

                break

    # 保存修改后的 XML 文件
    tree_a.write(a_file, encoding='UTF-8', xml_declaration=True)
    tree_b.write(b_file, encoding='UTF-8', xml_declaration=True)

# 使用示例
a_file = 'qssi.xml'
b_file = 'vendor.xml'
process_manifests(a_file, b_file)