# -*- coding: utf-8 -*-
import sys
import subprocess

def push_with_retry(repo_path, remote_name, branch_name):
    success = False
    while not success:
        try:
            output = subprocess.check_output(['git', '-C', repo_path, 'push', remote_name, 'HEAD:{}'.format(branch_name)], stderr=subprocess.STDOUT)
            success = True
            print('Successfully pushed {} to {} in {}'.format(branch_name, remote_name, repo_path))
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode('utf-8')
            print('Push to {} in {} failed with error: {}'.format(remote_name, repo_path, error_message))
            if 'Could not read from remote repository' in error_message or 'incorrect signature' in error_message:
                print('Retry pushing due to error: {}'.format(error_message))
                success = False
            else:
                raise e
    return success

def main():
    if len(sys.argv) < 2:
        print('Please provide the new branch name as a command line argument.')
        sys.exit(1)

    new_branch = sys.argv[1]
    remote_name = 'caf'

    output = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
    repo_paths = output.split('\n')[:-1]  # Remove the last empty string

    failed_repos = []
    for repo_path in repo_paths:
        success = push_with_retry(repo_path, remote_name, new_branch)
        if not success:
            failed_repos.append(repo_path)

    while failed_repos:
        for repo_path in failed_repos[:]:
            print('Retrying push for {}'.format(repo_path))
            success = push_with_retry(repo_path, remote_name, new_branch)
            if success:
                failed_repos.remove(repo_path)

    print('Push completed. {} repositories failed to push.'.format(len(failed_repos)))

if __name__ == '__main__':
    main()