# coding=utf-8
import os
import sys
import errno
import shutil
import argparse
import xml.etree.ElementTree as ET
import logging
import yaml
def setup_logging():
    """配置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def validate_path(path):
    """验证路径是否存在且有效"""
    if not os.path.exists(path):
        logging.error("路径不存在: {}".format(path))
        raise argparse.ArgumentTypeError("路径不存在: {}".format(path))
    return path

def mkdir_p(path):
    """
    递归创建目录
    类似 mkdir -p 命令
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def are_directories_different(dir1, dir2):
    """
    比较两个目录是否完全相同
    返回True表示目录不同，需要更新
    """
    # 比较目录中的文件数量和内容
    def dir_content(path):
        return set(os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn)
    
    # 简单比较文件列表
    return dir_content(dir1) != dir_content(dir2)

def create_repo(manifest_path, demo_path, output_dir):
    """
    根据manifest创建仓库
    
    :param manifest_path: manifest.xml文件路径
    :param demo_path: demo.git模板路径
    :param output_dir: 输出目录
    """
    try:
        # 解析manifest.xml文件
        tree = ET.parse(manifest_path)
        root = tree.getroot()

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 统计创建仓库数量
        repo_count = 0

        # 遍历所有project元素
        for project in root.findall('project'):
            name = project.get('name')
            
            # 构建目标路径，添加.git后缀
            target_path = os.path.join(output_dir, name + '.git')
            
            try:
                # 如果目标目录已存在，先删除
                if os.path.exists(target_path):
                    shutil.rmtree(target_path)
                    logging.info("已删除已存在的仓库: {}".format(target_path))
                
                # 创建父目录（如果不存在）
                parent_dir = os.path.dirname(target_path)
                try:
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                except OSError as exc:
                    if exc.errno == errno.EEXIST and os.path.isdir(parent_dir):
                        pass
                    else:
                        raise
                
                # 复制demo.git到目标路径
                shutil.copytree(demo_path, target_path)
                
                logging.info("成功创建/更新仓库: {}".format(target_path))
                repo_count += 1
            
            except Exception as copy_error:
                logging.error("创建仓库 {} 失败: {}".format(target_path, copy_error))
        
        logging.info("总共创建/更新 {} 个仓库".format(repo_count))
    
    except ET.ParseError:
        logging.error("解析 XML 文件 {} 失败".format(manifest_path))
    except Exception as e:
        logging.error("发生未知错误: {}".format(e))

def process_sync_yaml(folder_path):
    """
    处理文件夹中的 sync.yaml 文件
    
    :param folder_path: 包含 sync.yaml 的文件夹路径
    """
    sync_yaml_path = os.path.join(folder_path, 'sync.yaml')
    
    if not os.path.exists(sync_yaml_path):
        logging.error("未找到 sync.yaml 文件")
        return
    
    try:
        with open(sync_yaml_path, 'r') as yaml_file:
            sync_config = yaml.safe_load(yaml_file)
        
        # 遍历 sync.yaml 中的配置
        for config in sync_config:
            # 获取配置项
            manifest_path = os.path.join(folder_path, config.get('manifest', ''))
            demo_path = config.get('demo', '')
            output_dir = config.get('output', '')
            
            # 验证必要的配置项
            if not manifest_path or not demo_path or not output_dir:
                logging.error("配置不完整: 缺少 manifest, demo 或 output")
                continue
            
            # 确保路径是绝对路径
            manifest_path = os.path.abspath(manifest_path)
            demo_path = os.path.abspath(demo_path)
            output_dir = os.path.abspath(output_dir)
            
            logging.info("处理配置: Manifest={}, Demo={}, Output={}".format(
                manifest_path, demo_path, output_dir))
            
            # 直接使用配置的输出目录创建仓库
            create_repo(manifest_path, demo_path, output_dir)
    
    except yaml.YAMLError as yaml_error:
        logging.error("解析 YAML 文件错误: {}".format(yaml_error))
    except Exception as e:
        logging.error("处理 sync.yaml 时发生错误: {}".format(e))
def main():
    # 设置日志
    setup_logging()

    # 创建参数解析器
    parser = argparse.ArgumentParser(description='根据manifest创建Git仓库')
    
    # 添加必需的命令行参数
    parser.add_argument('-m', '--manifest', 
                        type=validate_path, 
                        help='manifest.xml文件路径')
    parser.add_argument('-d', '--demo', 
                        type=validate_path, 
                        help='demo.git模板路径')
    parser.add_argument('-o', '--output', 
                        type=str, 
                        help='输出目录')
    parser.add_argument('-f', '--folder', 
                        type=validate_path, 
                        help='包含sync.yaml的文件夹路径')
    
    # 如果没有参数，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    # 解析命令行参数
    try:
        args = parser.parse_args()
    except Exception as e:
        logging.error("参数解析错误: {}".format(e))
        sys.exit(1)
    
    # 根据参数执行操作
    if args.folder:
        # 处理文件夹中的 sync.yaml
        process_sync_yaml(args.folder)
    elif args.manifest and args.demo and args.output:
        # 直接使用命令行参数创建仓库
     create_repo(args.manifest, args.demo, args.output)
    else:
        logging.error("参数不完整，请提供完整的参数或文件夹路径")
        sys.exit(1)
if __name__ == '__main__':
    main()