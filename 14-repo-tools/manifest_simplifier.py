#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import yaml
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
import codecs

def load_yaml_config(yaml_path):
    """加载YAML配置文件"""
    try:
        with codecs.open(yaml_path, 'r', 'utf-8') as f:  # 使用codecs打开文件以支持utf-8编码
            config = yaml.safe_load(f)
        return config.get('operations', [])
    except Exception as e:
        print("Error reading YAML file: %s" % e)
        sys.exit(1)

def normalize_project_path(project):
    """确保project的path属性正确设置"""
    name = project.get('name')
    path = project.get('path')
    
    # 如果没有path属性，将path设置为name
    if path is None:
        project.set('path', name)
    
    return project

def apply_prefixes(project, name_prefix, path_prefix):
    """应用前缀到project的name和path属性"""
    if name_prefix:
        project.set('name', name_prefix + project.get('name'))
    if path_prefix:
        project.set('path', path_prefix + project.get('path'))

def update_link_copyfile_paths(project, path_prefix):
    """更新linkfile和copyfile的dst路径"""
    for linkfile in project.findall('linkfile'):
        dst = linkfile.get('dest')
        
        if dst is None or not isinstance(dst, str) or not dst.strip():  # 检查dst是否有效
            print("Error: linkfile 'dest' is None or not a valid string for project: '{}'".format(project.get('name')))
            continue  # 跳过这个linkfile的处理
        
        if path_prefix is None:
            print("Warning: path_prefix is None for project: '{}'".format(project.get('name')))
            continue
        
        linkfile.set('dest', os.path.join(path_prefix, dst))
    
    for copyfile in project.findall('copyfile'):
        dst = copyfile.get('dest')
        
        if dst is None or not isinstance(dst, str) or not dst.strip():  # 检查dst是否有效
            print("Error: copyfile 'dest' is None or not a valid string for project: '{}'".format(project.get('name')))
            continue  # 跳过这个copyfile的处理
        
        if path_prefix is None:
            print("Warning: path_prefix is None for project: '{}'".format(project.get('name')))
            continue
        
        copyfile.set('dest', os.path.join(path_prefix, dst))

def parse_manifest(manifest_path):
    """解析manifest文件"""
    try:
        tree = ET.parse(manifest_path)
        return tree
    except ET.ParseError as e:
        print("Error parsing manifest: %s" % e)
        sys.exit(1)
    except IOError as e:
        print("Error reading manifest file: %s" % e)
        sys.exit(1)

def prettify_xml(elem):
    """美化XML输出"""
    # 使用 tostring 方法转换为 UTF-8 编码的字节串
    rough_string = ET.tostring(elem, encoding='utf-8')
    
    # 使用 parseString 解析字节串
    reparsed = minidom.parseString(rough_string)
    
    # 获取 pretty XML 并确保是字符串
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # 移除空行
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    
    return '\n'.join(lines)

def write_manifest(root, output_path):

    """写入manifest文件"""

    try:

        # 移除属性值为 None 的属性

        for elem in root.iter():

            attrs_to_remove = [k for k, v in elem.attrib.items() if v is None]

            for attr in attrs_to_remove:

                del elem.attrib[attr]


        output_dir = os.path.dirname(output_path)

        if output_dir and not os.path.exists(output_dir):

            os.makedirs(output_dir)

        

        # 将 XML 转换为字符串

        rough_string = ET.tostring(root, encoding='utf-8')

        reparsed = minidom.parseString(rough_string)

        pretty_xml = reparsed.toprettyxml(indent="  ")

        

        # 对于 Python 2，使用 codecs 模块处理 UTF-8 编码

        import codecs

        with codecs.open(output_path, 'w', encoding='utf-8') as f:

            # 移除空行

            lines = [line for line in pretty_xml.split('\n') if line.strip()]

            f.write('\n'.join(lines))

        

        print("New manifest written to: %s" % output_path)

    except Exception as e:

        print("Error writing manifest: %s" % e)

        import traceback

        traceback.print_exc()
