#!/bin/bash
# 使用 find 命令递归查找所有 Git 仓库
find . -type d -name ".git" | while read gitdir; do
    # 获取 Git 仓库的路径
    project_dir=$(dirname "$gitdir")

    # 进入该 git 仓库目录
    cd "$project_dir" || continue

    # 获取提交数量
    commit_count=$(git rev-list --count HEAD)

    # 如果提交数量为 1，输出该项目的路径
    if [ "$commit_count" -eq 1 ]; then
        echo "$project_dir"
    fi

    # 返回上层目录
    cd - > /dev/null
done
