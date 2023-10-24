#!/usr/bin/env python
# -*- coding: utf8 -*-
# --------------------------------------------------------------
#  push 命令 
# wangnanwang 2022 01
# --------------------------------------------------------------

import subprocess  


def test_echo():
    print(" ===== Test ! =====")

    p = subprocess.Popen('pwd', stdout=subprocess.PIPE, shell=True) 
    output = p.stdout.read()
    print(output)

    return

def get_output (cmd) :
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True) 
    return result.stdout.decode().strip()

def get_push_output (branch ,caf) :
    cmd = 'git push '+ caf + ' '+ 'HEAD:refs/for/'+branch
    print(cmd)
    result = subprocess.run(cmd , stdout=subprocess.PIPE, shell=True, check=True) 
    return result.stdout.decode()

def do_git_push ():
    branch = get_output('git branch --show-current')
    caf = get_output('git remote')
    ret = get_push_output(branch,caf)
    print (ret)

if __name__ == '__main__':

    do_git_push ()