def process_single_xml(input_path, name_prefix, path_prefix):

    """处理单个XML文件"""

    print("Processing XML file: '{}'".format(input_path))  # 输出正在处理的XML文件名

    original_tree = parse_manifest(input_path)

    original_root = original_tree.getroot()


    # 获取文件基本名（不包含扩展名）

    base_filename = os.path.splitext(os.path.basename(input_path))[0]


    # 生成所有项目文件

    all_projects_root = ET.Element('manifest')

    comment = ET.Comment("All projects from: {}".format(os.path.basename(input_path)))

    all_projects_root.append(comment)

    

    # 生成特殊项目（有linkfile或copyfile）的文件

    special_projects_root = ET.Element('manifest')

    special_comment = ET.Comment("Special projects from: {}".format(os.path.basename(input_path)))

    special_projects_root.append(special_comment)

    

    # 生成完整特殊项目的文件

    full_special_projects_root = ET.Element('manifest')

    full_special_comment = ET.Comment("Full special projects from: {}".format(os.path.basename(input_path)))

    full_special_projects_root.append(full_special_comment)


    for project in original_root.findall('project'):

        # 标准化project的path属性

        normalize_project_path(project)


        # 应用前缀

        apply_prefixes(project, name_prefix, path_prefix)


        # 更新linkfile和copyfile的dst路径

        update_link_copyfile_paths(project, path_prefix)


        # 所有项目文件

        all_project_elem = ET.SubElement(all_projects_root, 'project')

        safe_set_attribute(all_project_elem, 'name', project.get('name'))

        safe_set_attribute(all_project_elem, 'path', project.get('path'))


        # 检查是否为特殊项目

        if project.find('linkfile') is not None or project.find('copyfile') is not None:

            # 特殊项目（不包含链接和复制文件）

            special_project_elem = ET.SubElement(special_projects_root, 'project')

            safe_set_attribute(special_project_elem, 'name', project.get('name'))

            safe_set_attribute(special_project_elem, 'path', project.get('path'))


            # 完整特殊项目

            full_special_project_elem = ET.SubElement(full_special_projects_root, 'project')

            safe_set_attribute(full_special_project_elem, 'name', project.get('name'))

            safe_set_attribute(full_special_project_elem, 'path', project.get('path'))

            

            # 添加linkfile和copyfile元素

            for linkfile in project.findall('linkfile'):

                # 创建一个新的linkfile元素，确保属性安全

                new_linkfile = ET.Element('linkfile')

                safe_set_attribute(new_linkfile, 'src', linkfile.get('src'))

                safe_set_attribute(new_linkfile, 'dest', linkfile.get('dest'))

                full_special_project_elem.append(new_linkfile)

            

            for copyfile in project.findall('copyfile'):

                # 创建一个新的copyfile元素，确保属性安全

                new_copyfile = ET.Element('copyfile')

                safe_set_attribute(new_copyfile, 'src', copyfile.get('src'))

                safe_set_attribute(new_copyfile, 'dest', copyfile.get('dest'))

                full_special_project_elem.append(new_copyfile)


    # 写入每个文件的结果（使用输入文件名为前缀）

    write_manifest(all_projects_root, os.path.join(os.path.dirname(input_path), base_filename + '_all_projects.xml'))

    

    if len(special_projects_root) > 1:

        write_manifest(special_projects_root, os.path.join(os.path.dirname(input_path), base_filename + '_special_projects.xml'))

    

    if len(full_special_projects_root) > 1:

        write_manifest(full_special_projects_root, os.path.join(os.path.dirname(input_path), base_filename + '_full_special_projects.xml'))

