# coding=utf-8
#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET
import copy

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def get_projects(root):
    projects = {}
    for project in root.findall('project'):
        name = project.get('name')
        projects[name] = project
    return projects

def compare_projects(qssi_projects, vendor_projects):
    not_in_vendor = []
    for qssi_name, qssi_project in qssi_projects.items():
        vendor_name = qssi_name.replace('qssi/', '', 1)
        if vendor_name not in vendor_projects:
            not_in_vendor.append(qssi_project)
    return not_in_vendor

def create_manifest(missing_projects, output_file):
    root = ET.Element('manifest')
    
    for project in missing_projects:
        root.append(copy.deepcopy(project))
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

def main():
    qssi_file = 'qssi.xml'
    vendor_file = 'vendor.xml'
    output_file = 'manifest.xml'

    qssi_root = parse_xml(qssi_file)
    vendor_root = parse_xml(vendor_file)

    qssi_projects = get_projects(qssi_root)
    vendor_projects = get_projects(vendor_root)

    missing_projects = compare_projects(qssi_projects, vendor_projects)

    create_manifest(missing_projects, output_file)

    print "Projects found in qssi.xml but not in vendor.xml have been written to 'manifest.xml'"

if __name__ == "__main__":
    main()