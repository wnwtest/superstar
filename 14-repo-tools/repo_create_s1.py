# -*- coding: utf-8 -*-
import os
import yaml
import argparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import logging
import traceback
import sys


# 确保兼容Python 2和3的字符串处理
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 导入兼容的StringIO
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
# 配置日志
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def extract_product_family(soup):
    """
    从HTML中提取Software Product Family，精确匹配
    """
    try:
        # 查找class为build的表格
        build_table = soup.find('table', class_='build')
        
        if not build_table:
            #logging.error("No table with class 'build' found")
            return 'manifest'
        
        # 打印表格的原始HTML，用于调试
        #logging.debug("Build Table HTML:\n{}".format(build_table))
        
        # 遍历所有行
        for row in build_table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            
            # 确保有足够的单元格
            if len(cells) < 2:
                continue
            
            # 精确匹配 "Software Product Family"
            first_cell_text = cells[0].get_text(strip=True)
            #logging.debug("Checking first cell: '{}'".format(first_cell_text))
            
            if first_cell_text == "Software Product Family":
                # 获取第二个单元格的值
                product_family = cells[1].get_text(strip=True)
                #logging.info("Exact Product Family found: {}".format(product_family))
                
                # 如果第二个单元格是 "Distribution"，则使用第一行的值
                if product_family == "Distribution":
                    # 查找包含实际值的行
                    data_row = row.find_next_sibling('tr')
                    if data_row:
                        data_cells = data_row.find_all(['th', 'td'])
                        if len(data_cells) > 0:
                            product_family = data_cells[0].get_text(strip=True)
                            #logging.info("Fallback Product Family found: {}".format(product_family))
                
                return sanitize_filename(product_family)
        
        # 如果没有找到，尝试直接查找第一行的值
        first_row = build_table.find('tr')
        if first_row:
            cells = first_row.find_all(['th', 'td'])
            if len(cells) > 1:
                product_family = cells[0].get_text(strip=True)
                #logging.info("Fallback first row Product Family: {}".format(product_family))
                return sanitize_filename(product_family)
        
        logging.warning("Unable to find Product Family")
        return 'manifest'
    
    except Exception as e:
        #logging.error(f"Error extracting product family: {e}")
        logging.error(traceback.format_exc())
        return 'manifest'
def sanitize_filename(name):
    """
    清理文件名，确保其有效且安全
    """
    import re
    # 替换特殊字符和空格
    name = re.sub(r'[^\w\-_\.]', '_', name)
    # 去除连续的下划线
    name = re.sub(r'_+', '_', name)
    # 截断过长的文件名
    return name[:255]


def parse_html_and_generate_manifest(html_content, config):
    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')


    # 从配置中获取产品和其他参数
    product = config.get('baseline', {}).get('product', '')


    # 找到组件表格
    component_table = soup.find('table', class_='component')


    # 创建manifest的根元素
    manifest = ET.Element('manifest')


    # 遍历表格行
    matched_projects = []
    for row in component_table.find_all('tr')[1:]:  # 跳过表头
        columns = row.find_all('td')


        # 检查是否有足够的列
        if len(columns) < 4:
            continue


        # 检查产品是否匹配
        products_cell = columns[0].get_text(strip=True)


        # 获取Image和Distro Path
        image = columns[1].get_text(strip=True)
        distro_path = columns[3].get_text(strip=True)


        if not product or (product and any(p.strip() in products_cell for p in product.split(','))):
            # 创建project元素
            project = ET.SubElement(manifest, 'project')
            project.set('name', image)
            project.set('path', distro_path)


            matched_projects.append(image)


    # 美化XML
    tree = ET.ElementTree(manifest)


    # 使用StringIO来处理XML输出
    output = StringIO()
    tree.write(output, encoding='utf-8', xml_declaration=False)


    # 获取XML字符串
    xml_str = output.getvalue()


    # 使用minidom进行美化
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')


    return pretty_xml, matched_projects



def show_selection_menu(matched_projects):
    """显示选择菜单，允许用户选择项目"""
    print("请选择要包含在 manifest XML 中的项目 (用逗号分隔选择，输入 'done' 结束选择):")
    for index, project in enumerate(matched_projects):
        print(u"{}: {}".format(index + 1, project))


    selected_indices = []
    while True:
        user_input = raw_input("输入项目编号 (如 1,2) 或 'done': ") if sys.version_info[0] < 3 else input("输入项目编号 (如 1,2) 或 'done': ")
        
        if user_input.lower() == 'done':
            break
        try:
            indices = [int(i.strip()) - 1 for i in user_input.split(',')]
            selected_indices.extend(indices)
        except ValueError:
            print("无效输入，请重新输入.")


    # 返回所选项目
    return [matched_projects[i] for i in selected_indices if 0 <= i < len(matched_projects)]


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Generate manifest XML from HTML build report')
    parser.add_argument('-c', '--config',
                        help='Path to YAML configuration file',
                        default='repo.yaml')
    parser.add_argument('-f', '--html',
                        help='Path to HTML input file',
                        required=True)
    parser.add_argument('-o', '--output',
                        help='Path to output manifest XML',
                        default=None)
    parser.add_argument('-p', '--product',
                        help='Override product from config',
                        default=None)


    # 解析命令行参数
    args = parser.parse_args()


    # 读取配置文件
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file) or {}
    except IOError:
        config = {}


    # 如果命令行指定了产品，覆盖配置文件中的产品
    if args.product:
        config['baseline'] = config.get('baseline', {})
        config['baseline']['product'] = args.product


    # 读取HTML文件
    with open(args.html, 'r') as file:
        html_content = file.read()


    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')


    # 添加详细日志
    logging.info("Parsing HTML for Product Family")


    # 确定输出文件名
    if not args.output:
        # 从HTML中提取产品系列作为文件名
        product_family = extract_product_family(soup) 
        logging.info("Extracted Product Family: {}".format(product_family))
        output_filename = "{}.xml".format(product_family)
    else:
        output_filename = args.output
    
    # 生成manifest
    manifest_xml, matched_projects = parse_html_and_generate_manifest(html_content, config)
    
    # 输出结果
    print("Product Family: {}".format(extract_product_family(soup)))
    print("\nMatched Projects:")
    for project in matched_projects:
        print("- {}".format(project))
    
    # 写入输出文件
    with open(output_filename, 'w') as file:
        file.write(manifest_xml)
    
    print("\nManifest XML generated: {}".format(output_filename))
if __name__ == '__main__':
    main()