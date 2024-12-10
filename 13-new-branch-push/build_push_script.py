# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import yaml
import argparse
'''
# 默认推送分支（从 YAML 解析）
python script.py


# 指定分支名推送
python script.py new_branch_name


# 删除分支
python script.py branch_to_delete --delete

'''
def validate_build_yaml():
    """验证 build.yaml 文件的完整性和正确性"""
    yaml_path = 'build.yaml'
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # 定义必须存在的键
        required_keys = [
            ('project', 'model', 'internal'),
            ('project', 'model', 'external'),
            ('project', 'chip', 'platform'),
            ('project', 'version', 'android'),
            ('project', 'date'),
            ('project', 'baseline')
        ]
            
        # 检查所有必需的键
        for key_path in required_keys:
            current = config
            for key in key_path:
                if key not in current:
                    print("缺少必需的配置键: {}".format(' -> '.join(key_path)))
                    return False
                current = current[key]
            
        return True
    except Exception as e:
        print("验证 build.yaml 时发生错误: {}".format(str(e)))
        return False
def get_repo_root_path_from_yaml(yaml_path='build.yaml'):
    """
    从YAML文件中获取repo根目录路径
    
    Args:
        yaml_path (str): YAML文件路径
    
    Returns:
        str: repo根目录路径
    """
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        # 从project中获取repo根目录路径
        repo_root_path = ''
        if isinstance(config, dict):
            repo_root_path = config.get('project', {}).get('repo_root_path', '')
        
        # 如果yaml中未指定路径，则使用当前脚本所在目录的父目录
        if not repo_root_path:
            # 获取当前脚本所在目录的父目录
            repo_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 转换为绝对路径
        repo_root_path = os.path.abspath(repo_root_path)
        
        # 验证是否是一个有效的repo根目录
        if not os.path.exists(os.path.join(repo_root_path, '.repo')):
            print("警告：{} 不是一个有效的repo根目录".format(repo_root_path))
            return None
        
        return repo_root_path
    
    except Exception as e:
        print("读取repo根目录路径失败: {}".format(e))
        return None
    
def safe_str(value):
    """确保值被转换为字符串"""
    if value is None:
        return ''
    # 如果是集合类型，取第一个元素
    if isinstance(value, set):
        return str(list(value)[0]) if value else ''
    # 去除多余的引号
    if isinstance(value, basestring):
        return value.strip('"\'')
    return str(value)

def parse_build_yaml():
    """解析 build.yaml 文件并生成分支名"""
    yaml_path = 'build.yaml'
    if not os.path.exists(yaml_path):
        return None, None, None
    try:
        with open(yaml_path, 'r') as f:
            # 使用 SafeLoader 来加载 YAML
            config = yaml.load(f, Loader=yaml.SafeLoader)
        
        # 从配置中获取值
        project_config = config.get('project', {})
        model_config = project_config.get('model', {})
        
        # 直接获取外部型号
        model_ext = model_config.get('external', '')
        if isinstance(model_ext, (str, unicode)):
            model_ext = model_ext.strip('"\'')
        elif isinstance(model_ext, set):
            model_ext = list(model_ext)[0] if model_ext else ''
        
        # 生成分支名组件
        branch_components = [
            safe_str(model_config.get('internal', '')),
            safe_str(model_ext),
            safe_str(project_config.get('chip', {}).get('platform', '')),
            safe_str(project_config.get('version', {}).get('android', '')),
            safe_str(project_config.get('date', ''))
        ]
        
        # 移除空字符串
        branch_components = [comp for comp in branch_components if comp]
        
        # 生成分支名
        branch_name = "_".join(branch_components)
        
        # 获取 baseline
        baseline = safe_str(project_config.get('baseline', 'default_baseline'))
        
        # 调试输出
        print("解析的分支名组件: {}".format(branch_components))
        print("生成的分支名: {}".format(branch_name))
        print("基线: {}".format(baseline))
        print("Model External: {}".format(model_ext))
        
        return branch_name, baseline, model_ext
    except Exception as e:
        import traceback
        print("解析 build.yaml 出错: {}".format(str(e)))
        print("详细错误信息:")
        traceback.print_exc()
        return None, None, None

def create_repo_guide(branch_name, baseline, model_ext):
    """生成 repo 使用指导文档"""
    if not branch_name or not baseline:
        print("无法生成 repo 指导文档：分支名或基线为空")
        return False

    guide_content = """Repo 初始化和同步指导
1. 初始化仓库:
repo init -u ssh://username@192.168.117.71:29418/{baseline}/platform/manifest.git \\
-b {branch_name} -m {model_ext}.xml \\
--repo-url=ssh://username@192.168.117.71:29418/repo.git \\
--repo-branch=caf-stable

2. 同步代码:
repo sync

3. 创建开发分支:
repo start {branch_name} --all
""".format(
        baseline=baseline,
        branch_name=branch_name,
        model_ext=model_ext  
    )
    
    try:
        with open('repo_guide.txt', 'w') as f:
            f.write(guide_content)
        print("已生成 repo_guide.txt")
        return True
    except Exception as e:
        print("生成 repo_guide.txt 失败: {}".format(str(e)))
        return False

