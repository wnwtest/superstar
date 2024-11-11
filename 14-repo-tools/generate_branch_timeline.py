#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import sys
import git
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def get_branches_info(repo_path):
    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        print("Error: The specified path is not a valid Git repository.")
        print("Path: " + repo_path)
        sys.exit(1)

    branches = []
    seen_branches = set()  # 用于追踪已处理的分支
    for ref in repo.references:
        # 去掉前缀，并过滤掉default和master分支
        branch_name = ref.name.replace("origin/", "").replace("remotes/", "")
        if branch_name in ["default", "master"] or branch_name in seen_branches:
            continue
        
        # 仅处理远程分支
        if ref.name.startswith("origin/") or ref.name.startswith("remotes/"):
            try:
                first_commit = list(repo.iter_commits(ref.name, max_count=1, reverse=True))[0]
                branches.append({
                    'name': branch_name,
                    'date': datetime.fromtimestamp(first_commit.committed_date),
                    'author': first_commit.author.name
                })
                seen_branches.add(branch_name)  # 标记为已处理
            except git.exc.GitCommandError as e:
                print("Warning: Could not retrieve commits for branch {}: {}".format(branch_name,e))

    if not branches:
        print("Warning: No branches found in the repository.")
    return sorted(branches, key=lambda x: x['date'])

def create_timeline(branches, output_file):
    if not branches:
        print("No branches to display.")
        return

    # 删除旧的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.yaxis.set_visible(False)  # 隐藏y轴
    ax.xaxis.set_major_formatter(plt.NullFormatter())  # 隐藏x轴时间刻度

    # 时间顺序均匀分布
    positions = np.linspace(0, 1, len(branches))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(branches)))
    branch_names = []

    for i, (branch, position) in enumerate(zip(branches, positions)):
        ax.plot([position, position], [0, 1], color=colors[i], lw=3)  # 加粗曲线
        branch_names.append((branch['name'], colors[i]))
        # 在曲线顶部显示分支创建时间
        ax.text(position, 1.05, branch['date'].strftime('%Y-%m-%d'), rotation=45, ha='right')

    # 底部图例
    legend_labels = [plt.Line2D([0], [0], color=color, lw=3, label=name) for name, color in branch_names]
    ax.legend(handles=legend_labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)

    plt.title('Branch Creation Timeline')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print("Timeline image created: {}".format(output_file))

if __name__ == '__main__':
    default_repo_path = os.path.join(os.getcwd(), '.repo', 'manifests')
    
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = default_repo_path
    output_file = os.path.join(os.getcwd(), 'branch_timeline.png')
    print("Analyzing Git repository at: " + repo_path)
    branches = get_branches_info(repo_path)
    create_timeline(branches, output_file)
    #print("Timeline image created: " + output_file)