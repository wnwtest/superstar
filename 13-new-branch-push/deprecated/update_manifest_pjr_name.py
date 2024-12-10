# coding=utf-8
import os
import sys
import xml.etree.ElementTree as ET

def update_manifest(prefix, manifest_file):
    # 解析XML
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    # 找到所有的'project'节点
    for project in root.findall('project'):
        # 获取'name'属性
        name = project.get('name')
        # 更新'name'属性
        project.set('name', os.path.join(prefix, name))

    # 将更新后的XML写回文件
    tree.write(manifest_file, encoding='utf-8')

if __name__ == '__main__':
    # 从命令行参数获取前缀和manifest文件名
    if len(sys.argv) < 3:
        print('Usage: python update_manifest.py [prefix] [manifest_file]')
        sys.exit(1)

    prefix = sys.argv[1]
    manifest_file = sys.argv[2]

    update_manifest(prefix, manifest_file)