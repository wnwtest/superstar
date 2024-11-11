#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
import copy
def parse_manifest(manifest_path):
    """
    解析manifest文件
    :param manifest_path: manifest文件路径
    :return: 解析后的ElementTree
    """
    try:
        tree = ET.parse(manifest_path)
        return tree
    except ET.ParseError as e:
        print "Error parsing manifest: %s" % e
        sys.exit(1)
    except IOError as e:
        print "Error reading manifest file: %s" % e
        sys.exit(1)
def update_manifest(tree, name_prefix=None, path_prefix=None, name_replace=None, path_replace=None):
    """
    更新manifest文件
    :param tree: 原始manifest的ElementTree
    :param name_prefix: project name前缀
    :param path_prefix: project path前缀
    :param name_replace: project name替换规则
    :param path_replace: project path替换规则
    :return: 更新后的根元素
    """
    # 创建深拷贝，避免修改原始树
    root = copy.deepcopy(tree.getroot())
    # 处理project元素
    for project in root.findall('project'):
        # 更新name
        if name_prefix:
            current_name = project.get('name', '')
            project.set('name', os.path.join(name_prefix, current_name))
        
        if name_replace:
            current_name = project.get('name', '')
            new_name = current_name.replace(name_replace[0], name_replace[1])
            project.set('name', new_name)
        
        # 更新path
        if path_prefix:
            current_path = project.get('path', '')
            project.set('path', os.path.join(path_prefix, current_path))
        
        if path_replace:
            current_path = project.get('path', '')
            new_path = current_path.replace(path_replace[0], path_replace[1])
            project.set('path', new_path)
    return root
def prettify_xml(elem):
    """
    美化XML输出
    :param elem: XML元素
    :return: 格式化的XML字符串
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    # 自定义格式化
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # 移除空行
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    
    return '\n'.join(lines)

def write_manifest(root, output_path):
    """
    写入新的manifest文件
    :param root: XML根元素
    :param output_path: 输出文件路径
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 美化并写入XML文件
        pretty_xml = prettify_xml(root)
        
        with open(output_path, 'w') as f:
            f.write(pretty_xml)
        
        print "New manifest written to: %s" % output_path
        
        # 同时输出到控制台
        print "\n--- Preview of Manifest ---"
        print pretty_xml
        
    except Exception as e:
        print "Error writing manifest: %s" % e
        sys.exit(1)
def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Update repo manifest file')
    
    # 添加必需的参数
    parser.add_argument('-i', '--input', 
                        required=True, 
                        help='Input manifest file path')
    
    # 添加可选的输出参数
    parser.add_argument('-o', '--output', 
                        default='updated_manifest.xml',
                        help='Output manifest file path (default: updated_manifest.xml)')
    
    # 添加name前缀参数
    parser.add_argument('--name-prefix', 
                        help='Add prefix to project names')
    
    # 添加path前缀参数
    parser.add_argument('--path-prefix', 
                        help='Add prefix to project paths')
    
    # 添加name替换参数
    parser.add_argument('--name-replace', 
                        nargs=2,
                        metavar=('OLD', 'NEW'),
                        help='Replace part of project names')
    
    # 添加path替换参数
    parser.add_argument('--path-replace', 
                        nargs=2,
                        metavar=('OLD', 'NEW'),
                        help='Replace part of project paths')
    
    # 添加是否显示详细输出的参数
    parser.add_argument('-v', '--verbose', 
                        action='store_true',
                        help='Enable verbose output')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 验证输入文件是否存在
    if not os.path.exists(args.input):
        print "Input manifest file does not exist: %s" % args.input
        sys.exit(1)
    
    # 解析原始manifest
    original_tree = parse_manifest(args.input)
    
    # 更新manifest
    updated_root = update_manifest(
        original_tree, 
        name_prefix=args.name_prefix,
        path_prefix=args.path_prefix,
        name_replace=args.name_replace,
        path_replace=args.path_replace
    )
    
    # 写入新的manifest
    write_manifest(updated_root, args.output)
    
    # 如果启用详细输出，可以添加额外的日志
    if args.verbose:
        print "\n--- Verbose Information ---"
        print "Total projects processed: %d" % len(updated_root.findall('project'))
if __name__ == '__main__':
    main()