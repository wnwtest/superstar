#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
class RepoTagError(Exception):
    """自定义异常类，用于处理 Repo Tag 相关的错误"""
    pass
def command_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
def check_commands():
    for cmd in ['repo', 'git']:
        if not command_exists(cmd):
            raise RepoTagError(f"错误: {cmd} 未安装。请安装后再运行此脚本。")
def check_repo_dir():
    if not os.path.isdir('.repo'):
        raise RepoTagError("错误: 当前目录不是 repo 工作目录。")
def create_manifest(tag_name):
    """
    创建 manifest 文件
    :param tag_name: 标签名称
    :return: manifest 文件的相对路径
    """
    tag_dir = os.path.join('.repo', 'manifests')
    if not os.path.exists(tag_dir):
        os.makedirs(tag_dir)
    manifest_file = os.path.join(tag_dir, f"{tag_name}.xml")
    subprocess.check_call(['repo', 'manifest', '-r', manifest_file])
    return os.path.join('tag', f"{tag_name}.xml")
def push_changes(tag_name, manifest_file, remote_branch='master'):
    """
    推送更改到远程仓库
    :param tag_name: 标签名称
    :param manifest_file: manifest 文件的相对路径
    :param remote_branch: 远程分支名称
    """
    try:
        os.chdir(os.path.join('.repo', 'manifests'))
        
        # 检查远程分支是否存在
        result = subprocess.run(['git', 'ls-remote', '--heads', 'origin', remote_branch],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not result.stdout:
            raise RepoTagError(f"远程分支 '{remote_branch}' 不存在")
        subprocess.check_call(['git', 'add', manifest_file])
        subprocess.check_call(['git', 'commit', '-m', f'Add manifest for tag {tag_name}'])
        subprocess.check_call(['git', 'push', 'origin', f'HEAD:{remote_branch}'])
    except subprocess.CalledProcessError as e:
        raise RepoTagError(f"Git 操作失败: {str(e)}")
    finally:
        # 返回到原始目录
        os.chdir(os.path.dirname(os.path.dirname(os.getcwd())))
def create_and_push_tag(tag_name, push=False, remote_branch='master'):
    """
    创建新的 manifest 文件并可选择性地推送到远程仓库。
    :param tag_name: 新标签的名称
    :param push: 是否推送更改到远程仓库，默认为 False
    :param remote_branch: 要推送到的远程分支名称，默认为 'master'
    :return: 生成的 manifest 文件路径
    :raises: RepoTagError 当操作失败时
    """
    try:
        if not tag_name:
            raise RepoTagError("错误: 标签名不能为空。")
        check_commands()
        check_repo_dir()
        manifest_file = create_manifest(tag_name)
        print(f"新的 manifest 文件已生成: {manifest_file}")
        if push:
            push_changes(tag_name, manifest_file, remote_branch)
            print("更改已成功推送到远程仓库的 {} 分支。".format(remote_branch))
        else:
            print("更改未推送到远程仓库。")
            print("注意: 新的 manifest 文件已生成，但尚未提交到版本控制。")
        return manifest_file
    except RepoTagError:
        raise
    except Exception as e:
        raise RepoTagError(f"未预期的错误: {str(e)}")
if __name__ == '__main__':
    # 模块测试代码
    pass