def get_remote_name(repo_path):
    output = subprocess.check_output(['git', '-C', repo_path, 'remote', '-v'])
    lines = output.split('\n')
    remote_name = lines[0].split('\t')[0]
    return remote_name

def push_with_retry(repo_path, branch_name, delete=False):
    """
    推送或删除分支，包含重试逻辑和错误处理
    :param repo_path: 仓库路径
    :param branch_name: 分支名称
    :param delete: 是否为删除操作
    :return: (success, skip)
    """
    success = False
    skip = False
    remote_name = get_remote_name(repo_path)
    
    while not success and not skip:
        try:
            if delete:
                # 首先检查远程分支是否存在
                try:
                    subprocess.check_output(
                        ['git', '-C', repo_path, 'ls-remote', '--heads', remote_name, branch_name],
                        stderr=subprocess.STDOUT
                    )
                except subprocess.CalledProcessError:
                    print('Branch %s does not exist in %s, skipping...' % (branch_name, repo_path))
                    return True, True  # 将不存在的分支视为成功处理，并标记为跳过

                # 如果分支存在，执行删除
                output = subprocess.check_output(
                    ['git', '-C', repo_path, 'push', remote_name, '--delete', branch_name],
                    stderr=subprocess.STDOUT
                )
                print('Successfully deleted branch %s from %s in %s' % (branch_name, remote_name, repo_path))
            else:
                output = subprocess.check_output(
                    ['git', '-C', repo_path, 'push', remote_name, 'HEAD:refs/heads/%s' % branch_name],
                    stderr=subprocess.STDOUT
                )
                print('Successfully pushed %s to %s in %s' % (branch_name, remote_name, repo_path))
            success = True
        except subprocess.CalledProcessError as e:
            error_message = e.output
            if delete and 'remote ref does not exist' in error_message:
                print('Branch %s does not exist in %s, skipping...' % (branch_name, repo_path))
                return True, True
            elif 'Could not read from remote repository' in error_message or 'incorrect signature' in error_message:
                print('Retry operation due to error in %s: %s' % (repo_path, error_message))
                continue
            else:
                print('Operation failed in %s with error: %s' % (repo_path, error_message))
                return False, False
    
    return success, False

def main():
    # 参数解析
    parser = argparse.ArgumentParser(description='Repo 分支管理工具')
    parser.add_argument('branch', nargs='?', help='分支名（可选）')
    parser.add_argument('--delete', action='store_true', help='删除分支')
    parser.add_argument('--push', action='store_true', help='推送分支')
    args = parser.parse_args()
    # 验证操作的唯一性
    operation_count = sum([args.delete, args.push])
    if operation_count > 1:
        print("错误：不能同时使用 --delete 和 --push")
        sys.exit(1)
    # 验证 YAML 配置
    if not validate_build_yaml():
        print("build.yaml 配置不完整或不正确")
        sys.exit(1)
        # 确定分支名
    if not args.branch:
        new_branch, baseline, model_ext = parse_build_yaml()
        if not new_branch:
            print('请提供新分支名或确保 build.yaml 配置正确')
            sys.exit(1)
    else:
        new_branch = args.branch
        baseline = None
        model_ext = None
    # 获取仓库路径
    repo_root = get_repo_root_path_from_yaml()
    
    if not repo_root:
        print("无法确定repo根目录")
        sys.exit(1) 
    # 切换到repo根目录
    os.chdir(repo_root) 
    # 只在非删除操作时生成 repo 使用指导文档
    if not args.delete and baseline:
        create_repo_guide(new_branch, baseline,model_ext)
    
    # 获取所有仓库路径
    output = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
    repo_paths = output.strip().split('\n')
    
    # 执行操作到所有仓库
    operation_type = "deletion" if  args.delete else "push"
    print("Starting %s operation for branch: %s" % (operation_type, new_branch))
    
    failed_repos = []
    skipped_repos = []
    
    for repo_path in repo_paths:
        success, skipped = push_with_retry(repo_path, new_branch,  args.delete)
        if not success:
            failed_repos.append(repo_path)
        elif skipped:
            skipped_repos.append(repo_path)
    
    # 重试失败的仓库
    retry_count = 0
    max_retries = 5
    while failed_repos and retry_count < max_retries:
        retry_count += 1
        print("\nRetry attempt %d of %d" % (retry_count, max_retries))
        for repo_path in failed_repos[:]:
            print('Retrying operation for %s' % repo_path)
            success, skipped = push_with_retry(repo_path, new_branch,  args.delete)
            if success:
                failed_repos.remove(repo_path)
                if skipped:
                    skipped_repos.append(repo_path)
    
    # 打印操作总结
    print("\nOperation Summary:")
    #print("%s operation completed." % ("Deletion" if  args.delete else "Push"))
    print("{} operation completed.".format(operation_type.capitalize()))
    if skipped_repos:
        print("Skipped repositories (branch does not exist): %d" % len(skipped_repos))
        for repo in skipped_repos:
            print("  - %s" % repo)
    
    if failed_repos:
        print("\nFailed repositories: %d" % len(failed_repos))
        for repo in failed_repos:
            print("  - %s" % repo)
        sys.exit(1)  # 如果有失败的仓库，以非零状态码退出
    else:
        print("\nAll operations completed successfully.")

if __name__ == '__main__':
    main()