# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom as minidom

def parse_manifest(file_path):
    doc = minidom.parse(file_path)
    project_nodes = doc.getElementsByTagName('project')
    return {node.getAttribute('name'): node.getAttribute('path') for node in project_nodes}

def compare_manifests(before_file, after_file):
    before_projects = parse_manifest(before_file)
    after_projects = parse_manifest(after_file)

    before_set = set(before_projects.keys())
    after_set = set(after_projects.keys())

    common = before_set & after_set

    only_in_before = before_set - common
    only_in_after = after_set - common

    print('Only in before manifest:')
    for project_name in only_in_before:
        print('Project name: {}, path: {}'.format(project_name, before_projects[project_name]))

    print('Only in after manifest:')
    for project_name in only_in_after:
        print('Project name: {}, path: {}'.format(project_name, after_projects[project_name]))

    print('Different configuration in common projects:')
    for project_name in common:
        if before_projects[project_name] != after_projects[project_name]:
            print('Project name: {}'.format(project_name))
            print('Before path: {}'.format(before_projects[project_name]))
            print('After path: {}'.format(after_projects[project_name]))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python compare_manifests.py before.xml after.xml')
        sys.exit(1)
    compare_manifests(sys.argv[1], sys.argv[2])