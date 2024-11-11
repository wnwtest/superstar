#!/bin/bash
# 确保脚本在错误时退出
set -e
# 函数：检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}
# 检查必要的命令是否存在
for cmd in repo git; do
    if ! command_exists $cmd; then
        echo "错误: $cmd 未安装。请安装后再运行此脚本。"
        exit 1
    fi
done
# 检查是否在 repo 工作目录中
if [ ! -d .repo ]; then
    echo "错误: 当前目录不是 repo 工作目录。"
    exit 1
fi
# 获取标签名称
read -p "请输入新的标签名称: " tag_name
# 确保标签名不为空
if [ -z "$tag_name" ]; then
    echo "错误: 标签名不能为空。"
    exit 1
fi
# 创建 tag 文件夹（如果不存在）
tag_dir=".repo/manifests/tag"
mkdir -p "$tag_dir"
# 生成新的 manifest
manifest_file="$tag_dir/$tag_name.xml"
repo manifest -r -o "$manifest_file"
echo "新的 manifest 文件已生成: $manifest_file"
# 询问是否要推送更改
read -p "是否要推送更改到远程仓库？ (y/n): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    # 切换到 .repo/manifests 目录
    cd .repo/manifests
    # 添加新生成的 manifest 文件
    git add "tag/$tag_name.xml"
    # 提交更改
    git commit -m "Add manifest for tag $tag_name"
    # 推送更改
    echo "正在推送更改到远程仓库..."
    if git push origin HEAD:refs/heads/master; then
        echo "更改已成功推送到远程仓库。"
    else
        echo "推送失败。请检查您的权限和网络连接。"
        exit 1
    fi
else
    echo "更改未推送到远程仓库。"
    echo "注意: 新的 manifest 文件已生成，但尚未提交到版本控制。"
fi
echo "操作完成。"