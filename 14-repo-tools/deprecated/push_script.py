# -*- coding: utf-8 -*-
import sys
import subprocess


def get_remote_name(repo_path):
    output = subprocess.check_output(['git', '-C', repo_path, 'remote', '-v'])
    lines = output.split('\n')
    remote_name = lines[0].split('\t')[0]
    return remote_name

def push_with_retry(repo_path,  branch_name, delete=False):
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
    if len(sys.argv) < 2:
        print('Please provide the new branch name as command line argument.')
        sys.exit(1)

    new_branch = sys.argv[1]
    delete = False  # Default value

    if len(sys.argv) > 2:
        action = sys.argv[2].lower()
        delete = action == 'del'  # Modify to delete if 'del' is provided
    # 确定是否执行推送操作
    should_push = action == 'push' if len(sys.argv) > 2 else False

    output = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
    repo_paths = output.split('\n')[:-1]  # Remove the last empty string

    failed_repos = []
    for repo_path in repo_paths:
        success = push_with_retry(repo_path,  new_branch, delete)
        if not success:
            failed_repos.append(repo_path)

    while failed_repos:
        for repo_path in failed_repos[:]:
            print('Retrying push for {}'.format(repo_path))
            success = push_with_retry(repo_path, new_branch, delete)
            if success:
                failed_repos.remove(repo_path)

    print('Push completed. {} repositories failed to push.'.format(len(failed_repos)))

    if should_push :
    # 创建 manifest 文件
        try:
            # 确保导入 repo_cust_manager
            import repo_cust_manger  # 确保模块名称拼写正确
            
            # 只创建 manifest 文件，不推送
            manifest_file = repo_cust_manger.create_and_push_tag(new_branch)
            print("Manifest 文件已创建: {}".format(manifest_file))
            # 创建 manifest 文件并推送到指定的远程分支
            # manifest_file = repo_tag_manager.create_and_push_tag(
            #     tag_name=new_branch,
            #     push=True,
            #     remote_branch=new_branch  # 指定推送到 develop 分支
            # )
            #print(f"Manifest 文件已创建并推送: {manifest_file}")
            #print('Manifest 文件已创建并推送:{}'.format(manifest_file))

        except ImportError:
            print("警告: repo_cust_manger 包未安装，无法执行相关操作。")
        
        except repo_cust_manger.RepoTagError as e:  # 使用已经导入的模块名称
            print("Repo Tag 操作失败: {}".format(str(e)))
        
        except Exception as e:
            print("发生未预期的错误: {}".format(str(e)))


if __name__ == '__main__':
    main()