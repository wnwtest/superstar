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
    # 默认分支名处理
    new_branch = None
    baseline = None
    delete = False
    should_push = False
    model_ext = False
    # 根据参数数量和内容处理分支名
    if len(sys.argv) < 2:
        if not validate_build_yaml():
            print("build.yaml 配置不完整或不正确")
            sys.exit(1)
        # 如果没有提供参数，尝试从 build.yaml 解析
        new_branch, baseline,model_ext = parse_build_yaml()
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
                baseline = config.get('project', {}).get('baseline')
        except:
            baseline = 'default_baseline'
    
    # 只在非删除操作时生成 repo 使用指导文档
    if not delete:
        create_repo_guide(new_branch, baseline,model_ext)
    
    # 获取所有仓库路径
    output = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
    repo_paths = output.strip().split('\n')
    
    # 执行操作到所有仓库
    operation_type = "deletion" if delete else "push"
    print("Starting %s operation for branch: %s" % (operation_type, new_branch))
    
    failed_repos = []
    skipped_repos = []
    
    for repo_path in repo_paths:
        success, skipped = push_with_retry(repo_path, new_branch, delete)
        if not success:
            failed_repos.append(repo_path)
        elif skipped:
            skipped_repos.append(repo_path)
    
    # 重试失败的仓库
    retry_count = 0
    max_retries = 3
    while failed_repos and retry_count < max_retries:
        retry_count += 1
        print("\nRetry attempt %d of %d" % (retry_count, max_retries))
        for repo_path in failed_repos[:]:
            print('Retrying operation for %s' % repo_path)
            success, skipped = push_with_retry(repo_path, new_branch, delete)
            if success:
                failed_repos.remove(repo_path)
                if skipped:
                    skipped_repos.append(repo_path)
    
    # 打印操作总结
    print("\nOperation Summary:")
    print("%s operation completed." % ("Deletion" if delete else "Push"))
    if skipped_repos:
        print("Skipped repositories (branch does not exist): %d" % len(skipped_repos))
        for repo in skipped_repos:
            print("  - %s" % repo)
    
    if failed_repos:
        print("\nFailed repositories: %d" % len(failed_repos))
        for repo in failed_repos:
            print("  - %s" % repo)
    else:
        print("\nAll operations completed successfully.")

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