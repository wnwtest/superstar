#!/usr/bin/env python
# -*- coding: utf8 -*-
# --------------------------------------------------------------
#  push 命令 
# wangnanwang 2022 01
# add arg[1] usage: branch-name
# --------------------------------------------------------------
import subprocess
import sys

def test_echo():
    print(" ===== Test ! =====")

    p = subprocess.Popen('pwd', stdout=subprocess.PIPE, shell=True) 
    output = p.stdout.read()
    print(output)

    return

def get_output (cmd) :
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    if process.returncode != 0:
        raise Exception("Command failed: " + cmd)
    return output.decode().strip()


def get_push_output (branch ,caf) :
    cmd = 'git push ' + caf + ' ' + 'HEAD:refs/for/' + branch
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    if process.returncode != 0:
        raise Exception("Command failed: " + cmd)
    return output.decode()

def check_branch_availability(branch):
    branches = get_output('git branch -a')
    return branch in branches

def do_git_push ():
    if len(sys.argv) > 1:
        branch = sys.argv[1]
        if not check_branch_availability(branch):
            print(f"Branch {branch} does not exist.")
            return
    else:
        branch = get_output('git rev-parse --abbrev-ref HEAD') 

    caf = get_output('git remote')
    ret = get_push_output(branch, caf)
    print(ret)

if __name__ == '__main__':
    do_git_push ()