#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

def get_git_projects(root_dir):
    git_projects = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirnames:
            git_projects.append(dirpath)
    return git_projects

def count_git_logs(project_path):
    try:
        output = subprocess.check_output(['git', 'log', '--oneline'], cwd=project_path)
        return len(output.strip().split('\n'))
    except subprocess.CalledProcessError:
        return 0

def main():
    root_dir = os.getcwd()  # 使用当前目录作为根目录，你也可以指定其他目录
    git_projects = get_git_projects(root_dir)

    for project_path in git_projects:
        log_count = count_git_logs(project_path)
        if log_count == 1:
            project_name = os.path.basename(project_path)
            print u"项目名称: {0}".format(project_name)
            print u"项目路径: {0}".format(project_path)
            print "------------------------"

if __name__ == "__main__":
    main()