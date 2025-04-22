#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import yaml
import subprocess
import logging
import time
import traceback
import commands  # type: ignore
import functools

def retry_decorator(max_attempts=3, delay=5):
        """重试装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(self, *args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        self.logger.warning("第 {} 次尝试失败: {}".format(attempts, e))
                        if attempts == max_attempts:
                            self.logger.error("操作 {} 最终失败".format(func.__name__))
                            raise
                        time.sleep(delay)
                return None
            return wrapper
        return decorator

class SyncManager:
    def __init__(self, config_path='sync.yaml', log_path='sync.log'):
        """初始化同步管理器"""
        # 记录脚本的当前工作目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.setup_logging(log_path)
        self.load_config(config_path)
        self.errors = []

    def setup_logging(self, log_path):
        """设置日志配置"""
        # 确保日志文件的完整路径
        log_path = os.path.join(self.script_dir, log_path)
        
        # 创建Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件Handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # 创建Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加Handler到Logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


    def load_config(self, config_path):
        """加载配置文件"""
        try:
            # 使用脚本目录下的配置文件
            full_config_path = os.path.join(self.script_dir, config_path)
            with open(full_config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            self.logger.error("加载配置文件失败: %s", str(e))
            sys.exit(1)


    def check_git_changes(self, directory):
        """
        检查Git仓库是否有变更
        
        :param directory: Git仓库目录
        :return: 是否有变更
        """
        try:
            # 切换到目标目录
            original_dir = os.getcwd()
            os.chdir(directory)
            
            # 检查是否有未跟踪或已修改的文件
            status, output = commands.getstatusoutput('git status --porcelain')
            
            # 切换回原目录
            os.chdir(original_dir)
            
            # 如果输出为空，说明没有变更
            return bool(output.strip())
        
        except Exception as e:
            error_msg = traceback.format_exc()
            self.logger.error("检查Git变更时发生异常: %s", str(e))
            self.logger.error("异常详细信息:\n%s", error_msg)
            return False


    def git_operations(self, directory, branch):
        """
        Git操作：add, commit, push
        
        :param directory: Git仓库目录
        :param branch: 分支名称
        """
        try:
            # 切换到目标目录
            original_dir = os.getcwd()
            os.chdir(directory)
            try:
                # 获取并打印Git项目名称
                status, git_remote_url = commands.getstatusoutput("git remote get-url unicair")
                if status == 0 and git_remote_url:
                    # 使用正则表达式过滤掉SSH协议、IP和端口
                    import re
                    # 匹配 ssh://IP:端口/ 后的路径
                    match = re.search(r'ssh://[^/]+/(.+)', git_remote_url)
                    
                    if match:
                        git_project_name = match.group(1)
                    else:
                        # 如果正则匹配失败，使用原始路径
                        git_project_name = git_remote_url
                else:
                    # 备选方案：使用当前目录名
                    git_project_name = os.path.basename(directory)
                
                self.logger.info("当前Git项目名称: %s", git_project_name)

            except Exception as name_error:
                self.logger.warning("无法获取Git项目名称: %s", str(name_error))
                git_project_name = "Unknown"

            # 检查是否有变更
            # if not self.check_git_changes(directory):
            #     self.logger.info("目录 %s 没有检测到变更，跳过Git操作", directory)
            #     return
            
            # 准备Git命令
            # git push unicair HEAD:refs/for/%s
            commands_list = [
                "git add .",
                "git commit -m \"%s\"" % branch,
                "git push unicair HEAD:%s" % branch
            ]
            
            # 依次执行命令
            for cmd in commands_list:
                # 使用 commands.getstatusoutput
                status, output = commands.getstatusoutput(cmd)
                
                # 检查命令执行结果
                if status != 0:
                    error_msg = output.strip()
                    self.logger.error("执行 %s 失败: %s", cmd, error_msg)
                    
                    # 处理特定错误
                    if "nothing to commit" in error_msg:
                        self.logger.info("没有需要提交的变更")
                        break
                    elif "no changes added to commit" in error_msg:
                        self.logger.info("没有变更被添加")
                        break
                    else:
                        raise Exception("Git操作失败: %s" % error_msg)
                else:
                    self.logger.info("成功执行: %s", cmd)
            
            os.chdir(original_dir)
            
        except Exception as e:
            os.chdir(original_dir)
            error_msg = traceback.format_exc()
            self.logger.error("Git操作异常: %s", str(e))
            self.logger.error("异常详细信息:\n%s", error_msg)
            raise
    @retry_decorator(max_attempts=3, delay=2)
    def local_rsync(self, source, target):
        """执行本地文件同步"""
        try:
            rsync_cmd = [
                'rsync', '-avrcuz',
                '--exclude=.repo',
                '--exclude=.git',
                '--exclude=.gitignore',                
                '--exclude=.gitattributes',
                "{}/".format(source),
                target
            ]
            result = subprocess.Popen(
                rsync_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = result.communicate()
            
            if result.returncode != 0:
                self.logger.error("Rsync失败: %s", stderr)
                raise Exception("Rsync失败: %s" % stderr)
            
            self.logger.info("文件同步成功: %s -> %s", source, target)
            return target  # 返回目标路径
        except Exception as e:
            self.logger.error("文件同步异常: %s", str(e))
            raise


    def normalize_path(self, path):
        """
        规范化路径，转换为绝对路径
        """
        base_dir = os.getcwd()
        full_path = os.path.normpath(os.path.join(base_dir, path))
        self.logger.info("路径规范化: %s -> %s", path, full_path)
        return full_path


    def find_git_repos(self, target_dir):
        """
        查找目标目录下的所有git仓库，包括嵌套的仓库
        """
        git_repos = []
        target_dir = self.normalize_path(target_dir)
        self.logger.info("开始搜索Git仓库，目标目录: %s", target_dir)


        if not os.path.exists(target_dir):
            self.logger.error("目标目录不存在: %s", target_dir)
            return git_repos


        for root, dirs, files in os.walk(target_dir):
            #self.logger.debug("当前搜索目录: %s", root)
            #self.logger.debug("当前目录下的子目录: %s", dirs)
            
            # 检查当前目录是否是Git仓库
            if '.git' in dirs:
                git_dir = os.path.join(root, '.git')
                if os.path.isdir(git_dir):
                    self.logger.info("找到Git仓库: %s", root)
                    git_repos.append(root)
                    dirs.remove('.git')  # 移除.git，避免重复查找
            
            # 继续搜索子目录，不阻止进一步查找
            # 移除已经确认为Git仓库的目录，避免重复添加
            dirs[:] = [d for d in dirs if d != '.git']


        self.logger.info("总共找到 %d 个Git仓库", len(git_repos))
        
        if not git_repos:
            self.logger.warning("在 %s 及其子目录中未找到任何Git仓库", target_dir)
        
        return git_repos
    @retry_decorator(max_attempts=10, delay=10)
    def repo_operations(self, target_dir, branch, target, option=False):
        """在指定目录执行repo操作"""
        original_dir = os.getcwd()  # 记录原始目录
        target_dir = self.normalize_path(target_dir)  # 规范化目标目录
        
        try:
            os.chdir(target_dir)  # 切换到目标目录
            
            if option:  # 非全仓库模式，单独处理每个git仓库
                git_repos = self.find_git_repos(target)  # 查找所有git仓库
                
                for repo_path in git_repos:
                    self.git_operations(repo_path, branch)  # 对每个仓库执行操作
            
            else:  # 全仓库模式
                if not os.path.exists('.repo'):
                    self.logger.error("目标目录不是repo仓库: %s", target_dir)
                    raise Exception("不是有效的repo仓库")
                
                # 执行repo操作的命令
                commands = [
                    "repo forall -c 'git add .'",
                    "repo forall -c 'git commit -m \"Source code upload\"'",
                    "repo forall -c 'git push unicair  HEAD:{}'".format(branch)
                ]
                
                for cmd in commands:
                    self.logger.info("执行命令: %s", cmd)  # 记录当前执行的命令
                    result = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = result.communicate()
                    
                    if result.returncode != 0:
                        self.logger.error("Repo操作失败: %s", cmd)
                        self.logger.error("错误信息: %s", stderr.strip())
                        raise Exception("Repo操作失败: %s" % stderr.strip())
            
            self.logger.info("仓库操作成功，分支: %s", branch)  # 操作成功的日志
            
        except Exception as e:
            # 确保即使出错也返回原始目录
            os.chdir(original_dir)
            error_msg = traceback.format_exc()
            self.logger.error("仓库操作异常: %s", error_msg)
            raise  # 重新抛出异常以供上层调用处理
        finally:
            os.chdir(original_dir)  # 确保返回原始目录

    def execute_sync(self):
        """执行同步流程"""
        try:
            for sync_item in self.config:
                source = sync_item.get('source')
                target = sync_item.get('target')
                branch = sync_item.get('branch')
                target_dir = sync_item.get('target_dir')
                option = sync_item.get('option', False)
              
                #target_path = self.local_rsync(source, os.path.join(target_dir, target))
                self.repo_operations(target_dir, branch, target, option)
        
        except Exception as e:
            self.logger.error("同步过程出现异常: %s", str(e))
            traceback.print_exc()


def main():
    config_path = 'sync.yaml'
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    sync_manager = SyncManager(config_path)
    sync_manager.execute_sync()


if __name__ == "__main__":
    main()