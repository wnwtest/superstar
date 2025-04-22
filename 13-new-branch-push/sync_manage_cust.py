#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import yaml
# import commands  # u'已弃用, 被 subprocess 替代'
import subprocess # u'使用 subprocess 代替 commands'
import logging
import time
import traceback
import functools
import threading
import multiprocessing
import argparse
import re

# u'处理 Python 2.7 的 ThreadPoolExecutor 兼容性'
try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    try:
        # u'futures 包是 concurrent.futures 的 Python 2.7 backport'
        from futures import ThreadPoolExecutor
    except ImportError:
        # u'使用英文输出错误信息'
        print >> sys.stderr, "Error: Missing 'futures' module. Please run 'pip install futures' to install it."
        sys.exit(1)

# --- 常量 ---
DEFAULT_CONFIG_FILE = 'sync.yaml'
DEFAULT_LOG_FILE = 'sync.log'
DEFAULT_REMOTE_NAME = 'origin' # u'提供一个更标准的默认远程名称'

'''
u'示例 repo 命令 (通常在 repo 工作区根目录执行):'
repo forall -c 'git add .'
repo forall -c 'git commit -m "提交说明"'
repo forall -c 'git push <remote_name> HEAD:<target_branch>'

u'示例 单个 git 命令 (在 git 仓库根目录执行):'
git add .
git commit -m "提交说明"'
git push <remote_name> HEAD:<target_branch>'
'''

def safe_decode(byte_string):
    # u"""安全地将字节串解码为 Unicode 字符串 (UTF-8)，忽略错误。"""
    if byte_string is None:
        return u''
    if isinstance(byte_string, unicode):
        return byte_string
    try:
        return byte_string.decode('utf-8', errors='ignore')
    except Exception as e:
        # u'记录解码失败，但继续执行'
        logging.warning("Failed to decode bytes to unicode: %s", e)
        # u'返回一个表示错误的 Unicode 字符串或空字符串'
        return u'[Decode Error]'

def run_subprocess(cmd, cwd=None, shell=True):
    # u"""
    # u'使用 subprocess 执行命令，返回状态码、stdout、stderr (均为 Unicode)。
    # u':param cmd: 要执行的命令字符串。
    # u':param cwd: 命令执行的工作目录 (默认为 None，使用当前目录)。
    # u':param shell: 是否通过 shell 执行 (默认为 True)。
    # u':return: (returncode, stdout_unicode, stderr_unicode)
    # u"""
    try:
        logging.debug("Running command: [%s] in directory [%s]", cmd, cwd or os.getcwd())
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        )
        stdout_bytes, stderr_bytes = process.communicate()
        returncode = process.returncode

        # u'解码输出为 Unicode'
        stdout_unicode = safe_decode(stdout_bytes)
        stderr_unicode = safe_decode(stderr_bytes)

        if returncode != 0:
             logging.warning("Command failed with return code %d: [%s]", returncode, cmd)
             logging.debug("Stderr:\n%s", stderr_unicode)
             logging.debug("Stdout:\n%s", stdout_unicode)
        # else:
        #      logging.debug("Command succeeded: [%s]", cmd) # u'成功信息可能过多，注释掉'

        return returncode, stdout_unicode, stderr_unicode

    except OSError as e:
        # u'命令未找到等 OS 错误'
        err_msg = u"Command execution OSError: %s, Command: %s" % (e, cmd)
        logging.error(err_msg)
        return -1, u'', err_msg
    except Exception as e:
        # u'其他未知错误'
        err_msg = u"Command execution unknown error: %s, Command: %s" % (e, cmd)
        logging.error(err_msg)
        logging.debug(traceback.format_exc())
        return -1, u'', err_msg


def retry_decorator(max_attempts=3, delay=5):
    # u"""
    # u'重试装饰器: 当被装饰的函数抛出异常时，自动重试。
    # u':param max_attempts: 最大尝试次数
    # u':param delay: 每次重试之间的延迟时间（秒）
    # u':return: 装饰器
    # u"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs): # u'修正参数签名'
            attempts = 0
            last_exception = None
            func_name = func.__name__ # u'获取函数名用于日志'

            while attempts < max_attempts:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    # u'使用 self.logger (假设 self 是 SyncManager 实例)'
                    logger_instance = getattr(self, 'logger', None)
                    log_prefix = "[Retry %d/%d]" % (attempts, max_attempts)

                    # u'构造英文错误消息'
                    error_message = "Function '%s' failed on attempt %d: %s" % (func_name, attempts, unicode(e))

                    if logger_instance:
                        logger_instance.warning("%s %s", log_prefix, error_message)
                        if attempts < max_attempts:
                            logger_instance.info("%s Retrying in %d seconds...", log_prefix, delay)
                            time.sleep(delay)
                        else:
                            logger_instance.error("%s Function '%s' failed after %d attempts.", log_prefix, func_name, max_attempts)
                    else: # u'如果 self 没有 logger，则打印到 stderr (英文)'
                        print >> sys.stderr, "%s %s" % (log_prefix, error_message)
                        if attempts < max_attempts:
                             print >> sys.stderr, "%s Retrying in %d seconds..." % (log_prefix, delay)
                             time.sleep(delay)
                        else:
                            print >> sys.stderr, "%s Error: Function '%s' failed after %d attempts." % (log_prefix, func_name, max_attempts)

            # u'如果所有尝试都失败，再次抛出最后一次的异常'
            raise last_exception

        return wrapper
    return decorator

