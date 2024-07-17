# coding=utf-8
#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET
import os
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

def normalize_name(name):
    return name.replace('SM7675P/qssi/', '').replace('qssi/', '')

def compare_projects(qssi_projects, baseline_projects):
    not_in_baseline = []
    not_in_qssi = []
    
    for qssi_name, qssi_project in qssi_projects.items():
        normalized_name = normalize_name(qssi_name)
        if normalized_name not in [normalize_name(name) for name in baseline_projects.keys()]:
            not_in_baseline.append(qssi_project)
    
    for baseline_name, baseline_project in baseline_projects.items():
        normalized_name = normalize_name(baseline_name)
        if normalized_name not in [normalize_name(name) for name in qssi_projects.keys()]:
            not_in_qssi.append(baseline_project)
    
    return not_in_baseline, not_in_qssi

def create_manifest(projects, output_file):
    root = ET.Element('manifest')
    
    for project in projects:
        root.append(copy.deepcopy(project))
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qssi_file = os.path.join(script_dir, 'qssi.xml')
    baseline_file = os.path.join(script_dir, 'qssibaseline.xml')
    output_file_qssi = 'manifest_qssi_only.xml'
    output_file_baseline = 'manifest_baseline_only.xml'

    qssi_root = parse_xml(qssi_file)
    baseline_root = parse_xml(baseline_file)

    qssi_projects = get_projects(qssi_root)
    baseline_projects = get_projects(baseline_root)

    not_in_baseline, not_in_qssi = compare_projects(qssi_projects, baseline_projects)

    create_manifest(not_in_baseline, output_file_qssi)
    create_manifest(not_in_qssi, output_file_baseline)

    print "Projects found in qssi.xml but not in qssibaseline.xml have been written to '{}'".format(output_file_qssi)
    print "Projects found in qssibaseline.xml but not in qssi.xml have been written to '{}'".format(output_file_baseline)

if __name__ == "__main__":
    main()