def process_global_special_projects(input_dir, operations):
    """生成全局特殊项目文件"""
    global_special_projects_root = ET.Element('manifest')
    global_full_special_projects_root = ET.Element('manifest')

    # 按照原始 XML 文件对特殊项目进行分组
    special_projects_by_file = {}
    full_special_projects_by_file = {}

    for operation in operations:
        input_file = operation.get('file')
        name_prefix = operation.get('name_prefix', '')
        path_prefix = operation.get('path_prefix', '')
        input_path = os.path.join(input_dir, input_file)
        original_tree = parse_manifest(input_path)
        original_root = original_tree.getroot()

        # 为每个文件初始化分组
        special_projects_by_file[input_file] = []
        full_special_projects_by_file[input_file] = []

        for project in original_root.findall('project'):
            # 标准化project的path属性
            project_name = project.get('name', '')
            project_path = project.get('path', project_name)

            # 检查是否为特殊项目，并确保linkfile和copyfile元素完整
            linkfiles = project.findall('linkfile')
            copyfiles = project.findall('copyfile')

            # 严格检查linkfile的有效性
            valid_linkfiles = [
                lf for lf in linkfiles 
                if lf.get('src') and lf.get('dest')
            ]

            # 严格检查copyfile的有效性
            valid_copyfiles = [
                cf for cf in copyfiles 
                if cf.get('src') and cf.get('dest')
            ]

            # 只处理具有有效linkfile或copyfile的项目
            if valid_linkfiles or valid_copyfiles:
                # 应用前缀
                prefixed_name = name_prefix + project_name
                prefixed_path = path_prefix + project_path

                # 全局特殊项目（不包含链接和复制文件）
                special_project_elem = ET.Element('project')
                special_project_elem.set('name', prefixed_name)
                special_project_elem.set('path', prefixed_path)
                special_projects_by_file[input_file].append(special_project_elem)

                # 全局完整特殊项目（包含链接和复制文件）
                full_special_project_elem = ET.Element('project')
                full_special_project_elem.set('name', prefixed_name)
                full_special_project_elem.set('path', prefixed_path)

                # 添加有效的linkfile元素
                for linkfile in valid_linkfiles:
                    new_linkfile = ET.Element('linkfile')
                    new_linkfile.set('src', linkfile.get('src'))
                    new_linkfile.set('dest', os.path.join(path_prefix, linkfile.get('dest')))
                    full_special_project_elem.append(new_linkfile)
                
                # 添加有效的copyfile元素
                for copyfile in valid_copyfiles:
                    new_copyfile = ET.Element('copyfile')
                    new_copyfile.set('src', copyfile.get('src'))
                    new_copyfile.set('dest', os.path.join(path_prefix, copyfile.get('dest')))
                    full_special_project_elem.append(new_copyfile)

                full_special_projects_by_file[input_file].append(full_special_project_elem)

    # 构建全局特殊项目文件
    for input_file, projects in special_projects_by_file.items():
        if projects:
            file_group_comment = ET.Comment("Projects from: {}".format(input_file))
            global_special_projects_root.append(file_group_comment)
            for project in projects:
                global_special_projects_root.append(project)

    for input_file, projects in full_special_projects_by_file.items():
        if projects:
            file_group_comment = ET.Comment("Projects from: {}".format(input_file))
            global_full_special_projects_root.append(file_group_comment)
            for project in projects:
                global_full_special_projects_root.append(project)

    # 写入全局特殊项目文件
    if len(global_special_projects_root) > 1:
        write_manifest(global_special_projects_root, os.path.join(input_dir, 'special_projects.xml'))
    if len(global_full_special_projects_root) > 1:
        write_manifest(global_full_special_projects_root, os.path.join(input_dir, 'full_special_projects.xml'))
def safe_set_attribute(element, key, value):

    """

    安全地设置 XML 元素的属性，确保值不为 None

    """

    if value is not None:

        element.set(key, str(value))        
def main():
    parser = argparse.ArgumentParser(description='Manifest Simplifier')
    parser.add_argument('input_dir', help='Input directory containing XML files')
    parser.add_argument('--config', help='YAML configuration file', default='config.yaml')
    args = parser.parse_args()

    # 检查输入目录下是否存在config.yaml
    if not os.path.isfile(args.config):
        config_path = os.path.join(args.input_dir, 'config.yaml')
        if os.path.isfile(config_path):
            args.config = config_path
        else:
            print("Error: Configuration file not found.")
            sys.exit(1)

    operations = load_yaml_config(args.config)

    # 处理每个XML文件
    for operation in operations:
        input_file = operation.get('file')
        name_prefix = operation.get('name_prefix')
        path_prefix = operation.get('path_prefix')

        input_path = os.path.join(args.input_dir, input_file)
        process_single_xml(input_path, name_prefix, path_prefix)

    # 生成全局特殊项目文件
    process_global_special_projects(args.input_dir, operations)

if __name__ == '__main__':
    main()