class SyncManager(object):  # u'使用新式类'
    def __init__(self, config_path=DEFAULT_CONFIG_FILE, log_path=DEFAULT_LOG_FILE):
        # u"""
        # u'初始化同步管理器。
        # u':param config_path: 配置文件的相对路径或绝对路径。
        # u':param log_path: 日志文件的相对路径或绝对路径。
        # u"""
        try:
            # u'获取CPU核心数 (Python 2.7 兼容)'
            self.max_workers = multiprocessing.cpu_count() * 2
        except NotImplementedError:
            # u'某些环境可能不支持，设置默认值'
            self.max_workers = 8
            print >> sys.stderr, "Warning: Could not detect CPU count, using default max_workers = %d" % self.max_workers # u'英文输出'

        # u'获取脚本所在目录的绝对路径'
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        # u'设置日志记录器'
        self.setup_logging(log_path)
        # u'加载配置文件'
        self.load_config(config_path)
        # u'用于存储执行过程中遇到的错误信息 (英文)'
        self.errors = []
        # u'线程锁，用于保护可能冲突的操作 (例如 repo forall)'
        self.repo_lock = threading.Lock()
        self.logger.info("SyncManager initialized. Max workers: %d", self.max_workers) # u'英文日志'

    def setup_logging(self, log_path):
        # u"""
        # u'设置日志配置。
        # u':param log_path: 日志文件的路径 (可以是相对路径)。
        # u"""
        # u'处理相对路径和绝对路径'
        if os.path.isabs(log_path):
             full_log_path = log_path
        else:
             full_log_path = os.path.join(self.script_dir, log_path)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) # u'记录 DEBUG 及以上级别'
        # u'防止重复添加 handler'
        if self.logger.handlers:
            self.logger.handlers = []

        try:
            # u'确保日志目录存在'
            log_dir = os.path.dirname(full_log_path)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_handler = logging.FileHandler(full_log_path, encoding='utf-8')
        except IOError as e:
             # u'英文错误信息'
             print >> sys.stderr, "Error: Cannot open or create log file %s: %s" % (full_log_path, e)
             print >> sys.stderr, "Please check directory permissions or path."
             sys.exit(1)

        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO) # u'控制台只显示 INFO 及以上'
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.info("Logging setup complete. Log file: %s", full_log_path) # u'英文日志'

    def load_config(self, config_path):
        # u"""
        # u'加载并解析 YAML 配置文件。需要新格式 (包含 sync_config 和可选的 _defaults)。
        # u':param config_path: 配置文件的路径。
        # u"""
        # u'处理相对路径和绝对路径'
        if os.path.isabs(config_path):
            full_config_path = config_path
        else:
            full_config_path = os.path.join(self.script_dir, config_path)

        self.logger.info("Loading configuration file: %s", full_config_path) # u'英文日志'
        if not os.path.exists(full_config_path):
            self.logger.error("Configuration file not found: %s", full_config_path) # u'英文日志'
            self.logger.error("Please ensure the config file exists or provide the correct path.") # u'英文日志'
            sys.exit(1)
        try:
            with open(full_config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            if not config_data:
                self.logger.error("Configuration file is empty or invalid: %s", full_config_path) # u'英文日志'
                sys.exit(1)

            # u'强制要求新格式'
            if not isinstance(config_data, dict) or 'sync_config' not in config_data:
                 self.logger.error("Invalid configuration format. Root element must be a dictionary containing 'sync_config'.") # u'英文日志'
                 self.logger.error("Old list-based format is no longer supported. Please update your config file.") # u'英文日志'
                 sys.exit(1)

            self.logger.info("Detected new configuration format.") # u'英文日志'
            self.config = []
            global_defaults = config_data.get('_defaults', {}) # u'全局默认值'
            # u'确保默认远程名称存在'
            global_defaults.setdefault('remote_name', DEFAULT_REMOTE_NAME)
            self.logger.debug("Global defaults: %s", global_defaults)

            sync_config_list = config_data.get('sync_config', [])
            if not isinstance(sync_config_list, list):
                self.logger.error("Configuration error: 'sync_config' must be a list.")
                sys.exit(1)

            for item_idx, item in enumerate(sync_config_list):
                if not isinstance(item, dict):
                    self.logger.warning("Skipping invalid item #%d in 'sync_config' (not a dictionary): %s", item_idx + 1, item)
                    continue

                item_defaults = item.get('_defaults', {}) # u'项级别默认值'
                # u'合并默认值：项级别覆盖全局级别'
                merged_defaults = global_defaults.copy()
                merged_defaults.update(item_defaults)

                # u'准备 sync_item 结构'
                sync_item = {
                    'sources': [self.normalize_path(src) for src in item.get('sources', []) if src], # u'过滤空源路径'
                    'targets': [],
                    # u'option 和 threshold 优先用 item 里的，其次用合并后的 defaults 里的'
                    # u'option: False = 使用 repo forall (默认), True = 使用单个 git 命令'
                    'option': item.get('option', merged_defaults.get('option', False)),
                    'large_repo_threshold': item.get('large_repo_threshold', merged_defaults.get('large_repo_threshold', 1024)), # u'默认1GB (MB)'
                    'item_index': item_idx + 1 # u'用于日志记录'
                }

                targets_list = item.get('targets', [])
                if not isinstance(targets_list, list):
                     self.logger.warning("Skipping targets for item #%d because 'targets' is not a list: %s", item_idx + 1, targets_list)
                     continue

                if not sync_item['sources']:
                     self.logger.warning("Skipping item #%d because 'sources' is empty or invalid.", item_idx + 1)
                     continue

                for target_idx, target in enumerate(targets_list):
                     if not isinstance(target, dict):
                        self.logger.warning("Skipping invalid target #%d in item #%d (not a dictionary): %s", target_idx + 1, item_idx + 1, target)
                        continue

                     # u'合并 target 和 defaults：target 覆盖 defaults'
                     final_target = merged_defaults.copy()
                     final_target.update(target)

                     # u'验证必需字段'
                     if 'dir' in final_target and 'path' in final_target and 'branch' in final_target:
                         final_target['repo_dir'] = self.normalize_path(final_target['dir'])
                         final_target['full_target_path'] = self.normalize_path(os.path.join(final_target['dir'], final_target['path']))
                         # u'将合并后的 option 和 threshold 也加入 target_info'
                         final_target['option'] = sync_item['option'] # u'使用顶层 item 的 option'
                         final_target['large_repo_threshold'] = sync_item['large_repo_threshold']
                         # u'确保 remote_name 存在 (来自 defaults 或 target 自身)'
                         final_target.setdefault('remote_name', merged_defaults.get('remote_name', DEFAULT_REMOTE_NAME))

                         # u'检查路径是否有效'
                         if not final_target['repo_dir'] or not final_target['full_target_path']:
                             self.logger.warning(u"Skipping target #%d in item #%d due to invalid 'dir' or 'path': %s", target_idx + 1, item_idx + 1, target)
                             continue

                         sync_item['targets'].append(final_target)
                     else:
                         # u'英文日志'
                         self.logger.warning("Skipping target #%d in item #%d due to missing 'dir', 'path', or 'branch': %s", target_idx + 1, item_idx + 1, target)

                # u'只有当 sync_item 有效的目标时才添加到最终配置'
                if sync_item['targets']:
                    self.config.append(sync_item)
                else:
                    self.logger.warning("Item #%d has no valid targets after processing, it will be skipped.", item_idx + 1)


            self.logger.info("Configuration loaded and parsed successfully. Found %d valid sync configurations.", len(self.config)) # u'英文日志'
            # self.logger.debug("Loaded configuration details: %s", self.config) # u'调试信息，可能非常长'

        except yaml.YAMLError as ye:
            mark = getattr(ye, 'problem_mark', None)
            # u'英文错误信息'
            error_msg = "Configuration format error (YAML syntax issue):\n"
            if mark:
                error_msg += "  Error near line %s, column %s\n" % (mark.line + 1, mark.column + 1)
            error_msg += "  Description: %s\n" % unicode(ye)
            error_msg += "Please check the YAML syntax in '%s'." % full_config_path
            self.logger.error(error_msg)
            sys.exit(1)
        except Exception as e:
            # u'英文错误信息'
            self.logger.error("An unexpected error occurred while loading or parsing the configuration file: %s", unicode(e))
            self.logger.error("Config file path: %s", full_config_path)
            self.logger.debug(traceback.format_exc())
            sys.exit(1)

    @retry_decorator(max_attempts=2, delay=3) # u'Git 操作通常不需要太多重试'
    def git_operations(self, directory, branch, remote_name):
        # u"""
        # u'在指定目录执行 Git 操作 (add, commit, push)。用于 option: true。
        # u':param directory: Git 仓库的根目录路径。
        # u':param branch: 要推送到的目标分支名。
        # u':param remote_name: 要推送到的远程仓库名称。
        # u':raises: Exception 如果 Git 命令执行失败。
        # u"""
        target_dir = self.normalize_path(directory)
        # u'英文日志'
        self.logger.info("Running Git operations in single repository [%s] (Branch: %s, Remote: %s)",
                       os.path.basename(target_dir), branch, remote_name)

        # u'检查是否是 Git 仓库'
        if not os.path.isdir(os.path.join(target_dir, '.git')):
            self.logger.warning("Directory [%s] is not a valid Git repository, skipping Git operations.", target_dir) # u'英文日志'
            return # u'不是错误，直接返回'

        commit_needed = True # u'假设需要提交'

        # 1. Git Add
        cmd_add = "git add ."
        ret_add, out_add, err_add = run_subprocess(cmd_add, cwd=target_dir)
        if ret_add != 0:
            error_msg = "Git add failed in [%s]:\nReturn Code: %d\nStderr: %s" % (target_dir, ret_add, err_add) # u'英文日志'
            self.logger.error(error_msg)
            raise Exception(error_msg)
        # self.logger.debug("Git add output:\n%s", out_add)

        # 2. Git Commit
        commit_message = "Automated sync commit %s - %s" % (os.path.basename(target_dir), time.strftime("%Y-%m-%d %H:%M:%S")) # u'英文提交信息'
        # u'更安全的引号处理 (适用于 POSIX shell)'
        safe_commit_message = commit_message.replace("'", "'\\''")
        cmd_commit = "git commit -m '%s'" % safe_commit_message # u'使用单引号通常更安全'

        ret_commit, out_commit, err_commit = run_subprocess(cmd_commit, cwd=target_dir)

        if ret_commit == 0:
            self.logger.info("Git commit successful in [%s]", os.path.basename(target_dir)) # u'英文日志'
            # self.logger.debug("Git commit output:\n%s", out_commit)
        elif ret_commit == 1 and (u"nothing to commit" in out_commit.lower() or
                                  u"no changes added to commit" in out_commit.lower() or
                                  u"nothing added to commit" in out_commit.lower()):
             self.logger.info("No changes detected to commit in [%s].", os.path.basename(target_dir)) # u'英文日志'
             commit_needed = False # u'无需推送'
        else:
            # u'其他提交错误'
            error_msg = "Git commit failed in [%s]:\nReturn Code: %d\nStdout: %s\nStderr: %s" % (target_dir, ret_commit, out_commit, err_commit) # u'英文日志'
            self.logger.error(error_msg)
            raise Exception(error_msg)

        # 3. Git Push (仅当 commit 发生时)
        if commit_needed:
            cmd_push = "git push %s HEAD:%s" % (remote_name, branch)
            ret_push, out_push, err_push = run_subprocess(cmd_push, cwd=target_dir)

            if ret_push != 0:
                # u'推送失败'
                error_msg = "Git push failed for [%s] (Branch: %s, Remote: %s):\nReturn Code: %d\nStdout: %s\nStderr: %s" % (target_dir, branch, remote_name, ret_push, out_push, err_push) # u'英文日志'
                self.logger.error(error_msg)
                # u'检查 non-fast-forward'
                if "non-fast-forward" in err_push.lower() or "! [rejected]" in err_push:
                     self.logger.warning("Push rejected for [%s], possibly due to remote updates on branch '%s'. Manual intervention required.", target_dir, branch) # u'英文日志'
                     # u'记录错误但不抛出异常，允许脚本继续处理其他仓库？取决于需求'
                     self.errors.append("Git push rejected (non-fast-forward): Repo=%s, Branch=%s" % (os.path.basename(target_dir), branch))
                     # return # u'如果需要中断此仓库处理'
                     raise Exception(error_msg) # u'或者让 retry 处理'
                else:
                    raise Exception(error_msg) # u'其他推送错误'
            else:
                self.logger.info("Git push successful for [%s] (Branch: %s, Remote: %s)", os.path.basename(target_dir), branch, remote_name) # u'英文日志'
                # self.logger.debug("Git push output:\n%s", out_push)
        else:
             self.logger.info("Skipping Git push for [%s] as there were no new commits.", os.path.basename(target_dir)) # u'英文日志'

        self.logger.info("Git operations completed for single repository [%s].", os.path.basename(target_dir)) # u'英文日志'

    @retry_decorator(max_attempts=3, delay=5)
    def local_rsync(self, source, target):
        # u"""
        # u'使用 rsync 同步本地目录。
        # u':param source: 源目录路径。
        # u':param target: 目标目录路径。
        # u':return: 目标路径 (如果成功)。
        # u':raises: Exception 如果 rsync 命令失败。
        # u"""
        norm_source = self.normalize_path(source)
        norm_target = self.normalize_path(target)

        if not norm_source or not os.path.isdir(norm_source):
            msg = "Rsync source path is not a valid directory or does not exist: %s" % source # u'英文日志'
            self.logger.error(msg)
            raise Exception(msg)
        if not norm_target:
            msg = "Rsync target path is invalid: %s" % target # u'英文日志'
            self.logger.error(msg)
            raise Exception(msg)

        # u'确保目标父目录存在'
        target_parent_dir = os.path.dirname(norm_target)
        if not os.path.exists(target_parent_dir):
            try:
                self.logger.info("Target parent directory does not exist, creating: %s", target_parent_dir) # u'英文日志'
                os.makedirs(target_parent_dir)
            except OSError as e:
                msg = "Failed to create target parent directory %s: %s" % (target_parent_dir, e) # u'英文日志'
                self.logger.error(msg)
                raise Exception(msg)

        # u'英文日志'
        self.logger.info("Starting rsync: [%s] -> [%s]", os.path.basename(norm_source), os.path.basename(norm_target))
        # u'确保源路径以 / 结尾，以便 rsync 复制内容而不是目录本身'
        source_with_slash = norm_source.rstrip('/') + '/'
        # u'使用更安全的引号处理 (针对路径中的空格等)'
        # u'注意：如果路径可能包含单引号本身，需要更复杂的处理'
        rsync_cmd = "rsync -avrcuz --exclude='.repo' --exclude='.git*' '%s' '%s'" % (
            source_with_slash.replace("'", "'\\''"),
            norm_target.replace("'", "'\\''")
        )

        status, output, error = run_subprocess(rsync_cmd)

        if status != 0:
            # u'英文日志'
            self.logger.error("Rsync command failed! Return code: %d", status)
            error_details = error if error else output # u'优先记录 stderr'
            self.logger.error("Rsync output/error:\n%s", error_details)
            err_summary = error_details.strip().splitlines()[-1] if error_details.strip() else "Unknown error" # u'取最后一行作摘要'
            err_msg = "Rsync failed [%s -> %s]: %s" % (os.path.basename(norm_source), os.path.basename(norm_target), err_summary)
            self.errors.append(err_msg)
            raise Exception("Rsync sync failed (Code %d): %s" % (status, err_summary)) # u'英文异常消息'
        else:
            # u'尝试解析摘要信息 (英文)'
            def parse_rsync_summary(out_str):
                 lines = out_str.splitlines()
                 summary = {'sent': 0, 'received': 0, 'rate': 0.0, 'size': 0, 'speedup': 0.0}
                 try:
                     for line in lines[-3:]: # u'通常在最后几行'
                          if "sent" in line and "received" in line and "bytes/sec" in line:
                              m = re.search(r"sent ([\d,]+) bytes\s+received ([\d,]+) bytes\s+([\d,.]+) bytes/sec", line)
                              if m:
                                  summary['sent'] = int(m.group(1).replace(",", ""))
                                  summary['received'] = int(m.group(2).replace(",", ""))
                                  # summary['rate'] = float(m.group(3).replace(",", "")) # 'rate' is actually transfer rate, not total bytes/sec usually
                          elif "total size" in line and "speedup" in line:
                              m = re.search(r"total size is ([\d,]+)\s+speedup is ([\d,.]+)", line)
                              if m:
                                  summary['size'] = int(m.group(1).replace(",", ""))
                                  # summary['speedup'] = float(m.group(2).replace(",", ""))
                 except Exception as parse_e:
                     logging.warning("Could not parse rsync summary: %s", parse_e)
                 return summary

            summary_data = parse_rsync_summary(output)
            # u'英文概要日志'
            log_summary = ""
            if summary_data['size'] > 0 or summary_data['sent'] > 0:
                 log_summary = " (Sent: {:.1f}KB, Total Size: {:.1f}MB)".format(
                     summary_data['sent'] / 1024.0,
                     summary_data['size'] / (1024.0 * 1024.0)
                 )
            self.logger.info("Rsync succeeded: [%s] -> [%s]%s", os.path.basename(norm_source), os.path.basename(norm_target), log_summary)
            return norm_target

    def normalize_path(self, path):
        # u"""
        # u'规范化路径: 转为绝对路径，处理 '..', 基于脚本目录。
        # u':param path: 输入路径字符串。
        # u':return: 规范化的绝对路径，如果输入无效则返回 None。
        # u"""
        if not path or not isinstance(path, basestring): # u'Python 2 使用 basestring'
            # self.logger.warning("Invalid path provided for normalization: %s", path) # u'可能日志过多'
            return None
        try:
            if os.path.isabs(path):
                full_path = os.path.normpath(path)
            else:
                full_path = os.path.normpath(os.path.join(self.script_dir, path))
            # self.logger.debug("Normalized path '%s' to '%s'", path, full_path)
            return full_path
        except Exception as e:
            self.logger.error("Error normalizing path '%s': %s", path, e)
            return None


    def find_git_repos(self, target_dir):
        # u"""
        # u'查找目标目录及其子目录下的所有 Git 仓库 (.git 目录)。用于 option: true。
        # u':param target_dir: 要搜索的起始目录路径。
        # u':return: 包含所有找到的 Git 仓库根目录路径的列表。
        # u"""
        git_repos = []
        search_root = self.normalize_path(target_dir)
        if not search_root:
             self.logger.warning("Invalid directory provided to find_git_repos: %s", target_dir) # u'英文日志'
             return git_repos

        self.logger.info("Searching for Git repositories under [%s] (for option:true mode)...", search_root) # u'英文日志'

        if not os.path.isdir(search_root):
            self.logger.error("Search directory does not exist or is not a directory: %s", search_root) # u'英文日志'
            return git_repos

        for root, dirs, files in os.walk(search_root, topdown=True):
            if '.git' in dirs:
                git_dir_path = os.path.join(root, '.git')
                if os.path.isdir(git_dir_path): # u'确保是目录，而不是文件'
                    repo_path = root
                    self.logger.info("Found Git repository: %s", repo_path) # u'英文日志'
                    git_repos.append(repo_path)
                    # u'从 dirs 移除 .git 防止进入 .git 内部或重复计算子模块'
                    dirs.remove('.git')
            # u'从 dirs 移除 .repo 防止进入 .repo 内部 (如果存在)'
            if '.repo' in dirs:
                dirs.remove('.repo')


        if not git_repos:
            self.logger.warning("No Git repositories found under directory [%s].", search_root) # u'英文日志'
        else:
            self.logger.info("Search complete. Found %d Git repositories under [%s].", len(git_repos), search_root) # u'英文日志'

        return git_repos

    @retry_decorator(max_attempts=2, delay=10) # u'Repo 操作失败可能需要较长间隔重试'
    def repo_operations(self, repo_dir, branch, remote_name):
        # u"""
        # u'在 Repo 工作区根目录执行 'repo forall' 命令。用于 option: false。
        # u':param repo_dir: repo 工作区的根目录路径。
        # u':param branch: 要推送到的目标分支名。
        # u':param remote_name: 要推送到的远程仓库名称。
        # u':raises: Exception 如果 repo 命令或环境检查失败。
        # u"""
        target_rel_path = os.path.basename(repo_dir) # u'使用目录名作为标识'
        # u'英文日志'
        self.logger.info("Running Repo operations in workspace [%s] (Branch: %s, Remote: %s)",
                       target_rel_path, branch, remote_name)

        # u'加锁确保 repo 命令串行执行 (防止多个 sync 进程冲突)'
        with self.repo_lock:
            self.logger.debug("Acquired repo lock for workspace [%s]", target_rel_path)
            try:
                # u'检查是否是有效的 repo 工作区'
                if not os.path.isdir(os.path.join(repo_dir, '.repo')):
                     msg = "Target directory [%s] is not a valid Repo workspace (missing .repo directory)." % repo_dir # u'英文日志'
                     self.logger.error(msg)
                     self.errors.append("Repo operations failed: Invalid workspace [%s]" % target_rel_path) # u'英文错误'
                     raise Exception(msg)

                # u'构建 repo forall 命令'
                commit_message = "Automated sync commit %s - %s" % (target_rel_path, time.strftime("%Y-%m-%d %H:%M:%S")) # u'英文提交信息'
                # u'安全处理引号'
                safe_commit_message = commit_message.replace("'", "'\\''")
                # u'从配置获取 remote_name 和 branch'
                # u'使用 -j 控制并行度，可以适当调整'
                repo_jobs = max(1, self.max_workers / 2) # u'示例：分配一半 worker'
                # repo_jobs = 16 # u'或者固定一个值'

                # u'构建命令，确保先 add 成功再 commit，最后 push'
                # u'注意: 如果某个子仓库 git commit 失败 (非"nothing to commit")，可能不会阻止后续 push 尝试？'
                # u'更安全的做法可能是分步执行，但这会显著增加时间'
                repo_cmd_parts = [
                    "git add .",
                    # u'尝试 commit，忽略 "nothing to commit" 错误'
                    "git commit -m '%s' || case $? in 1) exit 0;; *) exit $?;; esac" % safe_commit_message,
                    # u'如果前面成功，则 push'
                    "git push %s HEAD:%s" % (remote_name, branch)
                ]
                repo_cmd = "repo forall  -c '%s'" % ( " && ".join(repo_cmd_parts))

                self.logger.info("Executing Repo command (Parallelism: %d) in [%s]...", repo_jobs, target_rel_path) # u'英文日志'
                self.logger.debug("Repo command details: %s", repo_cmd)

                # u'执行 repo 命令'
                status, output, error = run_subprocess(repo_cmd, cwd=repo_dir)

                # u'检查 repo forall 的状态和错误输出'
                # u'repo forall 即使部分子项目失败也可能返回 0，需要检查 stderr'
                failed_projects_stderr = [line for line in error.splitlines() if re.search(r'(error:|fatal:|fail|unable|rejected)', line, re.IGNORECASE)]
                failed_projects_stdout = [line for line in output.splitlines() if re.search(r'\bfail\b', line, re.IGNORECASE)] # u'有时失败信息在 stdout'

                if status != 0 or failed_projects_stderr or failed_projects_stdout:
                    # u'提取错误摘要'
                    error_summary_lines = failed_projects_stderr[-5:] + failed_projects_stdout[-5:] # u'取最后几条错误行
                    error_summary = "\n".join(error_summary_lines)
                    if not error_summary:
                         # u'如果没匹配到特定关键字，取 stderr 最后几行'
                         stderr_lines = error.strip().splitlines()
                         error_summary = "\n".join(stderr_lines[-5:])

                    error_msg = "Repo forall command failed or errors detected in workspace [%s]! Return Code: %d.\nError Summary:\n%s" % (target_rel_path, status, error_summary) # u'英文日志'
                    self.logger.error(error_msg)
                    self.errors.append("Repo operations failed [%s]: %s" % (target_rel_path, error_summary.replace('\n', ' '))) # u'英文错误'
                    raise Exception("Repo operations failed, check logs for details.") # u'英文异常'
                else:
                    self.logger.info("Repo forall command completed successfully in workspace [%s].", target_rel_path) # u'英文日志'

            except Exception as e:
                 # u'捕获并记录在 repo 操作期间的异常'
                 self.logger.error("Exception during Repo operations in workspace [%s]: %s", target_rel_path, unicode(e)) # u'英文日志'
                 if unicode(e) not in unicode(self.errors[-5:]): # u'避免重复记录相同错误'
                     self.errors.append("Repo operation exception [%s]: %s" % (target_rel_path, unicode(e)))
                 raise # u'重新抛出异常，以便 retry 机制可以捕获'
            finally:
                 self.logger.debug("Released repo lock for workspace [%s]", target_rel_path)
                 # u'锁在 with 语句结束时自动释放'

    # u'get_repo_size 保持不变，但注释掉调用，除非需要'
    def get_repo_size(self, repo_path):
        # u"""获取目录大小 (MB)"""
        try:
            norm_path = self.normalize_path(repo_path)
            if not os.path.exists(norm_path): return 0
            size_cmd = "du -sm '%s'" % norm_path.replace("'", "'\\''")
            status, output, error = run_subprocess(size_cmd)
            if status == 0 and output:
                 parts = output.split()
                 if parts and parts[0].isdigit(): return int(parts[0])
                 else: logging.warning("Could not parse size from 'du' output: %s", output.strip()); return 0
            else: logging.warning("Failed to get directory size for [%s]. Error: %s", norm_path, error.strip()); return 0
        except Exception as e: logging.error("Exception getting directory size for [%s]: %s", repo_path, unicode(e)); return 0

    def _execute_sync_tasks(self):
        # u"""
        # u'执行完整的同步流程：
        # u'1. 并行执行所有 rsync 任务。
        # u'2. 串行执行后续的版本库操作 (Repo 或 Git)，基于成功的 rsync 任务。
        # u'这是 'sync' 模式的实现。
        # u"""
        mode_description = "Full sync (rsync + version control)" # u'模式描述 (英文)'
        self.logger.info("Starting sync process (%s)...", mode_description) # u'英文日志'
        start_time = time.time()
        processed_targets = [] # u'存储成功完成 rsync 的目标信息 (完整 target_info)'

        # --- 阶段一: 并行执行 Rsync ---
        self.logger.info("Phase 1: Starting parallel Rsync tasks...") # u'英文日志'
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures_map = {} # {future: (target_info, source)}
                for item_idx, sync_item in enumerate(self.config):
                    sources = sync_item.get('sources', [])
                    targets = sync_item.get('targets', [])
                    item_id = sync_item.get('item_index', item_idx + 1) # u'获取用于日志的索引'

                    for target_idx, target_info in enumerate(targets):
                         # u'确定此目标的源路径'
                         source = None
                         if len(sources) == 1: source = sources[0]
                         elif len(sources) > target_idx: source = sources[target_idx] # u'假设 sources 和 targets 一一对应'

                         if not source:
                             self.logger.warning("Cannot determine source for target #%d in item #%d, skipping target: %s",
                                                 target_idx + 1, item_id, target_info.get('path', 'N/A')) # u'英文日志'
                             continue

                         target_path_for_log = target_info.get('path', u'Unknown path')
                         source_basename = os.path.basename(source) if source else 'N/A'
                         self.logger.info("Submitting Rsync task: [%s] -> [%s]", source_basename, target_path_for_log) # u'英文日志'
                         future = executor.submit(self.local_rsync, source, target_info['full_target_path'])
                         futures_map[future] = (target_info, source)

                self.logger.info("All (%d) Rsync tasks submitted, waiting for completion...", len(futures_map)) # u'英文日志'
                completed_count = 0
                for future in futures_map: # u'Python 2 中 futures map 迭代顺序不保证完成顺序'
                     target_info, source = futures_map[future]
                     source_basename = os.path.basename(source) if source else 'N/A'
                     target_path_for_log = target_info.get('path', u'Unknown path')
                     try:
                         # u'使用 future.result() 获取结果或异常'
                         result = future.result(timeout=3600) # u'增加超时 (例如1小时) 以防 rsync 卡死'
                         if result: # u'local_rsync 成功时返回目标路径'
                             self.logger.info("Rsync task completed successfully: [%s] -> [%s]", source_basename, target_path_for_log) # u'英文日志'
                             processed_targets.append(target_info) # u'记录成功的目标信息'
                         # else: # u'理论上 result 不应为 None 或 False，除非 local_rsync 内部逻辑改变'
                         #    self.logger.warning("Rsync task for [%s] -> [%s] returned unexpected result: %s", source_basename, target_path_for_log, result)

                     except Exception as e:
                         # u'捕获 rsync 任务执行中的异常 (包括超时)'
                         self.logger.error("Rsync task FAILED: [%s] -> [%s]. Error: %s", source_basename, target_path_for_log, unicode(e)) # u'英文日志'
                         # u'错误已由 local_rsync 或 retry_decorator 记录到 self.errors'
                     finally:
                          completed_count += 1
                          self.logger.debug("Rsync task %d/%d processed.", completed_count, len(futures_map))


        except Exception as e:
             # u'捕获线程池或任务提交阶段的意外错误'
             self.logger.error("An unexpected error occurred during the Rsync phase: %s", unicode(e)) # u'英文日志'
             self.logger.debug(traceback.format_exc())
             self.logger.error("Aborting subsequent version control operations due to errors in Rsync phase.") # u'英文日志'
             self._log_summary()
             return # u'中止执行'

        rsync_duration = time.time() - start_time
        self.logger.info("Phase 1 (Rsync) finished. Duration: %.2f seconds.", rsync_duration) # u'英文日志'

        if not processed_targets:
            self.logger.warning("No Rsync tasks completed successfully. Skipping version control phase.") # u'英文日志'
            self._log_summary()
            return

        # --- 阶段二: 串行执行版本库操作 (Repo 或 Git) ---
        self.logger.info("Phase 2: Starting serial version control operations for %d successfully synced targets...", len(processed_targets)) # u'英文日志'
        repo_git_start_time = time.time()
        for i, target_info in enumerate(processed_targets):
            option = target_info.get('option', False) # u'获取该目标的 option'
            repo_dir = target_info.get('repo_dir')    # u'用于 option=false'
            target_path = target_info.get('full_target_path') # u'用于 option=true'
            branch = target_info.get('branch')
            remote_name = target_info.get('remote_name', DEFAULT_REMOTE_NAME) # u'获取配置的远程名'
            target_rel_path = target_info.get('path') # u'用于日志'
            item_id = target_info.get('item_index', 'N/A') # u'获取父配置项索引'

            log_prefix = "[VC Task %d/%d]" % (i + 1, len(processed_targets)) # u'VC = Version Control'

            self.logger.info("%s Processing target: [%s] (from item #%s)", log_prefix, target_rel_path, item_id )

            # u'检查必要信息'
            if not branch or not remote_name or not target_rel_path or (not option and not repo_dir) or (option and not target_path):
                 self.logger.warning("%s Skipping version control for target [%s]: Incomplete configuration (Branch/Remote/Path missing?).", log_prefix, target_rel_path) # u'英文日志'
                 continue

            # --- 根据 option 选择操作 ---
            if option:
                # u'Option: true -> 查找并处理单个 Git 仓库'
                self.logger.info("%s Option=True: Finding and processing individual Git repositories under [%s] (Branch: %s, Remote: %s)",
                               log_prefix, target_path, branch, remote_name) # u'英文日志'
                try:
                    found_repos = self.find_git_repos(target_path)
                    if not found_repos:
                        self.logger.warning("%s No Git repositories found under [%s]. Skipping Git operations for this target.", log_prefix, target_path) # u'英文日志'
                        continue

                    # u'串行处理找到的每个仓库'
                    success_count = 0
                    fail_count = 0
                    self.logger.info("%s Found %d Git repositories to process.", log_prefix, len(found_repos))
                    for repo_idx, repo_path in enumerate(found_repos):
                        repo_log_prefix = "%s Git Repo %d/%d" % (log_prefix, repo_idx + 1, len(found_repos))
                        try:
                            # u'调用单个 git 操作函数，传入 remote_name'
                            self.git_operations(repo_path, branch, remote_name)
                            success_count += 1
                        except Exception as git_e:
                             # u'git_operations 内部会记录错误和日志'
                             self.logger.error("%s FAILED processing repository [%s]. See previous logs.", repo_log_prefix, os.path.basename(repo_path)) # u'英文日志'
                             fail_count += 1
                             # u'选择继续处理下一个仓库'
                             continue
                    self.logger.info("%s Finished processing Git repositories under [%s]: %d succeeded, %d failed.", log_prefix, target_path, success_count, fail_count) # u'英文日志'

                except Exception as find_e:
                     # u'find_git_repos 本身出错'
                     self.logger.error("%s Error finding Git repositories under [%s]: %s", log_prefix, target_path, unicode(find_e)) # u'英文日志'
                     self.errors.append("Failed to find Git repositories for [%s]: %s" % (target_rel_path, unicode(find_e)))
                     continue # u'处理下一个目标'

            else:
                # u'Option: false -> 执行 Repo 操作'
                self.logger.info("%s Option=False: Running 'repo forall' in workspace [%s] (Branch: %s, Remote: %s)",
                               log_prefix, os.path.basename(repo_dir), branch, remote_name) # u'英文日志'
                try:
                    # u'调用 repo 操作函数，传入 remote_name'
                    self.repo_operations(repo_dir, branch, remote_name)
                except Exception as repo_e:
                     # u'repo_operations 内部会记录错误和日志'
                     self.logger.error("%s FAILED running 'repo forall' in workspace [%s]. See previous logs.", log_prefix, os.path.basename(repo_dir)) # u'英文日志'
                     # u'继续处理下一个目标'
                     continue # u'处理下一个目标'

        repo_git_duration = time.time() - repo_git_start_time
        total_duration = time.time() - start_time
        self.logger.info("Phase 2 (Version Control) finished. Duration: %.2f seconds.", repo_git_duration) # u'英文日志'
        self.logger.info("Sync process (%s) finished. Total duration: %.2f seconds.", mode_description, total_duration) # u'英文日志'
        self._log_summary() # u'打印最终摘要'


    def execute_repo_only(self):
        # u"""
        # u'仅执行版本库操作 (Repo 或 Git)，跳过 rsync。
        # u'基于配置文件中的所有 targets 信息，串行执行。
        # u'这是 'repo' 模式的实现。
        # u"""
        mode_description = "Version control only" # u'模式描述 (英文)'
        self.logger.info("Starting process (%s)...", mode_description) # u'英文日志'
        start_time = time.time()
        tasks_to_run = []

        # u'从配置中提取所有需要执行版本库操作的目标'
        for item_idx, sync_item in enumerate(self.config):
             item_id = sync_item.get('item_index', item_idx + 1)
             for target_info in sync_item.get('targets', []):
                  # u'添加 item_id 到 target_info 以便追踪'
                  target_info['item_index'] = item_id
                  tasks_to_run.append(target_info)

        if not tasks_to_run:
            self.logger.warning("No targets found in configuration for version control operations.") # u'英文日志'
            return

        self.logger.info("Found %d targets configured for version control operations.", len(tasks_to_run)) # u'英文日志'

        # u'串行执行 Repo 或 Git 操作'
        for i, target_info in enumerate(tasks_to_run):
            option = target_info.get('option', False)
            repo_dir = target_info.get('repo_dir')
            target_path = target_info.get('full_target_path') # u'仅用于 option=true'
            branch = target_info.get('branch')
            remote_name = target_info.get('remote_name', DEFAULT_REMOTE_NAME)
            target_rel_path = target_info.get('path')
            item_id = target_info.get('item_index', 'N/A')

            log_prefix = "[VC Task %d/%d]" % (i + 1, len(tasks_to_run))

            self.logger.info("%s Processing target: [%s] (from item #%s)", log_prefix, target_rel_path, item_id )

            # u'检查必要信息'
            if not branch or not remote_name or not target_rel_path or (not option and not repo_dir) or (option and not target_path):
                 self.logger.warning("%s Skipping version control for target [%s]: Incomplete configuration.", log_prefix, target_rel_path) # u'英文日志'
                 continue

            # --- 根据 option 选择操作 ---
            if option:
                # u'Option: true -> 查找并处理单个 Git 仓库'
                self.logger.info("%s Option=True: Finding and processing individual Git repositories under [%s] (Branch: %s, Remote: %s)",
                               log_prefix, target_path, branch, remote_name) # u'英文日志'
                try:
                    found_repos = self.find_git_repos(target_path)
                    if not found_repos:
                        self.logger.warning("%s No Git repositories found under [%s]. Skipping.", log_prefix, target_path) # u'英文日志'
                        continue
                    success_count = 0
                    fail_count = 0
                    self.logger.info("%s Found %d Git repositories to process.", log_prefix, len(found_repos))
                    for repo_idx, repo_path in enumerate(found_repos):
                        repo_log_prefix = "%s Git Repo %d/%d" % (log_prefix, repo_idx + 1, len(found_repos))
                        try:
                            self.git_operations(repo_path, branch, remote_name)
                            success_count += 1
                        except Exception as git_e:
                             self.logger.error("%s FAILED processing repository [%s]. See previous logs.", repo_log_prefix, os.path.basename(repo_path)) # u'英文日志'
                             fail_count += 1
                             continue
                    self.logger.info("%s Finished processing Git repositories under [%s]: %d succeeded, %d failed.", log_prefix, target_path, success_count, fail_count) # u'英文日志'
                except Exception as find_e:
                     self.logger.error("%s Error finding Git repositories under [%s]: %s", log_prefix, target_path, unicode(find_e)) # u'英文日志'
                     self.errors.append("Failed to find Git repositories for [%s]: %s" % (target_rel_path, unicode(find_e)))
                     continue
            else:
                # u'Option: false -> 执行 Repo 操作'
                self.logger.info("%s Option=False: Running 'repo forall' in workspace [%s] (Branch: %s, Remote: %s)",
                               log_prefix, os.path.basename(repo_dir), branch, remote_name) # u'英文日志'
                try:
                    self.repo_operations(repo_dir, branch, remote_name)
                except Exception as repo_e:
                     self.logger.error("%s FAILED running 'repo forall' in workspace [%s]. See previous logs.", log_prefix, os.path.basename(repo_dir)) # u'英文日志'
                     continue

        total_duration = time.time() - start_time
        self.logger.info("Process (%s) finished. Total duration: %.2f seconds.", mode_description, total_duration) # u'英文日志'
        self._log_summary() # u'打印执行摘要'

    def _log_summary(self):
        # u"""在脚本结束时打印错误摘要 (英文)。"""
        if self.errors:
             summary_title = " Execution Summary: Errors Detected "
             self.logger.warning("="*25 + summary_title + "="*25) # u'英文标题'
             self.logger.warning("Found %d error(s)/warning(s) during execution:", len(self.errors)) # u'英文摘要'
             for i, err in enumerate(self.errors):
                 # u'限制错误消息长度，避免过长'
                 err_display = (err[:300] + u'...') if len(err) > 300 else err
                 self.logger.warning("  [%d]: %s", i + 1, err_display)
             self.logger.warning("="*(50 + len(summary_title)))
        else:
             summary_title = " Execution Summary: All tasks completed successfully "
             self.logger.info("="*15 + summary_title + "="*15) # u'英文标题'


def main():
    # u'使用 ArgumentParser 解析命令行参数'
    # u'英文描述'
    parser = argparse.ArgumentParser(
        description='Code synchronization and Repo/Git management tool (Python 2.7 compatible).',
        formatter_class=argparse.RawTextHelpFormatter # u'保留 help 文本中的换行'
    )

    # u'添加 --config 参数 (英文 help)'
    parser.add_argument('--config', default=DEFAULT_CONFIG_FILE,
                      help='Path to the configuration file (default: %s in script directory)' % DEFAULT_CONFIG_FILE)

    # u'添加 --log 参数 (英文 help)'
    parser.add_argument('--log', default=DEFAULT_LOG_FILE,
                      help='Path to the log file (default: %s in script directory)' % DEFAULT_LOG_FILE)


    # u'添加 --mode 参数 (必选), 更新模式和描述 (英文 help)'
    parser.add_argument('--mode', choices=['sync', 'repo'], required=True,
                      help='Select operation mode:\n'
                           'sync: Perform rsync, then run repo/git operations based on config.\n'
                           'repo: Perform ONLY repo/git operations based on config (skip rsync).'
                      )

    # u'解析参数'
    args = parser.parse_args()

    # u'实例化 SyncManager'
    try:
        # u'传入日志路径'
        sync_manager = SyncManager(config_path=args.config, log_path=args.log)
    except SystemExit:
         # u'初始化失败，错误信息已由 SyncManager 打印'
         sys.exit(1)
    except Exception as e:
         # u'捕获其他初始化期间的严重错误 (英文)'
         print >> sys.stderr, "Fatal error during SyncManager initialization: %s" % unicode(e)
         print >> sys.stderr, traceback.format_exc()
         sys.exit(1)

    # u'根据新模式执行相应操作'
    try:
        if args.mode == 'sync':
            # u'原 rsync/all 模式的功能'
            sync_manager._execute_sync_tasks()
        elif args.mode == 'repo':
            # u'原 repo 模式的功能'
            sync_manager.execute_repo_only()

    except KeyboardInterrupt:
          sync_manager.logger.warning("Received interrupt signal, attempting to stop...") # u'英文日志'
          # u'可以添加清理逻辑'
          sync_manager._log_summary() # u'打印已发生的错误'
          sys.exit(130) # u'Ctrl+C 的标准退出码'
    except Exception as e:
         # u'捕获主执行流程中的未处理错误'
         sync_manager.logger.error("An unhandled critical error occurred during script execution: %s", unicode(e)) # u'英文日志'
         sync_manager.logger.error("Please check the log file for detailed information.") # u'英文日志'
         sync_manager.logger.debug(traceback.format_exc())
         sync_manager._log_summary()
         sys.exit(1)

    # u'根据错误状态决定退出码'
    if sync_manager.errors:
        sync_manager.logger.warning("Script finished with errors.") # u'英文日志'
        sys.exit(1)
    else:
        sync_manager.logger.info("Script finished successfully.") # u'英文日志'
        sys.exit(0)

if __name__ == "__main__":
    # u'设置系统默认编码为 UTF-8 (对 Python 2 很重要)'
    # u'如果环境不允许或导致问题，可以注释掉'
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    except NameError: # u'reload 在 Python 3 中不存在'
        pass
    except Exception as e:
         # u'英文警告'
         print >> sys.stderr, "Warning: Failed to set default encoding to utf-8: %s" % e

    main()