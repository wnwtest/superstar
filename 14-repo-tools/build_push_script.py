# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import yaml

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

def parse_build_yaml():
    """解析 build.yaml 文件并生成分支名"""
    yaml_path = 'build.yaml'
    if not os.path.exists(yaml_path):
        return None, None
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # 安全地获取配置值，确保转换为字符串
        def safe_str(value):
            """确保值被转换为字符串"""
            if value is None:
                return ''
            return str(value)
        
        # 根据 YAML 结构生成分支名
        branch_components = [
            safe_str(config.get('project', {}).get('model', {}).get('internal', '')),
            safe_str(config.get('project', {}).get('model', {}).get('external', '')),
            safe_str(config.get('project', {}).get('chip', {}).get('platform', '')),
            safe_str(config.get('project', {}).get('version', {}).get('android', '')),
            safe_str(config.get('project', {}).get('date', ''))
        ]
        
        # 移除空字符串
        branch_components = [comp for comp in branch_components if comp]
        
        # 生成分支名
        branch_name = "_".join(branch_components)
        
        # 获取 baseline
        baseline = safe_str(config.get('project', {}).get('baseline', 'default_baseline'))
        
        # 额外的调试输出
        print("解析的分支名组件: {}".format(branch_components))
        print("生成的分支名: {}".format(branch_name))
        print("基线: {}".format(baseline))
        
        return branch_name, baseline
    except Exception as e:
        # 更详细的错误追踪
        import traceback
        print("解析 build.yaml 出错: {}".format(str(e)))
        print("详细错误信息:")
        traceback.print_exc()
        return None, None
def create_repo_guide(branch_name, baseline):
    """生成 repo 使用指导文档"""
    if not branch_name or not baseline:
        print("无法生成 repo 指导文档：分支名或基线为空")
        return False
    guide_content = """Repo 初始化和同步指导
1. 初始化仓库:
repo init -u ssh://username@192.168.117.71:29418/{baseline}/platform/manifest.git \
-b {branch_name} -m PAD5.xml \
--repo-url=ssh://username@192.168.117.71:29418/repo.git \
--repo-branch=caf-stable
2. 同步代码:
repo sync
3. 创建开发分支:
repo start {branch_name} --all
""".format(baseline=baseline, branch_name=branch_name)
    
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
    success = False
    remote_name = get_remote_name(repo_path)
    while not success:
        try:
            if delete:
                output = subprocess.check_output(['git', '-C', repo_path, 'push', remote_name, '--delete', branch_name], stderr=subprocess.STDOUT)
            else:
                output = subprocess.check_output(['git', '-C', repo_path, 'push', remote_name, 'HEAD:refs/heads/{}'.format(branch_name)], stderr=subprocess.STDOUT)
            success = True
            print('Successfully pushed {} to {} in {}'.format(branch_name, remote_name, repo_path))
        except subprocess.CalledProcessError as e:
            error_message = e.output
            print('Push to {} in {} failed with error: {}'.format(remote_name, repo_path, error_message))
            if 'Could not read from remote repository' in error_message or 'incorrect signature' in error_message:
                print('Retry pushing due to error: {}'.format(error_message))
                success = False
            else:
                raise e
    return success
def main():
    # 默认分支名处理
    new_branch = None
    baseline = None
    delete = False
    should_push = False
    
    # 根据参数数量和内容处理分支名
    if len(sys.argv) < 2:
        if not validate_build_yaml():
            print("build.yaml 配置不完整或不正确")
            sys.exit(1)
        # 如果没有提供参数，尝试从 build.yaml 解析
        new_branch, baseline = parse_build_yaml()
        if not new_branch:
            print('请提供新分支名或确保 build.yaml 配置正确')
            sys.exit(1)
    else:
        new_branch = sys.argv[1]
    
    # 处理可选参数
    if len(sys.argv) > 2:
        action = sys.argv[2].lower()
        delete = action == 'del'
        should_push = action == 'push'
    
    # 如果没有从 build.yaml 解析 baseline，尝试读取
    if not baseline:
        try:
            with open('build.yaml', 'r') as f:
                config = yaml.safe_load(f)
                baseline = config.get('project', {}).get('baseline', 'default_baseline')
        except:
            baseline = 'default_baseline'
    
    # 生成 repo 使用指导文档（无论是否推送）
    create_repo_guide(new_branch, baseline)
    
    # 获取所有仓库路径
    output = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
    repo_paths = output.split('\n')[:-1]  # Remove the last empty string
    failed_repos = []
    
    # 推送到所有仓库
    for repo_path in repo_paths:
        success = push_with_retry(repo_path, new_branch, delete)
        if not success:
            failed_repos.append(repo_path)
    
    # 重试失败的仓库
    while failed_repos:
        for repo_path in failed_repos[:]:
            print('Retrying push for {}'.format(repo_path))
            success = push_with_retry(repo_path, new_branch, delete)
            if success:
                failed_repos.remove(repo_path)
        
    print('Push completed. {} repositories failed to push.'.format(len(failed_repos)))
    
    # 如果需要推送，创建 manifest 文件
    if should_push:
        try:
            import repo_cust_manger
            manifest_file = repo_cust_manger.create_and_push_tag(new_branch)
            print("Manifest 文件已创建: {}".format(manifest_file))
        except ImportError:
            print("警告: repo_cust_manger 包未安装，无法执行相关操作。")
        except Exception as e:
            print("发生未预期的错误: {}".format(str(e)))

if __name__ == '__main__':
    main()