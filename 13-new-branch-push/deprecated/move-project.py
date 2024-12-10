# coding=utf-8
import sys
import xml.etree.ElementTree as ET

# 添加一个新的函数来进行格式化
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def convert_to_remove_project(input_file, output_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        # 创建一个新的XML根元素
        new_root = ET.Element('manifest')

        for project in root.findall('./project'):
            # 创建新的 remove-project 元素
            remove_project = ET.Element('remove-project')

            # 复制 'name' 属性
            if 'name' in project.attrib:
                remove_project.attrib['name'] = project.attrib['name']

            # 将新元素添加到新的根元素中
            new_root.append(remove_project)

        # 调用我们的格式化函数
        indent(new_root)

        # 创建并写入新的XML树
        new_tree = ET.ElementTree(new_root)
        new_tree.write(output_file, encoding='utf-8', xml_declaration=True, method="xml")

        print('Conversion successful, output written to {}'.format(output_file))

    except Exception as e:
        print('An error occurred while converting the file: {}'.format(e))

def main():
    if len(sys.argv) != 3:
        print('Usage: python script.py input_file.xml output_file.xml')
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_to_remove_project(input_file, output_file)

if __name__ == '__main__':
    main()