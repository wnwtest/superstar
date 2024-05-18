# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import subprocess
import difflib

def get_gerrit_projects(branch):
    command = "ssh -p 29418 wangnanwang@192.168.117.71 gerrit ls-projects"
    projects = subprocess.check_output(command.split(), universal_newlines=True).splitlines()

    # 找出存在特定分支的项目
    projects_with_branch = []
    for project in projects:
        command = "git ls-remote --heads http://wangnanwang:wangnanwang@192.168.117.71/{}.git {}".format(project, branch)
        try:
            branches = subprocess.check_output(command.split(), universal_newlines=True)
            if 'refs/heads/{}'.format(branch) in branches:
                projects_with_branch.append(project)
        except subprocess.CalledProcessError:
            # Handle the exception for the case where the command fails
            pass

    return projects_with_branch
# 加载和解析manifest文件
def parse_manifest(manifest_file):
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    # 获取默认分支
    default = root.find('default')
    revision = default.get('revision')

    # 获取Gerrit中在此分支下的项目列表
    projects = get_gerrit_projects(revision)

    # 遍历每个项目元素
    for project in root.findall('project'):
        name = project.get('name')

        # 检查项目名称是否在Gerrit中存在
        if name not in projects:
            print("Project " + name + " does not exist on Gerrit. Correcting...")

            # 将项目名称更正为最接近的项目名称
            closest_name = difflib.get_close_matches(name, projects, n=1)
            if closest_name:
                project.set('name', closest_name[0])

    # 将更正后的manifest文件保存
    tree.write('correct_manifest.xml')

# 将要解析的manifest作为第一个参数
parse_manifest('UPQ00915_Q1100.xml')