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
        delete = sys.argv[2].lower() == 'del'  # Modify to delete if 'del' is provided

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

if __name__ == '__main__':
    main()