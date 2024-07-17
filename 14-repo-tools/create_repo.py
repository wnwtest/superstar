# coding=utf-8
import os
import shutil
import xml.etree.ElementTree as ET

def create_repo(manifest_path, demo_path, output_dir):
    # 解析manifest.xml文件
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # 遍历所有project元素
    for project in root.findall('project'):
        name = project.get('name')
        
        # 构建目标路径
        target_path = os.path.join(output_dir, name + '.git')
        
        # 创建目标目录
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        
        # 复制demo.git到目标路径
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(demo_path, target_path)
        
        print "Created repository:", target_path

if __name__ == '__main__':
    manifest_path = 'gen_manifest.xml'  # 请替换为实际的manifest.xml路径
    demo_path = 'demo.git'  # 请替换为实际的demo.git路径
    output_dir = 'SM7675P'  # 请替换为实际的输出目录

    create_repo(manifest_path, demo_path, output_dir)