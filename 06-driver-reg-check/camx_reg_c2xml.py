import re
import os
import argparse
import logging
from lxml import etree

'''
python script.py -i mm-camera.txt -o output.xml
'''


def parse_c_array(file_path):
    """
    解析多种格式的 C 数组文件并提取数据
    
    Args:
        file_path (str): 输入文件路径
    
    Returns:
        list: 提取的数组数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            c_array = file.read()
        
        # 方法1：处理原始格式 {addr, data, delay}
        pattern1 = r'{(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*(?:,\s*(0x[0-9a-fA-F]+))?\s*(?://.*?)?(?:/\*.*?\*/)?}'
        matches1 = re.findall(pattern1, c_array, re.DOTALL)
        
        # 方法2：处理新格式 addr, data
        pattern2 = r'(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)'
        matches2 = re.findall(pattern2, c_array, re.DOTALL)
        
        # 合并结果，优先使用方法1
        array_data = matches1 if matches1 else matches2
        
        # 过滤掉 REG_NULL 或无效条目
        array_data = [
            item for item in array_data 
            if item[0] != '0x0000' and len(item[0]) > 0
        ]
        
        return array_data
    
    except FileNotFoundError:
        logging.error(f"文件 {file_path} 未找到")
        return []
    except Exception as e:
        logging.error(f"解析文件出错: {e}")
        return []


def generate_xml(array_data, output_path):
    """
    生成XML文件
    
    Args:
        array_data (list): 数组数据
        output_path (str): 输出文件路径
    """
    try:
        # 创建XML根元素
        root = etree.Element("resSettings")
        
        # 添加XML头部注释
        root.addprevious(etree.Comment("Camera Register Settings"))
        
        # 将数组数据添加到XML
        for index, item in enumerate(array_data, 1):
            # 处理不同长度的数据项
            addr = item[0]
            data = item[1]
            delay = item[2] if len(item) > 2 else "0"
            
            reg_setting = etree.SubElement(root, "regSetting")
            
            # 添加序号属性
            #reg_setting.set("id", str(index))
            
            # 创建子元素，并添加更多验证和默认值
            etree.SubElement(reg_setting, "registerAddr").text = addr
            
            etree.SubElement(reg_setting, "registerData").text = data
            # 16-bit address
            etree.SubElement(reg_setting, "regAddrType", attrib={
                "range": "[1,4]"
            }).text = "2"
            # 8-bit data
            etree.SubElement(reg_setting, "regDataType", attrib={
                "range": "[1,4]"
            }).text = "1"

            
            etree.SubElement(reg_setting, "operation").text = "WRITE"
            
            # 默认延迟为0
            etree.SubElement(reg_setting, "delayUs").text = "0x00"
        
        # 创建XML树
        tree = etree.ElementTree(root)
        
        # 将格式化的XML写入到输出文件
        tree.write(
            output_path, 
            pretty_print=True, 
            xml_declaration=True, 
            encoding='utf-8'
        )
        
        logging.info(f"XML文件已成功生成: {output_path}")
    
    except Exception as e:
        logging.error(f"生成XML文件出错: {e}")


def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='C数组转XML转换工具')
    parser.add_argument('-i', '--input', required=True, help='输入C数组文件路径')
    parser.add_argument('-o', '--output', default='camera_regs.xml', help='输出XML文件路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 解析C数组
    array_data = parse_c_array(args.input)
    
    if array_data:
        # 生成XML
        generate_xml(array_data, args.output)
    else:
        logging.warning("未解析到有效数据")


if __name__ == "__main__":
    main()